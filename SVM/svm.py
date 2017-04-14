from sklearn import svm
import numpy as np
import pandas as pd
from sklearn.model_selection import KFold, cross_val_score, GridSearchCV

encoded_data_file = '../input/math_expr/math_3.expr_formatted_encoded.csv'
feature_num = 6
data = pd.read_csv(encoded_data_file, sep=',', header=None, encoding='utf-8')
dataset = data.values

X = dataset[:, 0:feature_num]
y = dataset[:, feature_num]
print('Dataset size: {}'.format(dataset.shape))
print('Feature size: {}'.format(X.shape))

# X_folds = np.array_split(X, 3)
# y_folds = np.array_split(y, 3)

### K-fold cv
k_fold = KFold(n_splits=10)
svc = svm.SVC(C=1, kernel='linear')
# scores = list()
# for i in range(10):
#     for train_indices, test_indices in k_fold.split(X):
#         score = svc.fit(X[train_indices], y[train_indices]).score(X[test_indices], y[test_indices])
#     scores.append(score)
# print(scores)

# cv_scores = cross_val_score(svc, X, y, cv=10, scoring='precision_macro', n_jobs=-1)
# print(cv_scores)

model = svc.fit(X[:-1000], y[:-1000])
score = model.score(X[-1000:], y[-1000:])
print(score)
### K-fold cv
# scores = list()
#
# for i in range(3):
#     X_train = list(X_folds)
#     X_test = X_train.pop(i)
#     X_train = np.concatenate(X_train)
#     y_train = list(y_folds)
#     y_test = y_train.pop(i)
#     y_train = np.concatenate(y_train)
#     scores.append(svc.fit(X_train, y_train).score(X_test, y_test))
#
# print(scores)

### computes the score during the fit of an estimator on a parameter grid and chooses the parameters to maximize the cross-validation score.
# Cs = np.logspace(-6, -1, 10)
# clf = GridSearchCV(estimator=svc, param_grid=dict(C=Cs), n_jobs=-1)
# clf.fit(X[:1000],y[:1000])
# print(clf.best_score_)
# print(clf.best_estimator_.C)
# print(clf.score(X[1000:],y[1000:]))
# ### nested cv
# print(cross_val_score(clf, X, y))