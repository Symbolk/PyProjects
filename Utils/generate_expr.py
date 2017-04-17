import pickle as pk
import pandas as pd
import os
import xgboost as xgb
import numpy as np

### predict vars with highest proba in if, and generate corrsponding exors

## read the model and the predict data, get a list of ranked vars
def predict_vars(predict_file_path, model_file_path, encoded_raw_var):
    predict_file_name = predict_file_path.split('/')[-1][0:-4]
    model_file = model_file_path + predict_file_name + '_model.pkl'
    encoded_pred_file = predict_file_path[0:-4]+'_encoded.csv'

    # load unencoded training data
    predict_data = pd.read_csv(predict_file_path, sep='\t', header=None)
    predict_data_values = predict_data.values

    ## convert the data to encoded ones
    # for now, search and get the encoded lines
    locators = predict_data_values[:, 0:3]
    # print(locators)
    raw_data_path = '/home/symbolk/PycharmProjects/Expr_Var_Predicting/input/chart_var/chart_1.var.csv'
    row_num = list()
    raw_data = pd.read_csv(raw_data_path, sep='\t', header=0)
    raw_data_values = raw_data.values
    raw_locators = raw_data_values[:, 0:3]
    for l in locators:
        for i in range(0, raw_locators.shape[0]):
            rl = raw_locators[i]
            if rl[0]==l[0] and rl[1]==l[1] and rl[2]==l[2]:
                row_num.append(i)

    # read the encoded data and write them into the predicting file
    encoded_data = pd.read_csv(encoded_raw_var, sep=',', header=None)
    encoded_data_values = encoded_data.values
    encoded_pred = list()
    if not os.path.exists(encoded_pred_file):
        with open(encoded_pred_file, 'a+') as f:
            for r in row_num:
                row_encoded = encoded_data_values[r,:]
                for x in row_encoded:
                    f.write('%s,'%x)
                f.write('\n')

    for r in row_num:
        row_encoded = encoded_data_values[r, :]
        encoded_pred.append(row_encoded)

    # load the model from file
    if not os.path.exists(model_file):
        print('Model file does not exist!')
        os._exit(0)
    with open(model_file, 'r') as f:
        model = pk.load(f)
        print('Model loaded from {}'.format(model_file))
    print(model)

    encoded_pred_nd = np.array(encoded_pred)
    # print(encoded_pred_nd.shape)
    X_pred = encoded_pred_nd[:, 0:31]
    y_pred = encoded_pred_nd[:, 31]
    M_pred = xgb.DMatrix(X_pred, label=y_pred)
    y_prob = model.predict(M_pred)

    # var_prob = dict()
    # for i in range(0, X_pred.shape[0]):
    #     x = X_pred[i] # one row of x
    #     varname = x[2] # get the varname
    #     var_prob[varname]=y_prob[i]
    #
    # print(var_prob)
    varnames = list()
    for i in range(0, encoded_pred_nd.shape[0]):
        row = encoded_pred_nd[i]
        varnames.append(row[2])
    return(varnames)

## get the encoded lines with varnames and return the predicted exprs
def gen_exprs(encoded_raw_expr, varnames):
    encoded_data = pd.read_csv(encoded_raw_expr, sep=',', header=None)
    encoded_data_values = encoded_data.values
    X_expr = encoded_data_values[:, 0:6]
    X_varnames = encoded_data_values[:, 2]
    y_expr = encoded_data_values[:, 6]
    row_num = list()
    for v in varnames:
        for i in range(0, X_varnames.shape[0]):
            print(type(X_varnames[i]))
            if X_varnames[i]==v:
                row_num.append(i)
    print(row_num)

if __name__ == '__main__':
    predict_file_path = '../input/predicting/chart_1.var.csv'
    model_file_path = '../model/'
    encoded_raw_var = '../input/chart_var/chart_1.var_encoded.csv'
    encoded_raw_expr = '../input/chart_expr/chart_1.expr_formatted_encoded.csv'
    # get the predicted varnames
    varnames = predict_vars(predict_file_path, model_file_path, encoded_raw_var)
    # get the predicted exprs
    gen_exprs(encoded_raw_expr, varnames)