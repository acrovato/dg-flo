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

## Gauss quadrature rules test
# Adrien Crovato
#
# Test the Gaussian quadratures for order 4 (n = 5)

import fe.quadrature as quad
import utils.testing as tst

def tables():
    '''Tabulated data for Gauss-Legendre and Gauss-Legendre-Lobatto quadrature (order 4)
    '''
    xgl = [-0.906180, -0.538469, 0.0, 0.538469, 0.906180]
    wgl = [0.236927, 0.478629, 0.568889, 0.478629, 0.236927]
    xgll = [-1.0, -0.654654, 0.0, 0.654654, 1.0]
    wgll = [0.1, 0.544444, 0.711111, 0.544444, 0.1]
    return xgl, wgl, xgll, wgll

def main():
    # Create a Gauss-Legendre and a Gauss-Legendre-Lobatto quadrature rules
    gl = quad.GaussLegendre(4)
    gll = quad.GaussLegendreLobatto(4)

    # Test the positions and weights against tabulated data
    xgl, wgl, xgll, wgll = tables()
    tests = tst.Tests()
    for i in range(5):
        tests.add(tst.Test('GL x['+str(i)+']', gl.x[i], xgl[i], 1e-6))
        tests.add(tst.Test('GL w['+str(i)+']', gl.w[i], wgl[i], 1e-6))
        tests.add(tst.Test('GLL x['+str(i)+']', gll.x[i], xgll[i], 1e-6))
        tests.add(tst.Test('GLL w['+str(i)+']', gll.w[i], wgll[i], 1e-6))
    tests.run()

if __name__=="__main__":
    main()
