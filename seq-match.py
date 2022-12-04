from numpy import zeros, empty


def sa(x: str, y: str, s: tuple):
    d = (len(y) + 1, len(x) + 1)

    F = zeros(d)
    (
        ms,
        mms,
        gap_open,
        gap_extend,
    ) = s  # match, mismatch, gap open (d), and gap extend (e) from score tuple
    # NOTE: mms and gs should be passed as negative values

    """
    pointers will follow direction convention left = 2, up-left = 0, up = 1
    tuples of pointers kept for those occasions in which more than one
    string yields and optimal solution

    NOTE: No longer true for affine
    """
    P = empty(d, dtype=tuple)  # Keep track of pointers

    # 'match' is used to determine whether to add/subtract the score for a match/mismatch depending on the two letters presently compared
    match: bool

    # used to find the global max of the matrix the, where we will work backwards to determine the xy, for the optimal path
    globalMax = 0
    globalMaxXY: tuple = (1, 1)

    # Algorithm starts at [1, 1]  as top/left rows were previously intiialized
    for i in range(1, d[0]):
        for j in range(1, d[1]):
            match = x[j - 1] == y[i - 1]

            score = ms if match else mms

            # a formula: gamma(g) = -d -(g-1)e, affine gap penalty
            def gap_pen(g):
                return -gap_open - (g - 1) * gap_extend

            # We don't mind true maximum values being < 0 as these values will be mapped to 0 by the lambda on score array 'r' later
            row_max: int = None  # first loop
            rm_loc: int = None

            col_max: int = None  # second loop
            cm_loc: int = None

            for k in range(0, i):
                val = F[k][j] + gap_pen(i - k)
                if row_max is None or val > row_max:
                    row_max = val
                    rm_loc = k

            for k in range(0, j):
                val = F[i][k] + gap_pen(j - k)
                if col_max is None or val > col_max:
                    col_max = val
                    cm_loc = k

            r = [F[i - 1][j - 1] + score, row_max, col_max]

            """
            The minimum values in the array per the Smith-Waterman algorithm are 0 (e.g. no penalty for starting string-matching at arbitrary points in the pair of strings)

            The results array is mapped to reflect this; any scores below 0 are mapped to 0
            """
            r = list(map(lambda a: 0 if a < 0 else a, r))

            m = max(r)

            pointers: tuple = ()

            for k, e in enumerate(r):
                """
                If we use row_max, put (rm_loc, j) into the tuple,
                otherwise, if we use col_max, put (i, cm_loc) into the tuple

                Diagonal pointer can remain the same (up, left = 0)
                Left and top pointers will now be positive and negative-encoded
                Negative value = left (row)
                Positive value = top (col)
                |val| = the index along the row or column that we're pointing to
                """
                if e == m:
                    if k == 0:
                        pointers += (k,)
                    elif k == 1:  # up, column
                        pointers += (cm_loc,)
                    else:  # k == 2, left, row
                        pointers += (-rm_loc,)

            F[i][j] = m
            P[i][j] = pointers

            # finds the highest value in the matrix and saves the xy
            if globalMax < m:
                globalMax = m
                globalMaxXY = (i, j)
    return traceback(x, y, F, P, globalMaxXY)


## col string = the one on the top
## row string = the one on the left axis
## calculates the backtrack
def traceback(colString: str, rowString: str, matrix, ptrMatrix, globalMaxXY: tuple):
    currMax = matrix[globalMaxXY[0]][globalMaxXY[1]]
    recordOfCurMaxXY = []
    s1 = ""
    s2 = ""
    x = globalMaxXY[0]
    y = globalMaxXY[1]

    # first fill the array recordOfCurMaxXY with the optimal route x,y points
    while currMax != 0:
        recordOfCurMaxXY.insert(0, (x, y))
        currPtr = ptrMatrix[x][y]
        # this block came from the up-left position
        if currPtr[0] == 0:
            x = x - 1
            y = y - 1
            currMax = matrix[x][y]
        # this block came from the up position
        elif currPtr[0] > 0:
            x = currPtr[0]
            y = y - 1
            currMax = matrix[x][y]
        # this block came from the left position
        else:
            y = -currPtr[0]
            x = x - 1
            currMax = matrix[x][y]

    # once the optimal xy route is found, create the strings using the loop below
    lastx = -1
    lasty = -1
    for i in range(0, len(recordOfCurMaxXY)):
        tup = recordOfCurMaxXY[i]
        if tup[0] - lastx > 1 and i != 0:  # always shifting in affine
            s1 += rowString[lastx] + "_" * (tup[0] - lastx - 1)
            s2 += colString[(tup[1] - 1) : (tup[0] - lastx)]
        elif tup[1] - lasty > 1 and i != 0:
            s1 += rowString[(tup[0] - 1) : (tup[0] - 1) + (tup[1] - lasty)]
            s2 += colString[lasty] + "_" * (tup[1] - lasty - 1)
        else:  # no changes needed for affine
            s1 += rowString[tup[0] - 1]
            s2 += colString[tup[1] - 1]
        lastx = tup[0]
        lasty = tup[1]

    return (s1, s2)


print(sa("AAAGAATTCA", "AACATCACA", (10, -1, 3, 1)))
