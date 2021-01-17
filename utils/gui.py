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

## Graphical user interface (1D only)
# Adrien Crovato

import numpy as np
import matplotlib.pyplot as plt
import fe.shapes as shp

class Gui:
    def __init__(self):
        self.c2e = None # cell to element mesh data structure
        self.vars = ['u'] # (default) variable names
        self.frefs = [lambda x, t: 0.0] # (default) reference solutions
        self.ns = 25 # number of sampling point per element

    def init(self, c2e, u):
        '''Initialize mesh data structure and plot styling
        '''
        # Mesh data
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
        # Plot initial solution with style
        self.figs = []
        plt.ion()
        for v in range(len(self.vars)):
            self.figs.append(plt.figure(v))
            ax = self.figs[v].gca()
            ax.grid(True)
            for i, e in enumerate(self.c2e.values()):
                ax.plot(self.xn[i], [0.] * len(self.xn[i]), '-ko', markersize=10)
                ax.plot(self.xs[i], [0.] * len(self.xs[i]), c = 'tab:red', ls = '--', lw = 2)
                ax.plot(self.xs[i], [0.] * len(self.xs[i]), c = 'tab:blue', ls = '-', lw = 2)
                ax.plot(self.x[i], [0.] * len(self.x[i]), c = 'tab:blue', ls = '', marker = 'o', markersize=5)
            ax.set_xlabel('x')
            ax.set_ylabel(self.vars[v])

    def update(self, u, t, tmax):
        '''Update solution and plot
        '''
        # Get solution
        us = [[] for _ in range(len(self.vars))] # solution interpolated at sampling points
        ur = [[] for _ in range(len(self.vars))] # reference soution at sampling points
        for v in range(len(self.vars)):
            for i,e in enumerate(self.c2e.values()):
                ue = [[], []]
                for k in range(self.ns):
                    ue[0].append(self.frefs[v](self.xs[i][k], t)) # reference solution
                    ue[1].append(self.sf[i][k].dot(u[e.rows[v]])) # interpolated solution
                ur[v].append(ue[0])
                us[v].append(ue[1])
        # Plot
        for v in range(len(self.vars)):
            ax = self.figs[v].gca()
            lines = ax.get_lines()
            for i, e in enumerate(self.c2e.values()):
                lines[i*4 + 1].set_ydata(ur[v][i])
                lines[i*4 + 2].set_ydata(us[v][i])
                lines[i*4 + 3].set_ydata(u[e.rows[v]])
            maxu = max([max(np.concatenate(ur[v])), max(np.concatenate(us[v])), 0.0])
            minu = min([min(np.concatenate(ur[v])), min(np.concatenate(us[v])), 0.0])
            if minu != maxu: ax.set_ylim(minu*1.05, maxu*1.05)
            ax.set_title('time = {:5.3f} / {:5.3f}'.format(t, tmax))
            self.figs[v].canvas.draw()
            self.figs[v].canvas.flush_events()
