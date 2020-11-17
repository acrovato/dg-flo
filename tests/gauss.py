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

## Gauss-Legendre quadrature test
# Adrien Crovato
#
# Test the Gauss-Legendre quadrature for order 4 (n = 5)

import fe.quadrature as quad

def main():
    # Create a Gauss-Legendre quadrature rule
    gl = quad.GaussLegendre(4)
    print(gl)
    # Check roots and weights
    print(gl.x)
    print(gl.w)
    
    # Create a Gauss-Legendre-Lobatto quadrature rule
    gll = quad.GaussLegendreLobatto(4)
    print(gll)
    # Check roots and weights
    print(gll.x)
    print(gll.w)

if __name__=="__main__":
    main()
