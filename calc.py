import numpy
import math
import matplotlib.pyplot as plt

pi=math.pi
cos=math.cos
sin=math.sin

def SolveMFE(H,X,f):
#-u''(x)+q(x)*u(x)=f(x)
#u(a)=2.0923, u'(b)=16.1356
    n=len(X)
    A=numpy.zeros((n,n))
    b=numpy.zeros(n)
    for i in range(1,n-1):
        A[i,i]=1/H+1/H
        A[i,i+1]=-1/H
        A[i,i-1]=-1/H
        b[i]=f(X[i])/2*(H+H)

    A[0,0]=1/H+1/H
    A[0,1]=-1/H
    A[n-1,n-2]=-1/H
    A[n-1,n-1]=1/H
    b[0]=f(X[0])/2*(H+H)+2.0923/H

    b[n-1]=H/2*f(X[n-2]) + 16.1356

    y= numpy.linalg.solve(A, b)
    return y

def f(x=0):
    return -4*pi*(cos(2*pi*x)-pi*x*sin(2*pi*x))

def u_t(x=0):
    return x*sin(2*pi*x)

def calc(N=400):
    a = -2.2
    b = 4.15
    X = numpy.linspace(a, b, N)
    H = (b - a) / N
    Y = SolveMFE(H, X, f)
    return X, Y
