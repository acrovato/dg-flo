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

## Disretization of the advection equation in one dimension
# Adrien Crovato
#
# TODO list:
# - Refactor shape functions to eval/interp from GLL nodes to GL integration points on element and interface
# - Add a method to evaluate real coordinates from reduced coordinates of GLL nodes ("change of frame")
# - Refactor data structure based on above
# - Allow to have a general type of flux, not just LF
# - Optimize and add multi-threading

import numpy as np
from fe.element import Element

class Discretization:
    '''Build matrices and fluxes corresponding to a DG discretization of the 1D advection equation
        du/dt + a * du/dx = 0
    '''
    def __init__(self, frm, order, alpha):
        self.frm = frm # formulation
        self.alpha = alpha # Lax-Friedrich flux alpha TODO replace by type of flux
        # Associate an element to each cell of the field
        self.elements = {} # cell to element map
        for i, c in enumerate(self.frm.field.cells):
            rows = list(range(i*(order+1), (i+1)*(order+1))) # unknown rows in global solution list
            self.elements[c] = Element(rows, order, c)
        self.n = len(self.frm.field.cells) * (order + 1) # number of unknowns
        # Matrices (constants)
        self.mass = None
        self.stif = None
    def __str__(self):
        return 'Advection discretization'

    def __mass(self):
        '''Compute the mass matrix
            M(i, j) = sum_k w_k Ni_k Nj_k dj_k
            since the matrix is constant, it is computed once and for all
        '''
        if not self.mass:
            self.mass = []
            for e in self.elements.values():
                # build
                m = np.zeros((e.ep.n, e.ep.n))
                for k in range(e.ip.n):
                    m += e.ip.w[k] * np.outer(e.eshape.sf[k], e.eshape.sf[k]) * e.cell.djac[k]
                self.mass.append(np.linalg.inv(m))
        return self.mass

    def __stif(self):
        '''Compute the stiffness matrix
            S(i, j) = sum_k w_k Ni_k invj_k dNj_k dj_k
            since the matrix is constant, it is computed once and for all
        '''
        if not self.stif:
            self.stif = []
            for e in self.elements.values():
                # build
                m = np.zeros((e.ep.n, e.ep.n))
                for k in range(e.ip.n):
                    m += e.ip.w[k] * np.outer(e.eshape.sf[k], e.cell.ijac[k] * e.eshape.dsf[k]) * e.cell.djac[k]
                self.stif.append(m)
        return self.stif

    def __nflux(self, u, t):
        '''Compute numerical flux on all interfaces
        '''
        f = {}
        for i in self.frm.field.interfaces:
            e0 = self.elements[i.neighbors[0]]
            u0 = e0.evalu(i, u) # interpolate u from element evaluation points to interface integration points
            n0 = e0.normal(i)
            if len(i.neighbors) == 1:
                # TODO use a more general inlet/outlet class (not based on normal sign?)
                if self.frm.a * n0[0] < 0:
                    u1 = self.frm.bc.eval(e0, i, t) # inlet
                    n1 = np.array([np.sign(self.frm.a) ,0, 0])
                else:
                    u1 = u0 # outlet
                    n1 = np.array([-np.sign(self.frm.a) ,0, 0])
            elif len(i.neighbors) == 2:
                e1 = self.elements[i.neighbors[1]]
                u1 = e1.evalu(i, u)
                n1 = e1.normal(i)
            else:
                raise RuntimeError('Discretization.__nflux() Element must have one or two interfaces!')
            fi = [0.] * len(u0)
            for k in range(len(u0)):
                fi[k] = self.frm.a * (u0[k] + u1[k]) / 2 + (1 - self.alpha) / 2 * np.abs(self.frm.a) * (u0[k] * n0[0] + u1[k] * n1[0])
            f[i] = fi
        return f

    def __flux(self, nfluxes, u):
        '''Compute flux on all elements
        '''
        f = []
        for e in self.elements.values():
            fe = np.zeros(e.ep.n) # flux on element
            for i,b in enumerate(e.cell.boundaries):
                ue = e.evalu(b, u) # u at interface (integration point)
                nf = nfluxes[b] # fstar at interface (integration point)
                ne = e.ishape[i].sf # sf at interface (integration point)
                w = e.ipi[i].w # weight (integration point)
                nrm = e.inormal[i] # outward normal
                for k in range(len(ue)):
                    fe += w[k] * b.djac[k] * ( (self.frm.a * ue[k] - nf[k] ) * nrm[0] ) * ne[k]
            f.append(fe)
        return f

    def compute(self, u, t):
        '''Compute rhs of equation
        '''
        # Compute mass and stiffness matrices on all elements
        me = self.__mass()
        se = self.__stif()
        # Compte numerical fluxes on all interfaces
        nfi = self.__nflux(u, t)
        # Compute total fluxes on all elements
        fe = self.__flux(nfi, u)
        # Compute RHS
        rhs = np.zeros(len(u))
        i = 0
        for e in self.elements.values():
            ue = np.array(u[e.rows])
            rhs[e.rows] = me[i].dot(-self.frm.a * se[i].dot(ue) + fe[i]) # M^-1 * ( - a * S * u + f)
            i += 1
        return rhs
