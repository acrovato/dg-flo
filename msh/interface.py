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

## Interface between two cells
# Adrien Crovato

from enum import Enum
import numpy as np

# Interface type
class ITYPE(Enum):
    UNK = 0,
    VRTX = 1

    def __str__(self):
        if self == ITYPE.UNK:
            return 'UNKNOWN'
        elif self == ITYPE.VRTX:
            return 'VERTEX'

# Base class
class Interface:
    def __init__(self, nodes):
        self.no = 0 # interface number
        self.nodes = nodes # list of nodes defining the interface
        self.cg = np.zeros(3) # interface centroid
        for n in self.nodes:
            self.cg += n.x
        self.cg /= len(nodes)
        self.normal = np.zeros(3) # interface normal
        self.neighbors = [] # list of interface neighbor (left and right) cells
        self.djac = [] # list of Jacobian determinants (at integration points)
    def __str__(self):
        msg = 'interface #' + str(self.no) + ' (' + str(self.type()) + '), nodes:'
        for n in self.nodes:
            msg += ' #' + str(n.no)
        msg += ', neighbors:'
        for n in self.neighbors:
            msg += ' #' + str(n.no) + ' (' + str(n.type()) + ')'
        return msg

    def type(self):
        return ITYPE.UNK

# 0D vertex
class Vertex(Interface):
    '''Vertex interface between two Line cells
    '''
    def __init__(self, nodes):
        Interface.__init__(self, nodes)
        self.normal = np.array([1., 0., 0.])

    def type(self):
        return ITYPE.VRTX

    def update(self, xi):
        '''Update members depending on the integration points (non-geometric data)
        '''
        # For a vertex, Jacobian determinant is unity
        self.djac = [1.0]
