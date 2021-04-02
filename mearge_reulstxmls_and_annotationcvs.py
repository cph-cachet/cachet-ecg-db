import shutil
import os
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


def  copy_annotatiofiles_to_result_folder(src,dest):

    screening_images_path="/Users/deku/Desktop/unisens_data/screening_images"

    listOfSubjects = os.listdir(src)
    print(listOfSubjects)
    # listOfDir= listOfDir.remove(".DS_Store")

    if '.DS_Store' in listOfSubjects:
        listOfSubjects.remove('.DS_Store')
    print(listOfSubjects)

    for subject in listOfSubjects:
            print("processing  subject" + subject)
            listOfrecordings = os.listdir(src + "/" + subject)

            if not os.path.exists(screening_images_path+ "/" +subject+"/"):
                   os.makedirs(screening_images_path+ "/" +subject)

            if os.path.exists(screening_images_path+ "/" +subject+"/"+subject+ ".csv"):
                os.remove(screening_images_path+ "/" +subject+"/"+subject+ ".csv")
                print("Deleted old file")
            else:
                print('File does not exists')

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

                # print(length)
                for path in records:

                    if '.DS_Store' in records:
                        records.remove('.DS_Store')
                    # print(records)
                    # print("createing hrv of record"+ path+" of" + listOfrecording + " of " + subject)
                    file_src = src + "/" + subject + "/" + listOfrecording + "/" + path+"/annotation.csv"
                    #print(src + "/" + subject + "/" + listOfrecording + "/" + path + "/images")
                    file_dest = dest + "/" + subject + "/" + listOfrecording + "/" + path+ "/annotation.csv"


                    copyfile(file_src, file_dest)
                    #x = next(os.walk(images_src))[2]
                    print(file_src +" --- " +file_dest)

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
copy_annotatiofiles_to_result_folder( "/Users/deku/Desktop/CACHET-AFDB/FINAL/V1","/Users/deku/Desktop/CACHET-AFDB/FINAL/annotations")