from visual.graph import *
from random import random

# A model of an ideal gas with hard-sphere collisions
# Program uses Numeric Python arrays for high speed computations

print """
Click to expose the gas in the chamber.
Drag the slider to control the speed of the piston.
The red thermometer measures average translational kinetic energy.
Molecules gain or lose energy in collisions with the moving piston.
Very slow piston motions correspond to quasistatic adiabatic processes.
Fast piston motions correspond to nonequilibrium supersonic processes.
"""

win=600

Natoms = 100  # change this to have more or fewer atoms

# Typical values
##L = 1. # container is a cube L on a side
gray = (0.7,0.7,0.7) # color of edges of container
Raxes = 0.005 # radius of lines drawn on edges of cube
Matom = 4E-3/6E23 # helium mass
Ratom = 0.03 # wildly exaggerated size of helium atom
k = 1.4E-23 # Boltzmann constant
T = 300. # around room temperature
dt = 1E-5

scene = display(title="Gas", width=win, height=win, x=0, y=0)

thick = 0.1
wide = 1.
deep = wide
high = 2.
gray = (0.7, 0.7, 0.7)
darkgray = (0.5, 0.5, 0.5)
cylcolor = (0.788,0.788,0.788)
pistoncolor = (1.000,0.704,0.000)
bottom = box(pos=(0,-thick/2.,0),
             size=(wide,thick,deep), color=cylcolor)
left = box(pos=(-wide/2.-thick/2.,high/2.,-thick/2.),
           size=(thick,high+2.*thick,deep+thick), color=cylcolor)
right = box(pos=(wide/2.+thick/2.,high/2.,-thick/2.),
           size=(thick,high+2.*thick,deep+thick), color=cylcolor)
back = box(pos=(0,high/2.,-deep/2.-thick/2.),
           size=(wide,high+2.*thick,thick), color=cylcolor)
front = box(pos=(0,high/2.,deep/2.+thick/2.),
            size=(wide+2.*thick,high+2.*thick,thick), color=cylcolor)
piston = box(pos=(0,0.5*high+thick/2.,0),
             size=(wide,thick,deep), color=pistoncolor)

scene.center = (0,high/2.,0)

Atoms = []
colors = [color.red, color.green, color.blue,
          color.yellow, color.cyan, color.magenta]
poslist = []
plist = []
mlist = []
rlist = []
offset = 1.1*Ratom

for i in range(Natoms):
    Lmin = -wide/2.+offset
    Lmax = wide/2.-offset
    x = Lmin+(Lmax-Lmin)*random()
    Lmin = bottom.y+thick/2.+offset
    Lmax = piston.y-thick/2.-offset
    y = Lmin+(Lmax-Lmin)*random()
    Lmin = -deep/2.+offset
    Lmax = deep/2.-offset
    z = Lmin+(Lmax-Lmin)*random()
    r = Ratom
    Atoms = Atoms+[sphere(pos=(x,y,z), radius=r, color=colors[i % 6])]
    mass = Matom*r**3/Ratom**3
    pavg = sqrt(2.*mass*1.5*k*T) # average kinetic energy p**2/(2mass) = (3/2)kT
    theta = pi*random()
    phi = 2*pi*random()
    px = pavg*sin(theta)*cos(phi)
    py = pavg*sin(theta)*sin(phi)
    pz = pavg*cos(theta)
    poslist.append((x,y,z))
    plist.append((px,py,pz))
    mlist.append(mass)
    rlist.append(r)

pos = array(poslist)
p = array(plist)
m = array(mlist)
m.shape = (Natoms,1) # Numeric Python: (1 by Natoms) vs. (Natoms by 1)
radius = array(rlist)

t = 0.0
pos = pos+(p/m)*(dt/2.) # initial half-step
corner1 = array((-wide/2.+offset,bottom.y+thick/2.+offset,-deep/2.+offset))
corner2 = array((wide/2.-offset,piston.y-thick/2.-offset,deep/2.-offset))
T = sum(sum(p**2))/(2.*Matom)
Tscale = (high/5.)/T
thermometer = cylinder(pos=(bottom.x+wide/2.+2*thick,bottom.y-thick/2.,deep/2.), radius=thick/5.,
                       axis=(0,T*Tscale,0), color=color.red)
sphere(pos=thermometer.pos, radius=3.*thermometer.radius, color=thermometer.color)

# make slider
sthick = thick/2.
shaft = box(pos=(bottom.x-wide/2.-2*thick,bottom.y+high/2.,deep/2.), axis=(0,1,0),
               size=(high/2.,sthick,sthick), color=darkgray)
indicator = box(pos=shaft.pos, axis=(0,1,0), size=(2.*sthick,2.*sthick,2.*sthick), color=gray)
scene.autoscale = 0
scene.mouse.getclick()
front.visible = 0
vpiston = 0.
picked = None

while 1:
    rate(50)
##    observation.plot(data=mag(p/m))
    
    # Update all positions
    pos = pos+(p/m)*dt

    try:  # numpy
        r = pos-pos[:,newaxis] # all pairs of atom-to-atom vectors
        rmag = sqrt(add.reduce(r*r,-1)) # atom-to-atom scalar distances
        hit = less_equal(rmag,radius+radius[:,None])-identity(Natoms)
        hitlist = sort(nonzero(hit.flat)[0]).tolist() # i,j encoded as i*Natoms+j
    except: # old Numeric
        r = pos-pos[:,NewAxis] # all pairs of atom-to-atom vectors
        rmag = sqrt(add.reduce(r*r,-1)) # atom-to-atom scalar distances
        hit = less_equal(rmag,radius+radius[:,NewAxis])-identity(Natoms)
        hitlist = sort(nonzero(hit.flat)).tolist() # i,j encoded as i*Natoms+j

    # If any collisions took place:
    for ij in hitlist:
        i, j = divmod(ij,Natoms) # decode atom pair
        hitlist.remove(j*Natoms+i) # remove symmetric j,i pair from list
        ptot = p[i]+p[j]
        mi = m[i,0]
        mj = m[j,0]
        vi = p[i]/mi
        vj = p[j]/mj
        ri = Atoms[i].radius
        rj = Atoms[j].radius
        a = mag(vj-vi)**2
        if a == 0: continue # exactly same velocities
        b = 2*dot(pos[i]-pos[j],vj-vi)
        c = mag(pos[i]-pos[j])**2-(ri+rj)**2
        d = b**2-4.*a*c
        if d < 0: continue # something wrong; ignore this rare case
        deltat = (-b+sqrt(d))/(2.*a) # t-deltat is when they made contact
        pos[i] = pos[i]-(p[i]/mi)*deltat # back up to contact configuration
        pos[j] = pos[j]-(p[j]/mj)*deltat
        mtot = mi+mj
        pcmi = p[i]-ptot*mi/mtot # transform momenta to cm frame
        pcmj = p[j]-ptot*mj/mtot
        rrel = norm(pos[j]-pos[i])
        pcmi = pcmi-2*dot(pcmi,rrel)*rrel # bounce in cm frame
        pcmj = pcmj-2*dot(pcmj,rrel)*rrel
        p[i] = pcmi+ptot*mi/mtot # transform momenta back to lab frame
        p[j] = pcmj+ptot*mj/mtot
        pos[i] = pos[i]+(p[i]/mi)*deltat # move forward deltat in time
        pos[j] = pos[j]+(p[j]/mj)*deltat
 
    # Bounce off walls
    outside = less_equal(pos,corner1) # walls closest to origin
    p1 = p*outside
    p = p-p1+abs(p1) # force p component inward
    corner2 = array((wide/2.-offset,piston.y-thick/2.-offset,deep/2.-offset))
    outside = greater_equal(pos,corner2) # walls farther from origin
    p1 = p*outside
    p = p-p1-abs(p1) # force p component inward

    if scene.mouse.events:
        event = scene.mouse.getevent()
        if (not picked) and event.drag and (event.pick is indicator):
            picked = event.pick
            spos = event.project(normal=(0,0,1), d=indicator.z)
        else:
            picked = None
    if picked:
        newpos = scene.mouse.project(normal=(0,0,1), d=indicator.z)
        if newpos and newpos.y != spos.y:
            my = newpos.y
            if my < shaft.y-shaft.axis.y/2.:
                my = shaft.y-shaft.axis.y/2.
            elif my > shaft.y+shaft.axis.y/2.:
                my = shaft.y+shaft.axis.y/2.
            indicator.y = my
            vpiston = 0.04*(my-shaft.y)/dt
            spos = newpos
            if abs(my-shaft.y) < shaft.axis.y/25.:
                vpiston = 0.
            
    if vpiston != 0.0:
        newpy = piston.y+vpiston*dt
        if bottom.y+0.2*high < newpy < bottom.y+0.95*high:
            dp = 2.*Matom*vpiston
            if vpiston < 0.: # piston headed down, increase momenta of atoms caught up to
                hit = greater(pos+(p/m)*dt,array((wide,newpy-thick/2.-offset,deep)))
                pos = pos-pos*hit+(newpy-thick/2.-offset)*hit
                p1 = p*hit
                p = p-p1-abs(p1)+dp*hit
            else: # piston headed up, decrease momenta of atoms that catch up
                hit = greater(pos+(p/m)*dt,array((wide,newpy-thick/2.-offset,deep)))
                p1 = p*hit
                p = p-p1-abs(p1)+dp*hit
            piston.y = newpy

    # Update positions of display objects
    for i in range(Natoms):
        Atoms[i].pos = pos[i]
        
    T = sum(sum(p**2))/(2.*Matom)
    thermometer.axis.y = T*Tscale

    t = t+dt






        
