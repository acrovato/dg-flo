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
# TODO only homogeneous Neumann for now

class Initial:
    '''Initial conditions
    '''
    def __init__(self, group, funs):
        self.group = group # physical group
        self.funs = funs # list of functions(position, time) for each variable
    def __str__(self):
        return 'Initial conditions'

    def eval(self, celements):
        '''Evaluate the initial conditons on the nodes of the elements
        '''
        u = []
        for c in self.group.cells:
            xe = celements[c].evalx()
            for j in range(len(self.funs)):
                for i in range(len(xe)):
                    u.append(self.funs[j](xe[i], 0))
        return u

class Boundary:
    '''Boundary conditions
    '''
    def __init__(self, group, bcs):
        self.group = group # physical group
        self.bcs = bcs # list of boundary conditions for each variable
    def __str__(self):
        return 'Boundary conditions'

    def eval(self, x, t, u):
        '''Evaluate the boundary conditons at given positions and time
        '''
        ub = [[] for _ in range(len(x))]
        for i in range(len(x)):
            for v in range(len(self.bcs)):
                ub[i].append(self.bcs[v].eval(x[i], t, u[i][v]))
        return ub

class Dirichlet:
    '''Dirichlet boundary condition
    '''
    def __init__(self, fun):
        self.fun = fun # function(position, time)
    def __str__(self):
        return 'Dirichlet boundary condition'

    def eval(self, x, t, u):
        '''Evaluate the Dirichlet boundary conditon at given position and time
        '''
        return self.fun(x, t)

class Neumann:
    '''Neumann boundary condition
    '''
    def __init__(self):
        pass
    def __str__(self):
        return 'Neumann boundary condition'

    def eval(self, x, t, u):
        '''Evaluate homegeneous Neumann boundary conditon (return solution at current position and time so that the flux is null)
        '''
        return u
