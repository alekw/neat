from mapDeviation import map_deviation
from defuzWeight import defuz_weight
from aggrPreference import aggr_preference
from defuzPhi import defuz_phi

def NEAT_FPROMETHEE(NoOfCriteria, NoOfAlternatives, E, Wf, PrefDirection, PrefFun, q, p, s):
    # Adjust for preference direction
    for i in range(NoOfAlternatives):
        for j in range(NoOfCriteria):
            if PrefDirection[j] == 2:
                E[i][j] = [-x for x in E[i][j]][::-1]
    
    # Compute deviations and preference degrees
    P, d = map_deviation(NoOfAlternatives, NoOfCriteria, E, PrefFun, q, p, s)
    
    # Defuzzify weights
    W = defuz_weight(NoOfCriteria, Wf)
    
    # Aggregate preferences
    Phi, PhiPlus, PhiMinus, Pi = aggr_preference(NoOfAlternatives, NoOfCriteria, P, W)
    
    # Defuzzify preference flows
    crispPhi, crispPhiPlus, crispPhiMinus = defuz_phi(NoOfAlternatives, Phi, PhiPlus, PhiMinus)
    
    return crispPhi, crispPhiPlus, crispPhiMinus, Phi, PhiPlus, PhiMinus, Pi, W, P, d
