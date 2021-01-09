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

## Lagrange shape functions test
# Adrien Crovato
#
# Test the Lagrange shape functions for order p (n = p+1)

import numpy as np
import fe.quadrature as quad
import fe.shapes as shp
import utils.testing as tst
from run import parse

def main():
    # Create evaluation and interpolation points
    p = 4 # order
    x = np.linspace(-1,1,100)
    xi = quad.GaussLegendreLobatto(p).x
    # Create shape functions
    shape = shp.Lagrange(x, xi)
    print(shape)
    # Store and plot
    if parse().gui:
        import matplotlib.pyplot as plt
        l = np.zeros((shape.n, len(x)))
        dl = np.zeros((shape.n, len(x)))
        for k in range(len(x)):
            l[:, k] = np.transpose(shape.sf[k])
            dl[:, k] = shape.dsf[k]
        plt.figure(1)
        for i in range(shape.n):
            plt.plot(x, l[i, :])
            plt.plot(xi[i], 0, 'ko')
        plt.xlabel('x')
        plt.ylabel('N_i')
        plt.title('Shape functions of order {:d}'.format(p))
        plt.figure(2)
        for i in range(shape.n):
            plt.plot(x, dl[i, :])
            plt.plot(xi[i], 0, 'ko')
        plt.xlabel('x')
        plt.ylabel('dN_i/dx')
        plt.title('Shape function derivatives of order {:d}'.format(p))
        plt.show()

if __name__=="__main__":
    main()
