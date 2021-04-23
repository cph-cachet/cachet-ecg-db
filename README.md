# CACHET-CADB:  A Contextualized Ambulatory Electrocardiography Arrhythmia Dataset ToolKit

[![github stars](https://img.shields.io/github/stars/cph-cachet/carp.sensing-flutter.svg?style=flat&logo=github&colorB=deeppink&label=stars)](https://github.com/cph-cachet/cachet-ecg-db)
[![MIT License](https://img.shields.io/badge/license-MIT-purple.svg)](https://opensource.org/licenses/MIT)

Below we provide the Python scripts and other tools to use the CACHET-CADB



## Installation

Python libraries for reading Unisens file format:

```pip install git+https://github.com/Unisens/pyunisens```

Read more about [Unisens](http://unisens.org/features.html) file format for simultaneous and synchronous storage of multi-sensor data at different sample rates.
 
 ## Tool for UI based inspection of the raw file
 
 The [UnisensViewer](http://software.unisens.org/download/UnisensViewer/UnisensViewer_Setup.exe) is an application which can be used to view and browse the raw unisense files. Note that this tool is only avalable on Windows.
 
 
##  Jupiter notebook for database

We provide the [`CACHET-CADB-NoteBook.ipynb`](https://github.com/cph-cachet/cachet-ecg-db/blob/master/CACHET-CADB-NoteBook.ipynb) as an illustration on how to use the CACHET-CADB data in Python.

## Main Script for reading the annotations and the ECG 

The [`cachet-cadb_analysisMain.py`](https://github.com/cph-cachet/cachet-ecg-db/blob/master/cachet-cadb_analysisMain.py) Python script contains funtions to read the database and all the statistics.

## Features and bugs

Please read about existing issues and file new feature requests and bug reports at the [issue tracker][tracker].

[tracker]: https://github.com/cph-cachet/cachet-ecg-db/issues

## License

This software is copyright (c) [Copenhagen Center for Health Technology (CACHET)](https://www.cachet.dk/) at the [Technical University of Denmark (DTU)](https://www.dtu.dk).
This software is available 'as-is' under a [MIT license](https://github.com/cph-cachet/cachet-ecg-db/blob/master/LICENSE).
