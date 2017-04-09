import pickle as pk
import pandas as pd
from matplotlib import pyplot
from xgboost import plot_importance
import xgboost as xgb
import heapq as hq
import os
import datetime
from sklearn.metrics import accuracy_score

def predict(data_file_path, model_file_path, result_file_path, feature_num, classes, x_encoders, y_encoder):
    start_time = datetime.datetime.now()
    data_file_name = data_file_path.split('/')[-1][0:-4]
    model_file = model_file_path + data_file_name + '_model.pkl'
    result_file = result_file_path + data_file_name +'_results.csv'
    answer_file = result_file_path + data_file_name +'_answers.csv'
    encoded_data_file = data_file_path[0:-4] + '_encoded.csv'

    # load the testing data from file
    # testing_file = data_file_path[0:-4] + '_test.csv'
    testing_file = data_file_path[0:-4]+'_encoded.csv'
    if not os.path.exists(testing_file):
        print('Testing set file does not exist!')
        os._exit(0)
    # load encoded training data
    testing_data = pd.read_csv(encoded_data_file, sep=',', header=None, encoding='utf-8')
    testing_data_values = testing_data.values
    print('Testing set size: {}'.format(testing_data_values.shape))
    X_test = testing_data_values[:, 0:feature_num]
    y_test = testing_data_values[:, feature_num]

    # load the model from file
    if not os.path.exists(model_file):
        print('Model file does not exist!')
        os._exit(0)
    with open(model_file, 'r') as f:
        model = pk.load(f)
        print('Model loaded from {}'.format(model_file))
    print(model)

    # predicting the classes
    y_pred = model.predict(X_test)
    y_rounded_pred = [round(v) for v in y_pred]
    accuracy = accuracy_score(y_test, y_rounded_pred)
    print('Precision(Right Top1) : %.5f%%' % (accuracy*100.0))
    cerror = sum(int(y_pred[i]) != y_test[i] for i in range(len(y_test))) / float(len(y_test))

    # predicting the probablities
    y_prob = model.predict_proba(X_test)

    right10 = 0
    right5 = 0
    top = 10
    if os.path.exists(result_file):
        print('Result file already exists and be removed.')
        os.remove(result_file)
    if os.path.exists(answer_file):
        print('Answer file already exists and be removed.')
        os.remove(answer_file)

    right_indices = list()
    right_results = list()
    right_probas = list()
    with open(result_file, 'a+') as f:
        for i in range(len(y_prob)):
            line = y_prob[i]
            # decode the X_test to original string
            for h in range(0, X_test.shape[1]):
                X_org = x_encoders[h].inverse_transform(X_test[i, h])
                f.write('%s,' % X_org)
            alts = hq.nlargest(top, range(len(line)), line.__getitem__)
            for j in range(5):
                if alts[j] == y_test[i]:
                    right5 += 1
            for k in range(10):
                tag_pred = classes[alts[k]]
                original = y_encoder.inverse_transform(tag_pred)
                right_results.append(original)
                right_probas.append(line[alts[k]])
                f.write('{}={}'.format(original, line[alts[k]]))  # class=prob
                if alts[k] == y_test[i]:
                    right_indices.append(k)
                    right10 += 1
                f.write(',')
            f.write('\n')
    print('Results saved in {}'.format(result_file))
    # print('X_test length: {}'.format(len(right_indices)))
    with open(answer_file, 'a+') as f:
        for i in range(len(right_indices)):
            f.write('No {} is right.'.format(right_indices[i]+1))
            f.write(',')
            f.write('Right result is: {}.'.format(right_results[i]))
            f.write(',')
            f.write('Probability is: {}.'.format(right_probas[i]))
            f.write('\n')

    print('Right in top5: %d' % right5)
    print('Precision: %.5f%%' % (float(right5) / len(X_test) * 100.0))
    print('Right in top10: %d' % right10)
    print('Precision: %.5f%%' % (float(right10) / len(X_test) * 100.0))

    ### plot the feature importance
    ## with plt
    # pyplot.bar(range(len(model.feature_importances_)), model.feature_importances_)
    # pyplot.show()

    ### or with xg func
    # plot feature importance
    plot_importance(model)
    pyplot.show()

    end_time = datetime.datetime.now()
    run_time = end_time - start_time
    print('Predicting finished, time cost : {}'.format(run_time))
