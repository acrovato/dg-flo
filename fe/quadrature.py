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

## Quadrature rules
# Adrien Crovato
# 1D only

import numpy as np

# Legendre
class Legendre:
    '''Legendre polynomial
    '''
    def __init__(self):
        pass

    def eval(self, x, n):
        '''Evaluate Legendre polynomial of order n at x (recurrence)
        '''
        if n == 0:
            return 1.0
        elif n == 1:
            return x
        else:
            return ((2*n - 1) * x * self.eval(x, n-1) - (n-1) * self.eval(x, n-2)) / n

    def evald(self, x, n):
        '''Evaluate Legendre polynomial first derivative of order n at x (recurrence)
        '''
        if n == 0:
            return 0.0
        elif n == 1:
            return 1.0
        else:
            return ((2*n - 1) * x * self.evald(x, n-1) - n * self.evald(x, n-2)) / (n-1)

    def evaldd(self, x, n):
        '''Evaluate Legendre polynomial second derivative of order n at x (recurrence)
        '''
        if n == 0:
            return 0.0
        elif n == 1:
            return 0.0
        elif n == 2:
            return 3.0
        else:
            return ((2*n - 1) * x * self.evaldd(x, n-1) - (n+1) * self.evaldd(x, n-2)) / (n-2)

# Base class
class Quadrature:
    def __init__(self):
        self.n = 0 # number of quadrature points
        self.x = [] # position
        self.w = [] # weight
    def __str__(self):
        raise RuntimeError('Quadrature rule not implemented!')

# Gauss-Legendre
class GaussLegendre(Quadrature):
    '''Gauss-Legendre quadrature rule
       ref https://rosettacode.org/wiki/Numerical_integration/Gauss-Legendre_Quadrature#Python
    '''
    def __init__(self, order):
        # Sanity check
        if order < 0:
            raise RuntimeError('GaussLegendre quadrature rules not defined for order less than 0!')
        Quadrature.__init__(self)
        self.n = order + 1
        # Evaluate roots and weights
        lgd = Legendre()
        self.__roots(lgd)
        self.__weights(lgd)
    def __str__(self):
        return 'Gauss-Legendre quadrature rule (n = ' + str(self.n) + ')'

    def __roots(self, lgd):
        '''Evaluate roots
        '''
        xs = [] # roots are symmetric, so we only compute half of them
        for i in range(1, self.n // 2 + 1):
            x = np.cos(np.pi * (i-0.25) / (self.n + 0.5))
            dx = 1.0
            its = 0
            while np.abs(dx) > 1e-16:
                dx = - lgd.eval(x, self.n) / lgd.evald(x, self.n)
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

    def __weights(self, lgd):
        '''Evaluate weights
        '''
        for x in self.x:
            self.w.append(2.0 / ((1.0 - x*x) * (lgd.evald(x, self.n)**2)))

# Gauss-Legendre-Lobatto
class GaussLegendreLobatto(Quadrature):
    '''Gauss-Legendre-Lobatto quadrature rule (for interpolation points)
       ref https://www.ams.org/journals/mcom/1963-17-083/S0025-5718-1963-0158540-4/S0025-5718-1963-0158540-4.pdf
    '''
    def __init__(self, order):
        # Sanity check
        if order < 1:
            raise RuntimeError('GaussLegendreLobatto quadrature rules not defined for order less than 1!')
        Quadrature.__init__(self)
        self.n = order + 1
        # Evaluate roots and weights
        lgd = Legendre()
        self.__roots(lgd)
        self.__weights(lgd)
    def __str__(self):
        return 'Gauss-Legendre-Lobatto quadrature rule (n = ' + str(self.n) + ')'

    def __roots(self, lgd):
        '''Evaluate roots
        '''
        xs = [1.0] # roots are symmetric and always include the bounds, so we only compute half of them
        for i in range(1, self.n // 2):
            x = np.cos(np.pi * i / (self.n-1))
            dx = 1.0
            its = 0
            while np.abs(dx) > 1e-16:
                dx = - lgd.evald(x, self.n-1) / lgd.evaldd(x, self.n-1)
                x += dx
                its += 1
                if its > 100:
                    print('GaussLegendreLobatto: Newton method did not converge, error =', np.abs(dx))
            xs.append(x)
        # add the rest of the roots
        for x in xs:
            self.x.append(-x)
        if np.mod(self.n, 2) != 0:
            self.x.append(0.0)
        self.x += reversed(xs)

    def __weights(self, lgd):
        '''Evaluate weights
        '''
        for x in self.x:
            self.w.append(2.0 / (self.n * (self.n-1) * (lgd.eval(x, self.n-1)**2)))
