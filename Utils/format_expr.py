import pandas as pd
import numpy as np
import os
import collections

### drop infrequent classes, get rid of the header and the non-feature cols
## if-id left
def format_data(file_path, frequency):
    # with header, seperated by comma by default
    data = pd.read_csv(file_path, sep='\t', header=0, encoding='utf-8')
    data_list = data.values
    if_ids = data_list[:, 0]
    X=data_list[:, 3:9]
    # col 0
    # X_0 = data_list[:, 0:1] # must not be [0:] since it will be a vector instead of a matrix
    # # print(X_0.shape)
    # X_3_6 = data_list[:, 3:target_col]
    # # print(X_3_6.shape)
    # X_8 = data_list[:, 8:9]
    # X = np.concatenate((X_0, X_3_6, X_8), axis=1)
    print('feature size:{}'.format(X.shape))
    Y = data_list[:, 9]
    print('target size:{}'.format(Y.shape))

    # count the examples and drop the infrequent ones
    counter = collections.Counter(Y)
    frequent_y = list()
    for c in counter.items():
        if c[1]>frequency:
            frequent_y.append(c[0])

    print('All class num:{}'.format(len(np.unique(Y))))
    print('All rows num:{}'.format(Y.shape[0]))

    print('Frequent class(>{}) num:{}'.format(frequency, len(frequent_y)))
    frequent_indices = list()
    for i in range(0, Y.shape[0]):
        if Y[i] in frequent_y:
            frequent_indices.append(i)
    print('Frequent rows num:{}'.format(len(frequent_indices)))

    # write the data back to another file
    formatted_data_file = file_path[0:-4]+'_frequent_raw.csv'
    if os.path.exists(formatted_data_file):
        os.remove(formatted_data_file)

    with open(formatted_data_file, 'a+') as f:
        for i in frequent_indices:
            f.write('%s\t'%if_ids[i])
            for x in X[i]:
                f.write('%s\t'%(x))
            f.write('%s'%(Y[i]))
            f.write('\n')

if __name__ == '__main__':
    file_path = '../input/math/expr/math_3.expr.csv'
    # non_feature col indexes, start from 0
    # non_feature_cols = [1,2]
    # target_col = 7
    frequency = 20
    format_data(file_path, frequency)