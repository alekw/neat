# Linguistic variables for weights of criteria:
VL = [0, 0, 0.1, 0.2]  # Very Low
L = [0.1, 0.2, 0.2, 0.3]  # Low
ML = [0.2, 0.3, 0.4, 0.5]  # Medium Low
M = [0.4, 0.5, 0.5, 0.6]  # Medium
MH = [0.5, 0.6, 0.7, 0.8]  # Medium High
H = [0.7, 0.8, 0.8, 0.9]  # High
VH = [0.8, 0.9, 1.0, 1.0]  # Very High

# Linguistic variables for performances of alternatives:
VP = [0, 0, 1, 2]  # Very Poor
P = [1, 2, 2, 3]  # Poor
MP = [2, 3, 4, 5]  # Medium Poor
F = [4, 5, 5, 6]  # Fair
MG = [5, 6, 7, 8]  # Medium Good
G = [7, 8, 8, 9]  # Good
VG = [8, 9, 10, 10]  # Very Good


# Mapping of linguistic variables to their numerical ranges
LINGUISTIC_WEIGHTS = {
    "very low": [0, 0, 0.1, 0.2],  # Very Low
    "low": [0.1, 0.2, 0.2, 0.3],  # Low
    "medium low": [0.2, 0.3, 0.4, 0.5],  # Medium Low
    "medium": [0.4, 0.5, 0.5, 0.6],  # Medium
    "medium high": [0.5, 0.6, 0.7, 0.8],  # Medium High
    "high": [0.7, 0.8, 0.8, 0.9],  # High
    "very high": [0.8, 0.9, 1.0, 1.0]   # Very High
}
