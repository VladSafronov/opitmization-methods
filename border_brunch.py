import copy
import numpy as np

from b_b_tools import *

#2
# cij = [[float("Inf"), 26., 42., 15., 29., 25.],
#        [7., float("Inf"), 16., 1., 30., 25.],
#        [20., 13., float("Inf"), 35., 5., 0.],
#        [21., 16., 25., float("Inf"), 18., 18.],
#        [12., 46., 27., 48., float("Inf"), 5.],
#        [23., 5., 5., 9., 5., float("Inf")]
#        ]

cij = [[float("inf"),7.,16.,21.,2.,17.],
       [13.,float("inf"),21.,15.,43.,23.],
       [25.,3.,float("inf"),31.,17.,9.],
       [13.,10.,27.,float("inf"),33.,12.],
       [9.,2.,19.,14.,float("inf"),51.],
       [42.,17.,5.,9.,23.,float("inf")]
       ]
# cij = [[float("inf"),90.,80.,40.,100.],
#        [60.,float("inf"),40.,50.,70.],
#        [50.,30.,float("inf"),60.,20.],
#        [10.,70.,20.,float("inf"),50.],
#        [20.,40.,50.,20.,float("inf")]
#       ]
# cij = [[ float("inf") , 11.,  27. , float("inf"),  14.,  10.],
#  [  1. , float("inf") , 15.,   0. , 29.,  24.],
#  [ 15. , 13. , float("inf") , 35. ,  5.,   0.],
#  [  0. ,  0. ,  9. , float("inf") ,  2. ,  2.],
#  [  2.,  41.,  22.,  43., float("inf"),   0.],
#  [ 13. ,  0. ,  0. ,  4. ,  0., float("inf")]]
def choose_min_estimate_choice(choices):
    min_choice = None
    min = float("inf")
    for each in choices:
        if (min >= each.head_estimate or len(each.matrix)==1.):
            min = each.head_estimate
            min_choice = each

    if(min_choice is not None):
        choices.remove(min_choice)

    return min_choice

n = len(cij)

matrix = np.matrix(cij)
matr = Matrix(matrix)

matr.log = True

choices = []

l_r = matr.first_compute()

while(l_r["size"]>0):
    choices.append(l_r["left"])
    choices.append(l_r["right"])
    current = choose_min_estimate_choice(choices)

    print(current.head_estimate)
    print(current.path)

    l_r = current.compute2()

current = current.compute3()
print(current.head_estimate)
print(current.path)






