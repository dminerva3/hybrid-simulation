
def movement_dir(x_pos = 0, y_pos = 0, cc = 0, ff = 0, mm = 0,
                 tep = 0, h1 = 0, R_min = 0, error = 0,
                 d_n1 = 0, ki_n1 = 0, al_n1 = 0, ro1 = 0,
                 n_x = 0, n_y = 0, Matrix_tip = 0,
                 kappa1 = 0, mic1 = 0,
                 last = False):

    la = tep/(h1**2)
    h2 = h1/2

    vvx = 0.5/h1*(cc[x_pos+1,y_pos+1]-cc[x_pos-1,y_pos+1]+cc[x_pos+1,y_pos-1]-cc[x_pos-1,y_pos-1])
    vvy = 0.5/h1*(cc[x_pos+1,y_pos+1]+cc[x_pos-1,y_pos+1]-cc[x_pos+1,y_pos-1]-cc[x_pos-1,y_pos-1])
    
    wwx = 0.5/h1*(ff[x_pos+1,y_pos+1]-ff[x_pos-1,y_pos+1]+ff[x_pos+1,y_pos-1]-ff[x_pos-1,y_pos-1])
    wwy = 0.5/h1*(ff[x_pos+1,y_pos+1]+ff[x_pos-1,y_pos+1]-ff[x_pos+1,y_pos-1]-ff[x_pos-1,y_pos-1])
    
    vvx_p = max(0,vvx)
    vvx_n = max(0,-vvx)
    vvy_p = max(0,vvy)
    vvy_n = max(0,-vvy)
    
    wwx_p = max(0,wwx)
    wwx_n = max(0,-wwx)
    wwy_p = max(0,wwy)
    wwy_n = max(0,-wwy)
    
    '''With chemotaxis inhibition'''
    ki_n1 = ki_n1/(1+mic1*mm[x_pos,y_pos])
    
    '''With haptotaxis activation'''
    ro1 = ro1 + kappa1*mm[x_pos,y_pos]
    
    
    P_1 = la*d_n1+la*h1*ki_n1/(1+al_n1*cc[x_pos-1,y_pos+1])*vvx_n + la*h1*ro1*wwx_n
    P_2 = la*d_n1+la*h1*ki_n1/(1+al_n1*cc[x_pos+1,y_pos+1])*vvx_p + la*h1*ro1*wwx_p
    
    P_3 = la*d_n1+la*h1*ki_n1/(1+al_n1*cc[x_pos+1,y_pos-1])*vvy_n + la*h1*ro1*wwy_n
    P_4 = la*d_n1+la*h1*ki_n1/(1+al_n1*cc[x_pos+1,y_pos+1])*vvy_p + la*h1*ro1*wwy_p
    
    '''Boundary on the inner circle'''
    O_x = n_x/2*h2
    O_y = n_y/2*h2
    r_f = (x_pos*h2-O_x)**2 + (y_pos*h2-O_y)**2
    Pos = (x_pos,y_pos)
    
    for list_1_tip in Matrix_tip:
        for node in list_1_tip:
            if (x_pos-2,y_pos) == node:
                P_1 = 0
            if (x_pos+2,y_pos) == node:
                P_2 = 0
            if (x_pos,y_pos-2) == node:
                P_3 = 0
            if (x_pos,y_pos+2) == node:
                P_4 = 0
    if P_1 == 0 and P_2 == 0 and P_3 == 0 and P_4 == 0:
        P_1 = 0.25
        P_2 = 0.25
        P_3 = 0.25
        P_4 = 0.25
        last = True        
                
        
    if last == False:
        if Pos == Matrix_tip[0][0]:
            P_2 = 0        
        elif Pos == Matrix_tip[1][0]:
            P_1 = 0
        elif Pos == Matrix_tip[2][0]:
            P_4 = 0
        elif Pos == Matrix_tip[3][0]:
            P_3 = 0
        elif r_f <= (R_min**2 + error):
            if x_pos >= Matrix_tip[2][0][0] and y_pos >= Matrix_tip[0][0][1]:
                P_1 = 0
                P_3 = 0
            elif x_pos <= Matrix_tip[2][0][0] and y_pos >= Matrix_tip[0][0][1]:
                P_2 = 0
                P_3 = 0
            elif x_pos <= Matrix_tip[2][0][0] and y_pos <= Matrix_tip[0][0][1]:
                P_2 = 0
                P_4 = 0
            elif x_pos >= Matrix_tip[2][0][0] and y_pos <= Matrix_tip[0][0][1]:
                P_1 = 0
                P_4 = 0
    '''Using Non-reflection Boundary'''
            
    P_0 = 1-(P_1+P_2+P_3+P_4)
    R_0 = P_0
    R_1 = P_0+P_1
    R_2 = P_0+P_1+P_2
    R_3 = P_0+P_1+P_2+P_3
    R_4 = 1
    
    prob_range = [R_0,R_1,R_2,R_3,R_4, last]
#    print 'probability P', P_0, ',',P_1,',',P_2,',',P_3,',',P_4
    return prob_range;

def discrete_1_iter(iter = 0, hh = 0, Nx = 0, Ny = 0,
                    r_min = 0, r_max = 0,
                    ro = 0, d_n = 0, ki_n = 0, al_n = 0,
                    t_branch = 0,
                    matrix_tip = 0, list_last_movement = 0, 
                    list_tip_movement = 0, life_time_tip = 0,
                    stop_iter = 0, sp_stop = 0,
                    n = 0, tp = 0, c = 0, f = 0, m = 0,
                    Error = 0.01,
                    kappa = 0, mic = 0):
 
 
    
 

    import numpy
    import random
    from random import randint
    h2 = 2*hh
    O_x = Nx/2*hh
    O_y = Ny/2*hh
    
    '''Define Initial Profile'''
    if iter == 1:           
        matrix_tip = []
        list_last_movement = []
        list_tip_movement = []
        life_time_tip = []
        sp_stop = []
        
        matrix_tip_m = []
        list_last_movement_m = []
        list_tip_movement_m = []
        life_time_tip_m = []
        sp_stop_m = []
                        
        ''''Initial Tips'''
        n = numpy.zeros((Nx+1,Ny+1))
        
        y1 = Ny/2 + 1
        x = 1
        while x < Nx+1:
            if (x*hh-O_x)**2 + (y1*hh-O_y)**2 < r_min**2 + Error and (x*hh-O_x)**2 + (y1*hh-O_y)**2 > r_min**2:
                    matrix_tip.append([(x,y1)])
                    n[x,y1] = 1
                    list_last_movement.append('start') #last tip movement
                    list_tip_movement.append('start') #movement tip
                    life_time_tip.append(0) #lifetime
                    u = 10
            else:
                u = 2           
            x += u
            
        y1 = Nx/2 + 1
        x = 1
        while x < Nx+1:
            if (x*hh-O_x)**2 + (y1*hh-O_y)**2 < r_min**2 + Error and (x*hh-O_x)**2 + (y1*hh-O_y)**2 > r_min**2:
                    matrix_tip.append([(y1,x)])
                    n[y1,x] = 1
                    list_last_movement.append('start') #last tip movement
                    list_tip_movement.append('start') #movement tip
                    life_time_tip.append(0) #lifetime
                    u = 10
            else:
                u = 2           
            x += u
                 
        y1 = matrix_tip[2][0][0] + (matrix_tip[1][0][0]- matrix_tip[2][0][0])/2
        if y1 % 2 == 0:
            y1 += 1
        x = 1
        while x < Nx+1:
            if (x*hh-O_x)**2 + (y1*hh-O_y)**2 < r_min**2 + Error and (x*hh-O_x)**2 + (y1*hh-O_y)**2 > r_min**2:
                    matrix_tip.append([(y1,x)])
                    n[y1,x] = 1
                    list_last_movement.append('start') #last tip movement
                    list_tip_movement.append('start') #movement tip
                    life_time_tip.append(0) #lifetime
                    u = 10
            else:
                u = 2           
            x += u
                    
        y1 = matrix_tip[0][0][0] + (matrix_tip[2][0][0]-matrix_tip[0][0][0])/2
        if y1 % 2 == 0:
            y1 += 1
        x = 1
        while x < Nx+1:
            if (x*hh-O_x)**2 + (y1*hh-O_y)**2 < r_min**2 + Error and (x*hh-O_x)**2 + (y1*hh-O_y)**2 > r_min**2:
                    matrix_tip.append([(y1,x)])
                    n[y1,x] = 1
                    list_last_movement.append('start') #last tip movement
                    list_tip_movement.append('start') #movement tip
                    life_time_tip.append(0) #lifetime
                    u = 10
            else:
                u = 2           
            x += u
         
        '''Initial Tips'''
    else:
        '''1. Anastomosis''' #not yet
        sp_new_stop =[]
    #    for noms in range(0,len(matrix_tip)):         
    #        if not noms in sp_stop:
    #            '''1.1 Checking if looping itself'''
    #            if not globals()['tip%s' % noms] == 'stay':
    #                gg = globals()['sp%s' % noms][:]
    #                gg.pop()
    ##                gg = list(set(gg))    
    #                if len(gg) > 0: #mencegah start masuk ke bagian ini
    #                    if globals()['sp%s' % noms][-1] in gg:
    #                        sp_new_stop.append(noms)
    #                        print 'looping itself for tip number', noms
    #                        print 'looping to position', globals()['sp%s' % noms][-1]
    #                #kalau < = 0, artinya baru start iterasi
    #            #kalau 'stay', artinya aman. do nothing. done looping itself
    #            '''1.2 Checking if hit another sprout'''
    #            if noms in sp_new_stop or len(matrix_tip) == 1: #kalau sudah looping itself, gak usah cek hit others lg.
    #                pass
    #            elif not list_last_movement[noms] == 'stay':
    #                #making list of others
    #                other_tips = range(0,len(matrix_tip))
    #                other_tips.remove(noms)
    #                for i in other_tips:
    #                    if matrix_tip[noms][-1] in matrix_tip[i]:
    #                        sp_new_stop.append(noms)
    #                        print 'anastomosis for tip number ', noms, ' to tip number ', i 
    #                        print 'anastomosis at position', matrix_tip[noms][-1]
    #                    #kalau gak hit, do nothing
        '''1.3 Checking if two tips meet at one point'''
        other_tips = range(0,len(matrix_tip))
        for noms in range(0,len(matrix_tip)):         
            if not noms in sp_stop:
                if not list_last_movement[noms] == 'stay':
                    #making list of others
                    other_tips.remove(noms)
                    for i in other_tips:
                        if matrix_tip[noms][-1] in matrix_tip[i][-1]:
                            sp_new_stop.append(noms)
                else:
                     other_tips.remove(noms)
            else:
                other_tips.remove(noms)      
                    
    #    if len(sp_new_stop) >= 2:
    #        pair = [(0,0)]
    #        for j in sp_new_stop:
    #            other_tips = []
    #            for uu in sp_new_stop:
    #                other_tips.append(uu)
    #            other_tips.remove(j)
    #            for i in other_tips:
    #                if matrix_tip[j][-1] == matrix_tip[i][-1]:
    #                    jjj = (j,i)
    #                    if reversed(jjj) in pair:
    #                        lop = 1
    #                    else:
    #                        pair.append((j,i))
    #        pair.remove((0,0))
    #        if len(pair) >= 1:
    #            for j in range(1,len(pair)):             
    #                sp_new_stop.remove(pair[j][0])         
    #    sp_stop.extend(sp_new_stop)
    #    sp_stop = list(set(sp_stop))
    #    for noms in range(0,len(matrix_tip)):
    #        if not noms in sp_stop:
    #            for i in range(0,len(matrix_tip[noms])):
    #                if matrix_tip[noms][i][1] == Nx-1:
    #                    sp_stop.append(noms)
        for i in sp_stop:
            list_last_movement[i] = 'stop'
        
        '''2. Branching and Movement'''        
        if len(sp_stop) == len(matrix_tip):
            stop_iter = 100000 #sp_stop harus dicek di setiap movement and branching. karena sudah tidak bergerak lagi yang ada di list ini.
            print 'all looping itself or anastomosis'
        else:    
            ##branching decision and action. Also movement   
            line = range(1,11) #for Pb
            n_sp = len(matrix_tip) #to save original number of tips before branching
            
            for nom in range(0,n_sp): #dicek setiap tip
                if nom in sp_stop: #kalo dia sudah anastomosis, gak perlu branching dan move lg.
    #                 print 'no_moving for tip', nom
                    pass
                else:
                    xb = matrix_tip[nom][-1][0] #get x position of last tip position
                    yb = matrix_tip[nom][-1][1] #get y position of last tip position
                    #print 'xb,yb', xb,',',yb
                    dirr = movement_dir(x_pos = xb, y_pos = yb, cc = c, ff = f, mm = m,
                                        tep = tp, h1 = h2, R_min = r_min, error = Error,
                                        d_n1 = d_n, ki_n1 = ki_n, al_n1 = al_n, ro1 = ro,
                                        n_x = Nx, n_y = Ny, Matrix_tip = matrix_tip,
                                        kappa1 = kappa, mic1 = kappa)
                    if dirr[5] == True:
                        life_time_tip[nom] += tp
                        no_back = list_tip_movement[nom]
                        while no_back == list_tip_movement[nom]:
                            trial = random.uniform(0,1)
                            if trial <= dirr[0]: #stay
                                no_back = 'pro' #stay
                            elif trial <= dirr[1]: #left
                                no_back = 'right'
                            elif trial <= dirr[2]: #right
                                no_back = 'left'
                            elif trial <= dirr[3]: #down
                                no_back = 'up'
                            else: #>dirr[3] #up
                                no_back = 'down'
                        if no_back == 'pro':
                            tipp = 'stay'
    #                        globals()['sp%s' % nom].append(globals()['sp%s' % nom][-1])
                        elif no_back == 'right':
                            tipp = 'left'
                            xpos_new = matrix_tip[nom][-1][0] - 2
                            ypos_new = matrix_tip[nom][-1][1]
                            matrix_tip[nom].append((xpos_new,ypos_new))
                            n[xpos_new,ypos_new] = 1
                        elif no_back == 'left':
                            tipp = 'right'
                            xpos_new = matrix_tip[nom][-1][0] + 2
                            ypos_new = matrix_tip[nom][-1][1]
                            matrix_tip[nom].append((xpos_new,ypos_new)) 
                            n[xpos_new,ypos_new] = 1
                        elif no_back == 'up':
                            tipp = 'down'
                            xpos_new = matrix_tip[nom][-1][0]
                            ypos_new = matrix_tip[nom][-1][1] - 2
                            matrix_tip[nom].append((xpos_new,ypos_new)) 
                            n[xpos_new,ypos_new] = 1
                        else:
                            tipp = 'up'
                            xpos_new = matrix_tip[nom][-1][0]
                            ypos_new = matrix_tip[nom][-1][1] + 2
                            matrix_tip[nom].append((xpos_new,ypos_new))
                            n[xpos_new,ypos_new] = 1
                            
                        '''2.2.2 Renewal Some Vars'''
                        list_tip_movement[nom] = 'stop'
                        list_last_movement[nom] = 'stop'
                        sp_stop.append(nom)  
                    else: #the tip doesn't stuck
                        '''2.1 Branching Decision''' 
                        if life_time_tip[nom] >= t_branch: #being able to branch by life time               
                            #probabilty of branching
        #                    print 'NILAI C', c[xb+1,yb+1]
                            if c[xb+1,yb+1] >= 0 and c[xb+1,yb+1] < 0.1:
                                prob_weight = 2 # set the number to select here.
                                list_prob = random.sample(line, prob_weight) #list of selected numbers from line
                            elif c[xb+1,yb+1] >= 0.1 and c[xb+1,yb+1] < 0.2:
                                prob_weight = 3 # set the number to select here.
                                list_prob = random.sample(line, prob_weight)   
                            elif c[xb+1,yb+1] >= 0.2 and c[xb+1,yb+1] < 0.3:
                                prob_weight = 4 # set the number to select here.
                                list_prob = random.sample(line, prob_weight)  
                            elif c[xb+1,yb+1] >= 0.3: #do branching
                                list_prob = line
                            else: #no branching or in the condition: c[xb+1,yb+1,k+1] < 0.3
                                list_prob = [20]
                        else: #not branchable
                            list_prob = [20]
                        #apakah branching? meaning masuk dalam probability of branching?
                        tes = randint(1,10) #select integer number randomly between 1 and 10
                        if tes in list_prob:#do branching
                            '''2.1.1 Branching tip's movement: 1st tip movement: nom tip'''
                            '''2.1.1.1 Checking no back and stay movement'''
                            no1_back = list_tip_movement[nom]
                            no_back = list_tip_movement[nom]
                            while no_back == list_tip_movement[nom]:
                                trial = random.uniform(0,1)
                                if trial <= dirr[0]: #stay
                                    no_back = list_tip_movement[nom] #karna branching, dia harus move
                                elif trial <= dirr[1]: #left
                                    no_back = 'right'
                                elif trial <= dirr[2]: #right
                                    no_back = 'left'
                                elif trial <= dirr[3]: #down
                                    no_back = 'up'
                                else: #>dirr[3] #up
                                    no_back = 'down'
                            #movement 1st tip
                            if no_back == 'right':
                                tip_1 = 'left'
                                xpos_new = matrix_tip[nom][-1][0] - 2
                                ypos_new = matrix_tip[nom][-1][1]
                                matrix_tip[nom].append((xpos_new,ypos_new))
                            elif no_back == 'left':
                                tip_1 = 'right'
                                xpos_new = matrix_tip[nom][-1][0] + 2
                                ypos_new = matrix_tip[nom][-1][1]
                                matrix_tip[nom].append((xpos_new,ypos_new))
                            elif no_back == 'up':
                                tip_1 = 'down'
                                xpos_new = matrix_tip[nom][-1][0]
                                ypos_new = matrix_tip[nom][-1][1] - 2
                                matrix_tip[nom].append((xpos_new,ypos_new))
                            else:
                                tip_1 = 'up'
                                xpos_new = matrix_tip[nom][-1][0]
                                ypos_new = matrix_tip[nom][-1][1] + 2
                                matrix_tip[nom].append((xpos_new,ypos_new))
                            n[xpos_new,ypos_new] = 1
                            
                            '''2.1 Branhcing'''
                            
                            matrix_tip.append([(xb,yb)])
                            #waktunya diriset
                            life_time_tip.append(0)
                            life_time_tip[nom] = 0
                            
                            '''2.1.2 Branching tip's movement: 2nd tip movement : num_sp tip'''
                            '''2.1.2.1 Checking no back, tip 1, stay movement'''
                            #ada no1_back
                            #ada tip_1
                            dom = tip_1
                            while no1_back == list_tip_movement[nom] or dom == tip_1:
                                trial = random.uniform(0,1)
                                if trial <= dirr[0]:
                                    dom = tip_1
                                elif trial <= dirr[1]:
                                    dom = 'left'
                                    no1_back = 'right'
                                elif trial <= dirr[2]:
                                    dom = 'right'
                                    no1_back = 'left'
                                elif trial <= dirr[3]:
                                    dom = 'down'
                                    no1_back = 'up'
                                else: #>dirr[3]
                                    dom = 'up'
                                    no1_back = 'down'
                            #movement 2nd tip
                            if dom == 'left':
                                xpos_new = matrix_tip[-1][-1][0] - 2
                                ypos_new = matrix_tip[-1][-1][1]
                                matrix_tip[-1].append((xpos_new,ypos_new))
                            elif dom == 'right':
                                xpos_new = matrix_tip[-1][-1][0] + 2
                                ypos_new = matrix_tip[-1][-1][1]
                                matrix_tip[-1].append((xpos_new,ypos_new))
                            elif dom == 'down':
                                xpos_new = matrix_tip[-1][-1][0]
                                ypos_new = matrix_tip[-1][-1][1] - 2
                                matrix_tip[-1].append((xpos_new,ypos_new))
                            else: #dom == 'up'
                                xpos_new = matrix_tip[-1][-1][0]
                                ypos_new = matrix_tip[-1][-1][1] + 2
                                matrix_tip[-1].append((xpos_new,ypos_new))
                            
                            n[xpos_new,ypos_new] = 1
                            
                            '''2.1.3 Renewal Some Vars'''
                            if not dom == 'stay':
                                list_tip_movement.append(dom)
                            if not tip_1 == 'stay':
                                list_tip_movement[nom] = tip_1
                            list_last_movement.append(dom)
                            list_last_movement[nom] = tip_1   
        #                    life_time_tip[-1] = tp
                            
                        else: #no branching
                            '''2.2 No Branching'''
                            '''Movement only'''
                            '''2.2.1 Checking no back movement'''
                            life_time_tip[nom] += tp
                            no_back = list_tip_movement[nom]
                            while no_back == list_tip_movement[nom]:
                                trial = random.uniform(0,1)
                                if trial <= dirr[0]: #stay
                                    no_back = 'pro' #stay
                                elif trial <= dirr[1]: #left
                                    no_back = 'right'
                                elif trial <= dirr[2]: #right
                                    no_back = 'left'
                                elif trial <= dirr[3]: #down
                                    no_back = 'up'
                                else: #>dirr[3] #up
                                    no_back = 'down'
                            if no_back == 'pro':
                                tipp = 'stay'
        #                        globals()['sp%s' % nom].append(globals()['sp%s' % nom][-1])
                            elif no_back == 'right':
                                tipp = 'left'
                                xpos_new = matrix_tip[nom][-1][0] - 2
                                ypos_new = matrix_tip[nom][-1][1]
                                matrix_tip[nom].append((xpos_new,ypos_new))
                                n[xpos_new,ypos_new] = 1
                            elif no_back == 'left':
                                tipp = 'right'
                                xpos_new = matrix_tip[nom][-1][0] + 2
                                ypos_new = matrix_tip[nom][-1][1]
                                matrix_tip[nom].append((xpos_new,ypos_new)) 
                                n[xpos_new,ypos_new] = 1
                            elif no_back == 'up':
                                tipp = 'down'
                                xpos_new = matrix_tip[nom][-1][0]
                                ypos_new = matrix_tip[nom][-1][1] - 2
                                matrix_tip[nom].append((xpos_new,ypos_new)) 
                                n[xpos_new,ypos_new] = 1
                            else:
                                tipp = 'up'
                                xpos_new = matrix_tip[nom][-1][0]
                                ypos_new = matrix_tip[nom][-1][1] + 2
                                matrix_tip[nom].append((xpos_new,ypos_new))
                                n[xpos_new,ypos_new] = 1
                                
                            '''2.2.2 Renewal Some Vars'''
                            if not tipp == 'stay':
                                list_tip_movement[nom] = tipp
                            list_last_movement[nom] = tipp  
    
    for i in range(0, len(matrix_tip)):
        print 'tip',i,':',matrix_tip[i]
#         print 'life time tip',i+1,':', life_time_tip[i]   
#         print 'last tip movement of tip',i+1,':', list_last_movement[i]    
    print 'List Stop Tips:', sp_stop
    print 'Total Tips:', len(matrix_tip)
    print 'Total Stop Tips:', len(sp_stop)    
    '''***BRANCHING/PY END***'''
    
    ty = tp
    gg = [matrix_tip, list_last_movement, list_tip_movement, life_time_tip, stop_iter, sp_stop, n, ty]
    
    return gg
    