# ds-experiments

These are data sets from [Lakner et al 2008](http://dx.doi.org/10.1080/10635150801886156) as well as some scripts to run variational analyses.

Run analyses with

    python libsbn-scripts/benchmark_sbn_gradients.py .

This script requires MrBayes runs to execute.
Because these files are big, they are not included in the repository.

To generate the MrBayes runs, install MrBayes (available on Debian/Ubuntu via apt-get) and execute

    mb *.mb

in the data set corresponding to the analysis of interest to you.
The `_fixed` versions of the analyses have a fixed tree.




