from numpy import zeros, empty
from enum import Enum



def sa(x: str, y: str, s: tuple):
    d = (len(y) + 1, len(x) + 1)
    
    F = zeros(d)

    ms, mms, gs = s # match, mismatch, and gap scores from score tuple
    # NOTE: mms and gs should be passed as negative values

    """
    pointers will follow direction convention left = 2, up-left = 0, up = 1
    tuples of pointers kept for those occasions in which more than one
    string yields and optimal solution
    """
    P = empty(d, dtype=tuple) # Keep track of pointers

    # 'match' is used to determine whether to add/subtract the score for a match/mismatch depending on the two letters presently compared
    match: bool

    # used to find the global max of the matrix the, where we will work backwards to do the traceback
    globalMax = 0
    globalMaxXY: tuple = (1,1)


    # Algorithm starts at [1, 1]  as top/left rows were previously intiialized    
    for i in range(1, d[0]):
        for j in range(1, d[1]):
            match = x[j - 1] == y[i - 1]

            score = ms if match else mms
            r = [
                F[i - 1][j - 1] + score, 
                F[i - 1][j] + gs, 
                F[i][j - 1] + gs
                ]

            """
            The minimum values in the array per the Smith-Waterman algorithm are 0 (e.g. no penalty for starting string-matching at arbitrary points in the pair of strings)

            The results array is mapped to reflect this; any scores below 0 are mapped to 0
            """
            r = list(map(lambda a: 0 if a < 0 else a, r))

            m = max(r)

            pointers: tuple = ()

            for k, e in enumerate(r):
                if e == m:
                    pointers += (k,)

            F[i][j] = m
            P[i][j] = pointers

            # traceback logic
            if globalMax < m:
                globalMax = m
                globalMaxXY = (i, j)
    return (traceback(x, y, F, P, globalMaxXY))

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
        #this block came from the up-left position
        if currPtr[0] == 0:
            x = x - 1
            y = y - 1
            currMax = matrix[x][y]
        #this block came from the up position
        elif currPtr[0] == 1:
            x = x - 1
            currMax = matrix[x][y]
        #this block came from the left position
        else:
            y = y - 1
            currMax = matrix[x][y]

    #once the optimal xy route is found, create the strings using the loop below
    lastx = -1
    lasty = -1
    for i in range(0, len(recordOfCurMaxXY)):
        tuple = recordOfCurMaxXY[i]
        if tuple[0] == lastx:
            s1 += "_"
            s2 += colString[tuple[1] - 1]
        elif tuple[1] == lasty:
            s1 += rowString[tuple[0] - 1]
            s2 += "_"
        else:
            s1 += rowString[tuple[0] - 1]
            s2 += colString[tuple[1] - 1]
        lastx = tuple[0]
        lasty = tuple[1]

    return(s1, s2)


print(sa("AATTTTATGTA", "GATACTTG", (2, -1, -1)))
