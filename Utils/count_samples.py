import collections
import os
import pandas as pd
import numpy as np

### for a given file, build a dict [class]:[#samples]
def how_many_samples(file_path, target_col):
    # read the csv
    data = pd.read_csv(file_path, sep=',', header=None, encoding='utf-8')
    data_list = data.values
    # get the target col
    Y = data_list[:, target_col]
    classes = np.unique(Y)
    # for c in classes:
    #     print(c)
    # print(len(classes))
    # count the #rows
    counter = collections.Counter(Y)
    # convert the counter to a dict
    counter_dict = dict(counter)
    # sort the dict with value(return a list with tuple inside)
    counter_list = sorted(counter_dict.iteritems(), key=lambda d:d[1], reverse=True)

    # ordered = counter.most_common()
    # write the results into a file
    results_file = file_path[0:-4]+'_counts.csv'
    if os.path.exists(results_file):
        os.remove(results_file)
    with open(results_file, 'a+')as f:
        # for (k,v) in counter_dict.items():
        #     # write the resuls to file
        #     f.write('%s\t%d\n'%(k,v))
        for t in counter_list:
            f.write('%s\t%d\n'%(t[0],t[1]))


if __name__ == '__main__':
    file_path = '../input/expr/lang_7.expr.csv'
    # target col index, start from 0
    target_col = 7
    how_many_samples(file_path, target_col)