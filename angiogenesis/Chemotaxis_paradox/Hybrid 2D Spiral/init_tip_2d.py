import numpy
import math as m
from collections import OrderedDict
import random

def rec_5_tip(coef,set,sol): #2.1.2.(2)
    for i in range(10):
        x = random.randrange(1,400+1,2)
        y = random.randrange(1,400+1,2)
        sol['matrix_tip'].append([[x,y]])
        sol['n'][x,y] = 1
        sol['list_tip_movement'].append('start') #movement tip
        sol['life_time_tip'].append(0) #lifetime
    
    return sol

def init_tip_2d_(coef,set,sol):
    sol['n'] = numpy.zeros((set['Nx']+1,set['Ny']+1))
    sol['stalk'] = numpy.zeros((set['Nx']+1,set['Ny']+1))
#     sol['b'] = numpy.zeros((set['Nx']+1,set['Ny']+1))
#     sol['Vb_x'] = numpy.zeros((set['Nx']+1,set['Ny']+1))
#     sol['Vb_y'] = numpy.zeros((set['Nx']+1,set['Ny']+1))
    
    sol['matrix_tip'] = []
    sol['list_tip_movement'] = []
    sol['life_time_tip'] = []
    
    sol['sp_stop'] = []
    sol['tip_cell'] = []
    sol = rec_5_tip(coef,set,sol) #2.1.2.(2)
        
    '''Identifying Tip Cell'''
    for e,ti in enumerate(sol['matrix_tip']):
        sol['tip_cell'].append([sol['matrix_tip'][e][-1][0],sol['matrix_tip'][e][-1][1]])   
    return sol