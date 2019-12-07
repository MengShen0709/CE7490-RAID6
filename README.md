# CE7490 Project RAID6

CE7490 2019 Fall - Advanced Topics in Distributed System - Project 2: RAID-6 based distributed storage system

## Introduction
[RAID](https://en.wikipedia.org/wiki/RAID) (Redundant Array of Independent Disks) is developed for the demand of rising the reliability, capacity and speed of storage systems. The level of RAID6 is an extension of RAID5 by adding another parity block, which is designed to tolerate any two concurrent disk failure and maintain a relatively high storage efficiency. An example of RAID6 storage with double parity is shown below:

<p align="center">
    <img src='https://linustechtips.com/main/uploads/monthly_09_2015/post-239070-0-22015900-1441472733.gif' width="400" height="250">
</p>

## Installation Guide
The RAID-6 system is devloped in Python 3.8 environment with corresponding dependencies.

The project is supported on Linux and MacOS. It may be possible to install on Windows, though this hasn't been extensively tested.

### Installing Anaconda
Anaconda is a library that includes Python and many useful packages, as well as an environment manager called conda that makes package management simple.

Follow the [official instrutions](https://www.anaconda.com/distribution/) of Anaconda to install. Once it has been successfully installed, run the following command at terminal:

```
git clone https://github.com/GuluDeemo/CE7490-RAID6.git
cd CE7490-RAID6
conda env create -f environment.yml
```

To use Python from the environment you just created, activate the environment with

```
conda activate RAID6
```

## Running Experiments

The standard way to run the test from terminal is:

```
python test.py 
```

The original file is stored in ```./data/file```. We have provided three kinds of file (.txt, .pdf, .jpg) for recovering test. Feel free to add your preferred file type and define your RAID6 configuration at ```./src/config.py ```.

## Reference
An excellent tutorial of implementing RAID6 using Reed-Solomon coding can be found at http://www.cs.utk.edu/~plank/plank/papers/CS-96-332.html
