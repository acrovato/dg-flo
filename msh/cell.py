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

# Cell type
class CTYPE(Enum):
    UNK = 0,
    LINE2 = 1

    def __str__(self):
        if self == CTYPE.UNK:
            return 'UNKNOWN'
        elif self == CTYPE.LINE2:
            return 'LINE'

# Base class
class Cell:
    def __init__(self, no, nodes):
        self.no = no # cell number
        self.nodes = nodes # list of nodes of the cell
        self.boundaries = [] # list of boundaries of the cell
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
