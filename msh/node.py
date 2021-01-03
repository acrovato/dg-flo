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

## mesh node
# Adrien Crovato

import numpy as np

# Nodes container comparator
class EqNodes:
    def __init__(self, nodes):
        self.nods = nodes
    def __hash__(self):
        '''Assign a unique key to the object
        '''
        nsum = 0
        for n in self.nods:
            nsum += n.no
        return nsum
    def __eq__(self, other):
        '''Determine if two objects are the same
        '''
        cnt = 0
        # Compare nodes of self to nodes of other
        for i in range(len(self.nods)):
            for n1 in other.nods:
                if self.nods[i] == n1:
                    cnt += 1
                    break
            if cnt != i + 1:
                return False
        return True

# Node
class Node:
    def __init__(self, no, x):
        # Node number
        self.no = no
        # Node position
        if isinstance(x, list) and len(x) == 3: # python list
            self.x = np.array(x)
        elif isinstance(x, np.ndarray) and x.shape == (3,): # numpy array
            self.x = x
        else:
            raise RuntimeError('Node: no default constructor matches the argument list!')

    def __str__(self):
        return 'node #' + str(self.no) + ', position: ' + str(self.x)
