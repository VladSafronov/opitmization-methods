import math

g_data = [[19,17,15,13,11,9,7,10],
     [15,13,11,9,7,5,8,11],
     [10,8,6,4,7,10,13,16],
     [14,12,10,8,6,9,12,15]]
max_Y = len(g_data[0])


def f(i,delta_x):
     if(delta_x>0):
          return delta_x*2.5
     else:
          return math.fabs(delta_x*1.5)


def g(i,x):
  return g_data[i-1][x]

def B(i,Y):
     if(i==len(g_data)):
          min = float("inf")
          min_X = float("inf")

          for X in range(max_Y):
               bellman_step = f(i,X-Y)+g(i,X)
               if(bellman_step<min):
                    min = bellman_step
                    min_X = X

          return (min,min_X)

     else:
          min = float("inf")
          min_X = float("inf")

          for X in range(max_Y):
               bellman_step = f(i, X - Y) + g(i, X) + B(i+1,X)[0]
               if (bellman_step < min):
                    min = bellman_step
                    min_X = X

          return (min,min_X)

min_value = 0
current = B(1, max_Y)
print(current)
for i in range(2,len(g_data)+1):
     current = B(i,current[1])
     print(current)
