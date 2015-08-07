'''Domain'''
from duplicity.path import Path
X=1
Y=1
T=1

dx=0.01
dy=0.01
dt=0.01

Nx=int(X/dx)
Ny=int(Y/dy)
Nt=int(T/dt)


'''Initial condition ijk'''
import numpy
import math
old_settings = numpy.seterr(all='ignore')
nw = []
cw = []
fw = []
wx = []
wy = []
#initial n
n = numpy.zeros((Nx+1,Ny+1,Nt+1))
for i in range(Nx+1):
    n[i,0,0] = 1
    nw.append(n[i,0,0])
#for j in range(Ny+1):
    #for i in range(Nx+1):
#         n[i,j,0] = math.exp(-(j*dy)**2/0.001)*(math.sin(6*(math.pi)*i*dx))**2
        #nw.append(n[i,j,0])
#print n[:,Ny,0]

#initial c  n f
c = numpy.zeros((Nx+1,Ny+1,Nt+1))
f = numpy.zeros((Nx+1,Ny+1,Nt+1))
for i in range(Ny+1):
    for j in range(Nx+1):
        wx.append(j*dx)
        wy.append(i*dy)
        c[j,i,0] = math.exp(-(Y-dy*i)**2/0.45)
        #c[j,i,0] = math.exp(-((X-dx*j)**2+(Y-dy*i)**2)/0.45)
        f[j,i,0] = math.exp(-(dy*i)**2/0.35)
        fw.append(f[j,i,0])
        cw.append(c[j,i,0])
    #print n[:,i,0]
    #print f[:,i,0]
#node filling
##constant
D = 0.00035
al = 0.6
ki = 0.38
ro = 0.34
ga = 1#0.1
be = 1#0.05
nu = 0.1

for it in range(Nt):
    for iy in range(Ny+1):
        ##filling node boundary
        if (iy==0):#boundary bawah
            for ix in range(Nx+1):
                f[ix,iy,it+1] = f[ix,iy,it]*(1-dt*ga*n[ix,iy,it])+dt*be*n[ix,iy,it]
                c[ix,iy,it+1] = c[ix,iy,it]*(1-dt*nu*n[ix,iy,it])
                P_3 = dt*D/dx**2 - dt/(4*dx**2)*(ki*c[ix,iy,it]*(c[ix,iy+1,it]-c[ix,iy,it])+ro*(f[ix,iy+1,it]-f[ix,iy,it]))
                P_4 = dt*D/dx**2 + dt/(4*dx**2)*(ki*c[ix,iy,it]*(c[ix,iy+1,it]-c[ix,iy,it])+ro*(f[ix,iy+1,it]-f[ix,iy,it]))
                if (ix==0):#pojok kiri bawah
                    P_1 = dt*D/dx**2 - dt/(4*dx**2)*(ki*c[ix,iy,it]*(c[ix+1,iy,it]-c[ix,iy,it])+ro*(f[ix+1,iy,it]-f[ix,iy,it]))
                    P_2 = dt*D/dx**2 + dt/(4*dx**2)*(ki*c[ix,iy,it]*(c[ix+1,iy,it]-c[ix,iy,it])+ro*(f[ix+1,iy,it]-f[ix,iy,it]))
                    P_0 = 1-4*dt*D/dx**2 + dt*al*ki*c[ix,iy,it]/(4*dx**2*(1+al*c[ix,iy,it]))*((c[ix+1,iy,it]-c[ix,iy,it])**2+(c[ix,iy+1,it]-c[ix,iy,it])**2) - dt*ki*c[ix,iy,it]/dx**2*(c[ix+1,iy,it]+c[ix,iy,it]-4*c[ix,iy,it]+c[ix,iy+1,it]+c[ix,iy,it]) - dt*ro/dx**2*(f[ix+1,iy,it]+f[ix,iy,it]-4*f[ix,iy,it]+f[ix,iy+1,it]+f[ix,iy,it])
                    n[ix,iy,it+1] = P_0*n[ix,iy,it] + P_1*n[ix+1,iy,it] + P_2*n[ix,iy,it] + P_3*n[ix,iy+1,it] + P_4*n[ix,iy,it]
                elif (ix==Nx):#pojok kanan bawah
                    P_1 = dt*D/dx**2 - dt/(4*dx**2)*(ki*c[ix,iy,it]*(c[ix,iy,it]-c[ix-1,iy,it])+ro*(f[ix,iy,it]-f[ix-1,iy,it]))
                    P_2 = dt*D/dx**2 + dt/(4*dx**2)*(ki*c[ix,iy,it]*(c[ix,iy,it]-c[ix-1,iy,it])+ro*(f[ix,iy,it]-f[ix-1,iy,it]))
                    P_0 = 1-4*dt*D/dx**2 + dt*al*ki*c[ix,iy,it]/(4*dx**2*(1+al*c[ix,iy,it]))*((c[ix,iy,it]-c[ix-1,iy,it])**2+(c[ix,iy+1,it]-c[ix,iy,it])**2) - dt*ki*c[ix,iy,it]/dx**2*(c[ix,iy,it]+c[ix-1,iy,it]-4*c[ix,iy,it]+c[ix,iy+1,it]+c[ix,iy,it]) - dt*ro/dx**2*(f[ix,iy,it]+f[ix-1,iy,it]-4*f[ix,iy,it]+f[ix,iy+1,it]+f[ix,iy,it])
                    n[ix,iy,it+1] = P_0*n[ix,iy,it] + P_1*n[ix,iy,it] + P_2*n[ix-1,iy,it] + P_3*n[ix,iy+1,it] + P_4*n[ix,iy,it]
                else:#selain pojokan namun dibawah
                    P_1 = dt*D/dx**2 - dt/(4*dx**2)*(ki*c[ix,iy,it]*(c[ix+1,iy,it]-c[ix-1,iy,it])+ro*(f[ix+1,iy,it]-f[ix-1,iy,it]))
                    P_2 = dt*D/dx**2 + dt/(4*dx**2)*(ki*c[ix,iy,it]*(c[ix+1,iy,it]-c[ix-1,iy,it])+ro*(f[ix+1,iy,it]-f[ix-1,iy,it]))
                    P_0 = 1-4*dt*D/dx**2 + dt*al*ki*c[ix,iy,it]/(4*dx**2*(1+al*c[ix,iy,it]))*((c[ix+1,iy,it]-c[ix-1,iy,it])**2+(c[ix,iy+1,it]-c[ix,iy,it])**2) - dt*ki*c[ix,iy,it]/dx**2*(c[ix+1,iy,it]+c[ix-1,iy,it]-4*c[ix,iy,it]+c[ix,iy+1,it]+c[ix,iy,it]) - dt*ro/dx**2*(f[ix+1,iy,it]+f[ix-1,iy,it]-4*f[ix,iy,it]+f[ix,iy+1,it]+f[ix,iy,it])
                    n[ix,iy,it+1] = P_0*n[ix,iy,it] + P_1*n[ix+1,iy,it] + P_2*n[ix-1,iy,it] + P_3*n[ix,iy+1,it] + P_4*n[ix,iy-1,it]
        elif (iy==Ny):#boundary atas
            for ix in range(Nx+1):
                f[ix,iy,it+1] = f[ix,iy,it]*(1-dt*ga*n[ix,iy,it])+dt*be*n[ix,iy,it]
                c[ix,iy,it+1] = c[ix,iy,it]*(1-dt*nu*n[ix,iy,it])
                P_3 = dt*D/dx**2 - dt/(4*dx**2)*(ki*c[ix,iy,it]*(c[ix,iy,it]-c[ix,iy-1,it])+ro*(f[ix,iy,it]-f[ix,iy-1,it]))
                P_4 = dt*D/dx**2 + dt/(4*dx**2)*(ki*c[ix,iy,it]*(c[ix,iy,it]-c[ix,iy-1,it])+ro*(f[ix,iy,it]-f[ix,iy-1,it]))
                if (ix==0):#pojok kiri atas
                    P_1 = dt*D/dx**2 - dt/(4*dx**2)*(ki*c[ix,iy,it]*(c[ix+1,iy,it]-c[ix,iy,it])+ro*(f[ix+1,iy,it]-f[ix,iy,it]))
                    P_2 = dt*D/dx**2 + dt/(4*dx**2)*(ki*c[ix,iy,it]*(c[ix+1,iy,it]-c[ix,iy,it])+ro*(f[ix+1,iy,it]-f[ix,iy,it]))
                    P_0 = 1-4*dt*D/dx**2 + dt*al*ki*c[ix,iy,it]/(4*dx**2*(1+al*c[ix,iy,it]))*((c[ix+1,iy,it]-c[ix,iy,it])**2+(c[ix,iy,it]-c[ix,iy-1,it])**2) - dt*ki*c[ix,iy,it]/dx**2*(c[ix+1,iy,it]+c[ix,iy,it]-4*c[ix,iy,it]+c[ix,iy,it]+c[ix,iy-1,it]) - dt*ro/dx**2*(f[ix+1,iy,it]+f[ix,iy,it]-4*f[ix,iy,it]+f[ix,iy,it]+f[ix,iy-1,it])
                    n[ix,iy,it+1] = P_0*n[ix,iy,it] + P_1*n[ix+1,iy,it] + P_2*n[ix,iy,it] + P_3*n[ix,iy,it] + P_4*n[ix,iy-1,it]
                elif (ix==Nx):#pojok kanan atas
                    P_1 = dt*D/dx**2 - dt/(4*dx**2)*(ki*c[ix,iy,it]*(c[ix,iy,it]-c[ix-1,iy,it])+ro*(f[ix,iy,it]-f[ix-1,iy,it]))
                    P_2 = dt*D/dx**2 + dt/(4*dx**2)*(ki*c[ix,iy,it]*(c[ix,iy,it]-c[ix-1,iy,it])+ro*(f[ix,iy,it]-f[ix-1,iy,it]))
                    P_0 = 1-4*dt*D/dx**2 + dt*al*ki*c[ix,iy,it]/(4*dx**2*(1+al*c[ix,iy,it]))*((c[ix,iy,it]-c[ix-1,iy,it])**2+(c[ix,iy,it]-c[ix,iy-1,it])**2) - dt*ki*c[ix,iy,it]/dx**2*(c[ix,iy,it]+c[ix-1,iy,it]-4*c[ix,iy,it]+c[ix,iy,it]+c[ix,iy-1,it]) - dt*ro/dx**2*(f[ix,iy,it]+f[ix-1,iy,it]-4*f[ix,iy,it]+f[ix,iy,it]+f[ix,iy-1,it])
                    n[ix,iy,it+1] = P_0*n[ix,iy,it] + P_1*n[ix,iy,it] + P_2*n[ix-1,iy,it] + P_3*n[ix,iy,it] + P_4*n[ix,iy-1,it]
                else:#selain pojokan namun diatas
                    P_1 = dt*D/dx**2 - dt/(4*dx**2)*(ki*c[ix,iy,it]*(c[ix+1,iy,it]-c[ix-1,iy,it])+ro*(f[ix+1,iy,it]-f[ix-1,iy,it]))
                    P_2 = dt*D/dx**2 + dt/(4*dx**2)*(ki*c[ix,iy,it]*(c[ix+1,iy,it]-c[ix-1,iy,it])+ro*(f[ix+1,iy,it]-f[ix-1,iy,it]))
                    P_0 = 1-4*dt*D/dx**2 + dt*al*ki*c[ix,iy,it]/(4*dx**2*(1+al*c[ix,iy,it]))*((c[ix+1,iy,it]-c[ix-1,iy,it])**2+(c[ix,iy,it]-c[ix,iy-1,it])**2) - dt*ki*c[ix,iy,it]/dx**2*(c[ix+1,iy,it]+c[ix-1,iy,it]-4*c[ix,iy,it]+c[ix,iy,it]+c[ix,iy-1,it]) - dt*ro/dx**2*(f[ix+1,iy,it]+f[ix-1,iy,it]-4*f[ix,iy,it]+f[ix,iy,it]+f[ix,iy-1,it])
                    n[ix,iy,it+1] = P_0*n[ix,iy,it] + P_1*n[ix+1,iy,it] + P_2*n[ix-1,iy,it] + P_3*n[ix,iy,it] + P_4*n[ix,iy-1,it]
        else:#selain boundary atas bawah
            for ix in range(Nx+1):
                f[ix,iy,it+1] = f[ix,iy,it]*(1-dt*ga*n[ix,iy,it])+dt*be*n[ix,iy,it]
                c[ix,iy,it+1] = c[ix,iy,it]*(1-dt*nu*n[ix,iy,it])
                P_3 = dt*D/dx**2 - dt/(4*dx**2)*(ki*c[ix,iy,it]*(c[ix,iy+1,it]-c[ix,iy-1,it])+ro*(f[ix,iy+1,it]-f[ix,iy-1,it]))
                P_4 = dt*D/dx**2 + dt/(4*dx**2)*(ki*c[ix,iy,it]*(c[ix,iy+1,it]-c[ix,iy-1,it])+ro*(f[ix,iy+1,it]-f[ix,iy-1,it]))
                if (ix==0):#selain boundary atas bawah namun dipinggiran kiri
                    P_1 = dt*D/dx**2 - dt/(4*dx**2)*(ki*c[ix,iy,it]*(c[ix+1,iy,it]-c[ix,iy,it])+ro*(f[ix+1,iy,it]-f[ix,iy,it]))
                    P_2 = dt*D/dx**2 + dt/(4*dx**2)*(ki*c[ix,iy,it]*(c[ix+1,iy,it]-c[ix,iy,it])+ro*(f[ix+1,iy,it]-f[ix,iy,it]))
                    P_0 = 1-4*dt*D/dx**2 + dt*al*ki*c[ix,iy,it]/(4*dx**2*(1+al*c[ix,iy,it]))*((c[ix+1,iy,it]-c[ix,iy,it])**2+(c[ix,iy+1,it]-c[ix,iy-1,it])**2) - dt*ki*c[ix,iy,it]/dx**2*(c[ix+1,iy,it]+c[ix,iy,it]-4*c[ix,iy,it]+c[ix,iy+1,it]+c[ix,iy-1,it]) - dt*ro/dx**2*(f[ix+1,iy,it]+f[ix,iy,it]-4*f[ix,iy,it]+f[ix,iy+1,it]+f[ix,iy-1,it])
                    n[ix,iy,it+1] = P_0*n[ix,iy,it] + P_1*n[ix+1,iy,it] + P_2*n[ix,iy,it] + P_3*n[ix,iy+1,it] + P_4*n[ix,iy-1,it] 
                elif (ix==Nx):#selain boundary atas bawah namun dipinggiran kanan
                    P_1 = dt*D/dx**2 - dt/(4*dx**2)*(ki*c[ix,iy,it]*(c[ix,iy,it]-c[ix-1,iy,it])+ro*(f[ix,iy,it]-f[ix-1,iy,it]))
                    P_2 = dt*D/dx**2 + dt/(4*dx**2)*(ki*c[ix,iy,it]*(c[ix,iy,it]-c[ix-1,iy,it])+ro*(f[ix,iy,it]-f[ix-1,iy,it]))
                    P_0 = 1-4*dt*D/dx**2 + dt*al*ki*c[ix,iy,it]/(4*dx**2*(1+al*c[ix,iy,it]))*((c[ix,iy,it]-c[ix-1,iy,it])**2+(c[ix,iy+1,it]-c[ix,iy-1,it])**2) - dt*ki*c[ix,iy,it]/dx**2*(c[ix,iy,it]+c[ix-1,iy,it]-4*c[ix,iy,it]+c[ix,iy+1,it]+c[ix,iy-1,it]) - dt*ro/dx**2*(f[ix,iy,it]+f[ix-1,iy,it]-4*f[ix,iy,it]+f[ix,iy+1,it]+f[ix,iy-1,it])
                    n[ix,iy,it+1] = P_0*n[ix,iy,it] + P_1*n[ix,iy,it] + P_2*n[ix-1,iy,it] + P_3*n[ix,iy+1,it] + P_4*n[ix,iy-1,it] 
                else:#tengah2 selain boundary
                    P_1 = dt*D/dx**2 - dt/(4*dx**2)*(ki*c[ix,iy,it]*(c[ix+1,iy,it]-c[ix-1,iy,it])+ro*(f[ix+1,iy,it]-f[ix-1,iy,it]))
                    P_2 = dt*D/dx**2 + dt/(4*dx**2)*(ki*c[ix,iy,it]*(c[ix+1,iy,it]-c[ix-1,iy,it])+ro*(f[ix+1,iy,it]-f[ix-1,iy,it]))
                    P_0 = 1-4*dt*D/dx**2 + dt*al*ki*c[ix,iy,it]/(4*dx**2*(1+al*c[ix,iy,it]))*((c[ix+1,iy,it]-c[ix-1,iy,it])**2+(c[ix,iy+1,it]-c[ix,iy-1,it])**2) - dt*ki*c[ix,iy,it]/dx**2*(c[ix+1,iy,it]+c[ix-1,iy,it]-4*c[ix,iy,it]+c[ix,iy+1,it]+c[ix,iy-1,it]) - dt*ro/dx**2*(f[ix+1,iy,it]+f[ix-1,iy,it]-4*f[ix,iy,it]+f[ix,iy+1,it]+f[ix,iy-1,it])
                    n[ix,iy,it+1] = P_0*n[ix,iy,it] + P_1*n[ix+1,iy,it] + P_2*n[ix-1,iy,it] + P_3*n[ix,iy+1,it] + P_4*n[ix,iy-1,it]

for u1 in range(Nt+1):
    for u2 in range(Ny+1):
        for u3 in range(Nx+1):
            if n[u3,u2,u1]<0:
                print 'negative value'
                print u3, u2, u1
                #quit()
                break;
nw2 = []
for j in range(Ny+1):
    for i in range(Nx+1):
        nw2.append(n[i,j,3]) 
print nw2[100]  

nw1 = []
for j in range(Ny+1):
    for i in range(Nx+1):
        nw1.append(n[i,j,Nt]) 
print nw1[100]               
quit()
'''FIGURE'''
import matplotlib.pyplot as plt
from matplotlib import cm
import numpy as np
from matplotlib.mlab import griddata
xx = np.arange(0, (X+dx), dx)
yy = np.arange(0, (Y+dy), dy)
xx, yy = np.meshgrid(xx, yy)
Z1 = griddata(wx, wy, cw, xx, yy)
Z2 = griddata(wx, wy, fw, xx, yy)
#ZZ = griddata(wx, wy, nw, xx, yy)
ZZsol = griddata(wx, wy, nw1, xx, yy)
from mpl_toolkits.mplot3d import Axes3D

fig1 = plt.figure()
ax = plt.axes(projection='3d')
ax.plot_surface(xx, yy, ZZsol, rstride=1, cstride=1, cmap=cm.coolwarm,
        linewidth=0, antialiased=False)
plt.show()  


fig = plt.figure()
ax = plt.axes(projection='3d')
ax.plot_surface(xx, yy, Z1, rstride=1, cstride=1, cmap=cm.coolwarm,
        linewidth=0, antialiased=False)
ax.plot_surface(xx, yy, Z2, rstride=1, cstride=1, cmap=cm.coolwarm,
        linewidth=0, antialiased=False)
plt.show()


#fig1 = plt.figure()
#ax = plt.axes(projection='3d')
#ax.plot_surface(xx, yy, ZZ, rstride=1, cstride=1, cmap=cm.coolwarm,
#        linewidth=0, antialiased=False)
#plt.show()


                        
#  