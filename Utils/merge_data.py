import os
import re

def list_files(dir, fileList):
    newDir = dir
    if os.path.isfile(dir):
        fileList.append(dir.decode('gbk'))
    elif os.path.isdir(dir):
        for s in os.listdir(dir):
            newDir = os.path.join(dir, s)
            list_files(newDir, fileList)
    return fileList



### merge all the data files of the project_bugid.type.csv
## data_path : the abs path of the data files
## type : expr or var
def merge(data_path, project, type):
    # e.g. /home/symbolk/PycharmProjects/FroestFlying/input/res/lang_7.expr.csv
    # wanted_files=ur"data_path+project+_+*.+type+.csv"
    # file_list = list_files(data_path, [])
    # for l in file_list:
    #     if re.match(wanted_files, l):
    #         print(l)
    file_list1 =['/home/symbolk/PycharmProjects/FroestFlying/input/res/lang_7.expr.csv']
    file_list =['/home/symbolk/PycharmProjects/FroestFlying/input/res/lang_7.expr.csv',
                '/home/symbolk/PycharmProjects/FroestFlying/input/res/lang_24.expr.csv',
                '/home/symbolk/PycharmProjects/FroestFlying/input/res/lang_35.expr.csv',
                '/home/symbolk/PycharmProjects/FroestFlying/input/res/lang_39.expr.csv']
    merged_file = '/home/symbolk/PycharmProjects/FroestFlying/input/lang_expr/lang_7.expr.csv'
    data_set = set()
    data_list = list()

    if os.path.exists(merged_file):
        os.remove(merged_file)

    for fl in file_list:
        with open(fl ,'r') as f:
            orig_len = 0
            for line in f:
                if line.startswith('methodname'):
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
    data_path='/home/symbolk/PycharmProjects/FroestFlying/input/res/'
    project='lang'
    type='expr'
    merge(data_path, project, type)



