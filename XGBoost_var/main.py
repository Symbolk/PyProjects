from preprocessing import *
from training import *
from testing import *

def run_var(params):
    print('Training var model for {}_{}...'.format(params['project'], params['bugid']))

    data_file_path = params['input_path']+ params['project'] + '/var/' + params['project'] + '_'+params['bugid']+'.var.csv'
    model_saved_path = params['model_path']
    result_path = params['output_path']+params['project']+'/var/'

    # store vital info in the summary file
    summary_file = params['output_path'] + 'summary_var.csv'
    if not os.path.exists(summary_file):
        # write the header only once
        with open(summary_file, 'a+') as f:
            f.write(
                'time, project_bugid, #classes, #samples, #test_samples, accuracy, precision, recall, f1_score\n')

    with open(summary_file, 'a+') as f:
        f.write('%s,' % datetime.datetime.now())
        f.write('%s,' % (params['project'] + '_' + params['bugid']))

    # feature_num = # cols - 1(only one target)
    feature_num = 8
    # preprocess, encode
    x_encoders, y_encoder = preprocess(summary_file, data_file_path, feature_num)
    # train the model
    train(data_file_path, model_saved_path, feature_num, 'binary:logistic')
    # predict
    predict(data_file_path,model_saved_path, result_path, params['output_path'], summary_file, feature_num, x_encoders, y_encoder)


if __name__ == '__main__':
    params = {
        'project': 'guava',
        'bugid': '',
        'type': 'expr',
        'expr_frequency': 2,
        'model_path': '../model/',
        'input_path': '../input/',
        'output_path': '../output/',
        'gen_expr_top': 10
    }
    run_var(params)
