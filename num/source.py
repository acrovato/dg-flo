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

## Source term
# Adrien Crovato

class Source:
    '''Source term
    '''
    def __init__(self, funs):
        self.funs = funs # list of functions(position) for each variable
    def __str__(self):
        return 'Source term'

    def eval(self, e):
        '''Evaluate the source term on the nodes an element
        '''
        x = e.evalx()
        s = [[0.] * len(x) for _ in range(len(self.funs))]
        for i in range(len(x)):
            for j in range(len(self.funs)):
                s[j][i] = self.funs[j](x[i])
        return s
