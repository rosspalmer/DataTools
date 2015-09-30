#DataTools

> v0.1.2

The purpose of DataTools is to create a single platform to host many Python data analytics modules (Scikit-learn, Statsmodels, etc) within a standardized structure. We want to provide the end user with ability to experiment with several analytics techniques quickly without having to spend time coding for the needs of a particular analytics module.

DataTools is also designed to automatically regulate the flow of data between the modules as well as provide compatibility with many different data platforms, such as SQL, Excel/CSV files, and pandas.

#Features

##Supported Statistical Models

- Simple/Multiple Linear - `linear`
- Logistic Regression - `logistic`
- K-Means Clustering - `kmeans`
- K-Means Classification - `knearest`

###Planned Models

- Discriminate Analysis
- Additional GLS Methods
- Weighted Regression Models
- Neural Networks
- Classification Trees
- Support Vector Machines

##Supported I/O Data Platforms

- CSV Files

###Planned I/O Platfroms

- SQL (many flavors)
- Excel Files
- JSON
- XML
- External pandas DataFrames

##Additional Planned Features

- Randomized data partitioning
- Validation testing
- Automatic categorical variable conversion
- Variable choice optimization for models

#Installation

DataTools is currently only available via a source distribution install. PyPi (pip) distributions will be added in the future.

     git clone https://github.com/rosspalmer/DataTools.git
     cd DataTools
     python setup.py install

#[Documentation](https://github.com/rosspalmer/DataTools/wiki/Documentation)

#Quick Start Guide

Most end user actions are accessed using the `manager` method. Below is a short tutorial on loading data from a CSV file, fitting a `linear` regression model on the data, and then outputing the results as a series of CSV files.

_Note: Adding Tutorial_

#External Analysis Modules

As I stated in the introduction paragraph, DataTools ultizes external Python modules for statistical modelling. Below are the modules responsible for **ALL** of the statistical modules used within DataTools.

- [**StatsModels**](http://statsmodels.sourceforge.net/0.5.0/index.html)
- [**scikit-learn**](http://scikit-learn.org/stable/)

#License

The MIT License (MIT)

Copyright (c) 2015 Ross Palmer

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
