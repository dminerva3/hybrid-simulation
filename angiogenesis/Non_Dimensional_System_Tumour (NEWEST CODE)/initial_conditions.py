import numpy
import random
from random import randint
from init_2d import init_2d_
from init_tip_2d import init_tip_2d_
from init_3d import init_3d_
from init_tip_3d import init_tip_3d_
from init_tip_3d_n import init_tip_3d_n_

def initial_prof(coef, set, sol):
    if set['layout'] == '2D':
        sol = init_2d_(coef,set,sol)
        sol = init_tip_2d_(coef,set,sol)
    if set['layout'] == '3D':
        sol = init_3d_(coef,set,sol)
        #sol = init_tip_3d_(coef,set,sol)
        sol = init_tip_3d_n_(coef,set,sol)
    print 'initial tips:', sol['matrix_tip']
    if set['parent'] == 'two':
        print 'initial tips2:', sol['matrix_tip_2']
    return sol