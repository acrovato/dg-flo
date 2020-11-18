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

def setup(fpath):
    '''Perform basic setup
    '''
    import sys, os
    # Fix paths
    sys.path.append(os.path.dirname(os.path.realpath(__file__))) # adds "." to the python path
    # check input path and create workspace directory(ies)
    files = {}
    fpath = os.path.abspath(fpath)
    if os.path.isfile(fpath):
        wdir = onedir(fpath)
        files[fpath] = wdir
    elif os.path.isdir(fpath):
        for file in os.listdir(fpath):
            file = os.path.join(fpath, file)
            wdir = onedir(file)
            files[file] = wdir
    else:
        raise Exception('file or folder not found: ', fpath)
    return files, os.getcwd()

def parse():
    '''Parse command line arguments
    '''
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('f', help='path to python script(s) to be run, can be a file or a folder')
    return parser.parse_args()

def onedir(file):
    '''Create a single workspace directory per script, if needed
    '''
    import os
    common = os.path.commonprefix((file, os.getcwd())) + os.sep
    resdir = file[len(common):].replace(os.sep,'_')
    wdir = os.path.join(os.getcwd(), 'workspace', resdir[:-3])
    if not os.path.isdir(wdir):
        print('creating', wdir)
        os.makedirs(wdir)
    return wdir

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
    import os
    # init
    args = parse()
    files, thisdir = setup(args.f)
    # run
    for file, wdir in files.items():
        print('changing to workspace: ', wdir)
        os.chdir(wdir)
        logger = Log()
        printStart()
        global __file__
        __file__ = file # so that latter calls to __file__ will reference the script referenced by file
        exec(open(file, 'r', encoding='utf8').read(), globals(), globals())
        printEnd()
        os.chdir(thisdir)
        del logger

if __name__ == "__main__":
    main()
