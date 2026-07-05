(function(){
    window.NEAT_PARSE_JSON_URL = "http://127.0.0.1:5000/parse_json";

    // Plotly drawing helpers
    window.drawAll = function(data) {
        drawPhi(data)
        drawPhiPlus(data)
        drawPhiMinus(data)
    }

    window.drawPhi = function(data) {
        draw(data.Phi, data.rankPhi, data.crispPhi, "Phi");
    }

    window.drawPhiMinus = function(data) {
        draw(data.PhiMinus, data.rankPhiMinus, data.crispPhiMinus, "Phi-");
    }

    window.drawPhiPlus = function(data) {
        draw(data.PhiPlus, data.rankPhiPlus, data.crispPhiPlus, "Phi+");
    }

    window.draw = function(phi, rankPhi, crispPhi, divName) {
        const lines = [];

        const allRanks = Object.values(rankPhi);
        const maxRank = Math.max(...allRanks);

        for (const [altName, xValues] of Object.entries(phi)) {
            const rank = rankPhi[altName];
            const invertedRank = maxRank - rank + 1;

            const trace = {
                name: altName,
                x: xValues,
                y: [0, invertedRank, invertedRank, 0],
            };

            const crisp = crispPhi[altName];

            const verticalTrace = {
                name: "crisp " + altName,
                x: [crisp, crisp],
                y: [0, invertedRank],
                line: { dash: 'dot' }
            }

            lines.push(trace)
            lines.push(verticalTrace)
        }

        var layout = {
            title: { text: divName + ' fuzzy and crisp outranking flow' },
            xaxis: { title: { text: divName }, showgrid: false, zeroline: false },
            yaxis: { title: { text: 'Rank' }, showline: false },
        };

        Plotly.newPlot(divName, lines, layout);
    }

    window.renderFuzzySummaryTable = function(data) {
        const container = document.getElementById('data-table-container');
        if (!container) return;
        const alternatives = Object.keys(data.Phi).sort();

        let html = '<h3>Fuzzy Values Summary</h3>';
        html += '<table class="data-table"><thead><tr><th>Alternative</th><th>Phi+</th><th>Phi-</th><th>Phi</th></tr></thead><tbody>';

        alternatives.forEach(alt => {
            const phiValues = data.Phi[alt];
            const phiPlusValues = data.PhiPlus[alt];
            const phiMinusValues = data.PhiMinus[alt];

            html += `<tr>
                <td>${alt}</td>
                <td>[${phiPlusValues.map(v => v.toFixed(4)).join(', ')}]</td>
                <td>[${phiMinusValues.map(v => v.toFixed(4)).join(', ')}]</td>
                <td>[${phiValues.map(v => v.toFixed(4)).join(', ')}]</td>
            </tr>`;
        });

        html += '</tbody></table>';
        container.innerHTML = html;
    }

    window.renderCrispRankSummaryTable = function(data) {
        const container = document.getElementById('data-table-container');
        if (!container) return;
        const alternatives = Object.keys(data.Phi).sort();

        let html = '<h3>Crisp and Rank Summary</h3>';
        html += '<table class="data-table"><thead><tr><th>Alternative</th><th>Phi+ crisp</th><th>Rank Phi+</th><th>Phi- crisp</th><th>Rank Phi-</th><th>Phi net crisp</th><th>Rank Phi</th></tr></thead><tbody>';

        alternatives.forEach(alt => {
            const phiCrispPlus = data.crispPhiPlus?.[alt];
            const rankPhiPlus = data.rankPhiPlus?.[alt];
            const phiCrispMinus = data.crispPhiMinus?.[alt];
            const rankPhiMinus = data.rankPhiMinus?.[alt];
            const phiCrisp = data.crispPhi?.[alt];
            const rankPhi = data.rankPhi?.[alt];

            html += `<tr>
                <td>${alt}</td>
                <td>${phiCrispPlus.toFixed(4)}</td>
                <td>${rankPhiPlus ?? ''}</td>
                <td>${phiCrispMinus.toFixed(4)}</td>
                <td>${rankPhiMinus ?? ''}</td>
                <td>${phiCrisp.toFixed(4)}</td>
                <td>${rankPhi ?? ''}</td>
            </tr>`;
        });

        html += '</tbody></table>';
        container.innerHTML += html;
    }

    // Partial order helpers (cytoscape)
    window.drawPartialOrder = function(data) {
        const ids = Object.keys(data.rankPhiPlus);

        const nodes = ids.map(id => ({ data: { id, label: id } }));

        const denseEdges = [];

        for (let i = 0; i < ids.length; i++) {
            for (let j = 0; j < ids.length; j++) {
                if (i === j) continue;

                const a = ids[i];
                const b = ids[j];

                const pA = data.rankPhiPlus[a], pB = data.rankPhiPlus[b];
                const mA = data.rankPhiMinus[a], mB = data.rankPhiMinus[b];

                const prefers =
                    (pA < pB && mA < mB) ||
                    (pA === pB && mA < mB) ||
                    (pA < pB && mA === mB);

                if (prefers) {
                    denseEdges.push({ data: { source: a, target: b } });
                }
            }
        }

        const edges = transitiveReduction(nodes, denseEdges);

        var cy = window.cy = cytoscape({
            container: document.getElementById('cy'),

            boxSelectionEnabled: false,
            autounselectify: true,

            layout: { name: 'dagre' },

            style: [
                {
                    selector: 'node',
                    style: {
                        'background-color': '#11479e',
                        'label': 'data(label)',
                        'color': '#fff',
                        'text-valign': 'center',
                        'text-halign': 'center',
                        'font-size': '12px',
                        'text-outline-color': '#11479e',
                        'text-outline-width': 2
                    }
                },
                {
                    selector: 'edge',
                    style: {
                        'width': 4,
                        'target-arrow-shape': 'triangle',
                        'line-color': '#9dbaea',
                        'target-arrow-color': '#9dbaea',
                        'curve-style': 'bezier'
                    }
                }
            ],

            elements: { nodes: [...nodes], edges: [...edges] }
        });
    }

    window.transitiveReduction = function(nodes, edges) {
        const adj = {};
        nodes.forEach(n => adj[n.data.id] = []);

        edges.forEach(e => { adj[e.data.source].push(e.data.target); });

        function reachable(from, avoid) {
            const visited = new Set();
            const stack = [...adj[from].filter(t => t !== avoid)];
            while (stack.length) {
                const node = stack.pop();
                if (!visited.has(node)) {
                    visited.add(node);
                    stack.push(...adj[node]);
                }
            }
            return visited;
        }

        return edges.filter(e => {
            const { source, target } = e.data;
            const reach = reachable(source, target);
            return !reach.has(target);
        });
    }
})();
