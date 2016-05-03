#-*- endcoding:utf8 -*-

# x = [6.082,6.200,6.148,6.254,6.300,6.279,6.178,6.184,5.915,5.862,5.890,5.866,5.927,5.898]
# x = [11.51,11.85,11.72,11.88,12.22,12.06,11.79,11.86,11.34,11.03,11.07,10.83,10.94,10.81]
x = [17.30,17.61,17.70,17.38]
x = [10.59,10.57]

def EMA(x,n):
    if n is 1:
        return x[-1]
    this = x[-1]
    x = x[:-1]
    return (2*this + (n-1)*EMA(x,n-1))/(n+1)


def EMAsequence(x,n):
    length = len(x)
    sequence = []
    for i in range(length-n+1):
        num = EMA(x,n)
        sequence.insert(0,num)
        # sequence.append(num)
        x = x[:-1]

    return sequence

m = EMAsequence(x,2)
print m