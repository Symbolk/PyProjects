from preprocessing import *
from training import *
from testing import *

def run_var(params):
    data_file_path = params['input_path']+ params['project'] + '/var/' + params['project'] + '_'+params['bugid']+'.var.csv'
    model_saved_path = params['model_path']
    result_path = params['output_path']+params['project']+'/var/'
    # feature_num = # cols - 1(only one target)
    feature_num = 8
    # preprocess, encode
    x_encoders, y_encoder = preprocess(data_file_path, feature_num)
    # train the model
    train(data_file_path, model_saved_path, feature_num, 'binary:logistic')
    # predict
    # predict(data_file_path,model_saved_path, result_path, feature_num, x_encoders, y_encoder)


if __name__ == '__main__':
    params ={
        'project':'chart',
        'bugid':'19',
        'type': 'var',
        'model_path':'../model/',
        'expr_frequency': 10
    }
    # run_var(params)
