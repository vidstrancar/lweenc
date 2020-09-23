import random
import numpy
import math


def uniform_sample_n_ball(n, d = 1):
    s = numpy.array([random.random() for _ in range(n)])
    norm = numpy.linalg.norm(s)
    s = random.random()*d*(s/norm)
    return s

def mod_lattice(y, B):
    n = len(B)
    y = numpy.array(y)
    B = numpy.array(B)
    ks = numpy.linalg.solve(B, y)
    ks = [math.floor(k) for k in ks]
    #v = [0 for _ in range(n)]
    #for k, w in zip(ks, B):
    #   v += k*w
    v = B.dot(ks)
    return y - v

#??!??!?! wat iz rajt, wat iz wrong??    
def sample(B, d):
    n = len(B)
    p = uniform_sample_n_ball(n, d)
    e = mod_lattice(p, B)
    return [p,e]

#mora prejeti L kot seznam numpy.array objektov
def list_reduce(p, L, ro):
    n = len(L)
    i = 0
    while i < len(L):
        l = L[i]
        if numpy.linalg.norm(p-l) <= ro*numpy.linalg.norm(p):
            p -= l
            i = 0
        else:
            i += 1
    return p

def list_sieve(B, mi):
    n = len(B)
    L = [numpy.array([0 for _ in range(n)])]
    delta = 1-1/n
    i = 0

    ksi = 0.685
    c1 = math.log(ksi+math.sqrt(ksi**2+1))+0.401
    K = 2**(c1*n)
    
    while i < K:
        i += 1
        (p, e) = sample(B, ksi*mi)
        p = list_reduce(p, L, delta)
        v = p - e
        v = numpy.array([int(c) for c in v])
        for w in L:
            if numpy.array_equal(v,w):
                break
            elif numpy.linalg.norm(v-w) < mi:
                return v-w
        L.append(v)
    
    return None



B = [[5,3],[2,2]]
# rešitev je [-1,0]??

""" s = uniform_sample_n_ball(3,3)
print(s)
print(numpy.linalg.norm(s))
print(mod_lattice([1.2,1],B))
print(sample(B, 4)) """

print(list_sieve(B, 3.5))