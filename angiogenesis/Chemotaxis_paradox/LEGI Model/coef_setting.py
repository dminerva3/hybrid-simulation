from collections import OrderedDict

def declare_coef(): #1
    '''Coefficients'''
    #to store coefficients
    coef = {}
    set = {}
    sol = {} #
    
    '''LEGI Model'''
    coef['k_a'] = 3.3#0.3
    coef['k_i'] = 2.8#0.2
    coef['l_a'] = 0.2#0.02
    coef['l_i'] = 0.1#0.01
    coef['k_A'] = 3#5
    coef['k_I'] = 1.6#2
    coef['Ki_tot'] = 1
    coef['K_A'] = 0.44#3
    coef['K_I'] = 0.1#1

    ''''Tip (n)'''
    coef['D_n'] = 0.00018 #AUBERT, anderson chaplain tip Diffusion OK
#     coef['Ki_n'] = 0.33#133 #AUBERT, Stokes Chemotaxis coef (range max) OK
    coef['vel'] = 0.5#3 #velocity of wave
    coef['perio'] = 3#0.9 #period of wave
    coef['A_c'] = 0.8 #amplitude of wave
    
    '''Spatial and Temporal Meshes Number'''
    ##set dictionaries (fixed: never change)
    coef['X'] = 1
    coef['Y'] = 1
    set['T'] = 10.001 #
    set['Nt'] = 1000000
    set['h'] = 0.005 #0.005 #0.01#
    set['rad'] = 0.12
    set['dt'] = 0.001 #0.001
    set['Hh'] = set['h']/2
    set['Nx'] = int(coef['X']/set['Hh'])
    set['Ny'] = int(coef['Y']/set['Hh'])
       
    '''Initial Setting'''
    set['t'] = 0
    set['k'] = 0
       
    '''To store images'''
    ##sol dictionaries (can change)
    sol['stEC'] = 0
    sol['stEC_1'] = 0
    sol['stEC_2'] = 0
    sol['stEC_3'] = 0
    sol['stEC_4'] = 0
    sol['stEC_5'] = 0
    sol['stop_iter'] = 0
          
    return coef, set, sol