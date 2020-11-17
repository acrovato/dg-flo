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

## Polynomials
# Adrien Crovato

# Base class
class Polynomial:
    def __init__(self):
        pass
    def __str__(self):
        return 'Polynomial not implemented\n'

# Legendre
class Legendre(Polynomial):
    '''Legendre polynomial
    '''
    def __init__(self):
        pass
    def __str__(self):
        return 'Legendre polynomials\n'

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
