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

## Colors
# Adrien Crovato

def red(_str):
    return '\x1b[1;31m' + _str + '\x1b[0m'

def green(_str):
    return '\x1b[1;32m' + _str + '\x1b[0m'

def yellow(_str):
    return '\x1b[1;33m' + _str + '\x1b[0m'

def blue(_str):
    return '\x1b[1;34m' + _str + '\x1b[0m'
