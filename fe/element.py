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

import numpy as np
from fe.quadrature import GaussLegendre, GaussLegendreLobatto
from fe.shapes import Lagrange

# Base class
class Element:
    def __init__(self, rows, cell, order):
        self.rows = rows # row inidices in global solution vector
        self.cell = cell # underlying geometric mesh cell
        self.order = order # order of the element
        self.nn = order + 1 # number of nodes (points where unknowns are evaluated)
        self.gauss = GaussLegendre(order) # Gauss (integration) points and weights
        self.shape = Lagrange(self.gauss.x, GaussLegendreLobatto(order).x) # shape functions
        self.cell.update(self.gauss.x) # update geometric data at Gauss point
    def __str__(self):
       return 'DG element of order ' + str(self.order) + ', on ' + str(self.cell)

    def evalu(self, interface, u):
        '''Evaluate solution at integration points of interface
        '''
        # TODO valid for 1D shape function
        # TODO valid for 1 integration point (equal to evaluation point)
        if interface == self.cell.boundaries[0]:
            return [u[self.rows[0]]]
        elif interface == self.cell.boundaries[1]:
            return [u[self.rows[-1]]]
        else:
            raise RuntimeError('Element.eval interface not found!')

    def evaln(self, interface):
        '''Evaluate shape function at integration point of interface
        '''
        # TODO move to self.shape...
        # TODO valid for 1D shape function
        # TODO valid for 1 integration point (equal to evaluation point)
        if interface == self.cell.boundaries[0]:
            n = np.zeros(self.order+1)
            n[0] = 1.
        elif interface == self.cell.boundaries[1]:
            n = np.zeros(self.order+1)
            n[-1] = 1.
        else:
            raise RuntimeError('Element.eval interface not found!')
        return [n]
