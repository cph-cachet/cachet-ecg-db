import errno
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.pyplot import plot, show, title
# import ecg_plot
# from biosppy.signals import ecg
import unisens
import pandas as pd
import os
import numpy as np
from unisens import SignalEntry, EventEntry
import datetime
from datetime import datetime, timedelta
import time
from time import mktime
from unisens import CustomAttributes
import os
from distutils.dir_util import copy_tree


def __init__(self, **kwargs):
    super().__init__(**kwargs)


# dir = "/Users\\deku\\Desktop\\unisens_data"

def trimUnisensdata(dataDir, outputDir, segment_length_in_hours):
    # List of directory

    listOfDir = os.listdir(dataDir)

    print(listOfDir)
    # listOfDir= listOfDir.remove(".DS_Store")

    if '.DS_Store' in listOfDir:
        listOfDir.remove('.DS_Store')

    print(listOfDir)
    print(listOfDir)
    for dir in listOfDir:
        print("Processing ---" + dir)
        listOfInnerDir = os.listdir(dataDir + dir + "\\")
        if '.DS_Store' in listOfInnerDir:
            listOfInnerDir.remove('.DS_Store')

        for inner_dir in listOfInnerDir:
            unisens_input_dir = dataDir + dir + "\\" + inner_dir + "\\"
            u = unisens.Unisens(unisens_input_dir, readonly=True)

            print(u)

            customAttributes = u.entries['customAttributes']

            print(u)
            total_duration = int(float(u.duration))  # in Sec
            ecg_signal = u['ecg.bin']
            ecg_data = ecg_signal.get_data()
            ecg_data = ecg_data[0]
            print(ecg_data.dtype)
            print(ecg_data[0:15])
            ecg_data = np.array(ecg_data/0.0026858184230029595, dtype=np.int16)
            print(ecg_data.dtype)
            fs = 1024
            startTimestamp = u.timestampStart
            start_index = 0

            record = 1
            measurementId = u.measurementId
            u
            fs_marker = 64
            # accelerometer sampling freq
            fs_acc = 64
            acc = u['acc.bin']
            acc_data = acc.get_data()
            acc_data = np.array(acc_data / 0.00048828125, dtype=np.int16)



            # angularRate
            fs_angultar_rate = 64
            angultar_rate = u['angularrate.bin']
            angultar_rate = angultar_rate.get_data()

            angultar_rate = np.array(angultar_rate/0.07000000066757203, dtype=np.int16)

            # presser
            fs_presser_rate = 8
            press = u['press.bin']
            press = press.get_data()
            press = press[0]

            press = np.array(press/0.125, dtype=np.int32)

            # movementAcceleration
            fs_movementAcceleration = .016666666666666666
            movementAcceleration = u['movementacceleration_live.bin']
            movementAcceleration = movementAcceleration.get_data()
            movementAcceleration = movementAcceleration[0]

            movementAcceleration = np.array(movementAcceleration/0.00390625, dtype=np.int16)

            # Hr
            fs_hr = .016666666666666666
            hr_live = u['hr_live.bin']
            hr_live = hr_live.get_data()
            hr_live = hr_live[0]
            hr_live = np.array(hr_live, dtype=np.int16)

            # hrv
            fs_hrv = .016666666666666666
            hrv_live = u['hrvrmssd_live.bin']
            hrv_live = hrv_live.get_data()
            hrv_live = hrv_live[0]
            hrv_live = np.array(hrv_live, dtype=np.int16)

            # Marker
            isMarkerPresent=1
            try:
             marker_csv = u['marker.csv']
             fs_marker = 64
            except:
                isMarkerPresent=0
                print("Tap maker doesnt exists")



            time_str = u.timestampStart
            date_object = datetime.strptime(time_str, '%Y-%m-%dT%H:%M:%S.%f')
            time_object = datetime.strptime(time_str, '%Y-%m-%dT%H:%M:%S.%f').time()
            new_date_from_midnight = date_object.replace(microsecond=0) + timedelta(hours=24 - time_object.hour - 1,
                                                                                    minutes=60 - time_object.minute - 1,
                                                                                    seconds=60 - time_object.second,
                                                                                    )

            duration_of_first_record_tillmidnight = int(
                (new_date_from_midnight - date_object.replace(microsecond=0)).total_seconds())

            recordName = inner_dir  # u.get_attrib('measurementId')
            # root_dir = "\\Users\\deku\\Desktop\\unisens_data\\"
            root_dir = outputDir + dir + "\\"
            # create new directory for each subject and place sliced records in each
            if not os.path.exists(root_dir + recordName):
                print(root_dir + recordName)
                mkdir_path = Path(root_dir + recordName)
                mkdir_path.mkdir(parents=True, exist_ok=True)
                record_dir = root_dir + recordName

                location = record_dir + "\\" + "0"

                window_length = duration_of_first_record_tillmidnight  # one Day
                fixed_windod_lenght = duration_of_first_record_tillmidnight  # One Day

            if (total_duration > duration_of_first_record_tillmidnight):

                print("Do Something")

                tempstr = str(new_date_from_midnight).split(" ")
                new_time = tempstr[0] + "T" + tempstr[1]
                new_time.split(".")
                new_start_time = new_time.split(".")[0] + ".000"

                newUnisens = unisens.Unisens(location, duration=fixed_windod_lenght,
                                             timestampStart=str(startTimestamp),
                                             measurementId=measurementId, makenew=True, autosave=True,
                                             readonly=False)

                custom = CustomAttributes()
                custom.set_attrib('sensorLocation', customAttributes.sensorLocation)
                custom.set_attrib('gender', customAttributes.gender)
                custom.set_attrib('sensorVersion', '1.12.8')

                custom.set_attrib('sensorType', 'EcgMove4')
                custom.set_attrib('weight', customAttributes.weight)
                custom.set_attrib('age', customAttributes.age)
                custom.set_attrib('height', customAttributes.height)
                custom.set_attrib('personId', measurementId)
                newUnisens.add_entry(custom)

                ecg_entry = SignalEntry(id='ecg.bin')
                # parent=u makes sure the signal is added to this Unisens object
                # saving the data to eeg.bin
                newUnisens.add_entry(ecg_entry)
                print("********record******" + str(record))
                print(ecg_data[start_index * fs:fs * window_length])
                ecg_entry.set_data(ecg_data[start_index * fs:fs * window_length], sampleRate=fs,
                                   contentClass='ecg',
                                   ch_names=['ECG I'], dataType="int16", unit="mV",
                                   lsbValue="0.0026858184230029595",
                                   adcResolution="16", baseline="2048")

                # Acc entry
                acc_entry = SignalEntry(id='acc.bin')
                newUnisens.add_entry(acc_entry)
                x_acc = acc_data[0][start_index * fs_acc:fs_acc * window_length]
                y_acc = acc_data[1][start_index * fs_acc:fs_acc * window_length]
                z_acc = acc_data[2][start_index * fs_acc:fs_acc * window_length]
                acc_signal = np.array([x_acc, y_acc, z_acc])
                acc_entry.set_data(acc_signal, sampleRate=fs_acc, contentClass='acc', unit='g',
                                   lsbValue="0.00048828125",
                                   adcResolution="16", dataType="int16", comment="acc",
                                   ch_names=['accX', 'accY', 'accZ'])

                # Angultar_rate

                angultar_rate_entry = SignalEntry(id='angularrate.bin')
                newUnisens.add_entry(angultar_rate_entry)
                x_angultar_rate = angultar_rate[0][
                                  start_index * fs_angultar_rate:fs_angultar_rate * window_length]
                y_angultar_rate = angultar_rate[1][
                                  start_index * fs_angultar_rate:fs_angultar_rate * window_length]
                z_angultar_rate = angultar_rate[2][
                                  start_index * fs_angultar_rate:fs_angultar_rate * window_length]
                angultar_rate_signal = np.array([x_angultar_rate, y_angultar_rate, z_angultar_rate])
                angultar_rate_entry.set_data(angultar_rate_signal, sampleRate=fs_angultar_rate,
                                             contentClass='angularRate',
                                             unit='dps', dataType="int16",
                                             lsbValue="0.07000000066757203", adcResolution="16",
                                             comment="angularRate",
                                             ch_names=['angularRateX', 'angularRateY', 'angularRateZ'])

                # press

                press_entry = SignalEntry(id='press.bin')
                newUnisens.add_entry(press_entry)
                press_signal = press[start_index * 8:8 * window_length]
                press_entry.set_data(press_signal, adcResolution="32", ch_names=['press'], comment="press",
                                     contentClass="press",
                                     dataType="int32", id="press.bin", lsbValue="0.125", sampleRate="8",
                                     unit="Pa")

                # movementAcceleration
                movementAcceleration_entry = SignalEntry(id='movementacceleration_live.bin')
                newUnisens.add_entry(movementAcceleration_entry)
                movementAcceleration_signal = movementAcceleration[
                                              int(start_index * fs_movementAcceleration):int(
                                                  fs_movementAcceleration * window_length)]
                movementAcceleration_entry.set_data(movementAcceleration_signal, adcResolution="16",
                                                    comment="movementAcceleration_live",
                                                    ch_names=['movementAcceleration'],
                                                    contentClass="movementAcceleration_live",
                                                    dataType="int16",
                                                    id="movementacceleration_live.bin", lsbValue="0.00390625",
                                                    sampleRate="0.016666666666666666", unit="g")
                # hr
                hr_live_entry = SignalEntry(id='hr_live.bin')
                # parent=u makes sure the signal is added to this Unisens object
                # saving the data to eeg.bin
                newUnisens.add_entry(hr_live_entry)
                # print("********record******" + str(record))
                # print(ecg_data[start_index * fs:fs * window_length])
                hr_live_entry.set_data(
                    hr_live[int(start_index * .0166666666): int(.016666666666666666 * window_length)],

                    adcResolution="16",
                    ch_names=['hr'],
                    comment="hr_live",
                    contentClass="hr_live",
                    dataType="int16",
                    id="hr_live.bin",
                    lsbValue="1",
                    sampleRate="0.016666666666666666",
                    unit="1/min")

                # HRV

                hrvrmssd_live_entry = SignalEntry(id='hrvrmssd_live.bin')
                # parent=u makes sure the signal is added to this Unisens object
                # saving the data to eeg.bin
                newUnisens.add_entry(hrvrmssd_live_entry)
                # print("********record******" + str(record))
                # print(ecg_data[start_index * fs:fs * window_length])
                hrvrmssd_live_entry.set_data(
                    hrv_live[int(start_index * .16): int(.016666666666666666 * window_length)],

                    adcResolution="16",
                    comment="hrvRmssd_live",
                    ch_names=['hrvRmssd'],
                    contentClass="hrvRmssd_live",
                    dataType="int16",
                    id="hrvrmssd_live.bin",
                    lsbValue="1",
                    sampleRate="0.016666666666666666",
                    unit="ms")

                 # Marker
                if isMarkerPresent==1:
                    maker_values = []
                    for value in marker_csv.get_data():

                        if (fs_marker * start_index < value[0] <= fs_marker * window_length):
                            new_value = value[0] - fs_marker * start_index
                            maker_values.append(new_value)

                    if (len(maker_values) > 0):
                        with open(location + "\\" + "marker.csv", 'a') as f:
                            # print(length)
                            df = pd.DataFrame()
                            df['marker'] = maker_values

                            df.to_csv(f, header=None, index=False)
                        f.close()



                newUnisens.save()  # will update the unisens.xml
                # Move index
                startTimestamp = new_start_time
                start_index = int(duration_of_first_record_tillmidnight)
            else:
                print("copy it as it is ")
                location = record_dir + "\\" + "0"
                toDirectory = location

                copy_tree(unisens_input_dir, toDirectory)

                break
            # ***************************Remining record****************************

            window_length = int(3600 * segment_length_in_hours)  # one Day

            fixed_windod_lenght = int(3600 * segment_length_in_hours)  # One Day

            remaining_duration = total_duration - duration_of_first_record_tillmidnight
            number_of_record = remaining_duration / window_length
            remaining_record = remaining_duration % window_length
            # record = 2
            recordName = inner_dir  # u.get_attrib('measurementId')
            # root_dir = "/Users\\deku\\Desktop\\unisens_data\\"
            root_dir = outputDir + dir + "\\"
            # create new directory for each subject and place sliced records in each
            if not os.path.exists(root_dir + recordName):
                print(root_dir + recordName)
                mkdir_path = Path(root_dir + recordName)
                mkdir_path.mkdir(parents=True, exist_ok=True)
                record_dir = root_dir + recordName

            window_length = window_length + duration_of_first_record_tillmidnight
            while record <= number_of_record:
                # print(record_dir + str(record))
                if not os.path.exists(record_dir + "\\" + str(record)):
                    print(record_dir + "\\" + str(record))
                    location = record_dir + "\\" + str(record)
                    os.mkdir(location)
                    print("Directory ", record, " Created ")
                    # Create new unisens file
                    newUnisens = unisens.Unisens(location, duration=fixed_windod_lenght,
                                                 timestampStart=str(startTimestamp),
                                                 measurementId=measurementId, makenew=True, autosave=True,
                                                 readonly=False)

                    custom = CustomAttributes()
                    custom.set_attrib('sensorLocation', customAttributes.sensorLocation)
                    custom.set_attrib('gender', customAttributes.gender)
                    custom.set_attrib('sensorVersion', '1.12.8')

                    custom.set_attrib('sensorType', 'EcgMove4')
                    custom.set_attrib('weight', customAttributes.weight)
                    custom.set_attrib('age', customAttributes.age)
                    custom.set_attrib('height', customAttributes.height)
                    custom.set_attrib('personId', measurementId)
                    newUnisens.add_entry(custom)

                    ecg_entry = SignalEntry(id='ecg.bin')
                    # parent=u makes sure the signal is added to this Unisens object
                    # saving the data to eeg.bin
                    newUnisens.add_entry(ecg_entry)
                    print("********record******" + str(record))
                    print(ecg_data[start_index * fs:fs * window_length])
                    ecg_entry.set_data(ecg_data[start_index * fs:fs * window_length], sampleRate=fs,
                                       contentClass='ecg',
                                       ch_names=['ECG I'], dataType="int16", unit="mV",
                                       lsbValue="0.0026858184230029595",
                                       adcResolution="16", baseline="2048")

                    # Acc entry
                    acc_entry = SignalEntry(id='acc.bin')
                    newUnisens.add_entry(acc_entry)
                    x_acc = acc_data[0][start_index * fs_acc:fs_acc * window_length]
                    y_acc = acc_data[1][start_index * fs_acc:fs_acc * window_length]
                    z_acc = acc_data[2][start_index * fs_acc:fs_acc * window_length]
                    acc_signal = np.array([x_acc, y_acc, z_acc])
                    acc_entry.set_data(acc_signal, sampleRate=fs_acc, contentClass='acc', unit='g',
                                       lsbValue="0.00048828125",
                                       adcResolution="16", dataType="int16", comment="acc",
                                       ch_names=['accX', 'accY', 'accZ'])

                    # Angultar_rate

                    angultar_rate_entry = SignalEntry(id='angularrate.bin')
                    newUnisens.add_entry(angultar_rate_entry)
                    x_angultar_rate = angultar_rate[0][
                                      start_index * fs_angultar_rate:fs_angultar_rate * window_length]
                    y_angultar_rate = angultar_rate[1][
                                      start_index * fs_angultar_rate:fs_angultar_rate * window_length]
                    z_angultar_rate = angultar_rate[2][
                                      start_index * fs_angultar_rate:fs_angultar_rate * window_length]
                    angultar_rate_signal = np.array([x_angultar_rate, y_angultar_rate, z_angultar_rate])
                    angultar_rate_entry.set_data(angultar_rate_signal, sampleRate=fs_angultar_rate,
                                                 contentClass='angularRate',
                                                 unit='dps', dataType="int16",
                                                 lsbValue="0.07000000066757203", adcResolution="16",
                                                 comment="angularRate",
                                                 ch_names=['angularRateX', 'angularRateY', 'angularRateZ'])

                    # press

                    press_entry = SignalEntry(id='press.bin')
                    newUnisens.add_entry(press_entry)
                    press_signal = press[start_index * 8:8 * window_length]
                    press_entry.set_data(press_signal, adcResolution="32", ch_names=['press'], comment="press",
                                         contentClass="press",
                                         dataType="int32", id="press.bin", lsbValue="0.125", sampleRate="8",
                                         unit="Pa")

                    # movementAcceleration
                    movementAcceleration_entry = SignalEntry(id='movementacceleration_live.bin')
                    newUnisens.add_entry(movementAcceleration_entry)
                    movementAcceleration_signal = movementAcceleration[
                                                  int(start_index * fs_movementAcceleration):int(
                                                      fs_movementAcceleration * window_length)]
                    movementAcceleration_entry.set_data(movementAcceleration_signal, adcResolution="16",
                                                        comment="movementAcceleration_live",
                                                        ch_names=['movementAcceleration'],
                                                        contentClass="movementAcceleration_live",
                                                        dataType="int16",
                                                        id="movementacceleration_live.bin", lsbValue="0.00390625",
                                                        sampleRate="0.016666666666666666", unit="g")
                    # hr
                    hr_live_entry = SignalEntry(id='hr_live.bin')
                    # parent=u makes sure the signal is added to this Unisens object
                    # saving the data to eeg.bin
                    newUnisens.add_entry(hr_live_entry)
                    print("********record******" + str(record))
                    # print(ecg_data[start_index * fs:fs * window_length])
                    hr_live_entry.set_data(
                        hr_live[int(start_index * .0166666666): int(.016666666666666666 * window_length)],

                        adcResolution="16",
                        ch_names=['hr'],
                        comment="hr_live",
                        contentClass="hr_live",
                        dataType="int16",
                        id="hr_live.bin",
                        lsbValue="1",
                        sampleRate="0.016666666666666666",
                        unit="1/min")

                    # HRV

                    hrvrmssd_live_entry = SignalEntry(id='hrvrmssd_live.bin')
                    # parent=u makes sure the signal is added to this Unisens object
                    # saving the data to eeg.bin
                    newUnisens.add_entry(hrvrmssd_live_entry)
                    print("********record******" + str(record))
                    # print(ecg_data[start_index * fs:fs * window_length])
                    hrvrmssd_live_entry.set_data(
                        hrv_live[int(start_index * .016666666666666666): int(.016666666666666666 * window_length)],

                        adcResolution="16",
                        comment="hrvRmssd_live",
                        ch_names=['hrvRmssd'],
                        contentClass="hrvRmssd_live",
                        dataType="int16",
                        id="hrvrmssd_live.bin",
                        lsbValue="1",
                        sampleRate="0.016666666666666666",
                        unit="ms")

                    # Marker
                    if isMarkerPresent == 1:
                        maker_values = []
                        for value in marker_csv.get_data():

                            if (fs_marker * start_index < value[0] <= fs_marker * window_length):
                                new_value = value[0] - fs_marker * start_index
                                maker_values.append(new_value)

                        if (len(maker_values) > 0):
                            with open(location + "\\" + "marker.csv", 'a') as f:
                                # print(length)
                                df = pd.DataFrame()
                                df['marker'] = maker_values

                                df.to_csv(f, header=None, index=False)
                            f.close()


                    newUnisens.save()  # will update the unisens.xml

                    # record =record+1
                else:
                    print("Directory ", record, " already exists")
                record = record + 1
                start_index = window_length + 1
                window_length = window_length + fixed_windod_lenght
                # startTimestamp=startTimestamp+window_length
                t = datetime.strptime(startTimestamp, '%Y-%m-%dT%H:%M:%S.%f')
                unix_secs = mktime(t.timetuple())
                startTimestamp = (datetime.fromtimestamp(unix_secs + fixed_windod_lenght)).strftime(
                    '%Y-%m-%dT%H:%M:%S.%f')[
                                 :-3]

            print("Done " + str(record))

            ##Last record
            recode = record + 1
            location = record_dir + "\\" + str(record)

            newUnisens = unisens.Unisens(location + "-last", duration=remaining_record,
                                         timestampStart=str(startTimestamp),
                                         measurementId=measurementId, makenew=True, autosave=True, readonly=False)
            signal_window = ecg_data[start_index * fs:fs * total_duration - 1]

            custom = CustomAttributes()
            custom.set_attrib('sensorLocation', customAttributes.sensorLocation)
            custom.set_attrib('gender', customAttributes.gender)
            custom.set_attrib('sensorType', 'EcgMove4')
            custom.set_attrib('weight', customAttributes.weight)
            custom.set_attrib('age', customAttributes.age)
            custom.set_attrib('height', customAttributes.height)
            custom.set_attrib('personId', measurementId)
            newUnisens.add_entry(custom)

            entry = SignalEntry(id='ecg.bin')
            # parent=u makes sure the signal is added to this Unisens object
            # saving the data to eeg.bin
            newUnisens.add_entry(entry)
            entry.set_data(signal_window, sampleRate=fs, contentClass='ecg', ch_names=['ECG I'], unit="mV",
                           lsbValue="0.0026858184230029595", adcResolution="16", baseline="2048",
                           dataType="int16", )

            # Acc Last entry

            acc_entry = SignalEntry(id='acc.bin')
            newUnisens.add_entry(acc_entry)
            x_acc = acc_data[0][start_index * fs_acc:fs_acc * total_duration - 1]
            y_acc = acc_data[1][start_index * fs_acc:fs_acc * total_duration - 1]
            z_acc = acc_data[2][start_index * fs_acc:fs_acc * total_duration - 1]
            acc_signal = np.array([x_acc, y_acc, z_acc])

            acc_entry.set_data(acc_signal, sampleRate=fs_acc, contentClass='acc', unit='g',
                               lsbValue="0.00048828125", adcResolution="16", comment="acc",
                               ch_names=['accX', 'accY', 'accZ'])

            # Angular rate last entry
            angultar_rate_entry = SignalEntry(id='angularrate.bin')
            newUnisens.add_entry(angultar_rate_entry)
            x_angultar_rate = angultar_rate[0][start_index * fs_angultar_rate:fs_angultar_rate * total_duration - 1]
            y_angultar_rate = angultar_rate[1][start_index * fs_angultar_rate:fs_angultar_rate * total_duration - 1]
            z_angultar_rate = angultar_rate[2][start_index * fs_angultar_rate:fs_angultar_rate * total_duration - 1]
            angultar_rate_signal = np.array([x_acc, y_acc, z_acc])
            angultar_rate_entry.set_data(angultar_rate_signal, sampleRate=fs_angultar_rate,
                                         contentClass='angularRate',
                                         unit='dps',
                                         lsbValue="0.07000000066757203", adcResolution="16", comment="angularRate",
                                         dataType="int16",
                                         ch_names=['angularRateX', 'angularRateY', 'angularRateZ'])

            # press

            press_entry = SignalEntry(id='press.bin')
            newUnisens.add_entry(press_entry)
            press_signal = press[start_index * 8:8 * total_duration - 1]
            press_entry.set_data(press_signal, adcResolution="32", comment="press", contentClass="press",
                                 dataType="int32",
                                 id="press.bin", lsbValue="0.125", sampleRate="8", unit="Pa", ch_names=['press'])

            # movementAcceleration
            movementAcceleration_entry = SignalEntry(id='movementacceleration_live.bin')
            newUnisens.add_entry(movementAcceleration_entry)
            movementAcceleration_signal = movementAcceleration[
                                          int(start_index * fs_movementAcceleration):int(
                                              fs_movementAcceleration * total_duration) - 1]
            movementAcceleration_entry.set_data(movementAcceleration_signal, adcResolution="16",
                                                ch_names=['movementAcceleration'],
                                                comment="movementAcceleration_live",
                                                contentClass="movementAcceleration_live",
                                                dataType="int16", id="movementacceleration_live.bin",
                                                lsbValue="0.00390625",
                                                sampleRate="0.016666666666666666", unit="g")

            # hr
            hr_live_entry = SignalEntry(id='hr_live.bin')
            # parent=u makes sure the signal is added to this Unisens object
            # saving the data to eeg.bin
            newUnisens.add_entry(hr_live_entry)
            hr_live_entry.set_data(
                hr_live[int(start_index * .0166666): int(.016666666666666666 * total_duration) - 1],

                adcResolution="16",
                ch_names=['hr'],
                comment="hr_live",
                contentClass="hr_live",
                dataType="int16",
                id="hr_live.bin",
                lsbValue="1",
                sampleRate="0.016666666666666666",
                unit="1/min")

            # HRV

            hrvrmssd_live_entry = SignalEntry(id='hrvrmssd_live.bin')
            # parent=u makes sure the signal is added to this Unisens object
            # saving the data to eeg.bin
            newUnisens.add_entry(hrvrmssd_live_entry)

            hrvrmssd_live_entry.set_data(
                hrv_live[int(start_index * .016666666): int(.016666666666666666 * total_duration) - 1],

                adcResolution="16",
                ch_names=['hrvRmssd'],
                comment="hrvRmssd_live",
                contentClass="hrvRmssd_live",
                dataType="int16",
                id="hrvrmssd_live.bin",
                lsbValue="1",
                sampleRate="0.016666666666666666",
                unit="ms")

            # Marker
            if isMarkerPresent == 1:
                maker_values = []
                for value in marker_csv.get_data():

                    if (fs_marker * start_index < value[0] <= fs_marker * total_duration):
                        new_value = value[0] - fs_marker * start_index
                        maker_values.append(new_value)

                if (len(maker_values) > 0):
                    with open(location + "-last" + "\\" + "marker.csv", 'a') as f:
                        # print(length)
                        df = pd.DataFrame()
                        df['marker'] = maker_values

                        df.to_csv(f, header=None, index=False)
                    f.close()

            newUnisens.save()  # will update the unisens.xml


# if not os.path.exists(root_dir+recordName):
#      record_path=root_dir+recordName
#      os.mkdir(record_path)
#      print(record_path)
# record_dir=root_dir+recordName

#trimUnisensdata("/Users/deku/Desktop/unisens_data/raw/", "/Users/deku/Desktop/unisens_data/trimmed/", 24)
trimUnisensdata("C:\\Users\\deku\\Documents\\code\\data\\orignal\\", "C:\\Users\\deku\\Documents\\code\\data\\trimmed\\", 24)