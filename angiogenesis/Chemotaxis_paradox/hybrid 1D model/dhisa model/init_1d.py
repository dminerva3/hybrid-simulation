import numpy
import math as m

def c_prof(coef,set,sol): #2.1.1.(1)
    for x in range(0,set['Nx']+1,2):
        sol['c'][x] = coef['A_c']*m.exp(-(x*set['Hh']+coef['shifted']-coef['vel']*set['dt']*set['k'])**2/coef['vari'])#0.05 set['dt']*set['k']
        if coef['w'] > 1:
            for i in range(1,coef['w']):
                sol['c'][x] += coef['A_c']*m.exp(-(x*set['Hh']+coef['shifted']+i*coef['perio']-coef['vel']*set['dt']*set['k'])**2/coef['vari'])
        
#     '''Different Var'''
#     dd = 0
#     x = 0
#     while dd == 0 and x <= set['Nx']:
#         if sol['c'][x] == coef['A_c']:
#             dd = 1
#         elif sol['c'][x] < coef['A_c']:
#             vari = 0.1
#             sol['c'][x] = coef['A_c']*m.exp(-(x*set['Hh']+(-3)*set['rad']-coef['vel']*set['t'])**2/vari)#0.05 set['dt']*set['k']
#             for i in range(1,100):
#                 sol['c'][x] += coef['A_c']*m.exp(-(x*set['Hh']+(-3)*set['rad']+i*coef['perio']-coef['vel']*set['t'])**2/vari)
#             x += 2
#         
        
    return sol

def init_1d_(coef,set,sol): #2.1.1
    sol['c'] = numpy.zeros(set['Nx']+1)
    sol['n'] = [set['Nx']/2+1]
    sol['center'] = [sol['c'][set['Nx']/2]]
    
    sol['A'] = numpy.zeros(set['Nx']+1)
    sol['I'] = numpy.zeros(set['Nx']+1)
    sol['Ki'] = numpy.zeros(set['Nx']+1)
    
    sol['F_Ki'] = numpy.zeros(set['Nx']+1)
    sol['G_Ki'] = numpy.zeros(set['Nx']+1)
    
    sol['vel_n'] = [0]
#     sol['in_vel_n'] = [0]
    sol['c_x'] = [0]
    sol['c_'] = [0]
    sol['A_'] = [0]
    sol['I_'] = [0]
    sol['Ki_p'] = [0]
    sol['Ki_n'] = [0]
#     sol['a_per_b_coef'] = [coef['alpha']/(coef['beta'])]
#     sol['c_t'] = [0]
#     sol['c_t_f'] = [0] 
       
    sol = c_prof(coef,set,sol)
    
    n_p = sol['n'][0]
    side = int(coef['l']/set['Hh'])
    pos_plus = n_p + side
    pos_neg = n_p - side
    if pos_plus % 2 == 0:
        print 'even'
        Ki_plus_mean = sol['Ki'][pos_plus]
        Ki_neg_mean = sol['Ki'][pos_neg]
    else:
        print 'odd'
        Ki_plus_mean = (sol['Ki'][pos_plus+1] + sol['Ki'][pos_plus-1])/2 
        Ki_neg_mean = (sol['Ki'][pos_neg+1] + sol['Ki'][pos_neg-1])/2
    
    sol['center_Ki_p'] = [Ki_plus_mean]
    sol['center_Ki_n'] = [Ki_neg_mean]
    
    return sol
        