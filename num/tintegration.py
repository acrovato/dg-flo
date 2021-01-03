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

## Time integration
# Adrien Crovato
# TODO RK45 useful (Dormand and Ppince or SSPp159, ref292)?

import time
import numpy as np

# Base class
class TimeIntegration:
    def __init__(self, discretization, gui):
        self.disc = discretization
        self.gui = gui
    def __str__(self):
        raise RuntimeError('Time Integration method not implemented!')

    def run(self, dt, tmax):
        '''Perform time integration
        '''
        # Initial condition
        print('Setting initial condition...', end='')
        self.u = np.array(self.disc.frm.ic.eval(self.disc.elements))
        print('done!')
        # Set data structure for GUI
        if self.gui:
            self.gui.set(self.disc.elements)
        # Time loop
        print('Starting time loop using', self)
        print('{0:>12s}   {1:>12s}'.format('Iter', 'Time'))
        cpu = time.perf_counter()
        t = 0.
        it = 0
        while 1:
            # display solution
            if self.gui:
                self.gui.update(self.u, t, tmax)
            # check for end of the simulation
            if t >= tmax:
                break
            # update solution
            self.u = self.step(self.u, t, dt)
            t += dt
            it += 1
            # print
            print('{0:12d}   {1:12.6f}'.format(it, t))
        cpu = time.perf_counter() - cpu
        print('Computation done! Wall-clock time=', cpu, 's')

# Backward Euler
class BEuler(TimeIntegration):
    '''Backward (explicit) Euler time integration method
        u(t+dt) = u(t) + dt * rhs(t)
    '''
    def __init__(self, discretization, gui):
        TimeIntegration.__init__(self, discretization, gui)
    def __str__(self):
        return 'Backward Euler method'

    def step(self, u, t, dt):
        '''Compute solution increment at next time step t+dt
        '''
        return u + dt * self.disc.compute(u, t)

# Runge-Kutta
class Rk4(TimeIntegration):
    '''Runge Kutta order 4
    '''
    def __init__(self, discretization, gui):
        TimeIntegration.__init__(self, discretization, gui)
    def __str__(self):
        return 'Runge-Kutta order 4 method'

    def step(self, u, t, dt):
        '''Compute solution increment at next time step t+dt
        '''
        k1 = self.disc.compute(u, t)
        v1 = u + dt/2*k1
        k2 = self.disc.compute(v1, t+dt/2)
        v2 = u + dt/2*k2
        k3 = self.disc.compute(v2, t+dt/2)
        v3 = u + dt*k3
        k4 = self.disc.compute(v3, t+dt)
        return u + dt/6* ( k1+2*k2+2*k3+k4 )
