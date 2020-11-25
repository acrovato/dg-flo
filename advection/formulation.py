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

## Formulation of the advection equation in one dimension
# Adrien Crovato

class Formulation:
    '''Formulate the 1D advection equation
        du/dt + a * du/dx = 0
    '''
    def __init__(self, msh, fld, ic, bc, a):
        # Grid
        self.msh = msh # mesh
        self.field = fld # field
        self.ic = ic # initial condition
        self.bc = bc # inlet boundary condition
        # Physics
        self.a = a # advection velocity
    def __str__(self):
        return 'Advection formulation'
