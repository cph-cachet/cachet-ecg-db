import shutil
import os

import h5py
import pandas as pd
import unisens
import heartpy as hp
import  numpy as np



def read_annotations_and_load_correspondingECG(annotation_path, ecg_data_path, output_file_name):
    listOfSubjects = os.listdir(annotation_path)
    print(listOfSubjects)

    LABELS = []
    Signal = []

    with h5py.File(output_file_name, 'w') as f2:

        if '.DS_Store' in listOfSubjects:
            listOfSubjects.remove('.DS_Store')
        print(listOfSubjects)

        for subject in listOfSubjects:
            count = 0

            print("processing  subject" + subject)
            listOfrecordings = os.listdir(annotation_path + "/" + subject)

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
                        print(ecg_path)

                        count = 0

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

                                Signal = np.concatenate((Signal, filtered_signal), axis=0)  # AF signal array
                                LABELS = np.concatenate((LABELS, label), axis=0)  # Lable Array
                                print(str(count) + " --- ")


                        else:
                            print("Directory does not exist")

        LABELS = np.full((LABELS.size), 0, dtype=np.int32)
        f2["Signal"] = Signal
        f2["Labels"] = LABELS
        print("Finished")

        # final data is store in hdf5 file format with keys as "SIGNAL" and corresponding "LABELS"

        """
        The hdf5 can we read using the following code


        with h5py.File("hdf5 file name saved above", "w") as dset:
              d.keys()
              signal = dset["Signal"]
                    leb_AF = dset["LABELS"]


        """

    f2.close()



def test():
    
    # with h5py.File("/Users/deku/Documents/development/deep_learning/dl_and_context/data/cachet/CACHET-AFDB.hdf5", "r") as dset:
    # 
    #        print(dset.keys())
    #        signal = dset["Signal"]
    #        leb_AF = dset["LABELS"]

    with h5py.File("/Users/deku/Documents/development/deep_learning/dl_and_context/data/cachet/CACHET-AFDB.hdf5", "r") as dset:
                   print(dset.keys())
                   signal = dset["Signal"][:7649279]
                   labels = dset["Labels"][:7649279]
                   with h5py.File("/Users/deku/Documents/development/deep_learning/dl_and_context/data/cachet/nsr_from_new_annotations.hdf5","r") as f:
                         print(f.keys())
                         nsr_signal = f["Signal"]
                         nsr_lebels = f["Labels"]
                         print("hello")

                         final = h5py.File("/Users/deku/Documents/development/deep_learning/dl_and_context/data/cachet/CACHET-AFBD-final.hdf5", 'w')


                         final_sig= np.concatenate((signal,nsr_signal),axis=0)
                         final_label= np.concatenate((labels, nsr_lebels), axis=0)
                         final['Signal']= np.concatenate((signal,nsr_signal),axis=0)
                         final['Labels'] = np.concatenate((labels, nsr_lebels), axis=0)
                         final.close()


test()



path_of_annotations_folder="/Users/deku/Desktop/unisens_data/completed/final/"
path_of_rawdata_folder= "/Users/deku/Desktop/unisens_data/completed/cachet_afdb/"
resulting_hdf5_file_with_annotations_signal="/Users/deku/Desktop/unisens_data/completed/cachet_afdb/nsr_from_new_annotations.hdf5"
#
# read_annotations_and_load_correspondingECG(path_of_annotations_folder,
#                                            path_of_rawdata_folder,
#                                            resulting_hdf5_file_with_annotations_signal)
