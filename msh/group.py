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

## Group of elements in a mesh
# Adrien Crovato

class Group:
    def __init__(self, name, dim):
        self.name = name # name
        self.dim = dim # dimension
        self.cells = [] # list of cells
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
        msg = 'Group \"' + self.name + '\"(' + str(self.dim) + 'D) with:\n'
        msg += '- ' + str(len(self.cells)) + ' cells ( '
        for typ, cnt in ctyps.items():
            msg += str(cnt) + ' ' + str(typ) + ' '
        msg += ')\n'
        msg += '- ' + str(len(self.interfaces)) + ' interfaces ( '
        for typ, cnt in ityps.items():
            msg += str(cnt) + ' ' + str(typ) + ' '
        msg += ')'
        return msg
