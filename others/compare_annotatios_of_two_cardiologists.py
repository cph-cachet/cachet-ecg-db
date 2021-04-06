import os
import pandas as pd
from pathlib import Path


"""
Compares the annotation of two cardiologists  

@author: Devender Kumar
"""





#path = Path('/home/dail/first/second/third')

#path_destination= "/Users/deku/Desktop/unisens_data/final_annotation"

path= "/Users/deku/Desktop//unisens_data/annotation/disputed/helena"

final= "/Users/deku/Desktop//unisens_data/annotation/disputed/combined"
arr = os.listdir(path)
if '.DS_Store' in arr:
    arr.remove('.DS_Store')

for file in arr:
  print(path+"/"+file)
  df=pd.read_csv(path+"/"+file,header=None,)

  #print(df)
  for i, row in df.iterrows():

     #print(index)
     #print(row[1]+" "+row[2])

     label=row[2]

    # print(label)

     with open(final + "/"+file, 'a') as f:
         df = pd.DataFrame([[ row[0], row[1], row[2],"",""]],
                                                   columns=['url', 'image_name',"label_helana","label_kamal","final"])
        # print(i)

        # df.to_csv(f, index=False, header=False, line_terminator='\r\n', encoding='utf-8')

         if(i>0):
              df.to_csv(f, index=False, header=False, line_terminator='\r\n', encoding='utf-8')
         else:
               df.to_csv(f, index=False, header=True, line_terminator='\r\n', encoding='utf-8')

     f.close();


#path_destination= "/Users/deku/Desktop/unisens_data/final_annotation"

path= "/Users/deku/Desktop//unisens_data/annotation/disputed/kamal"

final= "/Users/deku/Desktop//unisens_data/annotation/disputed/combined/"
arr = os.listdir(path)
if '.DS_Store' in arr:
    arr.remove('.DS_Store')
for file in arr:
  print(path+file)
  df=pd.read_csv(path+"/"+file,header=None,)

  #print(df)
  annotations =[]
  for i, row in df.iterrows():

     #print(index)
     #print(row[1]+" "+row[2])

     label=row[2]

     # print(label)
     # print(i)
     annotations.append(label)

  #print(final + file)
  df1 = pd.read_csv(final + file)
  df1["label_kamal"]= annotations
  df1.append(df)
  df1.to_csv(final + file, index=False)



path= "/Users/deku/Desktop//unisens_data/annotation/disputed/combined/"

#final= "/Users/deku/Desktop//unisens_data/annotation/disputed/final/"
arr = os.listdir(path)
if '.DS_Store' in arr:
    arr.remove('.DS_Store')
total_samples = 0
total_AF_count=0
total_NSR_count=0
total_Noise_count=0
total_Other_count=0
total_Flutter_count=0
for file in arr:
  df=pd.read_csv(path+"/"+file)

  #print(df)
  annotations =[]
  match_count =0;
  af_count=0
  nsr_count=0
  noise_count=0
  other_count=0
  flutter_count=0
  for i, row in df.iterrows():
     #print("I=" +str(i)+"  "+row[1])
     total_samples =total_samples+1
     #print(index)
     #print(row[1]+" "+row[2])

     label=row[2]

     # print(label)
     # print(i)


     annotation= 'null';

     if (row[2] == row[3] or row[3]=='PVC' ):
         match_count = match_count + 1

     if(row[2]=='af' and row[3]=='af'):
         total_AF_count=total_AF_count+1
         af_count=af_count+1
         annotations.append(1)

     elif (row[2] == 'nsr' and row[3] == 'nsr'):
             total_NSR_count = total_NSR_count + 1
             nsr_count = nsr_count + 1
             annotations.append(2)

     elif (row[2] == 'noise' and row[3] == 'noise'):
             total_Noise_count = total_Noise_count + 1
             noise_count = noise_count + 1
             annotations.append(3)

     elif (row[2] == 'other' and row[3] == 'other'):
             total_Other_count = total_Other_count + 1
             other_count = other_count + 1
             annotations.append(4)
     elif (row[2] == 'flutter' and row[3] == 'flutter'):
             total_Flutter_count = total_Flutter_count + 1
             flutter_count = flutter_count + 1
             annotations.append(5)

     else:    annotations.append(0)


  print(path + file)
  df1 = pd.read_csv(path + file)
  df1["final"]= annotations
  df1.append(df)
  df1.to_csv(path + file, index=False)
  print("% Match between two Cardiologists = "+str((match_count/i)*100))
  print("AF segments= " + str((af_count)))

print("total_samples "+ str(total_samples))
print("total_AF_Count "+ str(total_AF_count))
print("total_NSR_Count "+ str(total_NSR_count))
print("total_Noise_Count "+ str(total_Noise_count))
print("total_Other_Count "+ str(total_Other_count))
print("total_Flutter_Count "+ str(total_Flutter_count))