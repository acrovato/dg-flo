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

## Flux
# Adrien Crovato

# Base class
class Flux:
    def __init__(self):
        pass
    def __str__(self):
        raise RuntimeError('Flux not implemented!')

# Lax–Friedrichs
class LaxFried(Flux):
    '''Lax–Friedrichs flux
    '''
    def __init__(self, alpha):
        Flux.__init__(self)
        self.alpha = alpha # upwind parameter
    def __str__(self):
        return 'Lax–Friedrichs flux (alpha = ' + str(self.alpha) + ')'

    def eval(self, f0, f1, c, nu0, nu1):
        '''Compute the flux at the interface between two cells using the physical fluxes f and the numerical fluxes nu at cell 0 and cell 1
        '''
        return 0.5 * (f0 + f1) + 0.5 * (1 - self.alpha) * c * (nu0 + nu1)
