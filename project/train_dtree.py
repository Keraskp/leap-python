#!/home/keras/miniconda3/envs/leap/bin/python2.7
import pandas as pd
import numpy as np
from sklearn.metrics import confusion_matrix
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier 
from sklearn.metrics import accuracy_score, precision_score
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
from sklearn.metrics import f1_score

import pickle

def main():
    # Loading Dataset
    df = pd.read_csv('./datasets/cleaned_dataset.csv')
    Y = df['gesture']
    X = df.drop('gesture',axis=1)
    x = np.array(X)
    y = np.array(Y)

    # Preprocessing Dataset
    scaler = pickle.load(open('sklearn_scaler/scaler.pkl', 'rb'))
    x = scaler.transform(x)

    # Train-Test Split
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size = 0.33, random_state = 42)

    # Training Models:
    # Decision Tree
    dtree_model = DecisionTreeClassifier(max_depth = 25).fit(x_train, y_train) 

    # Predictions
    dtree_pred = dtree_model.predict(x_test) 
    
    # Accuracy
    accuracy = dtree_model.score(x_test, y_test)
    print "Decision Tree Acc:", accuracy*100, "%"

    # Confusion Matrix
    cm_linear = confusion_matrix(y_test, dtree_pred)

    # Saving Models
    pickle.dump(dtree_model, open('sklearn_models/dtree_25.pkl','wb'))
    sample = dtree_model.predict(np.array([x_test[200]]))
    true_val = y_test[200]
    print true_val, sample[0]
    


if __name__ == "__main__":
    main()