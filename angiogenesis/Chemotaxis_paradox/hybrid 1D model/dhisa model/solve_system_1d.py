from random import randint, sample, uniform
import numpy
import math as m
import random
from random import randint
from sympy.polys.benchmarks.bench_solvers import sol_10x8

def set_list_prob(dirr): #2.2.(1)
    line_1 = range(1,10001)
    if dirr[1] == 0:
        list_prob_1 = []
    else:
        list_prob_1 = random.sample(line_1, dirr[1])
        for i in list_prob_1:
            line_1.remove(i)
    if dirr[2] == 0:
        list_prob_2 = []
    else:
        list_prob_2 = random.sample(line_1, dirr[2])
        for i in list_prob_2:
            line_1.remove(i)
    list_prob_0 = line_1
    return list_prob_0,list_prob_1,list_prob_2

def c_kinetic_(coef, set, sol, c_o, A_o, I_o, Ki_o):              
    '''at sub lattice'''
    for x in range(0,set['Nx']+1,2):
# #         sol['c'][x] = 0.5*(numpy.sin(2*m.pi/(coef['la'])*x*set['Hh']-2*m.pi/(coef['pe'])*set['dt']*set['k'])) 
# #         if sol['c'][x] < 0:
# #             sol['c'][x] *= 0
        '''Calculate c '''
        sol['c'][x] = coef['A_c']*m.exp(-(x*set['Hh']+coef['shifted']-coef['vel']*set['dt']*set['k'])**2/coef['vari'])
        if coef['w'] > 1:
            for i in range(1,coef['w']):
                sol['c'][x] += coef['A_c']*m.exp(-(x*set['Hh']+coef['shifted']+i*coef['perio']-coef['vel']*set['dt']*set['k'])**2/coef['vari'])        
        
        '''Calculate A,I,Ki'''
        sol['A'][x] = A_o[x]*(1-set['dt']*coef['l_a']) + set['dt']*coef['k_a']*c_o[x] + set['dt']*coef['teta_a']
        sol['I'][x] = I_o[x]*(1-set['dt']*coef['l_i']) + set['dt']*coef['k_i']*c_o[x] + set['dt']*coef['teta_i']
        
        if coef['LEGI'] == 'basic':
            ##Basic LEGI
            sol['F_Ki'][x] = coef['k_A']*(coef['R_o']-Ki_o[x])
            sol['G_Ki'][x] = coef['k_I']*Ki_o[x]
        elif coef['LEGI'] == 'ultrasensitive':
            ##Ultrasensitive LEGI
            sol['F_Ki'][x] = coef['k_A']*(coef['R_o']-Ki_o[x])/((coef['R_o']-Ki_o[x])+coef['K_A'])
            sol['G_Ki'][x] = coef['k_I']*Ki_o[x]/(Ki_o[x]+coef['K_I'])
            
        sol['Ki'][x] = Ki_o[x] + set['dt']*(sol['F_Ki'][x]*A_o[x] - sol['G_Ki'][x]*I_o[x])
        
    
    
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
    
    return sol
 
def system_1d(coef, set, sol): #2.3
    c_o = numpy.copy(sol['c']) #to save values at time step k (we are calculating at time step k+1)
    A_o = numpy.copy(sol['A'])
    I_o = numpy.copy(sol['I'])
    Ki_o = numpy.copy(sol['Ki'])
    
    sol = c_kinetic_(coef, set, sol, c_o, A_o, I_o, Ki_o)
    
    '''Calculate velocity of cell at n_p'''
    n_p = sol['n'][-1]
    print 'Position cell now:', n_p
    c_grad = (c_o[n_p+1]-c_o[n_p-1])/(set['h'])
    print 'c_grad', c_grad
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
    print 'KI', Ki_plus_mean - Ki_neg_mean
    print 'position of side -+', pos_neg, pos_plus
     
    vel_nn = coef['ki_o']* (Ki_plus_mean - Ki_neg_mean)# *c_grad
    sol['vel_n'].append(vel_nn)
    
    n_oo = sol['n'][0]
    side = int(coef['l']/set['Hh'])
    pos_plus = n_oo + side
    pos_neg = n_oo - side
    if pos_plus % 2 == 0:
        print 'even'
        Ki_c_plus_mean = sol['Ki'][pos_plus]
        Ki_c_neg_mean = sol['Ki'][pos_neg]
    else:
        print 'odd'
        Ki_c_plus_mean = (sol['Ki'][pos_plus+1] + sol['Ki'][pos_plus-1])/2 
        Ki_c_neg_mean = (sol['Ki'][pos_neg+1] + sol['Ki'][pos_neg-1])/2
    
    sol['center_Ki_p'].append(Ki_c_plus_mean)
    sol['center_Ki_n'].append(Ki_c_neg_mean)
    
    
    '''Save c, A, I, K'''
    c_mean = (c_o[n_p+1]+c_o[n_p-1])/2
    A_mean = (A_o[n_p+1]+A_o[n_p-1])/2
    I_mean = (I_o[n_p+1]+I_o[n_p-1])/2
    
#     '''Calculate Velocity of cell at n_p'''
#     n_p = sol['n'][-1]
#     print 'Position cell now:', n_p
    
#     c_mean_t = (sol['c'][n_p+1]+sol['c'][n_p-1])/2
#     c_grad = (c_o[n_p+1]-c_o[n_p-1])/(set['h'])
#     print 'c_grad at n', c_grad
#     a_per_b = c_mean/()
# #     if c_grad < 0:
# #         coef['alpha']
# #     elif c_grad > 0:
#     '''Metode c_t = cn'''    
# #     sol['vel_n'].append((coef['alpha'] - (coef['beta']*c_mean/((c_grad)**2+coef['xi'])))*c_grad) #SOL N_P = 1
# #     sol['in_vel_n'].append((coef['alpha'] - (coef['beta']*c_mean/((c_grad)**2+coef['xi']))))
# #     sol['a_per_b'].append(c_mean/((c_grad)**2+coef['xi']))
#     
#     '''Metode c_t = -w c_x'''
# #     sol['vel_n'].append((coef['alpha'] - (coef['beta']*coef['vel']*c_grad/((c_grad)**2+coef['xi'])))*c_grad)
# #     sol['in_vel_n'].append((coef['alpha'] - (coef['beta']*coef['vel']*c_grad/((c_grad)**2+coef['xi']))))
# #     sol['a_per_b_left'].append(coef['vel']*c_grad/((c_grad)**2+coef['xi']))
# #     sol['a_per_b_coef'].append(coef['alpha']/(coef['beta']))
#     
#     '''when vel w = 1'''
# #     sol['vel_n'].append(coef['alpha']*c_grad-coef['beta'])
# 
#     '''Using c_t = (c now - c yest) / dt'''
#     c_tt = (c_mean_t-c_mean)/set['dt']
#     sol['c_t'].append(c_tt)
# #     vel_nn = (coef['alpha']-coef['beta']*c_tt/((c_grad)**2+coef['xi']))*c_grad
# #     sol['vel_n'].append(vel_nn)
# #     
#     '''Using c_t = f_derivative'''
#     c_t_f = 0
#     for i in range(0,100): 
#         c_t_f += 2*coef['A_c']*(n_p*set['Hh']+(1)*set['rad']+i*coef['perio']-coef['vel']*set['t'])/coef['vari']*m.exp(-(n_p*set['Hh']+(1)*set['rad']+i*coef['perio']-coef['vel']*set['t'])**2/coef['vari'])
#     sol['c_t_f'].append(c_t_f)
#     vel_nn = (coef['alpha']-coef['beta']*c_t_f/((c_grad)**2+coef['xi']))*c_grad
#     sol['vel_n'].append(vel_nn)
    
    
    sol['c_x'].append(c_grad)
    sol['c_'].append(c_mean)
    sol['A_'].append(A_mean)
    sol['I_'].append(I_mean)
    sol['Ki_p'].append(Ki_plus_mean)
    sol['Ki_n'].append(Ki_neg_mean)
    sol['center'].append(sol['c'][set['Nx']/2])
    
    print '-----------------'
    print 'velocity_value', sol['vel_n'][-1]
    print '-----------------'
    
    '''Diffusion term'''
    p_1 = coef['D_n']*set['dt']/(set['h']**2)
    p_2 = p_1
    print 'diffusion term', p_1
    '''Adaptive term'''
    if sol['vel_n'][-1] < 0:
        p_1 += set['dt']/(set['h'])*(-sol['vel_n'][-1])
    else:
        p_2 += set['dt']/(set['h'])*(sol['vel_n'][-1])
    p_0 = 1-(p_1+p_2)    
    print 'prob', p_0,',', p_1, ',', p_2
    '''create integer number based on probability value'''
    P_1 = int(p_1*10000)
    P_2 = int(p_2*10000)
    
    '''boundary checking'''
    if n_p == 1:
        P_1 = 0
    elif n_p == set['Nx']-1:
        P_2 = 0
    P_0 = 10000-(P_1+P_2)
    
    '''Probability value'''
    dirr = [P_0, P_1, P_2]  
#     print dirr  
    list_prob_0,list_prob_1,list_prob_2 = set_list_prob(dirr)  
    
    '''Decide movement''' 
    tes = randint(1,10000)
    if tes in list_prob_0:
        sol['n'].append(sol['n'][-1])
        print 'stay'
    elif tes in list_prob_1:
        sol['n'].append(sol['n'][-1]-2)
        print 'left'
    elif tes in list_prob_2:
        sol['n'].append(sol['n'][-1]+2)
        print 'right'
    
    
                     
    return sol