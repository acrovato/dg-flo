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

## Quadrature rules
# Adrien Crovato

import numpy as np

# Base class
class Quadrature:
    def __init__(self):
        self.n = 0 # number of quadrature points
        self.x = [] # position
        self.w = [] # weight
    def __str__(self):
        return 'Quadrature rule not implemented'

# Gauss-Legendre quadrature
# from https://rosettacode.org/wiki/Numerical_integration/Gauss-Legendre_Quadrature#Python
# TODO optimize?
class GaussLegendre(Quadrature):
    def __init__(self, order):
        Quadrature.__init__(self)
        self.n = order // 2 + 1 # floor division
        self.__roots()
        self.__weights()
    def __str__(self):
        return 'Gauss-Legendre quadrature rule (n = ' + str(self.n) + ')\n'

    def __roots(self):
        '''Evaluate roots
        '''
        xs = [] # roots are symmetric, so we only compute half of them
        for i in range(1, self.n // 2 + 1):
            x = np.cos(np.pi * (i-0.25) / (self.n + 0.5))
            dx = 1.0
            its = 0
            while np.abs(dx) > 1e-16:
                dx = - self.__legendre(x, self.n) / self.__dlegendre(x, self.n)
                x += dx
                its += 1
                if its > 100:
                    print('GaussLegendre: Newton method did not converge, error =', np.abs(dx))
            xs.append(x)
        # add the rest of the roots
        for x in xs:
            self.x.append(-x)
        if np.mod(self.n, 2) != 0:
            self.x.append(0.0)
        self.x += reversed(xs)
    
    def __weights(self):
        '''Evaluate weights
        '''
        for x in self.x:
            self.w.append(2.0 / ((1.0 - x*x) * (self.__dlegendre(x, self.n)**2)))

    def __legendre(self, x, n):
        '''Evaluate Legendre polynomial of order n at x (recurrence)
        '''
        if n == 0:
            return 1.0
        elif n == 1:
            return x
        else:
            return ((2.0 * n - 1.0) * x * self.__legendre(x, n-1) - (n-1) * self.__legendre(x, n-2)) / n

    def __dlegendre(self, x, n):
        '''Evaluate Legendre polynomial derivative of order n at x (recurrence)
        '''
        if n == 0:
            return 0.0
        elif n == 1:
            return 1.0
        else:
            return n / (x*x - 1.0) * (x * self.__legendre(x, n) - self.__legendre(x, n-1))
