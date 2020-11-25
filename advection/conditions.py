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

## Initial and boundary conditions
# Adrien Crovato
# TODO these classes should be more general

import numpy as np
from fe.quadrature import GaussLegendreLobatto # TODO

class Initial:
    '''Initial condition
    '''
    def __init__(self, fun):
        self.fun = fun # function(position, time)
    def __str__(self):
        return 'Initial condition'

    def eval(self, celements):
        '''Evaluate the initial conditon on the nodes of the elements
        '''
        # TODO make an element.evalx method
        u = []
        for c,e in celements.items():
            xe = GaussLegendreLobatto(e.order).x
            for i in range(len(xe)):
                xe[i] = (xe[i] + 1) * (c.nodes[1].pos[0] - c.nodes[0].pos[0]) / 2 + c.nodes[0].pos[0]
                ue = self.fun(xe[i], 0)
                u.append(ue)
        return u

class Dirichlet:
    '''Dirichlet boundary condition
    '''
    def __init__(self, fun):
        self.fun = fun # function(position, time)
    def __str__(self):
        return 'Boundary condition'

    def eval(self, interface, t):
        '''Evaluate the dirichlet boundary conditon on the interface
        '''
        # TODO from interface find positions (need integration points and nodes)
        u = []
        for n in interface.nodes:
            u.append(self.fun(n.pos[0], t))
        return u
