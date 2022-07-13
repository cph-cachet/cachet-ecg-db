# CACHET-CADB ToolKit

[![github stars](https://img.shields.io/github/stars/cph-cachet/cachet-ecg-db.svg?style=flat&logo=github&colorB=deeppink&label=stars)](https://github.com/cph-cachet/cachet-ecg-db)
[![MIT License](https://img.shields.io/badge/license-MIT-purple.svg)](https://opensource.org/licenses/MIT)

This repro contains the Python scripts and other tools to access the data in the CACHET Contextualised Arrhythmia Database (CACHET-CADB)

## CACHET-CADB

CACHET-CADB is 259 days long contextualised single-channel ECG arrhythmia database from 24 patients recording under a free-living ambulatory setting. Along with the ECG, it also contains contextual information such as activities, body position, movement acceleration, patients reported unusual symptoms/events diary, step counts, patient-reported sleep quality, stress level, and food intake. I contain 1602 ten-second long ECG samples of AF, NSR, noise, and other rhythm classes, which are manually annotated by two cardiologists. The ECG is sampled at 1024 Hz and a 12-bit resolution.

The CACHET-CADB is available from DTU Data in two formats:

 * [CACHET-CADB](https://data.dtu.dk/articles/dataset/CACHET-CADB/14547264)
 * [CACHET-CADB Short Format](https://data.dtu.dk/articles/dataset/CACHET-CADB_Short_Format/14547330)



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

## Citation 

When using the CACHET-CADB dataset and code, please cite its data descriptor article : 

```
@article{kumar2022cachet,
  title={CACHET-CADB: A Contextualized Ambulatory Electrocardiography Arrhythmia Dataset},
  author={Kumar, Devender and Puthusserypady, Sadasivan and Dominguez, Helena and Sharma, Kamal and Bardram, Jakob E},
  journal={Frontiers in Cardiovascular Medicine},
  pages={1702},
  year={2022},
  publisher={Frontiers}
}
```

