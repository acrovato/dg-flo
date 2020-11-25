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

## Gauss quadrature rules test
# Adrien Crovato
#
# Test the Gaussian quadratures for order 4 (n = 5)

import numpy as np
import advection.conditions as advc
import advection.formulation as advf
import advection.discretization as advd
import num.tintegration as numt
import utils.lmesh as lmsh
import utils.testing as tst
import utils.gui as gui

from fe.quadrature import GaussLegendreLobatto # TODO

def main(gui):
    # Constants
    l = 10. # domain length
    a = 3. # advection velocity
    n = 3 # number of elements
    p = 4 # order of discretization
    alpha = 0. # alpha factor for LF flux (0: full-upwind, 1: central)
    cfl = 0.5 * 1 / (2*p+1) # half of max. Courant-Friedrich-Levy for stability
    # Functions
    def initial(x, t): return 0.0
    def fun(x, t): return np.sin(2*np.pi*(x-a*t)/l*2)
    if gui:
        gui.fexact = fun
    # Parameters
    dx = l / n # cell length
    dt = cfl * dx / a # time step
    tmax = round(l / a, 5) # simulation time (l/a)

    # Generate mesh
    msh = lmsh.run(l, n)
    # Generate formulation
    fld = msh.groups[0] # field cells
    ic = advc.Initial(initial) # initial condition
    inlet = advc.Dirichlet(fun) # inlet bc
    formul = advf.Formulation(msh, fld, ic, inlet, a)
    # Generate discretization
    disc = advd.Discretization(formul, p, alpha)
    # Define time integration method
    tint = numt.Rk2(disc, gui)
    tint.run(dt, tmax)

    # Test
    uexact = [] # TODO change method to generate interpolation point (element.evalx?)
    for c,e in disc.elements.items():
        xe = GaussLegendreLobatto(e.order).x
        for i in range(len(xe)):
            xe[i] = (xe[i] + 1) * (c.nodes[1].pos[0] - c.nodes[0].pos[0]) / 2 + c.nodes[0].pos[0]
            ue = fun(xe[i], tmax)
            uexact.append(ue)
    maxdiff = np.abs(np.max(tint.u - np.array(uexact)))
    tests = tst.Tests()
    tests.add(tst.Test('Max(u-u_exact)', maxdiff, 0., 1e-1))
    tests.run()

if __name__=="__main__":
    if parse().gui:
        main(gui.Gui())
        input('<ENTER TO QUIT>')
    else:
        main(None)
