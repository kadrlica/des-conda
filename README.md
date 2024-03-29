# des-conda

Control tools for the DES conda installation at Fermilab. More information on [conda](https://conda.io/docs/index.html).

The following instructions assume that your environment has the alias defined in [config/bashrc](config/bashrc).

## Installing Conda

ADVICE: If we were starting over, it may have been a better choice to start from a [miniconda](https://conda.io/miniconda.html) installation. This would keep the base/root environment very minimal.

Initial Anaconda installation only needs to happen once, so you proably won't need this, but just in case it is recorded for posterity.

```
> ssh -l cvmfsdes oasiscfs02.fnal.gov
> cd $DES_PATH
> cvmfs_transaction
# Check https://www.anaconda.com/download/ for the latest installer
> wget https://repo.continuum.io/archive/Anaconda3-4.4.0-Linux-x86_64.sh
> bash Anaconda2-4.4.0-Linux-x86_64.sh
> screen_publish
```

The `screen_publish` is necessary since conda makes a bunch of hardlinks that cvmfs is not happy about. To check on the status of publication
```
> screen -ls
<check for screen session name/number>
> screen -R -d <SESSION>
```

## Create a New Environment

See instructions for [managing an environment](https://conda.io/docs/using/envs.html) and [`conda create`](https://conda.io/docs/commands/conda-create.html). Assuming that you have the correct aliases from [`.bashrc`](config/bashrc)

```
> conda_setup
> cvmfs_transaction
> conda create --name <ENVNAME> <PACKAGES> | tee ~/log/<ENVNAME>.log
> screen_publish
```

In the above commands `<ENVNAME>` is the name of the environment that you want to create and `<PACKAGES>` is the list of python packages that you want to install into this environment. The conda workflow functions best when new environments are created with all their required packages rather than creating an environment and then installing packages piecemeal. To ensure this, we recommend pre-defining your environment in a yaml file. You can find several of these in the [env](env) directory. To create an environment from a yaml specification:

```
> conda_setup
> cvmfs_transaction
> conda env create -v -f <FILENAME> 2>&1 | tee ~/log/<ENVNAME>.log
> conda clean -v -y -ti
> screen_publish
```

## Install a Package in an Existing Environment

Installing a package into an existing environment (especially an environment that many people are using), can be dangerous. Before proceding, be familiar with the instructions for [managing an environment](https://conda.io/docs/using/envs.html) and [`conda install`](https://conda.io/docs/commands/conda-install.html). Our goal is first and foremost not to break anything.

```
> conda_setup
> source activate <ENVNAME>
> cvmfs_transaction
> conda install --no-update-deps --name <ENVNAME> <PACKAGE>
> screen_publish
```

## Updating conda/anaconda

From time to time we want to upgrade `conda` and `anaconda` themselves. More details on this process can be found [here](https://docs.anaconda.com/anaconda/install/update-version/) and an older thread [here](https://github.com/ContinuumIO/anaconda-issues/issues/984). I've found that it can be necessary to use `conda install` rather than `conda update`, and that it is better to update anaconda first.
```
> conda_setup
> cvmfs_transaction
> conda install -v anaconda=<VERSION>
> conda update -v conda
> screen_publish
```

There may be issues with updating the `anaconda` metapackage (i.e., unresolvable conflicts, etc.). In this case, we can update all packages, then revert to a specific Anaconda instance.
```
> conda_setup
> cvmfs_transaction
> conda update -v --all
> conda update -v conda
> screen_publish
```

## Tagging

To tag a version on cvmfs:
```
cvmfs_server tag -a des18a-1.0 -m "des18a conda environment" des.opensciencegrid.org
```
to list the tagged versions:
```
cvmfs_server tag -l des.opensciencegrid.org
```

## Cleaning Unused Packages

Conda can accumulate a lot of unused packages that fill up disk space (which cvmfs doesn't like). Packages can be cleaned up up with:
```
conda clean -v -y -ti
```

Note that we don't want to use the `--packages` option because cvmfs is breaking symlinks (see [here](https://github.com/conda/conda/issues/3308#issuecomment-244366064) and [here](https://docs.conda.io/projects/conda/en/latest/commands/clean.html)). 

## Notes

The `--no-update-deps` is important to keep from accidentally updating everything in your environment. Even so, be sure to check the lists of installs carefully before confirming the install. If you do end up accidentally updating a package that you didn't intend to, do not be shy about using `cvmfs_abort` to rollback your changes and try again.

You may run into issues with conda trying to modify packages from other channels. In theory the `--override-channels` flag should stop this, but on several occasions I've found that I need to comment out the channels in the [`.condarc`][config/condarc] file.

CVMFS complains and fails to publish if a `catalog` contains more than 500k entries. The documentation recommends creating [nested catalogs](https://twiki.cern.ch/twiki/bin/view/CvmFS/MaintainRepositories), containing between 1k and 200k entries. The easiest way to implement this was to make some of the largest packages nested catalogs:
```
for dir in $(ls -d ${DES_PATH}/fnal/anaconda2/pkgs/*/); do echo $(find $dir -type f | wc -l) $(basename $dir); done | sort -n -k1
for dir in $(\ls -d ${DES_PATH}/fnal/anaconda2/pkgs/{python,iraf,qt}-[0-9]*); do 
  touch ${dir}/.cvmfscatalog; 
done
```
It also seems reasonable to make each environment a nested catalog:
```
for dir in $(\ls -d ${DES_PATH}/fnal/anaconda2/envs/*/); do
  touch ${dir}/.cvmfscatalog; 
done
```
