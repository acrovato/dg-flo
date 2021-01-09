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

## Physical flux
# Adrien Crovato

# Base class
class PFlux:
    def __init__(self):
        pass
    def __str__(self):
        raise RuntimeError('Physical flux not implemented!')

# Advection
class Advection(PFlux):
    '''Advection flux
    '''
    def __init__(self, a):
        PFlux.__init__(self)
        self.a = a # advection (transport) velocity
    def __str__(self):
        return 'Advection flux (a = ' + str(self.a) + ')'

    def eval(self, u):
        '''Compute the physical flux vector
            f = a*u
        '''
        return [self.a * u[0]]

    def evald(self, u):
        '''Compute the physical flux derivative matrix
            df = a
        '''
        return [[self.a]]

class Advection2(PFlux):
    '''Advection flux
    '''
    def __init__(self, a, b):
        PFlux.__init__(self)
        self.a = a # first advection (transport) velocity
        self.b = b # second advection (transport) velocity
    def __str__(self):
        return 'Advection flux (a = ' + str(self.a) + ', b = ' + str(self.b) + ')'

    def eval(self, u):
        '''Compute the physical flux vector
            f = [a*u, b*v]
        '''
        f = [0.] * len(u)
        f[0] = self.a * u[0]
        f[1] = self.b * u[1]
        return f

    def evald(self, u):
        '''Compute the physical flux derivative matrix
            df = [a, 0;
                  0, b]
        '''
        df = [[0.] * len(u) for _ in range(len(u))]
        df[0][0] = self.a
        df[1][1] = self.b
        return df

# Burger's
class Burger(PFlux):
    '''Burger's flux
    '''
    def __init__(self):
        PFlux.__init__(self)
    def __str__(self):
        return 'Burger\'s flux'

    def eval(self, u):
        '''Compute the physical flux vector
            f = u*u/2
        '''
        return [0.5 * u[0] * u[0]]

    def evald(self, u):
        '''Compute the physical flux derivative matrix
            df = u
        '''
        return [[u[0]]]

# Euler
class Euler(PFlux):
    '''Euler flux
    '''
    def __init__(self, gamma):
        PFlux.__init__(self)
        self.gamma = gamma # heat capacity ratio
    def __str__(self):
        return 'Euler flux (gamma = ' + str(self.gamma) + ')'

    def eval(self, u):
        '''Compute the physical flux vector
        f = [rho*u, rho*u^2+p, (E+p)*u]
        '''
        # Pre-pro
        u[0] = self.__clamp(u[0], 0.01) # clamp the density
        v = u[1] / u[0] # u = rho * u / rho
        p = (self.gamma - 1) * (u[2] - 0.5 * u[1] * v) # (gamma - 1) * (E - 0.5 * rho*u*u)
        # Flux
        f = [0.] * len(u)
        f[0] = u[1]
        f[1] = u[1] * v + p
        f[2] = (u[2] + p) * v
        return f

    def evald(self, u):
        '''Compute the physical flux derivative matrix
            df = [0, 1, 0;
                  (gamma-3)/2*u^2, (3-gamma)*u, gamma-1;
                  -gamma*E*u/rho + (gamma-1)*u^3, gamma*E/rho + 3*(1-gamma)/2*u^2, gamma*u]
        '''
        # Pre-pro
        u[0] = self.__clamp(u[0], 0.01) # clamp the density
        v = u[1] / u[0] # = rho * u / rho
        e = u[2] / u[0] # = E / rho
        # Flux
        df = [[0.] * len(u) for _ in range(len(u))]
        df[0][1] = 1.
        df[1][0] = 0.5 * (self.gamma - 3) * v * v
        df[1][1] = (3 - self.gamma) * v
        df[1][2] = self.gamma - 1
        df[2][0] = -self.gamma * e * v + (self.gamma - 1) * v * v * v
        df[2][1] = self.gamma * e + 1.5 * (1 - self.gamma) * v * v
        df[2][2] = self.gamma * v
        return df

    def __clamp(self, u, mn):
        '''Clamp the solution in case in becomes non-physical
        '''
        # TODO EULER
        import numpy as np
        if isinstance(u, np.ndarray):
            for i in range(len(u)):
                u[i] = max([mn, u[i]])
        else:
            u = max([mn, u])
        return u
