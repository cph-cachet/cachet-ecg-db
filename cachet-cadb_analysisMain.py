


from cachet_cadb_utils import read_annotations_and_load_correspondingECG, get_gender_and_age, \
    count_annotation_type_in_each_record, count_total,conver_hdf5_file_to_csv



path_of_annotations_folder = "/Users/deku/Desktop/CACHET-AFDB/FINAL/annotations"
path_of_rawdata_folder = "/Users/deku/Desktop/CACHET-AFDB/FINAL/signal"
cachet_cadb_without_context = "/Users/deku/Desktop/CACHET-AFDB/FINAL/cachet-cadb_short_format_without_context.hdf5"

get_gender_and_age(path_of_rawdata_folder)
count_annotation_type_in_each_record("/Users/deku/Desktop/CACHET-AFDB/FINAL/annotations")

count_total("/Users/deku/Desktop/CACHET-AFDB/FINAL/annotations")

read_annotations_and_load_correspondingECG(path_of_annotations_folder, path_of_rawdata_folder,cachet_cadb_without_context)

#Convert short formate of database from hdf5 file to CSV
df = conver_hdf5_file_to_csv(cachet_cadb_without_context)
print(df.shape)
df.head()
save_df_path = '/Users/deku/Desktop/CACHET-AFDB/FINAL/cachet-acdb_short_format_without_context.csv'
df.to_csv(save_df_path)