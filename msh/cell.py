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

## Mesh cell
# Adrien Crovato

from enum import Enum
import numpy as np
from fe.shapes import Lagrange

# Cell type
class CTYPE(Enum):
    UNK = 0,
    LINE2 = 1,
    POINT1 = 15

    def __str__(self):
        if self == CTYPE.UNK:
            return 'UNKNOWN'
        elif self == CTYPE.LINE2:
            return 'LINE'
        elif self == CTYPE.POINT1:
            return 'POINT'

# Base class
class Cell:
    def __init__(self, no, nodes):
        self.no = no # cell number
        self.nodes = nodes # list of nodes of the cell
        self.cg = np.zeros(3) # cell centroid
        for n in self.nodes:
            self.cg += n.x
        self.cg /= len(nodes)
        self.boundaries = [] # list of boundaries of the cell
        self.jac = [] # list of Jacobian matrices (at integration points)
        self.ijac = [] # list of inverse Jacobian matrices (at integration points)
        self.djac = [] # list of Jacobian determinants (at integration points)
    def __str__(self):
        msg = 'cell #' + str(self.no) + ' (' + str(self.type()) + '), nodes:'
        for n in self.nodes:
            msg += ' #' + str(n.no)
        msg += ', boundaries:'
        for b in self.boundaries:
            msg += ' #' + str(b.no) + ' (' + str(b.type()) + ')'
        return msg

    def type(self):
        return CTYPE.UNK

# 1D line
class Line(Cell):
    '''Line cell, made of 2 nodes
    '''
    def __init__(self, no, nodes):
        Cell.__init__(self, no, nodes)

    def type(self):
        return CTYPE.LINE2

    def update(self, xi):
        '''Update members depending on the integration points (non-geometric data)
        '''
        # Compute Jacobian at integration points xi using classical linear shape functions
        self.jac = [np.zeros((1,1))] * len(xi)
        self.ijac = [np.zeros((1,1))] * len(xi)
        self.djac = [0.] * len(xi)
        dn = Lagrange(xi, [-1, 1]).dsf
        for k in range(len(xi)):
            jac = np.zeros((1,1))
            for i in range(len(self.nodes)):
                jac[0,0] += dn[k][0, i] * self.nodes[i].x[0]
            self.jac[k] = jac
            self.ijac[k] = np.linalg.inv(self.jac[k]) # inverse: 1/j
            self.djac[k] = np.linalg.det(self.jac[k]) # dtm: j

# 0D point
class Point(Cell):
    '''Point cell, made of 1 node
    '''
    def __init__(self, no, nodes):
        Cell.__init__(self, no, nodes)

    def type(self):
        return CTYPE.POINT1
