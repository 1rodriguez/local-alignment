from numpy import zeros, empty
from enum import Enum

class Alignment(Enum):
    NW = 1 # Needleman-Wunsch, global
    FIT = 2 # String fitting
    SW = 3 # Smith-Waterman, local
    

def sa(x: str, y: str, mode: Alignment, s: tuple):
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

    """
    The starting arrays will be altered as necessary:
    Needleman-Wunsch (NW): values for top and left rows given by -id and -jd respectively
    String Fitting (FIT): Top row (i, 0) values 0'd as no penalty given for fitting a prefix of longer string to all gaps in shorter string; left row given by -jd
    Smith-Waterman (SW): Top and left rows 0s

    NOTE: Due to this construction of the algorithm, when performing String Fitting, the long string should be passed as parameter x
    """

    if(mode is Alignment.NW):
        for i in range(d[0]):
            F[i][0] = i * gs
    if(mode is Alignment.FIT or mode is Alignment.NW):
        for j in range(d[1]):
            F[0][j] = j * gs

    # 'match' is used to determine whether to add/subtract the score for a match/mismatch depending on the two letters presently compared
    match: bool


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
            if mode is Alignment.SW: r = list(map(lambda a: 0 if a < 0 else a, r))

            m = max(r)

            pointers: tuple = ()

            for k, e in enumerate(r):
                if e == m:
                    pointers += (k,)

            F[i][j] = m
            P[i][j] = pointers
    
    print(F)
    print(P)
    

if __name__ == "__main__":
    # computes matrices used to calculate optimal solutions
    # note that traceback and optimal string construction was done manually
    print('\nGAATTC and GATTA global alignment: ')
    sa('GAATTC', 'GATTA', Alignment.NW, (2, -1, -1))
    print('\nfitting GACG to CTGAGAT: ')
    sa('GACG', 'CTGAGAT', Alignment.FIT, (2, -1, -1))
    print('\nGATACTTG and AATATGTA local alignment: ')
    sa('GATACTTG', 'AATATGTA', Alignment.SW, (2, -1, -1))
