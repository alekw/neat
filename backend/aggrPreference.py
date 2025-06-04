import numpy as np

def aggr_preference(NoOfAlternatives, NoOfCriteria, P, W):
    # Initialize Pi, PhiPlus, PhiMinus, Phi with zeros
    Pi = np.zeros((NoOfAlternatives, NoOfAlternatives, 4))
    PhiPlus = np.zeros((NoOfAlternatives, 4))
    PhiMinus = np.zeros((NoOfAlternatives, 4))
    Phi = np.zeros((NoOfAlternatives, 4))
    
    # Calculate global preference degrees
    for i in range(NoOfAlternatives):
        for j in range(NoOfAlternatives):
            if i != j:
                for k in range(NoOfCriteria):
                    Pi[i, j, 0] += P[i, j, k, 0] * W[k]
                    Pi[i, j, 1] += P[i, j, k, 1] * W[k]
                    Pi[i, j, 2] += P[i, j, k, 2] * W[k]
                    Pi[i, j, 3] += P[i, j, k, 3] * W[k]

    # Calculate fuzzy positive and negative outranking flows
    for i in range(NoOfAlternatives):
        for j in range(NoOfAlternatives):
            PhiPlus[i, 0] += Pi[i, j, 0] / (NoOfAlternatives - 1)
            PhiPlus[i, 1] += Pi[i, j, 1] / (NoOfAlternatives - 1)
            PhiPlus[i, 2] += Pi[i, j, 2] / (NoOfAlternatives - 1)
            PhiPlus[i, 3] += Pi[i, j, 3] / (NoOfAlternatives - 1)
            PhiMinus[i, 0] += Pi[j, i, 0] / (NoOfAlternatives - 1)
            PhiMinus[i, 1] += Pi[j, i, 1] / (NoOfAlternatives - 1)
            PhiMinus[i, 2] += Pi[j, i, 2] / (NoOfAlternatives - 1)
            PhiMinus[i, 3] += Pi[j, i, 3] / (NoOfAlternatives - 1)
    
    # Calculate fuzzy net outranking flow
    for i in range(NoOfAlternatives):
        Phi[i, 0] = PhiPlus[i, 0] - PhiMinus[i, 3]
        Phi[i, 1] = PhiPlus[i, 1] - PhiMinus[i, 2]
        Phi[i, 2] = PhiPlus[i, 2] - PhiMinus[i, 1]
        Phi[i, 3] = PhiPlus[i, 3] - PhiMinus[i, 0]
    
    return Phi, PhiPlus, PhiMinus, Pi
