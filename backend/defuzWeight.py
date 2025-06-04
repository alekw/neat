import numpy as np

def defuz_weight(NoOfCriteria, Wf):
    W = np.zeros(NoOfCriteria)
    
    for i in range(NoOfCriteria):
        # Extract values from the list of lists Wf
        w1, w2, w3, w4 = Wf[i]
        
        # Centroid method
        numerator = (w3**2 + w4**2 + w3 * w4 - w1**2 - w2**2 - w1 * w2)
        denominator = 3 * (w3 + w4 - w1 - w2)
        W[i] = numerator / denominator if denominator != 0 else w1
        
        # If weight is NaN or inf, rewrite weight
        if np.isnan(W[i]) or np.isinf(W[i]):
            W[i] = w1

    # Normalize to 1
    tmp = np.sum(W)
    if tmp != 0:
        W /= tmp
    
    return W
