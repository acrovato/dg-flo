# -*- coding: utf8 -*-
# test encoding: à-é-è-ô-ï-€

# Copyright 2021 Adrien Crovato
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

## Shallow water equations test
# Adrien Crovato
#
# Solve the shallow water equations (solitary wave - tsunami) on a 1D grid

import numpy as np
import phys.flux as pfl
import num.flux as nfl
import num.source as nsrc
import num.conditions as numc
import num.formulation as numf
import num.discretization as numd
import num.tintegration as numt
import utils.lmesh as lmsh
import utils.writer as wrtr
import utils.testing as tst

def main(gui):
    # Constants
    l = 400 # domain length
    g = 9.81 # acceleration due to gravity
    h = [1.0, 0.01] # steady state water height
    w = [0.1, 20] # height and width of initial wave
    z = [20, 100] # bed slope initial and final position
    n = 50 # number of elements
    p = 6 # order of discretization
    v = ['h', 'u'] # physical variables
    cfl = 1 / (2*p+1) # half of max. Courant-Friedrichs-Levy for stability
    # Functions
    # bed
    def zb(x):
        if x < l/2 + z[0]: return 0.
        elif x < l/2 + z[1]: return 0.5 * (h[0]-h[1]) * (1 - np.cos(np.pi/(z[1]-z[0]) * (x-l/2-z[0])))
        else: return h[0] - h[1]
    # source term function (bed slope * g)
    def gdzb(x):
        if x >= l/2 + z[0] and x < l/2 + z[1]: return g * 0.5 * np.pi * (h[0]-h[1])/(z[1]-z[0]) * np.sin(np.pi/(z[1]-z[0])*(x-l/2-z[0]))
        else: return 0.
    # initial and boundary conditions
    def h0(x, t): return h[0] + w[0] * np.cos(0.5*np.pi/w[1]*(x-l/2)) - zb(x) if abs(x-l/2) < w[1] else h[0] - zb(x)
    def u0(x, t): return 0.0
    def hl(x, t): return h[0] - zb(x)
    def ul(x, t): return 0.0
    # reference solutions
    def rfunh(x, t):
        if x < 116:
            return h[0]
        elif x < 160:
            return -0.0001*x*x + 0.0272*x - 0.7985
        elif x < 220:
            return h[0]
        elif x < 272:
            return -0.000192559021192277*x*x + 0.0810028508376352*x - 7.48640208379703
        elif x < 300:
            return 0.000308903323667424*x*x	- 0.186483075379383*x + 28.1505055888591
        else:
            return h[1]
    def rfunu(x, t):
        if x < 116:
            return 0.
        elif x < 156:
            return 0.000353056759525554*x*x - 0.0955691190357186*x + 6.32071941182482
        elif x < 245:
            return -1.12067281188971e-06*x*x + 0.000289440705269957*x - 0.0167770084481066
        elif x < 264:
            return -3.37962520178778e-05*x*x + 0.0300418744173713*x - 5.31085043131794
        elif x < 272:
            return -0.00755364567412781*x*x + 4.01701626023094*x - 533.785818827200
        else:
            return 0.
    funs = [rfunh, rfunu]
    if gui:
        gui.vars = v
        gui.frefs = funs
    # Parameters
    dx = l / n # cell length
    dt = cfl * dx / (0.5 + np.sqrt(g*h[0])) # time step
    tmax = 20 # simulation time (l/a)

    # Generate mesh
    msh = lmsh.run(l, n)
    fld = msh.groups[0] # field
    inl = msh.groups[1] # inlet
    oul = msh.groups[2] # outlet
    # Generate formulation
    pflx = pfl.ShallowWater(g) # physical transport flux
    ic = numc.Initial(fld, [h0, u0]) # initial condition
    left = numc.Boundary(inl, [numc.Dirichlet(hl), numc.Dirichlet(ul)]) # left bc
    right = numc.Boundary(oul, [numc.Dirichlet(hl), numc.Dirichlet(ul)]) # right bc
    formul = numf.Formulation(msh, fld, len(v), pflx, ic, [left, right], nsrc.Source([lambda x: 0., gdzb]))
    # Generate discretization
    nflx = nfl.LaxFried(pflx, 0.) # Lax–Friedrichs flux (0: full-upwind, 1: central)
    disc = numd.Discretization(formul, p, nflx)
    # Define time integration method
    wrt = wrtr.Writer('sol', 1, v, disc)
    tint = numt.SspRk4(disc, wrt, gui)
    tint.run(dt, tmax)

    # Test
    uexact = [[] for _ in range(len(v))] # exact solution at element eval point
    ucomp = [[] for _ in range(len(v))] # computed solution at element eval point
    for c,e in disc.elements.items():
        xe = e.evalx()
        for j in range(len(v)):
            for i in range(len(xe)):
                uexact[j].append(funs[j](xe[i], tint.t))
                ucomp[j].append(tint.u[e.rows[j][i]])
    maxdiff = [] # infinite norm
    nrmdiff = [] # Frobenius norm
    for j in range(len(v)):
        maxdiff.append(np.max(np.abs(np.array(ucomp[j]) - np.array(uexact[j]))))
        nrmdiff.append(np.linalg.norm(np.array(ucomp[j]) - np.array(uexact[j])))
    tests = tst.Tests()
    tests.add(tst.Test('Max(h-h_exact)', maxdiff[0], 0., 1e-1))
    tests.add(tst.Test('Norm(h-h_exact)', nrmdiff[0], 0., 1e-1))
    tests.add(tst.Test('Max(u-u_exact)', maxdiff[1], 0., 1e-1))
    tests.add(tst.Test('Norm(u-u_exact)', nrmdiff[1], 0., 1e-1))
    tests.run()

if __name__=="__main__":
    if parse().gui:
        import utils.gui as gui
        main(gui.Gui())
        input('<ENTER TO QUIT>')
    else:
        main(None)
