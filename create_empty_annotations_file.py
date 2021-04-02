import shutil
import os
import  pandas as pd


def  create_empty_csv_file_if_no_annotaions_exists(src):


    listOfSubjects = os.listdir(src)
    print(listOfSubjects)
    # listOfDir= listOfDir.remove(".DS_Store")

    if '.DS_Store' in listOfSubjects:
        listOfSubjects.remove('.DS_Store')
    print(listOfSubjects)

    count_no=0
    count_yes=0


    for subject in listOfSubjects:
            days = 0
            print("processing  subject" + subject)
            listOfrecordings = os.listdir(src + "/" + subject)

            # if not os.path.exists(screening_images_path+ "/" +subject+"/"):
            #        os.makedirs(screening_images_path+ "/" +subject)

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

                # print(length)
                for path in records:

                    if '.DS_Store' in records:
                        records.remove('.DS_Store')
                    # print(records)
                    # print("createing hrv of record"+ path+" of" + listOfrecording + " of " + subject)
                    file_src = src + "/" + subject + "/" + listOfrecording + "/" + path+"/annotation.csv"
                    #print(src + "/" + subject + "/" + listOfrecording + "/" + path + "/images")

                    if os.path.exists(file_src):
                        print("file exists ")
                        days+=1
                        count_yes+=1
                    else:
                        count_no += 1
                        print('File does not exists')
                        #pd.DataFrame({}).to_csv("annotation.csv")
                        # with open(file_src, 'w') as emptyfile:
                        #      passi
            print(days)
    print("no " + str(count_no))
    print("Yes" + str(count_yes))





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
create_empty_csv_file_if_no_annotaions_exists( "/Users/deku/Desktop/CACHET-AFDB/FINAL/annotations")