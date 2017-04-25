from preprocessing import *
from training import *
from testing import *

if __name__ == '__main__':
    data_file_path = '../input/chart/var/chart_19.var.csv'
    model_saved_path = '../model/'
    result_path = '../output/chart/var'
    # feature_num = # cols - 1(only one target)
    feature_num = 8
    # preprocess, encode
    x_encoders, y_encoder = preprocess(data_file_path, feature_num)
    # train the model
    train(data_file_path, model_saved_path, feature_num, 'binary:logistic')
    # predict
    # predict(data_file_path,model_saved_path, result_path, feature_num, x_encoders, y_encoder)
