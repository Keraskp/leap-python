#!/home/keras/miniconda3/envs/leap/bin/python2.7
import pandas as pd
import numpy as np
from sklearn.metrics import confusion_matrix
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier

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
    # Multi-Layer Perceptron
    mlp = MLPClassifier(max_iter=1000, hidden_layer_sizes=(100,),random_state=42).fit(x_train, y_train) 

    # Predictions
    mlp_pred = mlp.predict(x_test) 
    
    # Accuracy
    accuracy = mlp.score(x_test, y_test)
    print "MLP Acc:", accuracy*100, "%"

    # Confusion Matrix
    cm = confusion_matrix(y_test, mlp_pred)

    # Saving Models
    pickle.dump(mlp, open('sklearn_models/mlp.pkl','wb'))
    sample = mlp.predict(np.array([x_test[200]]))
    true_val = y_test[200]
    print true_val, sample[0]
    


if __name__ == "__main__":
    main()