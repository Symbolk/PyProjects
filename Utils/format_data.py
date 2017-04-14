import pandas as pd
import numpy as np
import os
import collections

### format the data file, get rid of the header and the non-feature cols
def format_data(file_path):
    # with header, seperated by comma by default
    data = pd.read_csv(file_path, sep='\t', header=0, encoding='utf-8')
    data_list = data.values
    X=data_list[:, 2:8]
    # col 0
    # X_0 = data_list[:, 0:1] # must not be [0:] since it will be a vector instead of a matrix
    # # print(X_0.shape)
    # X_3_6 = data_list[:, 3:target_col]
    # # print(X_3_6.shape)
    # X_8 = data_list[:, 8:9]
    # X = np.concatenate((X_0, X_3_6, X_8), axis=1)
    print('feature size:{}'.format(X.shape))
    Y = data_list[:, 8]
    print('target size:{}'.format(Y.shape))

    # count the examples and
    counter = collections.Counter(Y)
    frequent_y = list()
    for c in counter.items():
        if c[1]>10:
            frequent_y.append(c[0])

    print('all class num:{}'.format(len(np.unique(Y))))
    print('all rows num:{}'.format(Y.shape[0]))

    print('frequent class num:{}'.format(len(frequent_y)))
    frequent_indices = list()
    for i in range(0, Y.shape[0]):
        # print(Y[i])
        if Y[i] in frequent_y:
            frequent_indices.append(i)
    print('frequent rows num:{}'.format(len(frequent_indices)))

    # write the data back to another file
    formatted_data_file = file_path[0:-4]+'_formatted.csv'
    if os.path.exists(formatted_data_file):
        os.remove(formatted_data_file)

    with open(formatted_data_file, 'a+') as f:
        for i in frequent_indices:
            for x in X[i]:
                f.write('%s\t'%(x))
            f.write('%s'%(Y[i]))
            f.write('\n')

if __name__ == '__main__':
    file_path = '../input/lang_expr/m_3.expr.csv'
    # non_feature col indexes, start from 0
    # non_feature_cols = [1,2]
    # target_col = 7
    format_data(file_path)