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

from fe.quadrature import GaussLegendreLobatto # TODO

class Gui:
    def __init__(self):
        self.c2e = None
        self.fexact = None

    def set(self, c2e):
        self.c2e = c2e # cell to element mesh data structure
        # cell nodes
        self.xn = []
        for c in self.c2e.keys():
            xc = []
            for n in c.nodes:
                xc.append(n.pos[0])
            self.xn.append(xc)

    def update(self, u, t, tmax):
        '''Plot the solution on the mesh
        '''
        # Get data TODO interpolate solution using element shape function
        x = []
        for c, e in self.c2e.items():
            xe = GaussLegendreLobatto(e.order).x # TODO get it from e.shapes
            for i in range(len(xe)):
                xe[i] = (xe[i] + 1) * (c.nodes[1].pos[0] - c.nodes[0].pos[0]) / 2 + c.nodes[0].pos[0]
            x.append(xe)
        # Exact solution
        xex = []
        uex = []
        if self.fexact:
            for c in self.c2e.keys():
                xe = np.linspace(c.nodes[0].pos[0], c.nodes[1].pos[0], 25)
                ue = []
                for k in range(len(xe)): # TODO improve
                    ue.append(self.fexact(xe[k], t))
                xex.extend(xe)
                uex.extend(ue)
        # Plot
        plt.figure(1)
        plt.clf()
        plt.ylim(-1.5, 1.5)
        plt.grid(True)
        for i, e in enumerate(self.c2e.values()):
            plt.plot(self.xn[i], [0.] * len(self.xn[i]), '-ko', markersize=10)
            plt.plot(x[i], u[e.rows], '-bo', markersize=5)
        plt.plot(xex, uex, '--r')
        plt.xlabel('x')
        plt.ylabel('u')
        plt.title('time = {:5.3f} / {:5.3f}'.format(t, tmax))
        plt.draw()
        plt.pause(.001)
