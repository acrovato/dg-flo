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

## Writer
# Adrien Crovato

class Writer:
    def __init__(self, name, freq, _var, disc):
        self.name = name # base name of file
        self.freq = freq # save frequency
        self.vars = _var # list of names of the variables
        self.rows = [] # list of unknown indices
        self.x = [] # list of coordinates
        for e in disc.elements.values():
            self.rows.append(e.rows)
            self.x.append(e.evalx())

    def save(self, nt, t, u):
        '''Write results to disk
        '''
        if nt % self.freq == 0:
            # Open file
            f = open(self.name + '_{0:06d}'.format(nt) + '.dat', 'w+')
            # Write header
            f.write('$Info\n')
            f.write('      Iteration            Time\n')
            f.write('{0:15d} {1:15.6f}\n'.format(nt, t))
            # Write data
            f.write('$Solution\n')
            f.write('              x')
            for v in self.vars:
                f.write(' {0:>15s}'.format(v))
            f.write('\n')
            for i in range(len(self.x)):
                for j in range(len(self.x[i])):
                    f.write('{0:15.6f}'.format(self.x[i][j]))
                    for v in range(len(self.vars)):
                        f.write(' {0:15.6f}'.format(u[self.rows[i][v][j]]))
                    f.write('\n')
            # Close file
            f.close()
