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

## Mesh data structure
# Adrien Crovato

import numpy as np
import msh.cell as cell
import msh.interface as intf

class Mesh:
    def __init__(self):
        self.name = 'default' # name
        self.dim = 0 # dimension
        self.nodes = [] # list of nodes
        self.cells = [] # list of cells
        self.interfaces = [] # list of interfaces

    def __str__(self):
        msg = 'Mesh \"' + self.name + '\" with:\n'
        for n in self.nodes:
            msg += '- ' + str(n) + '\n'
        for c in self.cells:
            msg += '- ' + str(c) + '\n'
        for i in self.interfaces:
            msg += '- ' + str(i) + '\n'
        return msg

    def topology(self):
        '''Update the mesh topology using the given nodes and cells
        '''
        # Sanity checks
        if len(self.nodes) == 0 or len(self.cells) == 0:
            raise RuntimeError('Mesh.topology cannot update topology: no nodes or cells in the mesh!\n')
        # Update interfaces
        self.__interfaces()

    def __interfaces(self):
        '''Create the interfaces between all cells having the mesh dimension
           TODO consider using same function for all dimensions/types of cell
        '''
        interfaces = set() # set of interfaces, TODO consider using dict {Interface.__eq__() : Interface()}
        if self.dim == 1:
            nrm = [-1.0, 1.0]
            for c in self.cells:
                # Treat only 1D line cells
                if c.type() != cell.CTYPE.LINE2:
                    continue
                for i, n in enumerate(c.nodes):
                    trial = intf.Vertex([n])
                    # create the interface
                    if trial not in interfaces:
                        v = trial
                        v.no = len(interfaces) + 1
                        v.nrm = np.transpose(np.array([nrm[i], 0., 0.]))
                        interfaces.add(v)
                    # loop until interface is found
                    else:
                        it = iter(interfaces)
                        while True:
                            v = next(it)
                            if v == trial:
                                break
                    # link interface and cell
                    v.neighbors.append(c)
                    c.boundaries.append(v)
        else:
            raise RuntimeError('Mesh.__interfaces not implemented for dimensions > 1!\n')
        self.interfaces = list(interfaces)
