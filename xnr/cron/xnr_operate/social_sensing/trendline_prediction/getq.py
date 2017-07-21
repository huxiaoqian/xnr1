__author__ = 'ray'
import math
def floatrange(start,stop,steps):
    ''' Computes a range of floating value.

        Input:
            start (float)  : Start value.
            end   (float)  : End value
            steps (integer): Number of values

        Output:
            A list of floats

        Example:
            >>> print floatrange(0.25, 1.3, 5)
            [0.25, 0.51249999999999996, 0.77500000000000002, 1.0375000000000001, 1.3]
    '''
    return [start+float(i)*(stop-start)/(float(steps)-1) for i in range(steps)]
def getpq(p,t):
    result = 0
    sum = 99999
    for q in floatrange(0.001, 1.901, 190):

        if math.fabs(t-(1/(p+q)*math.log(q/p))) < sum:
            sum = math.fabs(t-(1/(p+q)*math.log(q/p)))
            result = q
    #print (t-(1/(p+q)*math.log(q/p)))
    return result
