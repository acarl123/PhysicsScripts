from __future__ import division
from visual import *

print """
Ruth Chabay Spring 2001
A plane sinusoidal wave; show there are E and B fields throughout space.
"""

scene.width=1000
scene.height=1000
scene.x = scene.y = 0
scene.background = color.white

c = 3e8
lamb = 1e-10
h = 1e-10
h=0
omega = 2*pi*c/lamb
##line = curve(pos=[(-2*lamb,0,0), (2*lamb,0,0)])
##scene.center = (-lamb,0,0)
scene.forward = (-1,-0.2,-1)
scene.range=lamb

##xx = arange(-2*lamb,2.0001*lamb,lamb/20.)
##xx = arange(-2*lamb,0.001*lamb, lamb/20.)
xx = arange(-3*lamb,1.001*lamb, lamb/20.)


xhat = vector(1,0,0)

Evec = []
for z in [-h,0,h]:
    for y in [-h,0,h]:
        for x in xx:
            ea = arrow(pos=(x,y,z), axis=(0,lamb/10.,0), color=(1.,.6,0),
                       shaftwidth=lamb/45., fixedwidth=1)
            ba = arrow(pos=(x,y,z), axis=(0,0,0), color=(0,1,1),
                       shaftwidth=lamb/45., fixedwidth=1)
            ea.B = ba
            Evec.append(ea)

t = 0.
dt = lamb/c/100.
print 'dt=',dt
print 'wavelength =', lamb
print 'omega = ', omega
E0 = lamb/3.

yy=-lamb/2
xx=-0.5*lamb
dyy = lamb/5
pts=[(xx,yy+dyy,0),(xx,yy-dyy,0),(xx,yy,0),(xx+lamb,yy,0),
     (xx+lamb,yy+dyy,0),(xx+lamb,yy-dyy,0)]
stick = curve(color=color.green, pos=pts,radius=lamb/60.,visible=0)

while 1:
    rate(20)
    t = t+dt
    nn = 0
    for ea in Evec:
        ea.axis = (0,E0*cos(omega*t - 2*pi*ea.x/lamb),0)
        ea.B.axis = cross(xhat,ea.axis)*.7
        nn += 1
##        if scene.mouse.clicked:
##            scene.mouse.getclick()
##            stick.visible = not(stick.visible)

