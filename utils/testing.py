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

## Testing utilities
# Adrien Crovato

import utils.coloring as clr

class Test:
    def __init__(self, name, val, expected, maxdiff=1e-10, refval=0.0, forceabs=False):
        self.name     = name                  # name of the test
        self.val      = float(val)            # calculated value
        self.expected = float(expected)       # expected value
        self.maxdiff  = abs(float(maxdiff))   # tolerance on max difference
        self.refval   = abs(float(refval))    # optional value used as denominator
                                              #   if the expected one is close to 0
        self.forceabs = forceabs              # force the calculation of an absolute diff

    def run(self):
        ok = True
        adiff = abs(self.val-self.expected) # absolute diff

        # the ref value is the largest among the expected value and
        # the one provided by the user
        denom = max(abs(self.refval), abs(self.expected))

        if not self.forceabs and denom>self.maxdiff:
            diff = adiff / denom # relative diff
            typ='rel'
            percent = '{:3.1f}%'.format(self.maxdiff*100)
        else:
            diff = adiff # absolute diff
            typ='abs'
            percent = '{:f}'.format(self.maxdiff)

        print('[{:s}] {:s} = {:f} (expected {:f} +/- {:s})'.format(clr.blue('Test'), self.name, self.val, self.expected, percent))

        if diff<=self.maxdiff:
            sgn = '<='
            info = clr.green('ok')
        else:
            sgn = '>'
            ok = False
            info = clr.red('wrong')
        print('\t{:s} diff = {:.5e} {:s} {:.5e} [{:s}]'.format(typ, diff, sgn, self.maxdiff, info))
        return ok

class Tests:
    def __init__(self):
        self.tests = []
    def add(self, t):
        self.tests.append(t)
    def run(self):
        ok = True
        for t in self.tests:
            ok = t.run() and ok

        if ok:
            print(clr.green('All tests are OK!'))
        else:
            raise Exception(clr.red('Some tests failed!'))
