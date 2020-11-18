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

## Mesh test
# Adrien Crovato
#
# Test the 1D mesh creation and reading

import utils.lmesh as lmesh

def main():
    # Create a 1D line mesh with 3 cells
    msh = lmesh.run(3)
    # Display mesh info
    print(msh)

if __name__=="__main__":
    main()
