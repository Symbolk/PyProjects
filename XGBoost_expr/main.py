from preprocessing import *
from training import *
from testing import *
from gen_exprs import  *

def run_expr(params):
    print('Training expr model for {}_{}...'.format(params['project'], params['bugid']))
    ## construct the path strings with params
    data_file_path = params['input_path']+params['project']+'/expr/'+params['project']+'_'+params['bugid']+'.expr.csv'
    frequent_file_path = params['input_path']+params['project']+'/expr/'+params['project']+'_'+params['bugid']+'.expr_frequent.csv'

    model_saved_path = params['model_path']
    result_path = params['output_path']+params['project']+'/expr/'
    # feature_num = # cols - 1(only one target)
    feature_num = 6
    frequency = params['expr_frequency']
    # preprocess, encode-
    classes, x_encoders, y_encoder = preprocess(data_file_path, feature_num, frequency)
    class_num = len(classes)
    # train the model
    # train(frequent_file_path, model_saved_path, feature_num, 'multi:softprob', class_num)
    # predict
    predict(data_file_path,model_saved_path, result_path, feature_num, classes, x_encoders, y_encoder)
    # run_gen_exprs(params, y_encoder)

if __name__ == '__main__':
    params ={
        'project':'retrofit',
        'bugid':'',
        'type': 'expr',
        'expr_frequency': 0,
        'model_path': '../model/',
        'input_path':'../input/',
        'output_path':'../output/',
        'gen_expr_top': 10
    }
    run_expr(params)
