import pandas as pd
import numpy as np
import os

### format the data file, get rid of the header and the non-feature cols
def format_data(file_path, non_feature_cols, target_col):
    # with header, seperated by comma by default
    data = pd.read_csv(file_path, sep=',', header=0, encoding='utf-8')
    data_list = data.values
    # col 0
    X_0 = data_list[:, 0:1] # must not be [0:] since it will be a vector instead of a matrix
    # print(X_0.shape)
    X_3_6 = data_list[:, 3:target_col]
    # print(X_3_6.shape)
    X_8 = data_list[:, 8:9]
    X = np.concatenate((X_0, X_3_6, X_8), axis=1)
    print('feature size:{}'.format(X.shape))
    Y = data_list[:, target_col:target_col+1]
    print('target size:{}'.format(Y.shape))
    # write the data back to another file
    formatted_data_file = file_path[0:-4]+'_formatted.csv'
    if os.path.exists(formatted_data_file):
        os.remove(formatted_data_file)

    with open(formatted_data_file, 'a+') as f:
        for i in range(0, X.shape[0]):
            for x in X[i]:
                f.write('%s,'%(x))
            for y in Y[i]:
                f.write('%s'%(y))
            f.write('\n')

if __name__ == '__main__':
    file_path = '../input/expr/lang_7.expr.csv'
    # non_feature col indexes, start from 0
    non_feature_cols = [1,2]
    target_col = 7
    format_data(file_path, non_feature_cols, target_col)