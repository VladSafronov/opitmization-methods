import numpy as np
import copy

bellman_func = str("belman_func")
last_solve_coor = str("last_solve_coor")

def B(k,Y):

    if(k==0):
        return {bellman_func: resource_efficiency[k][Y],last_solve_coor: Y}

    max_B_value = -float("inf")
    max_B = None
    max_Z = -1

    Z = 0
    while Z<=Y:

        bellman_func_value = B(k-1,Z)[bellman_func] + resource_efficiency[k][Y-Z]

        if (bellman_func_value >= max_B_value):
            max_B_value = bellman_func_value
            max_Z = Z

        Z += 1

    if (Y == 0):
        max_Z = Y


    last_solve_coor_value = Y-max_Z

    return{bellman_func:max_B_value,last_solve_coor:last_solve_coor_value}



resource_efficiency = [
                      [0,1,2,3,3,4],
                      [0,0,1,2,4,7],
                      [0,2,2,3,3,3]
                    ]


n = len(resource_efficiency)
Y = len(resource_efficiency[0])



table = copy.deepcopy(resource_efficiency)


for i in range(Y):
    table[0][i] = B(0,i)

for k in range(1,n):

    for currentY in range(Y):

        if(currentY==0):
            max_B = B(k,0)
        else:
            max_B = B(k,currentY)

        table[k][currentY] = max_B

print(table)