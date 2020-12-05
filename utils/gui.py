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

## Graphical user interface (1D only)
# Adrien Crovato

import numpy as np
import matplotlib.pyplot as plt
import fe.shapes as shp

class Gui:
    def __init__(self):
        self.c2e = None # cell to element mesh data structure
        self.fref = None # reference solution
        self.ns = 25 # number of sampling point per element

    def set(self, c2e):
        self.c2e = c2e
        self.xn = [] # cell nodes
        self.x = [] # coordinates of element evaluation points
        self.xs = [] # coordinates of element sampling points
        self.sf = [] # element shape functions
        for c,e in self.c2e.items():
            xc = []
            for n in c.nodes:
                xc.append(n.x[0])
            self.xn.append(xc)
            self.x.append(e.evalx())
            self.xs.append(np.linspace(c.nodes[0].x[0], c.nodes[1].x[0], self.ns))
            self.sf.append(shp.Lagrange(np.linspace(-1, 1, self.ns), e.ep.x).sf)

    def update(self, u, t, tmax):
        '''Plot the solution on the mesh
        '''
        us = [] # solution interpolated at sampling points
        ur = [] # reference soution at sampling points
        for i,e in enumerate(self.c2e.values()):
            ue = [[],[]]
            for k in range(self.ns):
                ue[0].append(self.fref(self.xs[i][k], t)) # reference solution
                ue[1].append(self.sf[i][k].dot(u[e.rows])) # interpolated solution
            ur.append(ue[0])
            us.append(ue[1])
        # Plot
        plt.figure(1)
        plt.clf()
        plt.ylim(-1.5, 1.5)
        plt.grid(True)
        for i, e in enumerate(self.c2e.values()):
            plt.plot(self.xn[i], [0.] * len(self.xn[i]), '-ko', markersize=10)
            plt.plot(self.xs[i], ur[i], c = 'tab:red', ls = '--', lw = 2)
            plt.plot(self.xs[i], us[i], c = 'tab:blue', ls = '-', lw = 2)
            plt.plot(self.x[i], u[e.rows], c = 'tab:blue', ls = '', marker = 'o', markersize=5)
        plt.xlabel('x')
        plt.ylabel('u')
        plt.title('time = {:5.3f} / {:5.3f}'.format(t, tmax))
        plt.draw()
        plt.pause(.001)
