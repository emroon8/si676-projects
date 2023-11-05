#SI 676 Inventorying Assignment
#Emma Rooney

import os
import datetime
import hashlib

import csv

def get_checksum(file_path, checksum_type):
    checksum_type = checksum_type.lower()

    with open(file_path, 'rb') as f:
        bytes = f.read()
        if checksum_type == 'md5':
            hash_string = hashlib.md5(bytes).hexdigest()
        elif checksum_type == 'sha256':
            hash_string = hashlib.sha256(bytes).hexdigest()
        else:
            raise('{} is not a hash function supposted by this program.')
    return hash_string


directory = os.path.join('data', 'webfiles-samples')
# dir_list = os.listdir(directory)
# print(dir_list)

fileInfo = list()
manifestInfo = list()
# print(directory)

for folder_name, sub_folders, file_names in os.walk(directory):
    for file in file_names:
        relative_path = os.path.join(folder_name, file)
        # print(relative_path)
        name = file
        file_extension = os.path.splitext(name)[1]
        file_size = os.path.getsize(relative_path)
        mod_time = datetime.datetime.strftime(datetime.datetime.fromtimestamp(os.path.getmtime(relative_path)), "%Y-%m-%dT%H:%M:%S%Z")
        file_integrity_info = get_checksum(relative_path, 'md5')


        fileInfo = [
            relative_path,
            name,
            file_extension,
            file_size,
            mod_time,
            file_integrity_info
            ]
        manifestInfo.append(fileInfo)

print(manifestInfo)

headers = [
    'relative_path',
    'file_name',
    'file_extension',
    'file_size',
    'mod_time',
    'file_integrity_info'
    ]

with open('file-manifest.csv', 'w') as f:
    writer = csv.writer(f)
    writer.writerow(headers)
    for file in manifestInfo:
        writer.writerow(file)