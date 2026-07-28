# Valley Proc

**Valley Proc** is a module for processing electron density profiles from the **Valley Long Pulse** mode at the Jicamarca Radio Observatory.

The repository contains both the preprocessing example and the post-processing routines required to estimate electron density profiles from Valley experiments.

## Repository structure

### Post-processing

The main processing pipeline is implemented in:

* **`main.py`**: Main script that performs the density estimation and post-processing.
* **`hdf5read.py`**: Utilities for reading the input HDF5 files.
* **`utils.py`** and **`write_utils.py`**: Helper functions used throughout the processing pipeline.

### Magnetic field model

* **`mkfact_short_2020_2.cpython-36m-x86_64-linux-gnu.so`** is the compiled C module used to compute the geomagnetic field correction required during the density estimation. It is configured for the Valley experiment geometry.

## Pre-processing example

The file

* **`Valley_2025_08_Long_Faraday_Rotation_15_pair45.py`**

provides an example of the preprocessing performed on a Valley experiment. It generates the HDF5 file that serves as the input to `main.py`.

## Example results

The notebook

* **`Valley_Fullcampaign.ipynb`**

contains examples of the resulting electron density profiles together with visualization routines.

If unexpected or nonphysical results are obtained, the first diagnostic should be to inspect the **phase continuity** of the processed data, as discontinuities in the phase can significantly affect the density estimation.

## Workflow

1. Run the Valley preprocessing module (example provided in `Valley_2025_08_Long_Faraday_Rotation_15_pair45.py`) to generate the input HDF5 file.
2. Execute `main.py` to estimate the electron density profiles.
3. Use `Valley_Fullcampaign.ipynb` to visualize and analyze the results.
