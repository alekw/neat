from flask import Flask, request, jsonify
from flask_cors import CORS
from jsonClasses import DecisionData
from prepare import calculate


app = Flask(__name__)
CORS(app)

@app.route('/parse_json', methods=['POST'])
def parse_json():
    try:
        # Get JSON data from the request
        data = request.get_json()
        
        # Parse the JSON into DecisionData object
        decision_data = DecisionData.from_json(data)

        rankPhi, rankPhiPlus, rankPhiMinus, crispPhi, crispPhiPlus, crispPhiMinus, Phi, PhiPlus, PhiMinus = calculate(decision_data);
        
        # Prepare the result
        result = {
            "rankPhi": rankPhi,
            "rankPhiPlus": rankPhiPlus,
            "rankPhiMinus": rankPhiMinus,
            "crispPhi": crispPhi,
            "crispPhiPlus": crispPhiPlus,
            "crispPhiMinus": crispPhiMinus,
            "Phi": Phi,
            "PhiPlus": PhiPlus,
            "PhiMinus": PhiMinus,
            
        }
        
        # Return JSON response
        return jsonify(result), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 400
    



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7776, debug=True, use_reloader=False, threaded=False)
