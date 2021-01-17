# dg-flo
Discontinuous Galerkin code to solve hyperbolic PDEs  
Adrien Crovato, 2021

[![Python](https://img.shields.io/badge/python-3.8-blue.svg)](https://www.python.org/downloads/release/python-386/)
[![Continuous integration](https://github.com/acrovato/dg-flo/workflows/Continuous%20integration/badge.svg)](https://github.com/acrovato/dg-flo/actions)
[![License](https://img.shields.io/badge/license-Apache_2.0-blue.svg)](https://www.apache.org/licenses/LICENSE-2.0)

## Features
dg-flo can solve one-dimensional hyperbolic partial differential equations of the form `dU/dt + dF(U)/dx + S(x) = 0`, where `U`, `F(U)` and `S(x)` are the vectors of unknowns, fluxes and sources.  
Sample problems are given under the [tests](tests/) directory for solving the
- [x] advection equation
- [x] Burger's equation
- [x] Euler's equations
- [x] shallow water equations

## Requirements
dg-flo needs a python 3 interpreter and its libraries, as well the `numpy` package. The `matplotlib` package is optional (needed to display the solution interactively).

### Linux
If you are using Linux, you can install python and the packages using Aptitude.
```bash
sudo apt-get update
sudo apt-get install python3-dev
sudo apt-get install python3--numpy python3-matplotlib
```

### Windows and MacOS
If you are using Windows or MacOS, you can install python from the installer provided on the [python's official site](https://www.python.org/downloads/) and the packages using pip.
```bash
python3 -m pip install numpy
python3 -m pip install matplotlib
```

## Usage
Run a computation by calling `python3 run.py path --gui`, where
- `path` is the (required) path to a python script or to a directory contaning several python scripts,
- `--gui` is an (optional) flag that activates the graphical user interface.

Output files will be saved in your current working directory under a `workspace` directory.

## Documentation
Coming soon...

## Credits
dg-flo contains bits of code borrowed from [waves](https://gitlab.uliege.be/am-dept/waves), and was started from [dg](https://gitlab.uliege.be/R.Boman/dg).
