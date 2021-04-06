import shutil
import os

import h5py
import  pandas as pd


def copyfile(src, dest):
    try:
        shutil.copyfile(src, dest)
    # Directories are the same
    except shutil.Error as e:
        print('file not copied. Error: %s' % e)
    # Any error saying that the directory doesn't exist
    except OSError as e:
        print('file not copied. Error: %s' % e)


def copy_noise_and_unisnedatafile(data_dir,dest_dir):
    list_of_records = os.listdir(data_dir)
    print(list_of_records)
    # listOfDir= listOfDir.remove(".DS_Store")

    if '.DS_Store' in list_of_records:
        list_of_records.remove('.DS_Store')
    print(list_of_records)

    for record in list_of_records:
        print("processing  record " + record)
        list_of_anonymous_Ids_in_signle_record = os.listdir(data_dir + "/" + record)

        if '.DS_Store' in list_of_anonymous_Ids_in_signle_record:
            list_of_anonymous_Ids_in_signle_record.remove('.DS_Store')
        print(list_of_anonymous_Ids_in_signle_record)

        for anonymous_Id in list_of_anonymous_Ids_in_signle_record:
            print("processing anonymous_Id " + anonymous_Id + " of " + record)
            number_of_days_recording = os.listdir(data_dir + "/" + record + "/" + anonymous_Id)
            # print(list_of_anonymous_Ids_in_signle_record)

            if '.DS_Store' in number_of_days_recording:
                number_of_days_recording.remove('.DS_Store')
            print(number_of_days_recording)

            for day in number_of_days_recording:
                # if '.DS_Store' in number_of_days_recording:
                #     number_of_days_recording.remove('.DS_Store')
                # print(number_of_days_recording)
                # print("createing hrv of record"+ path+" of" + anonymous_Id + " of " + record)
                src_path = data_dir + "/" + record + "/" + anonymous_Id + "/" + day
                print(data_dir + "/" + record + "/" + anonymous_Id + "/" + day)

                dest_path= dest_dir+ "/" + record + "/" + anonymous_Id + "/" + day

                if not os.path.exists(dest_path):
                      os.makedirs(dest_path)

                copyfile(src_path+'/noise.csv', dest_path+'/noise.csv')
                copyfile(src_path + '/unisensdata.hdf5', dest_path + '/unisensdata.hdf5')





def count_number_of_rpeaks(data_dir,result_dir):
    list_of_records = os.listdir(data_dir)
    print(list_of_records)
    # listOfDir= listOfDir.remove(".DS_Store")

    if '.DS_Store' in list_of_records:
        list_of_records.remove('.DS_Store')
    print(list_of_records)

    flag=0
    with open("/Users/deku/Desktop/CACHET-AFDB/raw/" + "stats_rpeaks_and_noise.csv", 'a') as f:
        for record in list_of_records:
            print("processing  record " + record)
            list_of_anonymous_Ids_in_signle_record = os.listdir(data_dir + "/" + record)

            if '.DS_Store' in list_of_anonymous_Ids_in_signle_record:
                list_of_anonymous_Ids_in_signle_record.remove('.DS_Store')
            print(list_of_anonymous_Ids_in_signle_record)

            for anonymous_Id in list_of_anonymous_Ids_in_signle_record:
                print("processing anonymous_Id " + anonymous_Id + " of " + record)
                number_of_days_recording = os.listdir(data_dir + "/" + record + "/" + anonymous_Id)
                # print(list_of_anonymous_Ids_in_signle_record)

                if '.DS_Store' in number_of_days_recording:
                    number_of_days_recording.remove('.DS_Store')
                print(number_of_days_recording)

                for day in number_of_days_recording:
                    # if '.DS_Store' in number_of_days_recording:
                    #     number_of_days_recording.remove('.DS_Store')
                    # print(number_of_days_recording)
                    # print("createing hrv of record"+ path+" of" + anonymous_Id + " of " + record)

                    result_path=result_dir+"/" + record + "/" + anonymous_Id + "/" + day
                    file_path = data_dir + "/" + record + "/" + anonymous_Id + "/" + day
                    print(data_dir + "/" + record + "/" + anonymous_Id + "/" + day)
                    with h5py.File(file_path + "/unisensdata.hdf5", "r") as dset:
                        # X, y, samp_idx = get_record(dset, rc, return_rpeaks=True)
                        print(dset.keys())
                        print(int(dset['Signal'][:].size / 1024))
                        print(dset['Data'][:].shape)
                        print(dset['r_peaks'][:].size)
                        # print(dset['Sample_idx'][:].shape)
                        sig_size = int(dset['Signal'][:].size / 1024)
                        r_peaks= dset['r_peaks'][:].size
                        print("")

                    if(os.stat(file_path + "/noise.csv").st_size!=0):
                        df = pd.read_csv(file_path + "/noise.csv")

                        noise = (df.index.size + 1) * 10
                        noise_per = str((noise * 100) / sig_size)

                        print("% of noise= " + str((noise * 100) / sig_size))
                    else:
                        noise=0
                        noise_per=0

                    result_df = pd.read_excel(result_path + "/Results.xlsx",usecols=[0, 3, 4, 5, 9, 22, 23, 24, 25, 26, 28, 31])
                    result_df.index = pd.to_datetime(result_df["Date abs [yyyy-mm-dd]"])

                    result_df['NonWearTime []'] = result_df['NonWearTime []'].fillna(0)

                    recording_length = int((result_df.index[-1] - result_df.index[0]).total_seconds())
                    print(recording_length)

                    #print(result_df['NonWearTime []'].sum(min_count=0))
                    non_wear_time = result_df['NonWearTime []'].sum()*10

                    df = pd.DataFrame([[record, anonymous_Id,  day,r_peaks,sig_size,noise,noise_per,non_wear_time]],
                                      columns=['record', 'anonymous_Id', "day","r_peaks","signal_length", "noise_length","%noise","non_wearTime"])
                    if(flag==0):
                         df.to_csv(f, index=False, header=True, line_terminator='\r\n', encoding='utf-8')
                         flag=1
                    else:
                         df.to_csv(f, index=False, header=False, line_terminator='\r\n', encoding='utf-8')

    f.close()



#copy_noise_and_unisnedatafile("/Users/deku/Desktop/CACHET-AFDB/raw/data_dir","/Users/deku/Desktop/CACHET-AFDB/raw/only_noise_hdf5_files")
count_number_of_rpeaks( "/Users/deku/Desktop/CACHET-AFDB/raw/only_noise_hdf5_files", "/Users/deku/Desktop/CACHET-AFDB/result")