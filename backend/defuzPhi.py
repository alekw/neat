import numpy as np

def defuz_phi(NoOfAlternatives, Phi, PhiPlus, PhiMinus):
    # Initialize arrays to store crisp values
    crispPhi = np.zeros(NoOfAlternatives)
    crispPhiPlus = np.zeros(NoOfAlternatives)
    crispPhiMinus = np.zeros(NoOfAlternatives)
    
    for i in range(NoOfAlternatives):
        # Defuzzify Phi Plus using centroid method
        denomPlus = 3 * (PhiPlus[i][2] + PhiPlus[i][3] - PhiPlus[i][0] - PhiPlus[i][1])
        if denomPlus != 0:
            crispPhiPlus[i] = (
                PhiPlus[i][2]**2 + PhiPlus[i][3]**2 + PhiPlus[i][2] * PhiPlus[i][3]
                - PhiPlus[i][0]**2 - PhiPlus[i][1]**2 - PhiPlus[i][0] * PhiPlus[i][1]
            ) / denomPlus
        else:
            crispPhiPlus[i] = PhiPlus[i][0]
        
        # Defuzzify Phi Minus using centroid method
        denomMinus = 3 * (PhiMinus[i][2] + PhiMinus[i][3] - PhiMinus[i][0] - PhiMinus[i][1])
        if denomMinus != 0:
            crispPhiMinus[i] = (
                PhiMinus[i][2]**2 + PhiMinus[i][3]**2 + PhiMinus[i][2] * PhiMinus[i][3]
                - PhiMinus[i][0]**2 - PhiMinus[i][1]**2 - PhiMinus[i][0] * PhiMinus[i][1]
            ) / denomMinus
        else:
            crispPhiMinus[i] = PhiMinus[i][0]
        
        # Defuzzify Phi using centroid method
        denomPhi = 3 * (Phi[i][2] + Phi[i][3] - Phi[i][0] - Phi[i][1])
        if denomPhi != 0:
            crispPhi[i] = (
                Phi[i][2]**2 + Phi[i][3]**2 + Phi[i][2] * Phi[i][3]
                - Phi[i][0]**2 - Phi[i][1]**2 - Phi[i][0] * Phi[i][1]
            ) / denomPhi
        else:
            crispPhi[i] = Phi[i][0]
        
        # Check for NaN or inf and rewrite if necessary
        if np.isnan(crispPhiPlus[i]) or np.isinf(crispPhiPlus[i]):
            crispPhiPlus[i] = PhiPlus[i][0]
        if np.isnan(crispPhiMinus[i]) or np.isinf(crispPhiMinus[i]):
            crispPhiMinus[i] = PhiMinus[i][0]
        if np.isnan(crispPhi[i]) or np.isinf(crispPhi[i]):
            crispPhi[i] = Phi[i][0]
    
    return crispPhi, crispPhiPlus, crispPhiMinus
