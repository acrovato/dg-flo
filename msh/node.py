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

class Node:
    def __init__(self, no, pos):
        # Node number
        self.no = no
        # Node position
        if isinstance(pos, list) and len(pos) == 3: # python list
            self.pos = np.transpose(np.array(pos))
        elif isinstance(pos, np.ndarray) and pos.shape == (3, 1): # numpy array
            self.pos = pos
        else:
            raise RuntimeError('Node: no default constructor matches the argument list!')

    def __str__(self):
        return 'node #' + str(self.no) + ', position: ' + str(np.transpose(self.pos))
