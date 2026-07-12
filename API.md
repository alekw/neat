# API description

This file describes the JSON format accepted by the NEAT API endpoint:

- Endpoint: POST /parse_json
- Content-Type: application/json

## Input JSON

The request body must contain two top-level arrays:

```json
{
  "criteria": [],
  "alternatives": []
}
```

### 1. Criteria

Each item in `criteria` describes one decision criterion.

```json
{
  "id": "C1",
  "weight": "high",
  "direction": "max",
  "preference_function": "v-shaped",
  "indifference_threshold": 0,
  "preference_threshold": 0.3,
  "gaussian_threshold": 0
}
```

Allowed values:

- `id`: string, for example `"C1"`, `"cost"`
- `weight`: one of
  - `very low`
  - `low`
  - `medium low`
  - `medium`
  - `medium high`
  - `high`
  - `very high`
- `direction`: `max` or `min`
- `preference_function`: one of
  - `usual` (also accepted: `true`)
  - `u-shaped` (also accepted: `semi`)
  - `v-shaped` (also accepted: `pre`)
  - `level`
  - `v-shaped indifference` (also accepted: `pseudo`)
  - `gaussian`
- `indifference_threshold`: number (or omitted / null). Used for `u-shaped`, `level`, and `v-shaped indifference`-type functions.
- `preference_threshold`: number (or omitted / null). Used for `v-shaped`, `level`, and `v-shaped indifference`-type functions.
- `gaussian_threshold`: number (or omitted / null). Used only for `gaussian`.

For `usual`, the thresholds are effectively not used. For `u-shaped`, only `indifference_threshold` matters. For `v-shaped`, only `preference_threshold` matters. For `level` and `v-shaped indifference`, both thresholds are used. For `gaussian`, only `gaussian_threshold` matters.

### 2. Alternatives

Each item in `alternatives` describes one alternative.

```json
{
  "id": "A1",
  "parameters": {
    "C1": { "L": 1, "A": 2, "B": 3, "R": 4 },
    "C2": { "performance": "good" }
  }
}
```

Rules:

- `id`: string, for example `"A1"`
- `parameters`: object where each key is a criterion id
- each criterion value must be one of:
  - an object with `L`, `A`, `B`, `R` values, for example `{ "L": 1, "A": 2, "B": 3, "R": 4 }`
  - or an object with a single `performance` field, for example `{ "performance": "good" }`

Allowed linguistic values for `performance`:

- `very poor`
- `poor`
- `medium poor`
- `fair`
- `medium good`
- `good`
- `very good`

## Output JSON

The API returns an object with the following fields:

```json
{
  "rankPhi": {},
  "rankPhiPlus": {},
  "rankPhiMinus": {},
  "crispPhi": {},
  "crispPhiPlus": {},
  "crispPhiMinus": {},
  "Phi": {},
  "PhiPlus": {},
  "PhiMinus": {}
}
```

Meaning:

- `rankPhi`, `rankPhiPlus`, `rankPhiMinus`: ranking numbers for each alternative
- `crispPhi`, `crispPhiPlus`, `crispPhiMinus`: single crisp score for each alternative
- `Phi`, `PhiPlus`, `PhiMinus`: fuzzy values for each alternative

Each result is grouped by alternative id.

## Minimal example

```json
{
  "criteria": [
    {
      "id": "C1",
      "weight": "high",
      "direction": "max",
      "preference_function": "v-shaped",
      "indifference_threshold": 0,
      "preference_threshold": 0.3,
      "gaussian_threshold": 0
    }
  ],
  "alternatives": [
    {
      "id": "A1",
      "parameters": {
        "C1": { "L": 1, "A": 2, "B": 3, "R": 4 }
      }
    },
    {
      "id": "A2",
      "parameters": {
        "C1": { "performance": "good" }
      }
    }
  ]
}
```
