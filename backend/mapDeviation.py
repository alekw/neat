import numpy as np
from checkCorrection import check_correction

def map_deviation(NoOfAlternatives, NoOfCriteria, E, PrefFun, q, p, s):
    # Initialize variables
    d = np.full((NoOfAlternatives, NoOfAlternatives, NoOfCriteria, 4), 0.0)
    P = np.full((NoOfAlternatives, NoOfAlternatives, NoOfCriteria, 4), 0.0)


    # Compute fuzzy deviation and map to unicriterion preference degrees
    for i in range(NoOfAlternatives):
        for j in range(NoOfAlternatives):
            if i != j:
                for k in range(NoOfCriteria):
                    # Compute fuzzy deviation
                    d[i, j, k] = E[i, k] - np.flip(E[j, k])
                    
                    # Process based on preference function
                    if PrefFun[k] == 1:
                        for l in range(4):
                            P[i, j, k, l] = 1 if d[i, j, k, l] > 0 else 0
                        # Correction
                        d1, d2 = check_correction(d[i, j, k], 0, 0)
                        if d1:
                            P[i, j, k, 1] = 0
                        if d2:
                            P[i, j, k, 2] = 1
                    
                    elif PrefFun[k] == 2:
                        for l in range(4):
                            P[i, j, k, l] = 1 if d[i, j, k, l] > q[k] else 0
                        # Correction
                        d1, d2 = check_correction(d[i, j, k], q[k], q[k])
                        if d1:
                            P[i, j, k, 1] = 0
                        if d2:
                            P[i, j, k, 2] = 1
                    
                    elif PrefFun[k] == 3:
                        for l in range(4):
                            if d[i, j, k, l] <= 0:
                                P[i, j, k, l] = 0
                            elif 0 < d[i, j, k, l] <= p[k]:
                                P[i, j, k, l] = d[i, j, k, l] / p[k]
                            else:
                                P[i, j, k, l] = 1
                        # Correction
                        d1, d2 = check_correction(d[i, j, k], 0, p[k])
                        if d1:
                            P[i, j, k, 1] = 0
                        if d2:
                            P[i, j, k, 2] = 1
                    
                    elif PrefFun[k] == 4:
                        for l in range(4):
                            if d[i, j, k, l] <= q[k]:
                                P[i, j, k, l] = 0
                            elif q[k] < d[i, j, k, l] <= p[k]:
                                P[i, j, k, l] = 0.5
                            else:
                                P[i, j, k, l] = 1
                        # Correction
                        d1, d2 = check_correction(d[i, j, k], q[k], p[k])
                        if d1:
                            P[i, j, k, 1] = 0
                        if d2:
                            P[i, j, k, 2] = 1
                    
                    elif PrefFun[k] == 5:
                        for l in range(4):
                            if d[i, j, k, l] <= q[k]:
                                P[i, j, k, l] = 0
                            elif q[k] < d[i, j, k, l] <= p[k]:
                                P[i, j, k, l] = (d[i, j, k, l] - q[k]) / (p[k] - q[k])
                            else:
                                P[i, j, k, l] = 1
                        # Correction
                        d1, d2 = check_correction(d[i, j, k], q[k], p[k])
                        if d1:
                            P[i, j, k, 1] = 0
                        if d2:
                            P[i, j, k, 2] = 1
                    
                    elif PrefFun[k] == 6:
                        for l in range(4):
                            if d[i, j, k, l] <= 0:
                                P[i, j, k, l] = 0
                            else:
                                P[i, j, k, l] = 1 - np.exp(-d[i, j, k, l]**2 / (2 * s[k]**2))
                        # Correction
                        d1, _ = check_correction(d[i, j, k], 0, np.inf)
                        if d1:
                            P[i, j, k, 1] = 0
    
    return P, d
