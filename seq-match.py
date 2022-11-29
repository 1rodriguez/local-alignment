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
    


if __name__ == "__main__":
    # computes matrices used to calculate optimal solutions
    # note that traceback and optimal string construction was done manually
    print('\nGAATTC and GATTA global alignment: ')
    sa('GAATTC', 'GATTA', Alignment.NW, (2, -1, -1))
    print('\nfitting GACG to CTGAGAT: ')
    sa('GACG', 'CTGAGAT', Alignment.FIT, (2, -1, -1))
    print('\nGATACTTG and AATATGTA local alignment: ')
    sa('GATACTTG', 'AATATGTA', Alignment.SW, (2, -1, -1))
