import matplotlib.pyplot as plt 
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
from mpl_toolkits.mplot3d import Axes3D



import numpy

def pic_2d(coef,set,sol):
    '''EC'''
    fig = plt.figure()
    plt.title('%s%f' % ('EC at t=',set['t']))
    plt.xlim(set['Hh'],coef['X']-set['Hh'])
    plt.ylim(set['Hh'],coef['Y']-set['Hh'])
    ax = fig.add_subplot(111)
    for i in range(0,len(sol['matrix_tip'])):
        x_p = []
        y_p = []
        for j in range(0,len(sol['matrix_tip'][i])):
            x_p.append(sol['matrix_tip'][i][j][0]*set['Hh'])
            y_p.append(sol['matrix_tip'][i][j][1]*set['Hh'])
        globals()['plo%s' % i] = ax.plot(x_p, y_p, 'c', color ='r')
    x_p = []
    y_p = []
    for tip in sol['tip_cell']:
        x_p.append(tip[0]*set['Hh'])
        y_p.append(tip[1]*set['Hh'])
    ax.scatter(x_p, y_p, marker = 'o', s = 2, color ='b')
    sol['stEC'] +=1  
    flag = 'EC=%s' % str(sol['stEC']) 
    plt.savefig("%s.png" % flag)
    plt.close()
    #plt.draw()
    
    if set['k'] % 50 == 0:
        ppp = 1
        '''Continuous Plot
        fig1 = plt.figure(1)
        plt.title('%s%f' % ('VEGF at t=',set['t']))
        #ax = fig1.gca(projection='3d')
        #ax.set_zlim(-0.1, 1)
        #ax.zaxis.set_major_locator(LinearLocator(10))
        #ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))

        #plt.set_xlabel('X')
        #plt.set_ylabel('Y')
        #plt.set_zlabel('Z')
        
        plt.xlabel('X')
        plt.ylabel('Y')
         
        x_sub_axis = numpy.arange(0, coef['X']+set['Hh'], set['h'])
        y_sub_axis = numpy.arange(0, coef['Y']+set['Hh'], set['h'])
        x_sub_axis, y_sub_axis = numpy.meshgrid(x_sub_axis, y_sub_axis)
         
        c_sol = numpy.zeros((set['Nx']/2+1, set['Ny']/2+1))
        for j, y in enumerate(range(0,set['Ny']+1,2)):
            for i, x in enumerate(range(0,set['Nx']+1,2)):
                c_sol[i,j] = sol['c'][x,y]
        #surf = ax.plot_surface(x_sub_axis, y_sub_axis, c_sol, rstride=1, cstride=1, cmap=cm.coolwarm,
        #        linewidth=0, antialiased=False)
        #fig1.colorbar(surf, shrink=0.5, aspect=5)
        plt.pcolormesh(y_sub_axis, x_sub_axis, c_sol)
        sol['stVEGF'] +=1  
        flag = 'VEGF=%s' % str(sol['stVEGF']) 
        plt.savefig("%s.png" % flag)
        plt.close()
        '''
        
        '''Continuous Plot b'''
        fig1 = plt.figure(1)
        plt.title('%s%f' % ('Stalk Cell at t=',set['t']))
        #ax = fig1.gca(projection='3d')
        #ax.set_zlim(-0.1, 1)
        #ax.zaxis.set_major_locator(LinearLocator(10))
        #ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))
        
        plt.xlabel('X')
        plt.ylabel('Y')
        
         
        x_sub_axis = numpy.arange(0, coef['X']+set['Hh'], set['h'])
        y_sub_axis = numpy.arange(0, coef['Y']+set['Hh'], set['h'])
        x_sub_axis, y_sub_axis = numpy.meshgrid(x_sub_axis, y_sub_axis)
         
        b_sol = numpy.zeros((set['Nx']/2+1, set['Ny']/2+1))
        for j, y in enumerate(range(0,set['Ny']+1,2)):
            for i, x in enumerate(range(0,set['Nx']+1,2)):
                b_sol[i,j] = sol['b'][x,y]
        #surf = ax.plot_surface(x_sub_axis, y_sub_axis, f_sol, rstride=1, cstride=1, cmap=cm.coolwarm,
        #        linewidth=0, antialiased=False)
        #fig1.colorbar(surf, shrink=0.5, aspect=5)
        plt.pcolormesh(y_sub_axis, x_sub_axis, b_sol)
        sol['stStalk'] +=1  
        flag = 'St=%s' % str(sol['stStalk']) 
        plt.savefig("%s.png" % flag)
        plt.close()
    
    return