import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_curve, roc_auc_score, classification_report, confusion_matrix
from sklearn.model_selection import train_test_split
import numpy as np

def rocCurveGraph(title, fpr, tpr):
    plt.plot([0, 1], [0, 1], 'k--')
    plt.plot(fpr, tpr)
    plt.xlabel('False positive rate')
    plt.ylabel('True positive rate')
    plt.title(f'{title} Logistic Regression - Roc Curve')
    plt.savefig('CovidRocCurve.png', dpi=None, facecolor='w', edgecolor='w')
    plt.show()

covidDf = pd.read_csv('CovidSpDataSus.csv', sep=';')
logReg = LogisticRegression()

covidX = covidDf[["Tosse", "Coriza", "Dor de Cabeça", "Febre", "Distúrbios Olfativos", "Distúrbios Gustativos", "profSaudeBool"]].values
covidy = covidDf['resultadoBool'].values

xTrain, xTest, yTrain, yTest = train_test_split(covidX, covidy, test_size=0.3, random_state=42, stratify=covidy)
logReg.fit(xTrain, yTrain)
yPred = logReg.predict(xTest)
yPredProbs = logReg.predict_proba(xTest)[:, 1]

# False positive and True Postive Rates
fpr, tpr, thresholds = roc_curve(yTest, yPredProbs)
title = 'Covid Test'
rocGraph = rocCurveGraph(title, fpr, tpr)

aucScore = roc_auc_score(yTest, yPredProbs)
confMatrix = confusion_matrix(yTest, yPred)
classReport = classification_report(yTest, yPred)

output = open('CovidOutPut.txt', 'w')
output.write(f"""
    Covid Logistic Regression OutPut\n\n
    Auc Roc Score: {round(aucScore*100, 2)}%\n
    This means that the model predicts {round(aucScore*100, 2)}% better than a random model\n\n
    Confusion matrix:\n
    True Negatives: {confMatrix[0][0]}\n
    False Negatives: {confMatrix[1][0]}\n
    True Positives: {confMatrix[0][1]}\n
    False Positives: {confMatrix[1][1]}\n\n
    Classification Report:\n
    {classReport}""")
output.close()
