from preprocessing import *
from training import *
from testing import *

if __name__ == '__main__':
    data_file_path = '../input/chart/expr/chart_19.expr.csv'
    frequent_file_path = '../input/chart/expr/chart_19.expr_frequent.csv'

    model_saved_path = '../model/'
    result_path = '../output/chart/expr'
    # feature_num = # cols - 1(only one target)
    feature_num = 6
    # preprocess, encode-
    classes, x_encoders, y_encoder = preprocess(data_file_path, feature_num)
    class_num = len(classes)
    # train the model
    train(frequent_file_path, model_saved_path, feature_num, 'multi:softprob', class_num)
    # predict
    # predict(data_file_path,model_saved_path, result_path, feature_num, classes, x_encoders, y_encoder)
