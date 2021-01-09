# -*- coding: utf8 -*-
# test encoding: à-é-è-ô-ï-€

# Copyright 2020 Adrien Crovato
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

## Advection equation test
# Adrien Crovato
#
# Solve the advection equation (2 variables) on a 1D grid

import numpy as np
import phys.flux as pfl
import num.flux as nfl
import num.conditions as numc
import num.formulation as numf
import num.discretization as numd
import num.tintegration as numt
import utils.lmesh as lmsh
import utils.writer as wrtr
import utils.testing as tst

def main(gui):
    # Constants
    l = 10 # domain length
    a = 3. # advection velocity
    n = 3 # number of elements
    p = 4 # order of discretization
    v = ['u', 'v'] # physical variables
    cfl = 0.5 * 1 / (2*p+1) # half of max. Courant-Friedrichs-Levy for stability
    # Functions
    def initial(x, t): return 0.0
    def funa(x, t): return np.sin(2*np.pi*(x-a*t)/l*2)
    def funb(x, t): return np.sin(2*np.pi*(x+a*t)/l*2)
    funs = [funa, funb]
    if gui:
        gui.vars = v
        gui.frefs = funs
    # Parameters
    dx = l / n # cell length
    dt = cfl * dx / a # time step
    tmax = round(l / a, 5) # simulation time (l/a)

    # Generate mesh
    msh = lmsh.run(l, n)
    fld = msh.groups[0] # field
    inl = msh.groups[1] # inlet
    oul = msh.groups[2] # outlet
    # Generate formulation
    pflx = pfl.Advection2(a, -a) # physical transport flux
    ic = numc.Initial(fld, [initial, initial]) # initial condition
    inlet = numc.Boundary(inl, [numc.Dirichlet(funa), numc.Neumann()]) # inlet bc
    outlet = numc.Boundary(oul, [numc.Neumann(), numc.Dirichlet(funb)]) # outlet bc
    formul = numf.Formulation(msh, fld, len(v), pflx, ic, [inlet, outlet])
    # Generate discretization
    nflx = nfl.LaxFried(pflx, 0.) # Lax–Friedrichs flux (0: full-upwind, 1: central)
    disc = numd.Discretization(formul, p, nflx)
    # Define time integration method
    wrt = wrtr.Writer('sol', 1, v, disc)
    tint = numt.Rk4(disc, wrt, gui)
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
    tests.add(tst.Test('Max(u-u_exact)', maxdiff[0], 0., 3e-1))
    tests.add(tst.Test('Norm(u-u_exact)', nrmdiff[0], 0., 3e-1))
    tests.add(tst.Test('Max(v-v_exact)', maxdiff[1], 0., 3e-1))
    tests.add(tst.Test('Norm(v-v_exact)', nrmdiff[1], 0., 3e-1))
    tests.run()

if __name__=="__main__":
    if parse().gui:
        import utils.gui as gui
        main(gui.Gui())
        input('<ENTER TO QUIT>')
    else:
        main(None)
