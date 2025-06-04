import numpy as np

def gen_ranking(v):
    # Check if the vector is not empty
    if not np.isnan(v).all():
        # Check vector length
        n = len(v)
        # Initialize ranking array
        ranking = np.zeros(n, dtype=int)
        # Initialize index
        i = 1
        
        # While there are alternatives not yet ranked
        while np.any(v != -np.inf):
            # Find alternative(s) with max performance
            max_val = np.max(v)
            tmp = np.where(v == max_val)[0]
            
            # If one alternative is found, give it rank i and mark it in v
            if len(tmp) == 1:
                ranking[tmp[0]] = i
                v[tmp[0]] = -np.inf
            # If multiple alternatives are found, give them the rank of i and mark them in v
            else:
                ranking[tmp] = i
                v[tmp] = -np.inf
            
            # Increase index by the number of ranked alternatives
            i += len(tmp)
        
        return ranking
    else:
        raise ValueError("Vector v is empty or contains NaN values")

# Example usage:
# v = np.array([3.5, 2.0, 3.5, 1.0])
# print(gen_ranking(v))  # Output: [1 3 1 4]
