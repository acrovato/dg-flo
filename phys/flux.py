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
        '''Compute the physical flux
        '''
        return self.a * u

    def evald(self, u):
        '''Compute the physical flux derivative
        '''
        return self.a

# Burger's
class Burger(PFlux):
    '''Burger's flux
    '''
    def __init__(self):
        PFlux.__init__(self)
    def __str__(self):
        return 'Burger\'s flux'

    def eval(self, u):
        '''Compute the physical flux
        '''
        return 0.5 * u * u

    def evald(self, u):
        '''Compute the physical flux derivative
        '''
        return u
