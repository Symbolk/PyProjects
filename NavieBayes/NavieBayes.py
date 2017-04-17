import os
import numpy as np
import heapq as hq
import pandas as pd
from sklearn.naive_bayes import MultinomialNB, GaussianNB, BernoulliNB
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import precision_recall_curve
from sklearn.metrics import classification_report


# preprossing
data = pd.read_csv('../input/lang_expr/lang_2.expr_formatted_test.csv', sep=',', header=None)

print('Reading the raw data file:')
dataset = data.values
X=dataset[:,0:6]
y=dataset[:,6]
# y=y.astype(str)

# print(dataset.shape)
# V=CountVectorizer()
# X=V.fit_transform(X)

# y=V.fit_transform(y)
X_train, X_test, y_train, y_test=train_test_split(X, y, test_size=0.2)
classes=np.unique(y)

print(len(classes))

print('Train data size:{}'.format(X_train.shape))
print('Test data size:{}'.format(y_test.shape))

# print(X[:,0].shape)

# count_vect=CountVectorizer()
# X_vec=count_vect.fit_transform(X[:,0])

# train the model multinomialNB
print('Training with NavieBayes:')
clf=GaussianNB()
clf.fit(X,y)
scores = cross_val_score(clf, X, y, cv=5)
print("CV Accuracy: %0.5f (+/- %0.5f)" % (scores.mean(), scores.std() * 2))

# predit with the model
y_pred=clf.predict(X_test) #exact results
y_prob=clf.predict_proba(X_test) #classification probabilites
# print(clf.class_count_)
# y_prob.sort(axis=1,kind='quicksort',order=None)
# print(y_prob.shape) #test rownum * classnum
# alternatives=np.argsort(y_prob, 1, 'quicksort', None)
# possible_results=np.empty([[1,2,3,4,5]])
# print(alternatives.shape)
# # all zeros, why????
# y_prob_list=y_prob.tolist()
# # print(y_prob_list)
# # print([zip(i, classes) for i in y_prob_list])
right10=0
right5=0
# get the top n alternatives
top=10
# print(y_pred)
if os.path.exists('../output/nbresults.csv'):
    print('Result file already exists and be removed.')
    os.remove('../output/nbresults.csv')

with open('../output/nbresults.csv','a+') as f:
    for i in range(len(y_prob)):
        f.write('%s' % X_test[i])
        f.write(',')
        line=y_prob[i]
        alts=hq.nlargest(top,range(len(line)),line.__getitem__)
        for j in range(5):
            cls=classes[alts[j]]
            if cls==y_test[i]:
                right5+=1
        for k in range(10):
            cls=classes[alts[k]]
            f.write('%d' % cls)
            f.write('=')
            # print(type(line[classes[k]]))
            f.write('%s' % line[alts[k]])
            if cls==y_test[i]:
                right10+=1
            f.write(',')
        f.write('\n')
    # altarray=np.array([alts])
    # print(altarray.shape)
    # possible_results=np.append(possible_results, altarray, axis=0)

# evalution
print('Classification results:')

print('Right in top10: %d'%right10)
print('Precision: %.5f%%'%(float(right10)/len(X_test)*100))

print('Right in top5: %d'%right5)
print('Precision: %.5f%%'%(float(right5)/len(X_test)*100))

# print(possible_results.shape)#[1:len(prs),:]
# print(y_pred)
# print(y_test)

right1=0
for i in range(len(y_test)):
    if y_pred[i]==y_test[i]:
        right1+=1
print('Right at top1: %d'%right1)
rate=np.mean(y_pred==y_test)
print('Precision: %.5f%%'%(rate*100.0))
# precision, recall, thresholds=precision_recall_curve(y_test, predict_result)
# results=predict_result[:,1]
# report=results>0.5
# # print(classification_report(y_test, report, target_names=['-']))
# print(precision)
