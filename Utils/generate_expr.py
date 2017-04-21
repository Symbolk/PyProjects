import pickle as pk
import pandas as pd
import os
import xgboost as xgb
import numpy as np

### predict vars with highest proba in if, and generate corrsponding exors

## read the model and the predict data, get a list of ranked vars
def predict_vars(predict_file_path, var_model_path, output_path, raw_var_path, encoded_raw_var):
    predict_file_name = predict_file_path.split('/')[-1][0:-4]
    encoded_pred_var = predict_file_path[0:-8]+'var_encoded.csv'
    var_predicted = output_path + predict_file_name+ '_pred.csv'

    # load unencoded training data
    predict_data = pd.read_csv(predict_file_path, sep='\t', header=None)
    predict_data_values = predict_data.values
    X = predict_data_values[:, 3:11]
    Y = predict_data_values[:, 11]

    ## convert the data to encoded ones
    # line + col + filename
    locators = predict_data_values[:, 1:4]
    # print(locators)
    row_num = list()
    raw_data = pd.read_csv(raw_var_path, sep='\t', header=0)
    raw_data_values = raw_data.values
    raw_locators = raw_data_values[:, 1:4]
    for l in locators:
        for i in range(0, raw_locators.shape[0]):
            rl = raw_locators[i]
            if rl[0]==l[0] and rl[1]==l[1] and rl[2]==l[2]:
                row_num.append(i)

    # read the encoded data and write them into the predicting file
    encoded_data = pd.read_csv(encoded_raw_var, sep=',', header=None)
    encoded_data_values = encoded_data.values
    if not os.path.exists(encoded_pred_var):
        with open(encoded_pred_var, 'a+') as f:
            for r in row_num:
                row_encoded = encoded_data_values[r,:]
                for x in row_encoded:
                    f.write('%s,'%x)
                f.write('\n')

    encoded_pred = list()
    for r in row_num:
        row_encoded = encoded_data_values[r, :]
        encoded_pred.append(row_encoded)

    # load the model from file
    if not os.path.exists(var_model_path):
        print('Model file does not exist!')
        os._exit(0)
    with open(var_model_path, 'r') as f:
        model = pk.load(f)
        print('Model loaded from {}'.format(var_model_path))
        print(model)

    encoded_pred_nd = np.array(encoded_pred)
    # print(encoded_pred_nd.shape)
    X_pred = encoded_pred_nd[:, 0:8]
    y_pred = encoded_pred_nd[:, 8]
    M_pred = xgb.DMatrix(X_pred, label=y_pred)
    y_prob = model.predict(M_pred)

    if os.path.exists(var_predicted):
        os.remove(var_predicted)

    with open(var_predicted, 'a+') as f:
        for i in range(0, X.shape[0]):
            for x in X[i]:
                f.write('%s,' % x)
            f.write('%s' % Y[i])
            f.write('%.4f' % y_prob[i])
            f.write('\n')

            ## diable sorting now
            # var_prob = dict()
            # for i in range(0, X_pred.shape[0]):
            #     x = X_pred[i] # one row of x
            #     varname = x[2] # get the varname
            #     var_prob[varname]=y_prob[i]
            #
            # print(var_prob)
            # for i in range(0, encoded_pred_nd.shape[0]):
            #     row = encoded_pred_nd[i]
            #     varnames.append(row[2])

## get the encoded lines with varnames and return the predicted exprs
def gen_exprs(predict_file_path, expr_model_path, output_path, raw_expr_path, encoded_raw_expr):
    encoded_pred_expr = '../input/predicting_var/chart_1.expr_encoded.csv'
    expr_predicted = '../output/chart_pred/chart_1.expr_pred.csv'
    raw_expr_formatted = '../input/chart_expr/chart_1.expr.csv'

    predict_data = pd.read_csv(predict_file_path, sep='\t', header=None)
    predict_data_values = predict_data.values
    raw_data = pd.read_csv(raw_expr_path, sep='\t', header=0)
    raw_data_values = raw_data.values
    raw_expr_formatted = pd.read_csv(raw_expr_formatted, sep='\t', header=None)
    raw_expr_formatted_values = raw_expr_formatted.values

    encoded_data = pd.read_csv(encoded_raw_expr, sep=',', header=None)
    encoded_data_values = encoded_data.values


    locators = predict_data_values[:, 1:4]
    # print(locators)
    row_num = list()
    raw_locators = raw_data_values[:, 0:3]
    for l in locators:
        for i in range(0, raw_locators.shape[0]):
            rl = raw_locators[i]
            if rl[0]==l[0] and rl[1]==l[1] and rl[2]==l[2]:
                row_num.append(i)
    print(row_num)
    if not os.path.exists(encoded_pred_expr):
        with open(encoded_pred_expr, 'a+') as f:
            for r in row_num:
                row_encoded = encoded_data_values[r,:]
                for x in row_encoded:
                    f.write('%s,'%x)
                f.write('\n')

    ## get the encoded expr features
    encoded_pred = list()
    for r in row_num:
        row_encoded = encoded_data_values[r, :]
        encoded_pred.append(row_encoded)
    ## get the raw expr rows
    raw_pred = list()
    for r in row_num:
        raw_pred.append(raw_expr_formatted_values[r, :])

    ## load the model
    if not os.path.exists(expr_model_path):
        print('Model file does not exist!')
        os._exit(0)
    with open(expr_model_path, 'r') as f:
        model = pk.load(f)
        print('Model loaded from {}'.format(expr_model_path))
        print(model)

    ## do predicting
    encoded_pred_nd = np.array(encoded_pred)
    print(encoded_pred_nd.shape)
    X_pred = encoded_pred_nd[:, 0:6]
    y_pred = encoded_pred_nd[:, 6]
    M_pred = xgb.DMatrix(X_pred, label=y_pred)
    y_prob = model.predict(M_pred)

    raw_pred_nd = np.array(raw_pred)
    X_raw = raw_pred_nd[:, 0:6]
    Y_raw = raw_pred_nd[:, 6]

    ## save the results
    if os.path.exists(expr_predicted):
        os.remove(expr_predicted)
    with open(expr_predicted, 'a+') as f:
        for i in range(0, X_raw.shape[0]):
            for x in X_raw[i]:
                f.write('%s,' % x)
            f.write('%s' % Y_raw[i])
            f.write('%.4f' % y_prob[i])
            f.write('\n')

if __name__ == '__main__':
    var_model_path = '../model/chart_1.var_model.pkl'
    expr_model_path = '../model/chart_1.expr_formatted_model.pkl'
    output_path = '../output/chart_pred/'

    predict_file_path = '../input/predicting_var/chart_1.var.csv'
    raw_var_path = '../input/chart_var/chart_1.var.csv'
    raw_expr_path = '../input/chart_expr/chart_1.expr.csv'

    encoded_raw_var = '../input/chart_var/chart_1.var_encoded.csv'
    encoded_raw_expr = '../input/chart_expr/chart_1.expr_formatted_encoded.csv'
    # get the predicted varnames
    # predict_vars(predict_file_path, var_model_path, output_path, raw_var_path, encoded_raw_var)
    # get the predicted exprs
    gen_exprs(predict_file_path, expr_model_path, output_path, raw_expr_path, encoded_raw_expr)