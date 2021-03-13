import shutil
import os

import h5py
import pandas as pd
import unisens
import heartpy as hp
import matplotlib.pyplot as plt
from matplotlib.ticker import (MultipleLocator, AutoMinorLocator)
import numpy as np


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


def combineCACHET_AFDB(src, ecg_data_path):
    listOfSubjects = os.listdir(src)
    print(listOfSubjects)
    # listOfDir= listOfDir.remove(".DS_Store")

    LABELS = []
    Signal = []
    out_dir = "/Users/deku/Desktop/unisens_data/completed/test.hdf5"

    with h5py.File(out_dir, 'w') as f2:

        if '.DS_Store' in listOfSubjects:
            listOfSubjects.remove('.DS_Store')
        print(listOfSubjects)


        for subject in listOfSubjects:
            count = 0



            print("processing  subject" + subject)
            listOfrecordings = os.listdir(src + "/" + subject)

            # if not os.path.exists(screening_images_path+ "/" +subject+"/"):
            #        os.makedirs(screening_images_path+ "/" +subject)
            #
            # if os.path.exists(screening_images_path+ "/" +subject+"/"+subject+ ".csv"):
            #     os.remove(screening_images_path+ "/" +subject+"/"+subject+ ".csv")
            #     print("Deleted old file")
            # else:
            #     print('File does not exists')

            # with open(screening_images_path+ "/" +subject+"/"+subject+ ".csv", 'a') as f:
            if '.DS_Store' in listOfrecordings:
                listOfrecordings.remove('.DS_Store')
            print(listOfrecordings)


            for listOfrecording in listOfrecordings:
                print("processing recording " + listOfrecording + " of " + subject)
                records = os.listdir(src + "/" + subject + "/" + listOfrecording)
                print(listOfrecordings)

                if '.DS_Store' in records:
                    records.remove('.DS_Store')
                print(records)

                AF_LABELS = []
                AF_Signal = []

                nonAF_LABELS = []
                nonAF_Signal = []



                # print(length)
                for path in records:



                    if '.DS_Store' in records:
                        records.remove('.DS_Store')
                    # print(records)
                    # print("createing hrv of record"+ path+" of" + listOfrecording + " of " + subject)

                    # print(src + "/" + subject + "/" + listOfrecording + "/" + path)
                    ann_path = src + "/" + subject + "/" + listOfrecording + "/" + path
                    ecg_path = ecg_data_path + "/" + subject + "/" + listOfrecording + "/" + path

                    if (os.path.getsize(ann_path + "/annotation.csv") != 0):
                        print(ecg_path)

                        # print(os.path.getsize(ecg_path + '/unisens.xml'))

                        if os.path.exists(ecg_path):
                            print("Directory exist")

                            df = pd.read_csv(ann_path + "/annotation.csv", header=None)

                            u = unisens.Unisens(ecg_path, readonly=True)
                            # /Users/deku/PycharmProjects/AF/u1t2m3@cachet.dk/

                            wL = 30

                            fs = 1024

                            # intersting usecase arround 3600 to 3640

                            # end_time =10000
                            signal = u['ecg.bin']
                            data = signal.get_data()
                            data = data[0]
                            # Bandpass Filter for removing Noise

                            for index, row in df.iterrows():
                                #print(str(row[0]) + " " + str(row[1]) + " " + str(row[2]))
                                start = row[0]
                                end = row[1]
                                anno = row[2]

                                # if anno == 1:
                                #     print(" annotation 1 " + ecg_path)

                                bandpass_signal = hp.filter_signal(data[start:end], cutoff=[.5, 40], sample_rate=1024,
                                                                   order=3,
                                                                   filtertype='bandpass')
                                filtered_signal = hp.smooth_signal(bandpass_signal, sample_rate=1024, polyorder=6)
                                # print(filtered_signal.size)

                                count = count + 1

                                if (anno != 3):

                                    Signal = np.concatenate((Signal, filtered_signal), axis=0)

                                    if (anno == 1):

                                        lab = np.ones(filtered_signal.size, dtype=np.int32)
                                        AF_Signal = np.concatenate((AF_Signal, filtered_signal), axis=0)
                                        AF_LABELS = np.concatenate((AF_LABELS, lab), axis=0)

                                    else:
                                        lab = np.zeros(filtered_signal.size, dtype=np.int32)
                                        nonAF_Signal = np.concatenate((nonAF_Signal, filtered_signal), axis=0)
                                        nonAF_LABELS = np.concatenate((nonAF_LABELS, lab), axis=0)

                                    # print(anno)

                                    # if (anno == 4):

                                    # plotImage(filtered_signal, fs)



                        else:
                            print("Directory does not exist")

                        print(str(count) + " --- ")

                    # f2[subject+'/signal']= np.concatenate(np.array(AF_Signal),np.array(nonAF_Signal))

                f2[subject + listOfrecording + '/AF_Signal'] = AF_Signal
                f2[subject + listOfrecording + '/AF_LABELS'] = AF_LABELS

                f2[subject + listOfrecording + '/nonAF_Signal'] = nonAF_Signal
                f2[subject + listOfrecording + '/nonAF_LABELS'] = nonAF_LABELS

                # f2[subject + '/signal'] = np.concatenate((AF_Signal,nonAF_Signal), axis=0)
                #
                # f2[subject + '/annotation'] = np.concatenate((AF_LABELS,nonAF_LABELS),axis=0)

                a = np.concatenate((AF_Signal, nonAF_Signal), axis=0)
                b = np.concatenate((AF_LABELS, nonAF_LABELS), axis=0)
                # plotImage(a, 1024)
                print("Finished")


        f2.close()


# image_dest = dest + "/" + subject + "/" + listOfrecording + "/" + path + "/images"

# if not os.path.exists(screening_images_path + "/" + subject + "/images/"):
#     os.makedirs(screening_images_path + "/" + subject + "/images/")
# for name in x:
#     print(name)
#
#     shutil.copyfile(images_src + "/" + name, screening_images_path + "/" + subject + "/images/" + name)
#     url = "https://github.com/cph-cachet/reafel.afib.annotation.images/blob/master/" + subject + "/" + listOfrecording + "/" + path + "/images/" + name + "?raw=true"
#
#
#     url= url.replace('@','%40')
#     df = pd.DataFrame([[url, name, "null"]])
#     # df.append(df1)
#     df.to_csv(f,  index=False,header=False,line_terminator='\r\n',encoding='utf-8')


# f.close()

#



def final_CACHET_AFDB(dir, output):
    arr = os.listdir(dir)



    AF_Signal = []
    AF_Labels = []

    nonAF_Signal = []
    nonAF_Labels = []
    size = 0
    Lib=[]
    Signal = []
    Labels = []

    if '.DS_Store' in arr:
        arr.remove('.DS_Store')
    print(arr)



    with h5py.File(output, "w") as f:



        for file in arr:
            print(file)
            with h5py.File(dir + file, "r") as dset:

                print(dset.keys())
                for name in dset.keys():
                    sig_AF = dset[name + "/AF_Signal"]
                    leb_AF = dset[name + "/AF_LABELS"]

                    AF_Signal= np.concatenate((np.array(AF_Signal),sig_AF), axis=0)


                    AF_Labels=np.concatenate((np.array(AF_Labels),leb_AF),axis=0)

                    # Lib =Lib+leb

                    sig_nonAF = dset[name + "/nonAF_Signal"]
                    leb_nonAF = dset[name + "/nonAF_LABELS"]
                    # nonAF_Signal = nonAF_Signal + sig_nonAF
                    # nonAF_Labels= nonAF_Labels+leb_nonAF

                    nonAF_Signal = np.concatenate((np.array(nonAF_Signal), sig_nonAF), axis=0)

                    nonAF_Labels = np.concatenate((np.array(nonAF_Labels), leb_nonAF), axis=0)

        print(" HEllo")
        f['Signal'] =  np.concatenate((AF_Signal,nonAF_Signal),axis=0)
        f['Labels'] = np.concatenate((AF_Labels,nonAF_Labels),axis=0)
        f['nonAF_Signal']= nonAF_Signal
        f['nonAF_Labels'] = nonAF_Labels



    #     Signal = np.concatenate((np.array(AF_Signal), np.array(nonAF_Signal)), axis=0)
    #     labels= np.concatenate((np.array(AF_Labels), np.array(nonAF_Labels)), axis=0
    # f['Signal'] = Signal
    # f['Labels'] =



    f.close()
    pass



def count_total(src):
    listOfSubjects = os.listdir(src)
    print(listOfSubjects)
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
        print(listOfrecordings)

        for listOfrecording in listOfrecordings:
            print("processing recording " + listOfrecording + " of " + subject)
            records = os.listdir(src + "/" + subject + "/" + listOfrecording)
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

                # print(src + "/" + subject + "/" + listOfrecording + "/" + path)
                ann_path = src + "/" + subject + "/" + listOfrecording + "/" + path
                #ecg_path = ecg_data_path + "/" + subject + "/" + listOfrecording + "/" + path

                if (os.path.getsize(ann_path + "/annotation.csv") != 0):
                    df = pd.read_csv(ann_path + "/annotation.csv", header=None)

                    # Bandpass Filter for removing Noise

                    for index, row in df.iterrows():
                        #print(str(row[0]) + " " + str(row[1]) + " " + str(row[2]))
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
        print(ann_path)
        print(" AF= " + str(count_af))
        print(" NSR= " + str(count_nsr))
        print(" Noise= " + str(count_noise))
        print(" Others= " + str(count_others))

        if count_af!=0:
            count+=1

    print(" AF= " + str(count_af))
    print(" NSR= " + str(count_nsr))
    print(" Noise= " + str(count_noise))
    print(" Others= " + str(count_others))

    print(count)
def count_undividual_record(src):
    listOfSubjects = os.listdir(src)
    print(listOfSubjects)
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
        print(listOfrecordings)

        for listOfrecording in listOfrecordings:
            print("processing recording " + listOfrecording + " of " + subject)
            records = os.listdir(src + "/" + subject + "/" + listOfrecording)
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

                # print(src + "/" + subject + "/" + listOfrecording + "/" + path)
                ann_path = src + "/" + subject + "/" + listOfrecording + "/" + path
                #ecg_path = ecg_data_path + "/" + subject + "/" + listOfrecording + "/" + path

                if (os.path.getsize(ann_path + "/annotation.csv") != 0):
                    df = pd.read_csv(ann_path + "/annotation.csv", header=None)

                    # Bandpass Filter for removing Noise

                    for index, row in df.iterrows():
                        #print(str(row[0]) + " " + str(row[1]) + " " + str(row[2]))
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
        print(ann_path)
        print(" AF= " + str(count_af))
        print(" NSR= " + str(count_nsr))
        print(" Noise= " + str(count_noise))
        print(" Others= " + str(count_others))

        if count_af!=0:
            count+=1

    print(" AF= " + str(count_af))
    print(" NSR= " + str(count_nsr))
    print(" Noise= " + str(count_noise))
    print(" Others= " + str(count_others))

    print(count)
#
#
# combineCACHET_AFDB("/Users/deku/Desktop/unisens_data/completed/final/",
#                     "/Users/deku/Desktop/unisens_data/completed/cachet_afdb/")

count_undividual_record("/Users/deku/Desktop/unisens_data/final_annotation/CACHET-AFDB-01-03-2021/V1")

count_total("/Users/deku/Desktop/unisens_data/final_annotation/CACHET-AFDB-01-03-2021/V1")

#final_CACHET_AFDB("/Users/deku/Desktop/unisens_data/completed/done/finaldata/","/Users/deku/Desktop/unisens_data/completed/done/CACHET-AFDB.hdf5")
