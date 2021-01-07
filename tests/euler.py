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

## Euler equations test
# Adrien Crovato
#
# Solve the Euler equations (Sod's problem) on a 1D grid

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
    l = 1 # domain length
    n = 11 # number of elements
    p = 1 # order of discretization
    gamma = 1.4 # heat capacity ratio
    v = ['rho', 'rhou', 'E'] # physical variables
    cfl = 0.5 * 1 / (2*p+1) # half of max. Courant-Friedrichs-Levy for stability
    # Functions
    def fun0(x, t): return 1. if x < l/2 else 0.125
    def fun1(x, t): return 0.
    def fun2(x, t): return 1. / (gamma-1) if x < l/2 else 0.1 / (gamma-1)
    def fun(x, t): return 0.
    if gui:
        gui.vars = v
        gui.frefs = [fun, fun, fun]
    # Parameters
    dx = l / n # cell length
    dt = cfl * dx / 5 # time step
    tmax = 0.2 # simulation time

    # Generate mesh and get groups
    msh = lmsh.run(l, n)
    fld = msh.groups[0] # field
    inl = msh.groups[1] # inlet
    oul = msh.groups[2] # outlet
    # Generate formulation
    pflx = pfl.Euler(gamma) # physical Euler flux
    ic = numc.Initial(fld, [fun0, fun1, fun2]) # initial condition
    dbcs = [numc.Dirichlet(fun0), numc.Dirichlet(fun1), numc.Dirichlet(fun2)] # Dirichlet BCs
    bcs = [numc.Boundary(inl, dbcs), numc.Boundary(oul, dbcs)] # inlet-outlet bc
    formul = numf.Formulation(msh, fld, len(v), pflx, ic, bcs)
    # Generate discretization
    nflx = nfl.LaxFried(pflx, 0.) # Lax–Friedrichs flux (0: full-upwind, 1: central)
    disc = numd.Discretization(formul, p, nflx)
    # Define time integration method
    wrt = wrtr.Writer('sol', 1, v, disc)
    tint = numt.Rk4(disc, wrt, gui)
    tint.run(dt, tmax)

    # Test
    # TODO EULER

if __name__=="__main__":
    if parse().gui:
        import utils.gui as gui
        main(gui.Gui())
        input('<ENTER TO QUIT>')
    else:
        main(None)
