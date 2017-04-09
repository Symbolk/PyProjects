from preprocessing import *
from training import *
from predicting import *

if __name__ == '__main__':
    data_file_path = '../input/lang_expr/lang.expr.csv'
    # data_file_path = '../input/math_3_buggy.csv'
    model_saved_path = '../model/'
    result_path = '../output/'
    # feature_num = # cols - 1(only one target)
    feature_num = 5
    # allow for assign one specific col as the target, start from 0
    target_col = 4
    # preprocess, encode
    classes, x_encoders, y_encoder = preprocess(data_file_path, feature_num, target_col)
    class_num = len(classes)
    # train the model
    # train(data_file_path, model_saved_path, feature_num, 'multi:softprob', class_num)
    # predict
    # predict(data_file_path,model_saved_path, result_path, feature_num, classes, x_encoders, y_encoder)
