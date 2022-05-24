from pyexpat import features
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split,RandomizedSearchCV,RepeatedStratifiedKFold,GridSearchCV
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report, f1_score,roc_auc_score, roc_curve, precision_score, recall_score
from scikitplot.metrics import plot_roc_curve as auc_roc

from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import BernoulliNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier,GradientBoostingClassifier

def classification_summary(pred, pred_prob, model):
    # result_df.loc[model,'Accuracy'] = round(accuracy_score(y_test,pred),3)*100
    # result_df.loc[model,'Precision'] = round(precision_score(y_test,pred,average='weighted'),3)*100
    # result_df.loc[model,'Recall'] = round(recall_score(y_test,pred,average='weighted'),3)*100
    # result_df.loc[model,'F1-score'] = round(f1_score(y_test,pred,average='weighted'),3)*100
    # result_df.loc[model,'AUC-ROC score'] = round(roc_auc_score(y_test,pred,multi_class='ovr'),3)*100

    print('{}{}\033[1m Evaluating {} \033[0m{}{}\n'.format('<'*3,'-'*25,model,'-'*25,'>'*3))
    print('Accuracy = {}%'.format(round(accuracy_score(y_test,pred),3)*100))
    print('F1 Score = {}%'.format(round(f1_score(y_test,pred,average='weighted'),3)*100))
    print('Precision Score = {}%'.format(round(precision_score(y_test,pred,average='weighted'),3)*100))
    print('Recall Score = {}%'.format(round(recall_score(y_test,pred,average='weighted'),3)*100))

    print('\n \033[1mConfusion Matrix:\033[0m\n',confusion_matrix(y_test,pred))
    print('\n\033[1mClassification Report:\033[0m\n',classification_report(y_test,pred))

    # auc_roc(y_test,pred_prob,curves=['each_class'])
    # plt.show()

# Visualizing Function
def auc_roc_plot(y_test,pred):
    ref = [0 for _ in range(len(y_test))]
    ref_auc = roc_auc_score(y_test,ref)
    lr_auc = roc_auc_score(y_test, pred)

    ns_fpr, ns_tpr, _ = roc_curve(y_test,ref)
    lr_fpr, lr_tpr, _ = roc_curve(y_test,pred)

    plt.plot(ns_fpr, ns_tpr, linestyle='=')
    plt.plot(lr_fpr, lr_tpr, marker='*', label='AUC = {}'.format(round(roc_auc_score(y_test,pred)*100,2)))
    plt.xlabel('Flase Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.legend()
    plt.show()

# Load pre processed data
label_file = './data/label.npy'
feature_file = './data/feature.npy'
label = np.load(label_file, allow_pickle=True)
feature = np.load(feature_file, allow_pickle=True)

#Assign labels to target value
label_mapping = {'negative':0,  'positive':1}

# Split data into training and testing sets
X = feature.tolist()
y = pd.Series(label).map(label_mapping)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

print('Original set  ---> ','feature size: ',X.shape,'label size',len(y))
print('Training set  ---> ','feature size: ',X_train.shape,'label size',len(y_train))
print('Test set  --->  ','feature size: ',X_test.shape,'label size',len(y_test))

# Building Logistic Regression Classifier
log_reg_model = LogisticRegression()
log_reg_model.fit(X_train, y_train)
pred = log_reg_model.predict(X_test)
pred_prob = log_reg_model.predict_proba(X_test)
classification_summary(pred,pred_prob,'Logistic Regression (LR)')

# Building  Decision Tree Classifier
# DT_model = DecisionTreeClassifier()
# DT_model.fit(X_train, y_train)
# pred = DT_model.predict(X_test)
# pred_prob = DT_model.predict_proba(X_test)
# classification_summary(pred, pred_prob, 'Decision Tree Classifier (DT)')