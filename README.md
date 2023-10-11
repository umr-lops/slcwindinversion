================
slcwindinversion
================



![pypi](https://img.shields.io/pypi/v/slcwindinversion.svg "https://pypi.python.org/pypi/slcwindinversion")
![travis](https://img.shields.io/travis/agrouaze/slcwindinversion.svg "https://travis-ci.com/agrouaze/slcwindinversion")
![readthedocs](https://readthedocs.org/projects/slcwindinversion/badge/?version=latest "https://slcwindinversion.readthedocs.io/en/latest/?version=latest")
![pyup](https://pyup.io/repos/github/agrouaze/slcwindinversion/shield.svg "https://pyup.io/repos/github/agrouaze/slcwindinversion/")


Python library to generate L2A wind speed products from intermediate Sentinel-1 TOPS SLC-derived products.


* Free software: MIT license
* Documentation: https://slcwindinversion.readthedocs.io.

Installation
------------

`pip install git+https://github.com/umr-lops/slcwindinversion`

Features
--------

* `slcwindinversion -h`:

```python

usage: slcwindinversion [-h] [--verbose] [--overwrite] --inputsafe INPUTSAFE --outputdir OUTPUTDIR --version VERSION [--dev]

L2AwindspeedProduction

options:
  -h, --help            show this help message and exit
  --verbose
  --overwrite           overwrite the existing outputs [default=False]
  --inputsafe INPUTSAFE
                        safe product full path to use as input
  --outputdir OUTPUTDIR
                        directory where to store output netCDF files
  --version VERSION     set the output product version (e.g. 1.4)
  --dev                 dev mode stops the computation early

```


