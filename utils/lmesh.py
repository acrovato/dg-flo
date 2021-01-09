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

## 1D line mesh generator
# Adrien Crovato

import msh.mesh as mesh
import msh.node as node
import msh.cell as cell
import msh.group as group

def run(l, n):
    '''Create a 1D (line) domain of length l and divide it in n cells
    '''
    # Create nodes and elements
    print('Creating 1D line mesh...', end='')
    nods = []
    cels = []
    for i in range(n+1):
        nods.append(node.Node(i+1, [i*l/n, 0, 0]))
    cels.append(cell.Point(1, [nods[0]]))
    cels.append(cell.Point(2, [nods[-1]]))
    for i in range(n):
        cels.append(cell.Line(i+3, [nods[i], nods[i+1]]))
    # Create groups
    fld = group.Group('field', 1)
    fld.cells = cels[-n:]
    inl = group.Group('inlet', 0)
    inl.cells = [cels[0]]
    oul = group.Group('outlet', 0)
    oul.cells = [cels[1]]
    # Create the mesh
    msh = mesh.Mesh()
    msh.name = '1dline'
    msh.dim = 1
    msh.nodes = nods
    msh.cells = cels
    msh.groups = [fld, inl, oul]
    msh.topology() # create the mesh topology
    print(' done!')
    return msh
