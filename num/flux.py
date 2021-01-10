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

## Numerical flux
# Adrien Crovato
# TODO Roe's flux (entropy consistency)
# TODO normal vector (which ref direction? where is dot product)

import numpy as np

# Base class
class NFlux:
    def __init__(self, flux):
        self.f = flux
    def __str__(self):
        raise RuntimeError('Flux not implemented!')

# Lax–Friedrichs
class LaxFried(NFlux):
    '''Lax–Friedrichs flux
    '''
    def __init__(self, flux, alpha):
        NFlux.__init__(self, flux)
        self.alpha = alpha # upwind parameter
    def __str__(self):
        return 'Lax–Friedrichs flux (alpha = ' + str(self.alpha) + ')'

    def eval(self, u0, u1, n0):
        '''Compute the flux at the interface between two cells using the physical fluxes f and the numerical fluxes nu at cell 0 and cell 1
        '''
        # Compute the maximum wave speed
        lam0, _ = np.linalg.eig(np.array(self.f.evald(u0))) # eigenvalues of flux derivative matrix
        lam1, _ = np.linalg.eig(np.array(self.f.evald(u1)))
        c = max([max(abs(lam0)), max(abs(lam1))]) # max. wave speed
        # Evaluate the numerical flux
        return 0.5 * (np.array(self.f.eval(u0)) + np.array(self.f.eval(u1))) + 0.5 * (1 - self.alpha) * c * n0 * (np.array(u0) - np.array(u1))
