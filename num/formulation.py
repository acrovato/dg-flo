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

## Formulation of a physical problem
# Adrien Crovato

class Formulation:
    '''Formulate a given physics
    '''
    def __init__(self, msh, fld, nv, flux, ic, bcs):
        # Grid and groups
        self.msh = msh # mesh
        self.field = fld # field
        # Physics
        self.nv = nv # number of variables (physical unknowns)
        self.flux = flux # flux
        # Conditions
        self.ic = ic # initial condition
        self.bcs = bcs # list of boundary conditions
    def __str__(self):
        return 'Formulation'
