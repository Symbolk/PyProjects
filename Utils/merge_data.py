import os
import re

def list_files(dir, filter, fileList):
    newDir = dir
    if os.path.isfile(dir):
        if re.search(filter, dir):# filter$
            fileList.append(dir.decode('gbk'))
    elif os.path.isdir(dir):
        for s in os.listdir(dir):
            newDir = os.path.join(dir, s)
            list_files(newDir, filter, fileList)
    return fileList



### merge all the data files of the project_bugid.type.csv
## data_path : the abs path of the data files
## type : expr or var
def merge(data_path, project, type):
    # e.g. ../input/res/lang_7.expr.csv
    # dynamically build the regex without ur''
    filter = project+'_\d*.'+type+'.csv'
    file_list = list_files(data_path, filter, [])
    # for f in file_list:
    #     print(f)
    print('Merging the following files...')
    merged_file = '../input/'+project+'_'+type+'/'+'math_3.'+type+'.csv'
    data_set = set()
    data_list = list()

    if os.path.exists(merged_file):
        os.remove(merged_file)

    ### for a single file, just modify here
    single_file = ['../input/res/math_3.expr.csv']
    for fl in single_file:
        with open(fl ,'r') as f:
            orig_len = 0
            for line in f:
                # get rid of the header
                if line.startswith('filename'):
                    continue
                orig_len+=1
                data_list.append(line)
                data_set.add(line)
            print('{} data size:{}'.format(fl, orig_len))

    print('Merged data size:{}'.format(len(data_set)))
    # for item in data_set:
    #     print("{} {}".format(data_list.count(item), item))

    with open(merged_file, 'a+') as f:
        for row in data_set:
            f.write('{}'.format(row))


if __name__ == '__main__':
    data_path='../input/res/'
    project='math'
    type='expr'
    ### merge all project_bugid.type.csv under the data_path folder
    merge(data_path, project, type)



