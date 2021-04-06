import csv
import shutil
import os
import  pandas as pd




def  rename_results_xlms_to_context(src):


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
            listOfrecordings[:] = [x for x in listOfrecordings if ".json" not in x]

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
                    file_src = src + "/" + subject + "/" + listOfrecording + "/" + path
                    #print(src + "/" + subject + "/" + listOfrecording + "/" + path + "/images")

                    if (os.path.getsize(file_src + "/annotation.csv") != 0):
                        print("file exists ")

                        # os.rename(file_src+"/Results.xlsx", file_src+"/context.xlsx")


                        with open(file_src + "/annotation.csv", newline='') as f:
                            r = csv.reader(f)
                            data = [line for line in r]
                        with open(file_src + "/annotation.csv", 'w', newline='') as f:
                            w = csv.writer(f)
                            w.writerow(['Start', 'End', 'Class'])
                            w.writerows(data)

                    else:
                        print('File does not exists')
                        count_no+=1

    print(days)
    print("no " + str(count_no))
    print("Yes" + str(count_yes))




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



rename_results_xlms_to_context("/Users/deku/Desktop/CACHET-AFDB/FINAL/annotations")


#create_empty_csv_file_if_no_annotaions_exists( "/Users/deku/Desktop/CACHET-AFDB/FINAL/annotations")