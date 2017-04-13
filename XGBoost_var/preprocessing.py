import numpy as np
import os
import datetime
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split

def preprocess(data_file_path, feature_num):
    start_time = datetime.datetime.now()
    training_file = data_file_path[0:-4]+'_train.csv'
    testing_file = data_file_path[0:-4]+'_test.csv'
    # also save the encoded data for later use
    encoded_data_file = data_file_path[0:-4]+'_encoded.csv'

    if os.path.exists(training_file):
        print('Training set file already exists and be removed.')
        os.remove(training_file)
    if os.path.exists(testing_file):
        print('Testing set file already exists and be removed.')
        os.remove(testing_file)
    if os.path.exists(encoded_data_file):
        print('Encoded_data file already exists and be removed.')
        os.remove(encoded_data_file)
    # load data from a csv file
    data = pd.read_csv(data_file_path, sep='\t', header=None, encoding='utf-8')
    dataset = data.values
    print('Dataset size: {}'.format(dataset.shape))
    # split data into X and y
    X = dataset[:, 0:feature_num]
    X = X.astype(str)
    Y = dataset[:, feature_num]
    # Y = dataset[:, target_col:target_col+1]
    # print(Y)
    # encoding string as integers
    encoded_x = None
    x_encoders = [None] * feature_num
    for i in range(0, X.shape[1]):
        x_encoders[i] = LabelEncoder()
        feature = x_encoders[i].fit_transform(X[:,i])
        feature = feature.reshape(X.shape[0],1)
        if encoded_x is None:
            encoded_x = feature
        else:
            encoded_x = np.concatenate((encoded_x, feature), axis=1)

    y_encoder = LabelEncoder()
    encoded_y = y_encoder.fit_transform(Y)
    classes = np.unique(Y)
    class_num = len(classes)

    print('Class number: %d' % class_num)

    # split the data into training and testing set
    X_train, X_test, y_train, y_test = train_test_split(encoded_x, encoded_y, test_size=0.2, random_state=7)
    print('Training set size: {}'.format(y_train.shape))
    print('Validation set size: {}'.format(y_test.shape))
    # write the encoded data into 2 files
    with open(training_file, 'a+') as f:
        for i in range(0, X_train.shape[0]):
            for x in X_train[i]:
                f.write('%s,'% x)
            f.write('%s' % y_train[i])
            f.write('\n')
    with open(testing_file, 'a+') as f:
        for i in range(0, X_test.shape[0]):
            for x in X_test[i]:
                f.write('%s,'% x)
            f.write('%s' % y_test[i])
            f.write('\n')

    ### write the encoded data into 1 file
    with open(encoded_data_file, 'a+') as f:
        for i in range(0, X.shape[0]):
            for x in encoded_x[i]:
                f.write("%s," % x)
            f.write("%s" % encoded_y[i])
            f.write('\n')

    end_time = datetime.datetime.now()
    run_time = end_time - start_time
    print('Preprossing finished, time cost : {}'.format(run_time))
    print('Data splited and saved in {} and {}'.format(training_file, testing_file))
    return (classes, x_encoders, y_encoder)