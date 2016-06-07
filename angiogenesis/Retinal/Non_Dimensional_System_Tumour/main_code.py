from solve_cfT import c_f_T
from initial_conditions import initial_prof
from hybrid import hybrid_tech_c
from timeit import default_timer as timer

def check_anastomosis(sol):
    #creating list of active tips to be checked if the tip meets
    sp_in = []
    '''Check Anastomosis'''
    for noms in range(0,len(sol['matrix_tip'])):         
        if not noms in sol['sp_stop']:
            sp_in.append(noms)
    for tip_o in sp_in:
        for tips in sp_in:
            if tips > tip_o:
                cek1 = str(tip_o)
                cek2 = str(tips)
                if sol['matrix_tip'][tip_o][-1] == sol['matrix_tip'][tips][-1]:# and not cek1 in sol['pp'] and not cek2 in sol['pp']:
                    sol['sp_stop'].append(tip_o)
                    sol['list_tip_movement'][tip_o] = 'stop'
    
    '''TIP CELL'''
    sol['tip_cell'] = []          
    if len(sol['sp_stop']) > 0:               
        for e,tip in enumerate(sol['matrix_tip']):
            if not e in sol['sp_stop']:
                sol['tip_cell'].append([tip[-1][0],tip[-1][1]])
    else:
        for tip in sol['matrix_tip']:
            sol['tip_cell'].append([tip[-1][0],tip[-1][1]])
                
    return sol

def boolean_1_iter(coef, set, sol, check = 'out'):                       
    if set['k'] == 0:
        '''Initial Profile'''
        sol = initial_prof(coef, set, sol)  
    else:                             
        if len(sol['sp_stop']) == len(sol['matrix_tip']):
            sol['stop_iter'] = 100000 #sp_stop harus dicek di setiap movement and branching. karena sudah tidak bergerak lagi yang ada di list ini.
            print 'all looping itself or anastomosis'
            check = 'in'
        else:
            '''2. Branching and Movement''' 
            start1 = timer()  
            sol = hybrid_tech_c(coef, set, sol)
            start2 = timer()
            '''1. Anastomosis & Tip Cell'''
            #sol = check_anastomosis(sol)
            start3 = timer()
            '''Solving c,f,T'''
            sol = c_f_T(coef, set, sol)
            start4 = timer()            
        if not check == 'in':
            print 'Check Anastomosis Time', start3-start2
            print 'Hybrid for n time', start2-start1
            print 'Solve c,f,T time', start4-start3
                    
    return sol