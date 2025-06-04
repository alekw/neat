def check_correction(d, t, u):
    # Initialize output variables
    out1 = 0
    out2 = 0
    
    # Check for the first condition
    if d[0] < t and d[1] >= t:
        y = (t - d[0]) / (d[1] - d[0])
        if y <= 0.5:
            out1 = 0
        else:
            out1 = 1
    
    # Check for the second condition
    if d[2] <= u and d[3] > u:
        y = (u - d[3]) / (d[2] - d[3])
        if y <= 0.5:
            out2 = 0
        else:
            out2 = 1
    
    return out1, out2
