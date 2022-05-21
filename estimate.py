import function


def estimate(roi):
    counts = function.count(roi)
    if function.isnone(counts) == 1:
        # print("NONE")
        return 0
    if function.iscocked(roi) == 1:
        # print("COCKED")
        return 1
    if function.isbias(counts) == 1:
        # print("BIAS")
        return 2
    if function.isincline() == 1:
        # print("INCLINE")
        return 3
    # print("WELL")
    return 4
