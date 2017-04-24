import pickle as pk
import pandas as pd
import os
import heapq as hq
import xgboost as xgb
import numpy as np

### predict vars with highest proba in if, and generate corrsponding exors

## read the model and the predict data, get a list of ranked vars
def predict_vars(project_bugid, oracle, var_model_path, output_path, raw_var_path, encoded_raw_var):
    encoded_oracle_var =  oracle[0:-4]+ '.var_encoded.csv'
    var_predicted = output_path + project_bugid + '.var_pred.csv'

    # load unencoded training data
    oracle_data = pd.read_csv(oracle, sep='\t', header=None)
    oracle_values = oracle_data.values
    raw_var = pd.read_csv(raw_var_path, sep='\t', header=0)
    raw_var_values = raw_var.values
    print(oracle_values.shape)

    ## convert the data to encoded ones(by matching in the original files)
    # match with if_ids and varnames
    # locators = oracle_values[:, 0:2]
    locators = np.concatenate((oracle_values[:, 0:1], oracle_values[:, 5:6]), axis=1)
    row_num = list()

    raw_locators = np.concatenate((raw_var_values[:,0:1], raw_var_values[:,5:6]),axis=1)
    for l in locators:
        for i in range(0, raw_locators.shape[0]):
            rl = raw_locators[i]
            if rl[0]==l[0] and rl[1]==l[1]:
                row_num.append(i)

    print('Matched rows:{}'.format(row_num))
    # read the encoded data and write them into the predicting file
    encoded_var = pd.read_csv(encoded_raw_var, sep=',', header=None)
    encoded_var_values = encoded_var.values
    if not os.path.exists(encoded_oracle_var):
        with open(encoded_oracle_var, 'a+') as f:
            for r in row_num:
                row_encoded = encoded_var_values[r,:]
                for x in row_encoded:
                    f.write('%s,'%x)
                f.write('\n')

    encoded_rows = list()
    varnames = list()
    if_ids = list()
    for r in row_num:
        row_encoded = encoded_var_values[r, :]
        encoded_rows.append(row_encoded)
        if_ids.append(raw_var_values[r, 0])
        varnames.append(raw_var_values[r, 5])
    # load the model from file
    if not os.path.exists(var_model_path):
        print('Model file does not exist!')
        os._exit(0)
    with open(var_model_path, 'r') as f:
        model = pk.load(f)
        print('Model loaded from {}'.format(var_model_path))
        print(model)

    encoded_rows_array = np.array(encoded_rows)
    # print(encoded_rows_array.shape)
    X_pred = encoded_rows_array[:, 0:8]
    y_pred = encoded_rows_array[:, 8]
    M_pred = xgb.DMatrix(X_pred, label=y_pred)
    y_prob = model.predict(M_pred)

    if os.path.exists(var_predicted):
        os.remove(var_predicted)

    with open(var_predicted, 'a+') as f:
        for i in range(0, X_pred.shape[0]):
            f.write('%s\t' % if_ids[i])
            f.write('%s\t' % varnames[i])
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
            # for i in range(0, encoded_rows_array.shape[0]):
            #     row = encoded_rows_array[i]
            #     varnames.append(row[2])

## get the encoded lines with varnames and return the predicted exprs
def gen_exprs(project_bugid, oracle, expr_model_path, output_path, raw_expr_path, encoded_raw_expr):
    encoded_oracle_expr = oracle[0:-4]+'.expr_encoded.csv'
    expr_predicted = output_path + project_bugid + '.expr_pred.csv'
    # raw_expr_formatted = '../input/chart_expr/chart_1.expr.csv'

    oracle_data = pd.read_csv(oracle, sep='\t', header=None)
    oracle_data_values = oracle_data.values
    raw_expr = pd.read_csv(raw_expr_path, sep='\t', header=0)
    raw_expr_values = raw_expr.values
    # raw_expr_formatted = pd.read_csv(raw_expr_formatted, sep='\t', header=None)
    # raw_expr_formatted_values = raw_expr_formatted.values

    encoded_expr = pd.read_csv(encoded_raw_expr, sep=',', header=None)
    encoded_expr_values = encoded_expr.values

    # get the if_id and the varname as the locators to match
    # locators = oracle_data_values[:, 0:2]
    # locators = np.concatenate((oracle_data_values[:,0:1], oracle_data_values[:,5:6]), axis=1)
    # row_num = list()
    # raw_locators = np.concatenate((raw_expr_values[:,0:1], raw_expr_values[:,5:6]), axis=1)
    # for l in locators:
    #     for i in range(0, raw_locators.shape[0]):
    #         rl = raw_locators[i]
    #         if rl[0]==l[0] and rl[1]==l[1]:
    #             row_num.append(i)

    ## get the classes from the raw expr
    Y = raw_expr_values[:, 9]
    classes = np.unique(Y)
    ## use only the varnames to match
    row_num = list()
    locators = oracle_data_values[:, 5]
    raw_locators = raw_expr_values[:, 5]
    count = -1
    for l in locators:
        for i in range(0, raw_locators.shape[0]):
            if l==raw_locators[i]:
                row_num.append(i)

    print('Matched rows:{}'.format(len(row_num)))

    if not os.path.exists(encoded_oracle_expr):
        with open(encoded_oracle_expr, 'a+') as f:
            for r in row_num:
                row_encoded = encoded_expr_values[r,:]
                for x in row_encoded:
                    f.write('%s,'%x)
                f.write('\n')

    ## get the encoded expr features
    encoded_rows = list()
    varnames = list()
    if_ids = list()
    raw_exprs = list()
    for r in row_num:
        row_encoded = encoded_expr_values[r, :]
        encoded_rows.append(row_encoded)
        if_ids.append(raw_expr_values[r, 0])
        varnames.append(raw_expr_values[r, 5])
        raw_exprs.append(raw_expr_values[r, :])

    ## load the model
    if not os.path.exists(expr_model_path):
        print('Model file does not exist!')
        os._exit(0)
    with open(expr_model_path, 'r') as f:
        model = pk.load(f)
        print('Model loaded from {}'.format(expr_model_path))
        print(model)

    ## do predicting
    encoded_rows_array = np.array(encoded_rows)
    # print(encoded_rows_array.shape)
    X_pred = encoded_rows_array[:, 0:6]
    print(X_pred.shape)
    y_pred = encoded_rows_array[:, 6]
    M_pred = xgb.DMatrix(X_pred)
    y_prob = model.predict(M_pred)

    raw_exprs_array = np.array(raw_exprs)
    X_raw = raw_exprs_array[:, 0:6]
    Y_raw = raw_exprs_array[:, 6]

    print(y_prob.shape)

    ## save the results
    if os.path.exists(expr_predicted):
        os.remove(expr_predicted)
    with open(expr_predicted, 'a+') as f:
        for i in range(0, X_pred.shape[0]):
            f.write('%s\t' % if_ids[i])
            f.write('%s\t' % varnames[i])
            # f.write('%s' % y_prob[i])
            line = y_prob[i]
            # the predicted indices, ordered with the classes in alphabet order
            # so classes = np.unique(Y) required to decode
            alts = hq.nlargest(20, range(len(line)), line.__getitem__)
            for j in range(20):
                if j != 0:
                    f.write('\t\t')
                tag_pred = classes[alts[j]]
                f.write('{}'.format(tag_pred))# predicate
                f.write('\t%f'%line[alts[j]])
                f.write('\n')




if __name__ == '__main__':
    project_bugid = 'time_15'

    var_model_path = '../model/'+project_bugid+'.var_model.pkl'
    expr_model_path = '../model/'+project_bugid+'.expr_model.pkl'
    output_path = '../output/time_pred/'

    # oracle = '../input/res_oracle/' + project_bugid + '.orc.csv'
    oracle = '../input/time_pred/'+project_bugid+'.csv'
    raw_var_path = '../input/time_var/'+project_bugid+ '.var.csv'
    raw_expr_path = '../input/time_expr/'+project_bugid+'.expr.csv'

    encoded_raw_var = '../input/time_var/'+project_bugid+'.var_encoded.csv'
    encoded_raw_expr = '../input/time_expr/'+project_bugid+'.expr_encoded.csv'
    # get the predicted varnames
    # predict_vars(project_bugid, oracle, var_model_path, output_path, raw_var_path, encoded_raw_var)
    # get the predicted exprs
    gen_exprs(project_bugid, oracle, expr_model_path, output_path, raw_expr_path, encoded_raw_expr)