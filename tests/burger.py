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

## Burger's equation test
# Adrien Crovato
#
# Solve the Burger's equation on a 1D grid

import numpy as np
import phys.flux as pfl
import num.flux as nfl
import num.conditions as numc
import num.formulation as numf
import num.discretization as numd
import num.tintegration as numt
import utils.lmesh as lmsh
import utils.testing as tst

def main(gui):
    # Constants
    l = 10 # domain length
    n = 3 # number of elements
    p = 5 # order of discretization
    u1 = 1.0 # in-out velocity
    cfl = 0.5 * 1 / (2*p+1) # half of max. Courant-Friedrichs-Levy for stability
    # Functions
    def initial(x, t): return -u1 * np.sign(x-l/2) if np.abs(x-l/2) > l/n else -n*u1/l * (x-l/2)
    def inout(x, t): return -u1 * np.sign(x-l/2)
    def fun(x, t): return -u1 * np.sign(x-l/2)
    if gui:
        gui.fref = fun
    # Parameters
    dx = l / n # cell length
    dt = cfl * dx / abs(u1) # time step
    tmax = 5.0 # simulation time

    # Generate mesh and get groups
    msh = lmsh.run(l, n)
    fld = msh.groups[0] # field
    inl = msh.groups[1] # inlet
    oul = msh.groups[2] # outlet
    # Generate formulation
    pflx = pfl.Burger() # physical Burger's flux
    ic = numc.Initial(fld, initial) # initial condition
    bcs = [numc.Dirichlet(inl, inout), numc.Dirichlet(oul, inout)] # inlet-outlet bc
    formul = numf.Formulation(msh, fld, pflx, ic, bcs)
    # Generate discretization
    nflx = nfl.LaxFried(pflx, 0.) # Lax–Friedrichs flux (0: full-upwind, 1: central)
    disc = numd.Discretization(formul, p, nflx)
    # Define time integration method
    tint = numt.Rk4(disc, gui)
    tint.run(dt, tmax)

    # Test
    uexact = [] # exact solution at element eval point
    for c,e in disc.elements.items():
        xe = e.evalx()
        for i in range(len(xe)):
            ue = fun(xe[i], tmax)
            uexact.append(ue)
    maxdiff = np.abs(np.max(tint.u - np.array(uexact)))
    tests = tst.Tests()
    tests.add(tst.Test('Max(u-u_exact)', maxdiff, 0., 1e-1))
    tests.run()

if __name__=="__main__":
    if parse().gui:
        import utils.gui as gui
        main(gui.Gui())
        input('<ENTER TO QUIT>')
    else:
        main(None)
