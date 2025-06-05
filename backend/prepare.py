import numpy as np
from genRanking import gen_ranking
from neatPromethee import NEAT_FPROMETHEE
from lingVal import *
from jsonClasses import DecisionData

def create_parameter_matrix(decision_data: DecisionData) -> np.ndarray:
    """
    Creates a 2D array where each element in the matrix corresponds to a list containing the 
    [L, A, B, R] values for each criterion and alternative, even if the order of criteria 
    varies in each alternative.

    :param decision_data: The decision data containing alternatives and criteria.
    :return: A 2D numpy array of shape (no_of_alternatives, no_of_criteria), where each element
             is a list of the form [L, A, B, R] for a given alternative and criterion.
    """
    num_alternatives = len(decision_data.alternatives)
    num_criteria = len(decision_data.criteria)
    
    # Initialize a 2D array with shape (num_alternatives, num_criteria)
    # Each cell will hold a list [L, A, B, R]
    E = np.empty((num_alternatives, num_criteria), dtype=object)

    # Create a dictionary to map criterion ids to their index in the criteria list
    criterion_id_to_index = {criterion.id: idx for idx, criterion in enumerate(decision_data.criteria)}

    # Iterate over alternatives
    for i, alternative in enumerate(decision_data.alternatives):
        # Iterate over the parameters of the current alternative
        for crit_id, param in alternative.parameters.items():
            # Find the index of the criterion in the criteria list
            crit_idx = criterion_id_to_index[crit_id]
            
            LABR = [param.L, param.A, param.B, param.R]
            
            #parse linquistic performance of alternative if provided
            if param.performance:
                LABR = LINGUISTIC_PERFORMANCES[param.performance]
                if LABR is None:
                    raise ValueError(f"Unknown performance label: '{param.performance}'")
            # Store the [L, A, B, R] values as a list in the appropriate cell
            E[i, crit_idx] = LABR

    return E


def prepare_data(decision_data: DecisionData):

    # Number of alternatives and criteria
    NoOfAlternatives = len(decision_data.alternatives)
    NoOfCriteria = len(decision_data.criteria)
    PrefDirection = [1 if criterion.direction == 'max' else 2 for criterion in decision_data.criteria]
    
    # Mapping of preference function strings to their corresponding IDs (alternative names are supported)
    preference_function_mapping = {
        'usual': 1,
        'true': 1,
        'u-shaped': 2,
        'semi': 2,
        'v-shaped': 3,
        'pre': 3,
        'level': 4,
        'v-shaped indifference': 5,
        'pseudo': 5,
        'gaussian': 6
    }
    
    # Map preference function string to ID
    PrefFun = [
        preference_function_mapping.get(criterion.preference_function, 0) 
        for criterion in decision_data.criteria
    ]

    
    q = [criterion.indifference_threshold for criterion in decision_data.criteria]
    p = [criterion.preference_threshold for criterion in decision_data.criteria]
    s = np.zeros(NoOfCriteria)
    s = np.array([criterion.gaussian_threshold if criterion.gaussian_threshold is not None else 0 for criterion in decision_data.criteria])
    names = [alt.id for alt in decision_data.alternatives]
    
    Wf = []
    for criterion in decision_data.criteria:
        if criterion.weight in LINGUISTIC_WEIGHTS:
            Wf.append((LINGUISTIC_WEIGHTS[criterion.weight]))
        else:
            raise ValueError(f"Invalid weight value: {criterion.weight}. Must be a valid linguistic variable.")
      
    E = create_parameter_matrix(decision_data)

    return NoOfAlternatives, NoOfCriteria, PrefDirection, PrefFun, q, p, s, names, Wf, E
    

def calculate(decision_data: DecisionData):
    NoOfAlternatives, NoOfCriteria, PrefDirection, PrefFun, q, p, s, names, Wf, E = prepare_data(decision_data);

    crispPhi, crispPhiPlus, crispPhiMinus, Phi, PhiPlus, PhiMinus, Pi, W, P, d = NEAT_FPROMETHEE(NoOfCriteria, NoOfAlternatives, E, Wf, PrefDirection, PrefFun, q, p, s)
    
    rankPhi = gen_ranking(np.round(crispPhi, 8))
    rankPhiPlus = gen_ranking(np.round(crispPhiPlus, 8))
    rankPhiMinus = gen_ranking(1 - np.round(crispPhiMinus, 8))
    
    # Display results
    print("Rankings based on crispPhi:", rankPhi)
    print("Rankings based on crispPhiPlus:", rankPhiPlus)
    print("Rankings based on crispPhiMinus:", rankPhiMinus)
    
    return create_named_ranking(rankPhi.tolist(), names), create_named_ranking(rankPhiPlus.tolist(), names), create_named_ranking(rankPhiMinus.tolist(), names), create_named_ranking(crispPhi.tolist(), names), create_named_ranking(crispPhiPlus.tolist(), names), create_named_ranking(crispPhiMinus.tolist(), names), create_named_ranking(Phi.tolist(), names), create_named_ranking(PhiPlus.tolist(), names), create_named_ranking(PhiMinus.tolist(), names)

def create_named_ranking(ranking, names):
    result = dict(zip(names, ranking))
    print(result)
    return result
