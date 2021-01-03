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
from msh.node import EqNodes
from msh.cell import CTYPE
from msh.interface import Vertex

class Mesh:
    def __init__(self):
        self.name = 'default' # name
        self.dim = 0 # dimension
        self.nodes = [] # list of nodes
        self.cells = [] # list of cells
        self.groups = [] # list of groups
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
        msg += '- ' + str(len(self.interfaces)) + ' interfaces ( '
        for typ, cnt in ityps.items():
            msg += str(cnt) + ' ' + str(typ) + ' '
        msg += ')\n'
        msg += '- ' + str(len(self.groups)) + ' groups'
        return msg

    def topology(self):
        '''Update the mesh topology using the given nodes and cells
        '''
        # Group listing and sanity checks
        if len(self.nodes) == 0 or len(self.cells) == 0:
            raise RuntimeError('Mesh.topology cannot update topology: no nodes or cells in the mesh!')
        fldgroups = []
        bndgroups = {}
        for g in self.groups:
            if g.dim == self.dim:
                fldgroups.append(g)
            elif g.dim == self.dim-1:
                cdict = {}
                for c in g.cells:
                    cdict[EqNodes(c.nodes)] = c # dict{EqNodes : Cell}
                bndgroups[g] = cdict
            else:
                raise RuntimeError('Mesh.topology groups must have the same or one dimension less than the mesh!')
        if len(fldgroups) != 1:
            raise RuntimeError('Mesh.topology the mesh should contain only one group having the same dimension than the mesh!')
        if len(bndgroups) == 0:
            raise RuntimeError('Mesh.topology the mesh should contain at least one group having one dimension less than the mesh!')
        fldgroup = fldgroups.pop()
        # Update interfaces
        self.__interfaces(fldgroup, bndgroups)

    def __interfaces(self, fldgroup, bndgroups):
        '''Create the interfaces between all cells having the mesh dimension
        '''
        interfaces = {} # dict{EqNodes : Interface}
        if self.dim == 1:
            for c in self.cells:
                # Treat only 1D line cells
                if c.type() != CTYPE.LINE2:
                    continue
                for n in c.nodes:
                    nods = [n] # list of nodes defining the interface
                    eqnds = EqNodes(nods) # nodes container comparator
                    # get the interface if it exists...
                    try:
                        v = interfaces[eqnds]
                    # ...or create the interface if it does not
                    except:
                        v = Vertex(nods)
                        v.no = len(interfaces) + 1
                        interfaces[eqnds] = v
                        # check if the interface is a boundary cell
                        isbnd = False
                        for g, gcs in bndgroups.items():
                            if eqnds in gcs:
                                g.interfaces.append(v)
                                isbnd = True
                                break
                        if not isbnd:
                            fldgroup.interfaces.append(v)
                    # link interface and cell
                    v.neighbors.append(c)
                    c.boundaries.append(v)
        else:
            raise RuntimeError('Mesh.__interfaces not implemented for dimensions > 1!')
        self.interfaces = list(interfaces.values())
