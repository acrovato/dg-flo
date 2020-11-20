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
from msh.cell import CTYPE
from msh.interface import Vertex

class Mesh:
    def __init__(self):
        self.name = 'default' # name
        self.dim = 0 # dimension
        self.nodes = [] # list of nodes
        self.cells = [] # list of cells
        self.groups= [] # list of groups
        self.interfaces = [] # list of interfaces

    def __str__(self):
        # count cell and interface types
        ctyps = {}
        ityps = {}
        for c in self.cells:
            if c.type() not in ctyps:
                ctyps[c.type()] = 1
            else:
                ctyps[c.type()] += 1
        for i in self.interfaces:
            if i.type() not in ityps:
                ityps[i.type()] = 1
            else:
                ityps[i.type()] += 1
        # Print
        msg = 'Mesh \"' + self.name + '\" (' + str(self.dim) + 'D) with:\n'
        msg += '- ' + str(len(self.nodes)) + ' nodes\n'
        msg += '- ' + str(len(self.cells)) + ' cells ( '
        for typ, cnt in ctyps.items():
            msg += str(cnt) + ' ' + str(typ) + ' '
        msg += ')\n'
        msg += '- ' + str(len(self.interfaces)) + ' interfaces ('
        for typ, cnt in ityps.items():
            msg += str(cnt) + ' ' + str(typ) + ' '
        msg += ')\n'
        msg += '- ' + str(len(self.groups)) + ' groups'
        return msg

    def topology(self):
        '''Update the mesh topology using the given nodes and cells
        '''
        # Sanity checks
        if len(self.nodes) == 0 or len(self.cells) == 0:
            raise RuntimeError('Mesh.topology cannot update topology: no nodes or cells in the mesh!')
        # Update interfaces
        self.__interfaces()
        # Update groups
        cnt = 0
        for g in self.groups:
            if g.dim == self.dim:
                cnt += 1
            g.update(self)
        if cnt != 1:
            raise RuntimeError('Mesh.topology the mesh should contain only one group having the same dimension as the mesh!')

    def __interfaces(self):
        '''Create the interfaces between all cells having the mesh dimension
           TODO consider using same function for all dimensions/types of cell
        '''
        interfaces = set() # set of interfaces, TODO consider using dict {Interface.__eq__() : Interface()}
        if self.dim == 1:
            nrm = [-1.0, 1.0]
            for c in self.cells:
                # Treat only 1D line cells
                if c.type() != CTYPE.LINE2:
                    continue
                for i, n in enumerate(c.nodes):
                    trial = Vertex([n])
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
            raise RuntimeError('Mesh.__interfaces not implemented for dimensions > 1!')
        self.interfaces = list(interfaces)
