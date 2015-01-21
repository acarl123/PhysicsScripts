# SHM.py
# Simple Harmonic Motion demo with graphs
# for Physics 1 level lecture demo use
# written by Daniel C. Hennessy, 2015
# This is a Visual Python script.  Run it using Python with the
#   Visual module installed; see http://www.vpython.org for
#   the necessary software.
#

from visual import *
from visual.graph import *

##########
# Define our simulation parameters
##########

Amp = 1.00    # Initial amplitude of oscillator (m)
Mass = 1.00   # Mass of oscillator (kg)
Springk = 1.00 # Spring constant (N/m)
SpringL = 10.0 # Length of spring (m)

Damping = 0.00 # damping constant (N*s/m)  (Note: critical damping is at sqrt(4*m*k))
Drivef = 0.059  # driving frequency (Hz) (Note: f_0 = sqrt(k/m)/(2*pi))
DriveA = 0.00  # driving amplitude (N)

dt = 0.005    # time step size (s)

##########
# Set up objects, display, and graphs
##########

spring = helix(pos=vector(0,0,0), axis=vector(SpringL+Amp,0,0), radius=0.1*SpringL, color=color.cyan)
ball = sphere(pos=vector(SpringL+Amp,0,0), radius=0.15*SpringL, color=color.red)

ball.v = vector(0,0,0)

scene.autoscale = 0
scene.center = vector(SpringL/2,0,0)

xdisp = gdisplay(x=450, y=0, width=500, height=200, title='position vs. time', xtitle = 't (s)', ytitle = 'position (m)', ymin = 8.0, ymax = 12.0, xmin = 0.0, xmax = 15.0)
xgraph = gcurve(color=color.red)  # graph position vs. time
vdisp = gdisplay(x=450, y=220, width=500, height=200, title='velocity vs. time', xtitle = 't (s)', ytitle = 'v (m/s)', xmin = 0.0, xmax = 15.0)
vgraph = gcurve(color=color.blue)  # graph velocity vs. time
adisp = gdisplay(x=450, y=420, width=500, height=200, title='acceleration vs. time', xtitle = 't (s)', ytitle = 'a (m/s^2)', xmin = 0.0, xmax = 15.0)
agraph = gcurve(color=color.magenta)  # graph accel. vs. time

cdisp = display(x=970, y=0, width=300, height=300, title='circular motion')
cdisp.range = 6.0
hub = sphere(display=cdisp, pos=vector(0,0,0), radius=1.0, color=color.red)
hand = cylinder(display=cdisp, pos=vector(0,0,0), axis=vector(0,-5.0,0), radius=0.5, color=color.red)

t = 0.00   # clock time

#########
# The main physics loop
#########

while 1:
    rate(1/dt)

    F = -Springk * vector(ball.pos - vector(SpringL,0,0))   # Hooke's Law

    F = F - Damping * ball.v    # damping force

    F = F + vector(DriveA,0,0) * cos(2*pi*Drivef*t) * (-1)   # driving force
    
    ball.v = ball.v + F*dt/Mass  # Newton's 2nd Law

    ball.pos = ball.pos + ball.v*dt   # kinematics

    spring.axis = vector(ball.pos.x,0,0)  # Move the spring so it stays connected to the ball

    xgraph.plot(pos=(t, ball.pos.x))
    vgraph.plot(pos=(t, ball.v.x))
    agraph.plot(pos=(t, F.x/Mass))

    hand.rotate(angle=-dt*sqrt(Springk/Mass), axis=(0,0,1.0), origin=(0,0,0))

    t = t + dt
    
