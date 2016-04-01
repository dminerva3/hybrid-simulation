import code_with_mural_dict as disc
from coef_setting import declare_coef
import numpy

from timeit import default_timer as timer 
import time

import matplotlib.pyplot as plt 
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
from mpl_toolkits.mplot3d import Axes3D
#from mpmath.functions.rszeta import coef
#import discrete_run as disc
'''Untuk Plot
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
from mpl_toolkits.mplot3d import Axes3D


plt.ion() #interactively
plt.show()
fig = plt.figure()
ax = fig.gca(projection='3d')
ax.set_zlim(-0.1, 1.2)
Untuk Plot'''

#declare coefficients & initial settings
coef, set, sol = declare_coef()

#to plot interactively
plt.ion()

#hybrid part
while set['t'] <= set['T'] and set['k'] < set['Nt']:
    start1 = timer()
    sol = disc.boolean_1_iter(coef, set, sol)
#     g = disc.discrete_1_iter(iter = k, hh = Hh, Nx = nx, Ny = ny,
#                              r_min = R_min, r_max = R_max,
#                              ro = Ro, d_n = D_n, ki_n = Ki_n, al_n = Al_n,
#                              kappa = Kappa, mic = Mic,
#                              d_c = D_c, nu = Nu, 
#                              be = Beta, ga = Gama, 
#                              d_m = D_m, ki_m = Ki_m, al_m = Al_m,
#                              a_p = A_p, b_p = B_p, dl = Dl,
#                              matrix_tip = g[0],  
#                              list_tip_movement = g[1], life_time_tip = g[2],
#                              stop_iter = g[3], sp_stop = g[4],
#                              n = g[5], c = g[6], f = g[7], tp = g[8], p = g[9], m = g[10], index_mn = g[11],
#                              Error = error,
#                              t_branch = T_branch,
#                              Rec = rec)                   
    start2 = timer()
    if sol['stop_iter'] >=100000:
        set['k'] = sol['stop_iter']
    print 'at Time', set['t']
    set['t'] += set['dt']
    set['k'] += 1
    
    #to print as control
    if not coef['Mic'] == 0 or not coef['Kappa'] == 0:
        print 'NILAI C, F, P MAX', sol['c'].max(), ',', sol['f'].max(), ',', sol['p'].max()
        print 'NILAI C, F, P MIN', sol['c'].min(), ',', sol['f'].min(), ',', sol['p'].min()
    else:
        print 'NILAI C, F MAX', sol['c'].max(), ',', sol['f'].max()
        print 'NILAI C, F MIN', sol['c'].min(), ',', sol['f'].min()
    print 'process time of Hybrid:', start2-start1
    print 'total time of processing:', time.clock()
    print '***************************************************'
    print
#     
#     if not Kappa == 0 or not Mic == 0:
#         if k == 500 or k == 1000 or k == 1500 or k == 2000 or k == 2500 or k == 3000 or k == 3500 or k == 4000:
#             fig = plt.figure()
#             plt.xlim(Hh,X-Hh)
#             plt.ylim(Hh,Y-Hh)
#             #plt.xlim(Hh*100,X-Hh*300)
#             #plt.ylim(Hh*100,Y-Hh*300)
#             ax = fig.add_subplot(111)
#             for i in range(0,len(g[0])):
#                 x_p = []
#                 y_p = []
#                 for j in range(0,len(g[0][i])):
#                     x_p.append(g[0][i][j][0]*Hh)
#                     y_p.append(g[0][i][j][1]*Hh)
#                 globals()['plo%s' % i] = ax.plot(x_p, y_p, 'b')
#             plt.draw()
#             
#             plt.figure()
#             plt.xlim(Hh,X-Hh)
#             plt.ylim(Hh,Y-Hh)
#             x_p = []
#             y_p = []
#             for y in range(1,ny,2):
#                 for x in range(1,nx,2):
#                     if g[10][x,y] == 1:
#                         x_p.append(x*Hh)
#                         y_p.append(y*Hh)
#             '''
#             for i in range(0,len(g[10])):
#                 x_p.append(g[10][i][0]*Hh)
#                 y_p.append(g[10][i][1]*Hh)
#             '''
#             plt.scatter(x_p, y_p, marker = 'o', s = 0.5, color ='green')
#             plt.draw()  
#             
#             plt.figure()
#             plt.xlim(Hh,X-Hh)
#             plt.ylim(Hh,Y-Hh)
#             #plt.xlim(Hh*100,X-Hh*100)
#             #plt.ylim(Hh*100,Y-Hh*100)
#             x_p = []
#             y_p = []
#             for i in range(0,len(g[11])):
#                 x_p.append(g[11][i][0]*Hh)
#                 y_p.append(g[11][i][1]*Hh)
#             plt.scatter(x_p, y_p, marker = 'o', s = 0.5, color ='red')
#             plt.draw()
#             
#             '''
#             fig1 = plt.figure(1)
#             ax = fig1.gca(projection='3d')
#             ax.set_zlim(-0.1, 1)
#             ax.zaxis.set_major_locator(LinearLocator(10))
#             ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))
#             
#             x_sub_axis = numpy.arange(0, X+Hh, h)
#             y_sub_axis = numpy.arange(0, Y+Hh, h)
#             x_sub_axis, y_sub_axis = numpy.meshgrid(x_sub_axis, y_sub_axis)
#             
#             p_sol = numpy.zeros((nx/2+1, ny/2+1))
#             for j, y in enumerate(range(0,ny+1,2)):
#                 for i, x in enumerate(range(0,nx+1,2)):
#                     p_sol[i,j] = g[9][x,y]
#             surf = ax.plot_surface(x_sub_axis, y_sub_axis, p_sol, rstride=1, cstride=1, cmap=cm.coolwarm,
#                     linewidth=0, antialiased=False)
#             fig1.colorbar(surf, shrink=0.5, aspect=5)
#             plt.draw()
#             '''
#             
#             del x_p
#             del y_p
#     else:
#         '''
#         if k == 1:
#             fig = plt.figure()
#             plt.xlim(Hh*170,X-Hh*170)
#             plt.ylim(Hh*170,Y-Hh*170)
#             x_p = []
#             y_p = []
#             for i in range(0,len(g[0])):
#                 x_p.append(g[0][i][0][0]*Hh)
#                 y_p.append(g[0][i][0][1]*Hh)
#             plt.scatter(x_p, y_p, marker = 'o', s = 10, color ='blue')
#             plt.draw()
#             del x_p
#             del y_p 
#         '''  
#         if k == 500 or k == 1000 or k == 1500 or k == 2000 or k == 2500 or k == 3000 or k == 3500 or k == 4000:
#             fig = plt.figure()
#             plt.xlim(Hh,X-Hh)
#             plt.ylim(Hh,Y-Hh)
#             ax = fig.add_subplot(111)
#             for i in range(0,len(g[0])):
#                 x_p = []
#                 y_p = []
#                 for j in range(0,len(g[0][i])):
#                     x_p.append(g[0][i][j][0]*Hh)
#                     y_p.append(g[0][i][j][1]*Hh)
#                 globals()['plo%s' % i] = ax.plot(x_p, y_p, 'b')
#             plt.draw()
#             del x_p
#             del y_p          
#         
#         '''
#         fig = plt.figure()
#         plt.xlim(Hh,X-Hh)#X-hh
#         plt.ylim(Hh,Y-Hh)#
#         ax = fig.add_subplot(111)
#         for i in range(0,len(g[0])):
#             x_p = []
#             y_p = []
#             for j in range(0,len(g[0][i])):
#                 x_p.append(g[0][i][j][0]*Hh)
#                 y_p.append(g[0][i][j][1]*Hh)
#             globals()['plo%s' % i] = ax.plot(x_p, y_p, 'b')  
#         plt.draw() 
#         
#         if not Kappa == 0 or not Mic == 0:
#             plt.figure()
#             plt.xlim(Hh,X-Hh)#X-hh
#             plt.ylim(Hh,Y-Hh)#
#             x_p = []
#             y_p = []
#             for i in range(0,len(g[11])):
#                 x_p.append(g[11][i][0]*Hh)
#                 y_p.append(g[11][i][1]*Hh)
#             plt.scatter(x_p, y_p, marker = 'o', s = 0.5)
#             plt.draw() 
#         '''
#     
    
print '*************DONE*****************'

'''Plot Continuous
fig1 = plt.figure(1)
ax = fig1.gca(projection='3d')
ax.set_zlim(-0.1, 1)
ax.zaxis.set_major_locator(LinearLocator(10))
ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))

x_main_axis = numpy.arange(0, X+Hh, h)
y_main_axis = numpy.arange(0, Y+Hh, h)
x_main_axis, y_main_axis = numpy.meshgrid(x_main_axis, y_main_axis)

c_sol = numpy.zeros((nx/2+1, ny/2+1))
for j, y in enumerate(range(0,ny+1,2)):
    for i, x in enumerate(range(0,nx+1,2)):
        c_sol[i,j] = g[8][x,y]
surf = ax.plot_surface(x_main_axis, y_main_axis, c_sol, rstride=1, cstride=1, cmap=cm.coolwarm,
        linewidth=0, antialiased=False)
fig1.colorbar(surf, shrink=0.5, aspect=5)
plt.draw()
Plot Continuous'''


'''Plot Hybrid
fig2 = plt.figure(2)
plt.xlim(Hh,X-Hh)#X-hh
plt.ylim(Hh,Y-Hh)#
ax = fig2.add_subplot(111)
for i in range(0,len(g[0])):
    x_p = []
    y_p = []
    for j in range(0,len(g[9][i])):
        x_p.append(g[9][i][j][0]*Hh)
        y_p.append(g[9][i][j][1]*Hh)
    globals()['plo%s' % i] = ax.plot(x_p, y_p, 'b')
fig2.show()
'''  

'''
fig3 = plt.figure(3)
plt.xlim(Hh,X-Hh)#X-hh
plt.ylim(Hh,Y-Hh)#
ax = fig3.add_subplot(111)
x_p = []
y_p = []
for i in range(0,len(g[11])):
    x_p.append(g[11][i][0]*Hh)
    y_p.append(g[11][i][1]*Hh)
scat = ax.scatter(x_p, y_p, marker = 'o')
fig3.show()   
'''


raw_input()
# plt.show(block=True)
