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

## Shape functions
# Adrien Crovato
# TODO optimize
# TODO 1D only

import numpy as np

# Base class
class Shapes:
    def __init__(self):
        self.n = 0 # number of sampling points
        self.sf = [] # shape functions
        self.dsf = [] # derivatives of shape functions
    def __str__(self):
        raise RuntimeError('Shape function not implemented!')

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
        return 'Lagrange shape functions (n = ' + str(self.n) + ')'

    def __eval(self, x, xi):
        '''Evaluate polynomials at x using interpolation points xi
        '''
        for k in range(len(x)):
            n = np.ones(self.n)
            for i in range(self.n):
                for j in range(self.n):
                    if i != j:
                        n[i] *= (x[k] - xi[j]) / (xi[i] - xi[j])
            self.sf.append(n)

    def __evald(self, x, xi):
        '''Evaluate polynomial derivatives at x using interpolation points xi 
        '''
        for k in range(len(x)):
            dn = np.zeros((1, self.n))
            for i in range(self.n):
                for j in range(self.n):
                    if i != j:
                        prod = 1.0 / (xi[i] - xi[j])
                        for l in range(self.n):
                            if l != i and l != j:
                                prod *= (x[k] - xi[l]) / (xi[i] - xi[l])
                        dn[:, i] += prod
            self.dsf.append(dn)
