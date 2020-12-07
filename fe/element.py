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

## Computational element
# Adrien Crovato
# TODO 1D, need to have specific SF and GP for element dimension
# TODO check generality of solution evaluation (evalu) and coordinates evaluation (evalx)

import numpy as np
from fe.quadrature import GaussLegendre, GaussLegendreLobatto
from fe.shapes import Lagrange

# Base class
class Element:
    def __init__(self, rows, order, cell):
        self.rows = rows # row inidices in global solution vector
        self.order = order # order of the element
        self.ep = GaussLegendreLobatto(order) # evaluation points (Gauss-Legendre-Lobatto)
        self.ip = GaussLegendre(order) # integration points and weights (Gauss-Legendre)
        self.eshape = Lagrange(self.ip.x, self.ep.x) # shape functions at element
        self.cell = cell # underlying geometric mesh cell
        self.cell.update(self.ip.x) # update geometric data at integration point
        self.ipi = [] # integration points and weights at interface
        self.ishape = [] # shape functions at interface
        self.inormal = [] # 
        for b in self.cell.boundaries:
            self.__map(b) # map integration points to the cell
            self.__normal(b) # compute outward normals
    def __str__(self):
       return 'DG element of order ' + str(self.order) + ', on ' + str(self.cell)

    def __map(self, interface):
        '''Map the coordinates of the (interface) integration point from the interface to the cell reference frame
        '''
        ip = GaussLegendre(0) # integration points
        if interface == self.cell.boundaries[0]:
            ip.x[0] = -1.0
        elif interface == self.cell.boundaries[1]:
            ip.x[0] = 1.0
        else:
            raise RuntimeError('Element.eval interface not found!')
        ip.w[0] = 1.0
        interface.update(ip.x) # update geometric data at integration point
        self.ipi.append(ip)
        self.ishape.append(Lagrange(ip.x, self.ep.x))

    def __normal(self, interface):
        '''Compute normal of interface pointing outward of element
        '''
        nrm = interface.normal # "true" normal
        dcg = interface.cg - self.cell.cg # vector joining cell CG to vertex CG
        if nrm.dot(dcg) > 0:
            self.inormal.append(nrm) # normal already points outward
        elif nrm.dot(dcg) < 0:
            self.inormal.append(-nrm) # normal points inward
        else:
            raise RuntimeError('Element.__normal bad cell shape (centroid on boundary face)!')

    def evalu(self, interface, u):
        '''Evaluate solution at integration points of interface
        '''
        ui = [] # solution at interface
        try:
            i = self.cell.boundaries.index(interface)
        except:
            raise RuntimeError('Element.eval interface not found!')
        for k in range(self.ipi[i].n):
            ui.append(self.ishape[i].sf[k].dot(u[self.rows]))
        return ui

    def evalx(self, interface = None):
        '''Compute true coordinates of evaluation points (if interface = None) or of interface integration points
        '''
        x = []
        if interface:
            try:
                i = self.cell.boundaries.index(interface)
            except:
                raise RuntimeError('Element.eval interface not found!')
            xp = self.ipi[i].x
        else:
            xp = self.ep.x
        for xe in xp:
            x.append((xe + 1) * (self.cell.nodes[1].x[0] - self.cell.nodes[0].x[0]) / 2 + self.cell.nodes[0].x[0])
        return x

    def normal(self, interface):
        '''Get outward normal of interface
        '''
        return self.inormal[self.cell.boundaries.index(interface)]
