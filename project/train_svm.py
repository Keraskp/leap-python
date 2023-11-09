#!/home/keras/miniconda3/envs/leap/bin/python2.7
import pandas as pd
import numpy as np
from sklearn.metrics import confusion_matrix
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC 
import pickle

def main():
    # Loading Dataset
    df = pd.read_csv('./datasets/cleaned_dataset.csv')
    Y = df['gesture']
    X = df.drop('gesture',axis=1)
    x = np.array(X)
    y = np.array(Y)

    # Preprocessing Dataset
    scaler = StandardScaler()
    scal = scaler.fit(x)
    x = scal.transform(x)

    # pickle.dump(scaler, open('sklearn_scaler/scaler.pkl', 'wb'))
    # Train-Test Split
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size = 0.33, random_state = 42)

    # Training Models:
    # SVM - linear
    # SVM - rbf
    svm_model_linear = SVC(kernel = 'linear', C = 1, gamma='auto').fit(x_train, y_train)
    svm_model_rbf = SVC(kernel='rbf', C=1, gamma='auto').fit(x_train, y_train)

    # Predictions
    svm_pred_linear = svm_model_linear.predict(x_test) 
    svm_pred_rbf = svm_model_rbf.predict(x_test)

    # Accuracy
    acc_linear = svm_model_linear.score(x_test, y_test)
    acc_rbf = svm_model_rbf.score(x_test, y_test)
    print "SVM linear Acc:", acc_linear*100, "%"
    print "SVM RBF Acc:", acc_rbf*100, "%"

    # Confusion Matrix
    cm_linear = confusion_matrix(y_test, svm_pred_linear)
    cm_rbf = confusion_matrix(y_test, svm_pred_rbf)

    # Saving Models
    # pickle.dump(svm_model_linear, open('sklearn_models/svm_linear.pkl','wb'))
    # pickle.dump(svm_model_rbf, open('sklearn_models/svm_rbf.pkl','wb'))
    sample = svm_model_rbf.predict(np.array([x_test[300]]))
    true_val = y_test[300]
    print true_val, sample[0]
    


if __name__ == "__main__":
    main()