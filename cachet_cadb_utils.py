import shutil
import os

import h5py
import pandas as pd
# import tqdm as tqdm
import unisens
import heartpy as hp
import matplotlib.pyplot as plt
from matplotlib.ticker import (MultipleLocator, AutoMinorLocator)
import numpy as np
from tqdm import tqdm


def plotImage(signal, fs):
    fig = plt.figure(figsize=(30, 9))
    fs = fs
    ax = fig.add_subplot(1, 1, 1)
    # ax1 = fig.add_subplot(3, 1, 2)
    # ax2 = fig.add_subplot(3, 1, 3)
    plt.style.use('seaborn-darkgrid')

    if (type == "on"):
        plt.suptitle("AF onset starts ", fontsize=35)

    if (type == "off" or type == "off-last"):
        plt.suptitle("AF offset ", fontsize=35)

    if (type == "m"):
        plt.suptitle("Random AF sample between an onset and offset", fontsize=35)

    Time = np.linspace(0, len(signal) / fs, num=len(signal))
    ax.minorticks_on()
    ax.plot(Time, signal)
    # plt.plot(Time, signal2)
    # Make the major grid
    ax.xaxis.set_major_locator(MultipleLocator(1))
    ax.grid(which='major', linestyle='-', color='#ff4d4d', linewidth='0.7')
    # Make the minor grid
    ax.grid(which='minor', linestyle=':', color='#ff4ccb', linewidth='0.4')
    plt.xlabel('# time in [s]')
    plt.ylabel(' Amplitude[mV]')

    plt.show()





def count_total(src):
    listOfSubjects = os.listdir(src)
    #print(listOfSubjects)
    # listOfDir= listOfDir.remove(".DS_Store")

    if '.DS_Store' in listOfSubjects:
        listOfSubjects.remove('.DS_Store')
    #print(listOfSubjects)

    # listOfSubjects[:] = [x for x in listOfSubjects if ".json" not in x]

    # count_af=0
    # count_nsr=0
    # count_noise=0
    # count_others=0

    count = 0
    count_af = 0
    count_nsr = 0
    count_noise = 0
    count_others = 0

    for subject in listOfSubjects:

        #print("processing  subject" + subject)
        listOfrecordings = os.listdir(src + "/" + subject)

        if '.DS_Store' in listOfrecordings:
            listOfrecordings.remove('.DS_Store')
        #print(listOfrecordings)
        listOfrecordings[:] = [x for x in listOfrecordings if ".json" not in x]

        for listOfrecording in listOfrecordings:
            #print("processing recording " + listOfrecording + " of " + subject)
            records = os.listdir(src + "/" + subject + "/" + listOfrecording)
            #print(listOfrecordings)

            if '.DS_Store' in records:
                records.remove('.DS_Store')

            #print(records)

            # print(length)
            for path in records:

                if '.DS_Store' in records:
                    records.remove('.DS_Store')
                # print(records)
                # print("createing hrv of record"+ path+" of" + listOfrecording + " of " + subject)

                # print(src + "/" + subject + "/" + listOfrecording + "/" + path)
                ann_path = src + "/" + subject + "/" + listOfrecording + "/" + path
                # ecg_path = ecg_data_path + "/" + subject + "/" + listOfrecording + "/" + path

                if (os.path.getsize(ann_path + "/annotation.csv") != 0):
                    df = pd.read_csv(ann_path + "/annotation.csv", header=0)

                    # Bandpass Filter for removing Noise

                    for index, row in df.iterrows():
                        # print(str(row[0]) + " " + str(row[1]) + " " + str(row[2]))
                        start = row[0]
                        end = row[1]
                        anno = row[2]

                        if anno == 1:
                            count_af = count_af + 1

                        if (anno == 2):
                            count_nsr = count_nsr + 1

                        if (anno == 3):
                            count_noise = count_noise + 1

                        if (anno == 4):
                            count_others = count_others + 1
        # print(ann_path)
        # print(" AF= " + str(count_af))
        # print(" NSR= " + str(count_nsr))
        # print(" Noise= " + str(count_noise))
        # print(" Others= " + str(count_others))
        #
        # if count_af!=0:
        #     count+=1

    print(" AF= " + str(count_af))
    print(" NSR= " + str(count_nsr))
    print(" Noise= " + str(count_noise))
    print(" Others= " + str(count_others))





"""":type

Count the number of annotations of each type  in each record

"""


def count_annotation_type_in_each_record(src):
    listOfSubjects = os.listdir(src)
    #print(listOfSubjects)

    # listOfDir= listOfDir.remove(".DS_Store")

    if '.DS_Store' in listOfSubjects:
        listOfSubjects.remove('.DS_Store')
    print(listOfSubjects)
    # count_af=0
    # count_nsr=0
    # count_noise=0
    # count_others=0


    count = 0

    for subject in listOfSubjects:

        count_af = 0
        count_nsr = 0
        count_noise = 0
        count_others = 0
        print("processing  subject" + subject)
        listOfrecordings = os.listdir(src + "/" + subject)

        if '.DS_Store' in listOfrecordings:
            listOfrecordings.remove('.DS_Store')
        #print(listOfrecordings)

        listOfrecordings[:] = [x for x in listOfrecordings if ".json" not in x]

        for listOfrecording in listOfrecordings:
           # print("processing recording " + listOfrecording + " of " + subject)
            records = os.listdir(src + "/" + subject + "/" + listOfrecording)
            #print(listOfrecordings)

            if '.DS_Store' in records:
                records.remove('.DS_Store')
            #print(records)

            # print(length)
            for path in records:

                if '.DS_Store' in records:
                    records.remove('.DS_Store')
                # print(records)
                # print("createing hrv of record"+ path+" of" + listOfrecording + " of " + subject)

                # print(src + "/" + subject + "/" + listOfrecording + "/" + path)
                ann_path = src + "/" + subject + "/" + listOfrecording + "/" + path
                # ecg_path = ecg_data_path + "/" + subject + "/" + listOfrecording + "/" + path

                if (os.path.getsize(ann_path + "/annotation.csv") != 0):
                    df = pd.read_csv(ann_path + "/annotation.csv", header=0)

                    # Bandpass Filter for removing Noise

                    for index, row in df.iterrows():
                        # print(str(row[0]) + " " + str(row[1]) + " " + str(row[2]))
                        start = row[0]
                        end = row[1]
                        anno = row[2]

                        if anno == 1:
                            count_af = count_af + 1

                        if (anno == 2):
                            count_nsr = count_nsr + 1

                        if (anno == 3):
                            count_noise = count_noise + 1

                        if (anno == 4):
                            count_others = count_others + 1
        #print(ann_path)
        print(" AF= " + str(count_af))
        print(" NSR= " + str(count_nsr))
        print(" Noise= " + str(count_noise))
        print(" Others= " + str(count_others))

        # if count_af != 0:
        #     count += 1

    # print(" AF= " + str(count_af))
    # print(" NSR= " + str(count_nsr))
    # print(" Noise= " + str(count_noise))
    # print(" Others= " + str(count_others))

    #print(count)






""":type

This function reads the annotation.csv file for each patient day by day and loads the corresponding ECG segment from the raw ECG. 
At the end of , it generates an hdf5 type file that contains ECG and annotation labels. 

The hdf5 can be read using the following code


with h5py.File("hdf5_file_path", "w") as dset:
      dset.keys()
      signal = dset["signal"]   #ECG signal
      annotation = dset["labels"]   # annotation (1=AF, 2=NSR, 3=Noise, 4=Other)





"""

def read_annotations_and_load_correspondingECG(annotation_path, ecg_data_path, output_file_name):
    listOfSubjects = os.listdir(annotation_path)
    print(listOfSubjects)

    final_labels = []
    final_signal = []

    with h5py.File(output_file_name, 'w') as f2:

        if '.DS_Store' in listOfSubjects:
            listOfSubjects.remove('.DS_Store')
        print(listOfSubjects)

        for subject in listOfSubjects:
            count = 0

            print("processing  subject" + subject)
            listOfrecordings = os.listdir(annotation_path + "/" + subject)

            if '.DS_Store' in listOfrecordings:
                listOfrecordings.remove('.DS_Store')
            print(listOfrecordings)
            listOfrecordings[:] = [x for x in listOfrecordings if ".json" not in x]
            #

            for listOfrecording in listOfrecordings:
                print("processing recording " + listOfrecording + " of " + subject)
                records = os.listdir(annotation_path + "/" + subject + "/" + listOfrecording)
                print(listOfrecordings)

                if '.DS_Store' in records:
                    records.remove('.DS_Store')
                print(records)

                # print(length)
                for path in records:

                    if '.DS_Store' in records:
                        records.remove('.DS_Store')
                    # print(records)
                    # print("createing hrv of record"+ path+" of" + listOfrecording + " of " + subject)

                    # print(annotation_path + "/" + subject + "/" + listOfrecording + "/" + path)
                    ann_path = annotation_path + "/" + subject + "/" + listOfrecording + "/" + path
                    ecg_path = ecg_data_path + "/" + subject + "/" + listOfrecording + "/" + path

                    if (os.path.getsize(ann_path + "/annotation.csv") != 0):
                        print("Processing --"+ecg_path)

                        count = 0

                        # print(os.path.getsize(ecg_path + '/unisens.xml'))

                        if os.path.exists(ecg_path):
                            #print("Directory exist")

                            df = pd.read_csv(ann_path + "/annotation.csv", header=0)

                            u = unisens.Unisens(ecg_path, readonly=True)
                            # /Users/deku/PycharmProjects/AF/u1t2m3@cachet.dk/

                            wL = 30

                            fs = 1024

                            # intersting usecase arround 3600 to 3640

                            # end_time =10000
                            signal = u['ecg.bin']  # Read the ECG signal from bin file
                            data = signal.get_data()
                            data = data[0]  # Final numpy array containing full days record

                            # Reads the annotation file row by row and  collect the corresponding ECG
                            for index, row in df.iterrows():
                                # print(str(row[0]) + " " + str(row[1]) + " " + str(row[2]))
                                start = row[
                                    0]  # start index  of 10 seconds segemt  in annotation.csv file of each record
                                end = row[1]  # end index  of 10 seconds segemt  in annotation.csv
                                anno = row[2]  # Class label  for the 10 seconds

                                # Bandpass Filter for removing Noise

                                bandpass_signal = hp.filter_signal(data[start:end], cutoff=[.5, 40], sample_rate=1024,
                                                                   order=3,
                                                                   filtertype='bandpass')
                                filtered_signal = hp.smooth_signal(bandpass_signal, sample_rate=1024, polyorder=6)
                                # print(filtered_signal.size)

                                if (anno == 1):  # If AF then assign 1 for the whole 10 seconds label lenth

                                    label = np.full((filtered_signal.size), 1,
                                                    dtype=np.int32)  # make 1 for the length of the signal

                                if (anno == 2):
                                    label = np.full((filtered_signal.size), 2, dtype=np.int32)

                                if (anno == 3):
                                    label = np.full((filtered_signal.size), 3, dtype=np.int32)

                                if (anno == 4):
                                    label = np.full((filtered_signal.size), 4, dtype=np.int32)


                                #plotImages(signal, path, subject, record, index, start, end, id, type):
                                final_signal = np.concatenate((final_signal, filtered_signal), axis=0)  # concatenate signal array
                                final_labels = np.concatenate((final_labels, label), axis=0)  # concatenate lable Array


                        else:
                            print("Directory does not exist")

        f2["signal"] = final_signal
        f2["labels"] = final_labels
        print("Finished----short version of the databases with ecg annotation has been created in .hdf5 file  ")

        # final data is store in hdf5 file format with keys as "signal" and corresponding "labels"

        """
        The hdf5 can be read using the following code


        with h5py.File("hdf5 file name saved above", "r") as dset:
              d.keys()
              signal = dset["signal"]
              label = dset["labels"]


        """

    f2.close()






""":type

Gives demographics of the datasets


"""

def get_gender_and_age(signal_folder_path):
    print("Get gender an age")

    listOfSubjects = os.listdir(signal_folder_path)
    #print(listOfSubjects)


    if '.DS_Store' in listOfSubjects:
        listOfSubjects.remove('.DS_Store')
   # print(listOfSubjects)

    male=0
    female=0
    age=0
    count=0

    for subject in listOfSubjects:

        flag=0

        print("Patient " + subject)
        listOfrecordings = os.listdir(signal_folder_path + "/" + subject)

        if '.DS_Store' in listOfrecordings:
            listOfrecordings.remove('.DS_Store')
        #print(listOfrecordings)
        listOfrecordings[:] = [x for x in listOfrecordings if ".json" not in x]
        #

        for listOfrecording in listOfrecordings:
            #print("processing recording " + listOfrecording + " of " + subject)
            records = os.listdir(signal_folder_path + "/" + subject + "/" + listOfrecording)
            #print(listOfrecordings)

            if '.DS_Store' in records:
                records.remove('.DS_Store')
            #print(records)

            # print(length)
            for path in records:

                if '.DS_Store' in records:
                    records.remove('.DS_Store')
                ecg_path = signal_folder_path + "/" + subject + "/" + listOfrecording + "/" + path
                #print(ecg_path)

                u = unisens.Unisens(ecg_path, readonly=True)
                customAttributes = u.entries['customAttributes']

                if(flag==0):
                 count+=1
                 age = age + float(customAttributes.age)
                 print(customAttributes.gender)
                 if(customAttributes.gender=='F'):
                     female+=1
                 else:
                      male+=1


                 print(customAttributes.age)
                 flag=1
    print("Male"+str(male))
    print("Female"+str(female))
    print("Avg Age"+ str(age/count))


def conver_hdf5_file_to_csv(path):
    """
    input: path of the .h5py file which holds both signals and labels
    output: a single pandas df where each row is a 10s signal, with a column 'labels'
    for each signal label
    note: original sample frquency is 1024 Hz. labels: 1='AF', 2='NSR', 3='Noise', 4='Others'
    """
    df = pd.DataFrame()  # start empty df
    index = np.concatenate(np.array([range(0, int(10 * 1024))]), axis=0)
    lab = []  # start empty labels list to add later
    with h5py.File(path, "r") as dset:
        print(dset.keys())
        signal = np.array(dset["signal"])
        all_lab = np.array(dset["labels"])
        # return signal, all_lab
        # signal = dset["Signal"]
        # leb_AF = dset["LABELS"]

    # now iterate through all individual signals and append them to pandas DataFrame
    for i in tqdm(range(0, len(signal), int(10 * 1024))):
        sig = signal[i:i + int(10 * 1024)]  # get the current position and add 10s onto it
        lab.append(all_lab[i + 1])

        df = df.append(pd.Series(sig, index=index), ignore_index=True)

    df['labels'] = lab

    return df






path_of_annotations_folder = "/Users/deku/Desktop/CACHET-AFDB/FINAL/annotations"
path_of_rawdata_folder = "/Users/deku/Desktop/CACHET-AFDB/FINAL/signal"
CACHET_CADB_without_context  = "/Users/deku/Desktop/CACHET-AFDB/FINAL/cachet-cadb_short_format_without_context.hdf5"
#
#
#read_annotations_and_load_correspondingECG(path_of_annotations_folder, path_of_rawdata_folder,CACHET_CADB_without_context)
#
#
#get_gender_and_age(path_of_rawdata_folder)
#
#count_annotation_type_in_each_record("/Users/deku/Desktop/CACHET-AFDB/FINAL/annotations")

#count_total("/Users/deku/Desktop/CACHET-AFDB/FINAL/annotations")

#
# df = conver_hdf5_file_to_csv(CACHET_CADB_without_context)
# print(df.shape)
# df.head()
# save_df_path = '/Users/deku/Desktop/CACHET-AFDB/FINAL/cachet-cadb_short_format_without_context.csv'
# df.to_csv(save_df_path)


#Read short hdf5 file created by annotations_and_load_correspondingECG() function
def readhdfs(path):
    with h5py.File(path, "r") as dset:
        dset.keys()
        signal = np.array( dset["signal"])
        labels = np.array(dset["labels"])
        print(dset.keys())

# readhdfs(CACHET_CADB_without_context)



