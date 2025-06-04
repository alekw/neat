from dataclasses import dataclass, field
from typing import List, Dict

# Define data classes to represent Criteria, Alternatives, and Parameters

@dataclass
class Parameter:
    L: float
    A: float
    B: float
    R: float

@dataclass
class Criterion:
    id: str
    weight: str
    direction: str
    preference_function: str
    indifference_threshold: float
    preference_threshold: float
    gaussian_threshold: float

@dataclass
class Alternative:
    id: str
    parameters: Dict[str, Parameter]  # key is criterion ID, value is Parameter object

@dataclass
class DecisionData:
    criteria: List[Criterion] = field(default_factory=list)
    alternatives: List[Alternative] = field(default_factory=list)

    @staticmethod
    def from_json(data: dict) -> "DecisionData":
        # Parse criteria
        criteria = [
            Criterion(
                id=c["id"],
                weight=c["weight"],
                direction=c["direction"],
                preference_function=c["preference_function"],
                indifference_threshold=c.get("indifference_threshold", 0), #thresholds are all optional
                preference_threshold=c.get("preference_threshold", 0), 
                gaussian_threshold=c.get("gaussian_threshold", 0)
            ) for c in data.get("criteria", [])
        ]

        # Parse alternatives with parameters
        alternatives = []
        for alt in data.get("alternatives", []):
            parameters = {
                crit_id: Parameter(**params) for crit_id, params in alt["parameters"].items()
            }
            alternatives.append(Alternative(id=alt["id"], parameters=parameters))

        return DecisionData(criteria=criteria, alternatives=alternatives)