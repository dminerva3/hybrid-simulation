import matplotlib.pyplot as plt 
import numpy
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
from mpl_toolkits.mplot3d import Axes3D

def pic_2d(coef,set,sol):           
    '''EC'''
    fig = plt.figure(1)
    plt.title('%s%f' % ('Vessel Growth at t=',set['t']))
    plt.xlabel('X')
    plt.ylabel('Y') 
    ax = fig.add_subplot(111)
    for i in range(0,len(sol['matrix_tip'])):
        x_p = []
        y_p = []
        for j in range(0,len(sol['matrix_tip'][i])):
            x_p.append(sol['matrix_tip'][i][j][0]*set['Hh'])
            y_p.append(sol['matrix_tip'][i][j][1]*set['Hh'])
        globals()['plo%s' % i] = ax.plot(x_p, y_p, 'c', color ='k')
    x_pp = []
    y_pp = []
    for tip in sol['tip_cell']:
        x_pp.append(tip[0]*set['Hh'])
        y_pp.append(tip[1]*set['Hh'])
    ax.scatter(x_pp, y_pp, marker = 'o', s = 5, color ='r')
    '''Backward Marker'''
    if len(sol['backward_list']) > 0:
        x_pp = []
        y_pp = []
        for tip in sol['backward_list']:
            x_pp.append(tip[0]*set['Hh'])
            y_pp.append(tip[1]*set['Hh'])
        ax.scatter(x_pp, y_pp, marker = '^', s = 10, color ='c')
    plt.xlim((set['Hh'],coef['X']-set['Hh']))
    plt.ylim((set['Hh'],coef['Y']-set['Hh']))
    sol['stEC'] +=1  
    flag = 'EC=%s' % str(sol['stEC']) 
    plt.savefig("%s.png" % flag)
    plt.close()
    
    '''Record for ecm, vegf'''
    x_sub_axis = numpy.arange(0, coef['X']+set['Hh'], set['h'])
    y_sub_axis = numpy.arange(0, coef['Y']+set['Hh'], set['h'])
    x_sub_axis, y_sub_axis = numpy.meshgrid(x_sub_axis, y_sub_axis)
     
    c_sol = numpy.zeros((set['Nx']/2+1, set['Ny']/2+1))
    for j, y in enumerate(range(0,set['Ny']+1,2)):
        for i, x in enumerate(range(0,set['Nx']+1,2)):
            c_sol[i,j] = sol['c'][x,y]
             
    f_sol = numpy.zeros((set['Nx']/2+1, set['Ny']/2+1))
    for j, y in enumerate(range(0,set['Ny']+1,2)):
        for i, x in enumerate(range(0,set['Nx']+1,2)):
            f_sol[i,j] = sol['f'][x,y]
     
    cn_sol = numpy.zeros((set['Nx']/2+1, set['Ny']/2+1))
    for j, y in enumerate(range(0,set['Ny']+1,2)):
        for i, x in enumerate(range(0,set['Nx']+1,2)):
            cn_sol[i,j] = sol['c_n'][x,y]
      
    '''Continuous Plot VEGF & ECM'''
    if set['k'] % 100 == 0:
        '''Only VEGF'''
        fig1 = plt.figure(2)
        plt.title('%s%f' % ('VEGF Distribution at t=',set['t']))
        plt.pcolormesh(y_sub_axis, x_sub_axis, c_sol, vmin = 0, vmax = 1, cmap="Blues", shading = 'gouraud')
        sol['VEGF'] +=1  
        flag = 'VEGF=%s' % str(sol['VEGF']) 
        plt.colorbar()
        plt.savefig("%s.png" % flag)
        plt.close()
         
        '''Only ECM'''
        fig2 = plt.figure(3)
        plt.title('%s%f' % ('ECM Distribution at t=',set['t']))
        plt.xlabel('X')
        plt.ylabel('Y')
        plt.pcolormesh(y_sub_axis, x_sub_axis, f_sol, vmin = 0.499, vmax = 0.504, cmap="BuPu", shading = 'gouraud')#
        sol['ECM'] +=1  
        flag = 'ECM=%s' % str(sol['ECM']) 
        plt.colorbar()
        plt.savefig("%s.png" % flag)
        plt.close()
         
        '''Different VEGF'''
        fig3 = plt.figure(4)
        plt.title('%s%f' % ('VEGF Distribution (Normalised) at t=',set['t']))
        plt.xlabel('X')
        plt.ylabel('Y')           
        cn_sol = numpy.ma.masked_array(cn_sol, cn_sol < 0.0001)
        plt.pcolormesh(y_sub_axis, x_sub_axis, cn_sol, vmin = 0, vmax = 1, cmap = 'winter', shading = 'gouraud')
        sol['VEGF1'] +=1  
        flag = 'VEGF_norm=%s' % str(sol['VEGF1']) 
        plt.colorbar()
        plt.savefig("%s.png" % flag)
        plt.close()
    
    '''MERGE_cn'''
    fig13 = plt.figure(6)
    plt.title('%s%f' % ('VEGF and Vessel t=',set['t']))
    ax = fig13.add_subplot(111)
    '''ecm'''
    c_sol = numpy.ma.masked_array(c_sol, c_sol < 0.0001)#-.5)
    ax.pcolormesh(y_sub_axis, x_sub_axis, c_sol, vmin = 0, vmax = 1, cmap="Blues", shading = 'gouraud')
    '''tip cell'''
    x_p = []
    y_p = []
    for tip in sol['tip_cell']:
        x_p.append(tip[0]*set['Hh'])
        y_p.append(tip[1]*set['Hh'])
    ax.scatter(x_p, y_p, marker = 'o', s = 10, color ='r')
    '''Backward Marker'''
    if len(sol['backward_list']) > 0:
        x_pp = []
        y_pp = []
        for tip in sol['backward_list']:
            x_pp.append(tip[0]*set['Hh'])
            y_pp.append(tip[1]*set['Hh'])
        ax.scatter(x_pp, y_pp, marker = '^', s = 10, color ='c')
    '''Vessel Growth'''
    for i in range(0,len(sol['matrix_tip'])):
        x_p = []
        y_p = []
        for j in range(0,len(sol['matrix_tip'][i])):
            x_p.append(sol['matrix_tip'][i][j][0]*set['Hh'])
            y_p.append(sol['matrix_tip'][i][j][1]*set['Hh'])
        globals()['plo%s' % i] = ax.plot(x_p, y_p, 'c', color ='k')
  
    plt.xlim((set['Hh'],coef['X']-set['Hh']))
    plt.ylim((set['Hh'],coef['Y']-set['Hh']))
    sol['Merge_cn'] +=1
    flag = 'Merge_cn=%s' % str(sol['Merge_fn']) 
    plt.savefig("%s.png" % flag)
    plt.close()
    
    '''MERGE_fn'''
    fig12 = plt.figure(5)
    plt.title('%s%f' % ('ECM and Vessel at t=',set['t']))
    ax = fig12.add_subplot(111)
    '''ECM'''
    f_sol = numpy.ma.masked_array(f_sol, f_sol < 0.0001)#-.5)
    ax.pcolormesh(y_sub_axis, x_sub_axis, f_sol, vmin = 0.499, vmax = 0.504, cmap="BuPu", shading = 'gouraud')
    '''Tip Cell'''
    x_p = []
    y_p = []
    for tip in sol['tip_cell']:
        x_p.append(tip[0]*set['Hh'])
        y_p.append(tip[1]*set['Hh'])
    ax.scatter(x_p, y_p, marker = 'o', s = 10, color ='r')
    '''Backward Marker'''
    if len(sol['backward_list']) > 0:
        x_pp = []
        y_pp = []
        for tip in sol['backward_list']:
            x_pp.append(tip[0]*set['Hh'])
            y_pp.append(tip[1]*set['Hh'])
        ax.scatter(x_pp, y_pp, marker = '^', s = 10, color ='c')
    '''Vessel Growth'''
    for i in range(0,len(sol['matrix_tip'])):
        x_p = []
        y_p = []
        for j in range(0,len(sol['matrix_tip'][i])):
            x_p.append(sol['matrix_tip'][i][j][0]*set['Hh'])
            y_p.append(sol['matrix_tip'][i][j][1]*set['Hh'])
        globals()['plo%s' % i] = ax.plot(x_p, y_p, 'c', color ='k')
    plt.xlim((set['Hh'],coef['X']-set['Hh']))
    plt.ylim((set['Hh'],coef['Y']-set['Hh']))
    sol['Merge_fn'] +=1
    flag = 'Merge_fn=%s' % str(sol['Merge_fn']) 
    plt.savefig("%s.png" % flag)
    plt.close()

    '''MERGE_cnd'''
    fig14 = plt.figure(7)
    plt.title('%s%f' % ('VEGF (Normalised) and Vessel at t=',set['t']))
    ax = fig14.add_subplot(111)
    '''ecm'''
    cn_sol = numpy.ma.masked_array(cn_sol, cn_sol < 0.0001)#-.5)
    ax.pcolormesh(y_sub_axis, x_sub_axis, cn_sol, vmin = 0, vmax = 1, cmap = 'winter', shading = 'gouraud')
    '''tip cell'''
    x_p = []
    y_p = []
    for tip in sol['tip_cell']:
        x_p.append(tip[0]*set['Hh'])
        y_p.append(tip[1]*set['Hh'])
    ax.scatter(x_p, y_p, marker = 'o', s = 10, color ='r')
    '''Backward Marker'''
    if len(sol['backward_list']) > 0:
        x_pp = []
        y_pp = []
        for tip in sol['backward_list']:
            x_pp.append(tip[0]*set['Hh'])
            y_pp.append(tip[1]*set['Hh'])
        ax.scatter(x_pp, y_pp, marker = '^', s = 10, color ='c')
    '''Vessel Growth'''
    for i in range(0,len(sol['matrix_tip'])):
        x_p = []
        y_p = []
        for j in range(0,len(sol['matrix_tip'][i])):
            x_p.append(sol['matrix_tip'][i][j][0]*set['Hh'])
            y_p.append(sol['matrix_tip'][i][j][1]*set['Hh'])
        globals()['plo%s' % i] = ax.plot(x_p, y_p, 'c', color ='k')
    plt.xlim((set['Hh'],coef['X']-set['Hh']))
    plt.ylim((set['Hh'],coef['Y']-set['Hh']))
    sol['Merge_cnd'] +=1
    flag = 'Merge_cn_norm=%s' % str(sol['Merge_cnd']) 
    plt.savefig("%s.png" % flag)
    plt.close()  

    return