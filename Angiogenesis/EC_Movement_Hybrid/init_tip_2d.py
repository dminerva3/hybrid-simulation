import numpy
import math as m
from collections import OrderedDict

def rec_1_tip(coef,set,sol): #2.1.2.(1)
    y = set['Ny']/2 
    if y % 2 == 0:
        y += 1
    sol['matrix_tip'].append([(3,y)])
    sol['n'][3,y] = 1
    sol['b'][1,y] = 1
    #sol['b'][5,y] = 1
    #sol['b'][7,y] = 1
    sol['list_tip_movement'].append('start') #movement tip
    sol['life_time_tip'].append(0) #lifetime
    return sol

def rec_5_tip(coef,set,sol): #2.1.2.(2)
    '''Tip 0'''
    y = set['Ny']/6
    if y % 2 == 0:
        y += 1
    sol['matrix_tip'].append([(11,y-24)])
    sol['n'][11,y-24] = 1
    sol['b'][5,y-24] = 1
    sol['list_tip_movement'].append('start') #movement tip
    sol['life_time_tip'].append(0) #lifetime
    
    '''TIP 1'''
    y1 = 2*y
    if y1 % 2 == 0:
        y1 += 1
    sol['matrix_tip'].append([(11,y1-14)])
    sol['n'][11,y1-14] = 1
    sol['b'][5,y1-14] = 1
    sol['list_tip_movement'].append('start') #movement tip
    sol['life_time_tip'].append(0) #lifetime
    
    '''TIP 2'''
    y2 = 3*y
    if y2 % 2 == 0:
        y2 += 1
    sol['matrix_tip'].append([(11,y2)])
    sol['n'][11,y2] = 1
    sol['b'][5,y2] = 1
    sol['list_tip_movement'].append('start') #movement tip
    sol['life_time_tip'].append(0) #lifetime
    
    '''TIP 3'''
    y2 = 4*y
    if y2 % 2 == 0:
        y2 += 1
    sol['matrix_tip'].append([(11,y2+14)])
    sol['n'][10,y2+14] = 1
    sol['b'][5,y2+14] = 1
    sol['list_tip_movement'].append('start') #movement tip
    sol['life_time_tip'].append(0) #lifetime
    
    '''TIP 4'''
    y2 = 5*y
    if y2 % 2 == 0:
        y2 += 1
    sol['matrix_tip'].append([(10,y2+24)])
    sol['n'][10,y2+24] = 1
    sol['b'][5,y2+24] = 1
    sol['list_tip_movement'].append('start') #movement tip
    sol['life_time_tip'].append(0) #lifetime
    
    return sol

def init_tip_2d_(coef,set,sol):
    sol['n'] = numpy.zeros((set['Nx']+1,set['Ny']+1))
    sol['b'] = numpy.zeros((set['Nx']+1,set['Ny']+1))
    sol['Vb_x'] = numpy.zeros((set['Nx']+1,set['Ny']+1))
    sol['Vb_y'] = numpy.zeros((set['Nx']+1,set['Ny']+1))
    
    sol['matrix_tip'] = []
    sol['list_tip_movement'] = []
    sol['life_time_tip'] = []
    
    sol['sp_stop'] = []
    sol['tip_cell'] = []
    sol = rec_1_tip(coef,set,sol) #2.1.2.(1)
#     sol = rec_5_tip(coef,set,sol) #2.1.2.(2)
        
    '''Identifying Tip Cell'''
    for e,ti in enumerate(sol['matrix_tip']):
        sol['tip_cell'].append([sol['matrix_tip'][e][-1][0],sol['matrix_tip'][e][-1][1]])
    
    return sol