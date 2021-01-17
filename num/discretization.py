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

## Disretization of a physical problem
# Adrien Crovato

import numpy as np
from fe.element import Element

class Discretization:
    '''Build matrices and fluxes corresponding to a DG discretization of a given physics
        dU/dt + dF/dx = 0
    '''
    def __init__(self, frm, order, flux):
        self.frm = frm # formulation
        self.flux = flux # flux discretization at interface between two cells
        # Associate an element to each cell of the field
        self.elements = {} # cell to element map
        for i, c in enumerate(self.frm.field.cells):
            rows = [] # unknown rows in global solution list
            for j in range(self.frm.nv):
                rows.append(list(range((j+i*self.frm.nv)*(order+1), (j+1+i*self.frm.nv)*(order+1))))
            self.elements[c] = Element(rows, order, c)
        self.n = len(self.frm.field.cells) * (order + 1) # number of unknowns
        # Matrices (constants)
        self.mass = None
        self.stif = None
        # Source term (constants)
        self.source = None
    def __str__(self):
        return 'Discretization'

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
                self.mass.append(np.linalg.inv(np.kron(np.eye(self.frm.nv), m)))
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
                self.stif.append(np.kron(np.eye(self.frm.nv), m))
        return self.stif

    def __iflux(self, u, t):
        '''Compute flux on all interfaces
        '''
        # Return element of one interface
        def getelem(interface, index):
            ei = self.elements[interface.neighbors[index]]
            ui = ei.evalu(interface, u) # interpolate u from element evaluation points to interface integration points
            ni = ei.normal(interface)
            return ei, ui, ni
        # Compute the flux on one interface
        def getflux(u0, u1, n0):
            fi = [0.] * len(u0)
            for k in range(len(u0)):
                fi[k] = self.flux.eval(u0[k], u1[k], n0[0])
            return fi
        # Compute all fluxes...
        f = {}
        # ... in the field
        for i in self.frm.field.interfaces:
            e0, u0, n0 = getelem(i, 0)
            e1, u1, _ = getelem(i, 1)
            f[i] = getflux(u0, u1, n0)
        # ... on the boundaries
        for bc in self.frm.bcs:
            for i in bc.group.interfaces:
                e0, u0, n0 = getelem(i, 0)
                u1 = bc.eval(e0.evalx(i), t, u0)
                f[i] = getflux(u0, u1, n0)
        return f

    def __eflux(self, ifluxes, u):
        '''Compute flux on all elements
        '''
        f = []
        for e in self.elements.values():
            fe = [np.zeros(e.ep.n) for _ in range(self.frm.nv)] # flux on element
            for i,b in enumerate(e.cell.boundaries):
                ue = e.evalu(b, u) # u at interface (integration point)
                fi = ifluxes[b] # fstar at interface (integration point)
                ne = e.ishape[i].sf # sf at interface (integration point)
                w = e.ipi[i].w # weight (integration point)
                nrm = e.normal(b) # outward normal
                for k in range(len(ue)):
                    fl = self.frm.flux.eval(ue[k])
                    for v in range(self.frm.nv):
                        fe[v] += w[k] * b.djac[k] * ((fl[v] - fi[k][v]) * nrm[0]) * ne[k]
            f.append(fe)
        return f

    def __source(self):
        '''Compute source term on all elements
            since the term is constant, it is computed once and for all
        '''
        if not self.source:
            self.source = []
            if self.frm.source:
                for e in self.elements.values():
                    self.source.append(self.frm.source.eval(e))
            else:
                for e in self.elements.values():
                    self.source.append([[0.] * len(e.evalx()) for _ in range(self.frm.nv)])
        return self.source

    def compute(self, u, t):
        '''Compute rhs of equation
        '''
        # Compute mass and stiffness matrices on all elements
        me = self.__mass()
        se = self.__stif()
        # Compte interface fluxes on all interfaces
        fi = self.__iflux(u, t)
        # Compute total fluxes on all elements
        fe = self.__eflux(fi, u)
        # Compute sources on all elements
        sc = self.__source()
        # Compute RHS
        rhs = np.zeros(len(u))
        i = 0
        for e in self.elements.values():
            ue = []
            for j in range(self.frm.nv):
                ue.append(np.array(u[e.rows[j]]))
            rhs[np.concatenate(e.rows)] = me[i].dot(-se[i].dot(np.concatenate(self.frm.flux.eval(ue))) + np.concatenate(fe[i])) - np.concatenate(sc[i]) # M^-1 * (-S * fp + fn + M * s)
            i += 1
        return rhs
