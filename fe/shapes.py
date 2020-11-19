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

## Shape functions
# Adrien Crovato
# TODO optimize
# TODO 1D only

import numpy as np

# Base class
class Shapes:
    def __init__(self):
        self.n = 0 # number of quadrature points
        self.phi = [] # shape functions
        self.dphi = [] # derivatives of shape functions
    def __str__(self):
        return 'Shape function not implemented\n'

# Lagrange
class Lagrange(Shapes):
    '''Lagrange shape functions
    '''
    def __init__(self, x, xi):
        Shapes.__init__(self)
        self.n = len(xi)
        self.__eval(x, xi)
        self.__evald(x, xi)
    def __str__(self):
        return 'Lagrange shape functions (n = ' + str(self.n) + ')\n'

    def __eval(self, x, xi):
        '''Evaluate polynomials at x using interpolation points xi
        '''
        for k in range(len(x)):
            phi = np.ones((self.n, 1))
            for i in range(self.n):
                for j in range(self.n):
                    if i != j:
                        phi[i, :] *= (x[k] - xi[j]) / (xi[i] - xi[j])
            self.phi.append(phi)

    def __evald(self, x, xi):
        '''Evaluate polynomial derivatives at x using interpolation points xi 
        '''
        for k in range(len(x)):
            dphi = np.zeros((self.n, 1))
            for i in range(self.n):
                for j in range(self.n):
                    if i != j:
                        prod = 1.0 / (xi[i] - xi[j])
                        for l in range(self.n):
                            if l != i and l != j:
                                prod *= (x[k] - xi[l]) / (xi[i] - xi[l])
                        dphi[i, :] += prod
            self.dphi.append(dphi)
