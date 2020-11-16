#!/usr/bin/env python3
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

## @package dg-flo
#  Discontinuous Galerkin code to solve flow equations
#  Adrien Crovato

class Log:
    '''Write data to console and to log file
    '''
    def __init__(self):
        import sys
        self.file = open('log', 'w')
        self.stdoutbak = sys.stdout
        self.stderrbak = sys.stderr
        sys.stdout = DupStream(sys.stdout, self.file)
        sys.stderr = DupStream(sys.stderr, self.file)
    def __del__(self):
        import sys
        sys.stdout = self.stdoutbak
        sys.stderr = self.stderrbak
        self.file.close()

class DupStream:
    '''Duplicate stream
    '''
    def __init__(self, stream1, stream2):
        self.stream1 = stream1
        self.stream2 = stream2
    def write(self, data):
        self.stream1.write(data)
        self.stream2.write(data)
    def flush(self):
        self.stream1.flush()
        self.stream2.flush()

def setup():
    '''Perform basic setup
    '''
    import sys, os, argparse
    # Parse cl arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('file', help='path to python script to be run')
    args = parser.parse_args()
    # Fix paths
    sys.path.append(os.path.dirname(os.path.realpath(__file__))) # adds "." to the python path
    # check input filepath
    fpath = os.path.abspath(args.file)
    if not os.path.isfile(fpath):
        raise Exception('file not found: ', fpath)
    # create workspace directory
    wdir = os.path.join(os.getcwd(), 'workspace', os.path.basename(os.path.realpath(fpath))[:-3])
    if not os.path.isdir(wdir):
        print('creating', wdir)
        os.makedirs(wdir)
    print('changing to workspace: ', wdir)
    os.chdir(wdir)
    return fpath
    
def recStart():
    import sys
    sys.stdout = open("stdout.txt", "w")
    sys.stderr = open("stderr.txt", "w")

def recStop():
    import sys
    sys.stdout.close()
    sys.stderr.close()

def printStart():
    import time, socket
    print('*' * 80)
    print('* dg-flo')
    print('* Adrien Crovato, 2020')
    print('* Distributed under Apache license 2.0')
    print('*' * 80)
    print('* Time:', time.strftime('%c'))
    print('* Host:', socket.gethostname())
    print('*' * 80)
    
def printEnd():
    print('*' * 80)
    print('* Done!')
    print('*' * 80)

def main():
    # start
    fpath = setup()
    logger = Log()
    printStart()
    # run
    global __file__
    __file__ = fpath # so that latter calls to __file__ will reference the script referenced by fpath
    exec(open(fpath, 'r', encoding='utf8').read(), globals(), globals())
    # end
    printEnd()

if __name__ == "__main__":
    main()
