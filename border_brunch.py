import copy
import numpy as np

from b_b_tools import *
#
cij = [[float("Inf"), 26., 42., 15., 29., 25.],
       [7., float("Inf"), 16., 1., 30., 25. ],
       [20., 13., float("Inf"), 35., 5., 0. ],
       [21., 16., 25., float("Inf"), 18.,18.],
        [12., 46., 27., 48., float("Inf"), 5.],
       [23., 5., 5., 9., 5., float("Inf")]
       ]
# cij = [[ float("inf") , 11.,  27. , float("inf"),  14.,  10.],
#  [  1. , float("inf") , 15.,   0. , 29.,  24.],
#  [ 15. , 13. , float("inf") , 35. ,  5.,   0.],
#  [  0. ,  0. ,  9. , float("inf") ,  2. ,  2.],
#  [  2.,  41.,  22.,  43., float("inf"),   0.],
#  [ 13. ,  0. ,  0. ,  4. ,  0., float("inf")]]

n = len(cij)

matrix = np.matrix(cij)
matr = Matrix(matrix)

matr.log=True

l_r = matr.first_compute()

l_r = l_r["left"].compute2()
l_r = l_r["left"].compute2()

#Errors in estmate on this steps
l_r = l_r["left"].compute2()
l_r = l_r["left"].compute2()
_r = l_r["left"].compute2()

print()