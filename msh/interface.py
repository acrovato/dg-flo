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
        self.neighbors = [] # list of interface neighbor (left and right) cells
    def __str__(self):
        msg = 'interface #' + str(self.no) + ' (' + str(self.type()) + '), nodes:'
        for n in self.nodes:
            msg += ' #' + str(n.no)
        msg += ', neighbors:'
        for n in self.neighbors:
            msg += ' #' + str(n.no) + ' (' + str(n.type()) + ')'
        return msg
    def __hash__(self):
        '''Assign a unique key to the object
        '''
        nsum = 0
        for n in self.nodes:
            nsum += n.no
        return nsum
    def __eq__(self, other):
        '''Determine if two interfaces are the same
        '''
        cnt = 0
        # Compare nodes of self to nodes of other
        for i in range(len(self.nodes)):
            for n1 in other.nodes:
                if self.nodes[i] == n1:
                    cnt += 1
                    break
            if cnt != i + 1:
                return False
        return True

    def type(self):
        return ITYPE.UNK

# 0D vertex
class Vertex(Interface):
    '''Vertex interface between two Line cells
    '''
    def __init__(self, nodes):
        Interface.__init__(self, nodes)

    def type(self):
        return ITYPE.VRTX
