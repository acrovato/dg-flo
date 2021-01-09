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
    n = 75 # number of elements
    p = 2 # order of discretization
    gamma = 1.4 # heat capacity ratio
    v = ['rho', 'rhou', 'E'] # physical variables
    cfl = 0.5 * 1 / (2*p+1) # half of max. Courant-Friedrichs-Levy for stability
    # Functions
    def fun0(x, t): return 1. if x < l/2 else 0.125
    def fun1(x, t): return 0.
    def fun2(x, t): return 1. / (gamma-1) if x < l/2 else 0.1 / (gamma-1)
    def rfun0(x, t):
        if x < 0.381*l:
            return 1.
        elif x < 0.489*l:
            return 15.5391*x*x - 18.7087*x + 5.8748
        elif x < 0.587*l:
            return 0.442
        elif x < 0.665*l:
            return 0.274
        else:
            return 0.125
    def rfun1(x, t):
        if x < 0.381*l:
            return 0.
        elif x < 0.489*l:
            return -36.1960*x*x + 35.0524*x - 8.0979
        elif x < 0.587*l:
            return 0.394
        elif x < 0.665*l:
            return 0.244
        else:
            return 0.
    def rfun2(x, t):
        if x < 0.381*l:
            return 2.5
        elif x < 0.489*l:
            return 50.3024*x*x - 58.8475*x + 17.6300
        elif x < 0.587*l:
            return 0.885
        elif x < 0.665*l:
            return 0.831
        else:
            return 0.25
    funs = [rfun0, rfun1, rfun2]
    if gui:
        gui.vars = v
        gui.frefs = funs
    # Parameters
    dx = l / n # cell length
    dt = cfl * dx / 2 # time step
    tmax = 0.1 # simulation time

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
    tests.add(tst.Test('Max(rho-rho_exact)', maxdiff[0], 0., 2e-1))
    tests.add(tst.Test('Norm(rho-rho_exact)', nrmdiff[0], 0., 5e-1))
    tests.add(tst.Test('Max(rhou-rhou_exact)', maxdiff[1], 0., 4e-1))
    tests.add(tst.Test('Norm(rhou-rhou_exact)', nrmdiff[1], 0., 5e-1))
    tests.add(tst.Test('Max(E-E_exact)', maxdiff[2], 0., 9e-1))
    tests.add(tst.Test('Norm(E-E_exact)', nrmdiff[2], 0., 2e-0))
    tests.run()

if __name__=="__main__":
    if parse().gui:
        import utils.gui as gui
        main(gui.Gui())
        input('<ENTER TO QUIT>')
    else:
        main(None)
