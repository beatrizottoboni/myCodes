'''
Codigo para prever se o teste de covid sera positivo ou nao
fonte de dados https://opendatasus.saude.gov.br/dataset/notificacoes-de-sindrome-gripal-leve-2022/resource/6c905d87-1f07-4019-9ab8-dfb63b44eace
Arquivo UF-SP - Lote 1
O arquivo considera 160.000 linhas
'''
import pandas as pd
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
import numpy as np
import matplotlib.pyplot as plt

covidDf = pd.read_csv('CovidSpDataSus.csv', sep=';')

covidX = covidDf[["Tosse", "Coriza", "Dor de Cabeça", "Febre", "Assintomático", "Distúrbios Olfativos", "Distúrbios Gustativos", "profSaudeBool"]].values
covidY = covidDf["resultadoBool"]

xTrain, xTest, yTrain, yTest = train_test_split(covidX, covidY, test_size=0.3, random_state=42, stratify=covidY)

numberNeighbors = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
trainAccuracy = {}
testAccuracy = {}

for number in numberNeighbors:
    neighborClass = KNeighborsClassifier(n_neighbors=number)
    neighborClass.fit(xTrain, yTrain)
    trainAccuracy[number] = neighborClass.score(xTrain, yTrain)
    testAccuracy[number] = neighborClass.score(xTest, yTest)

plt.figure(figsize=(11, 9))
plt.title("Varying Number of Neighbors - Covid Test Prediction")
plt.plot(numberNeighbors, trainAccuracy.values(), label="Train Accuracy", color="m")
plt.plot(numberNeighbors, testAccuracy.values(), label="Test Accuracy", color="c")
plt.legend()
plt.xlabel("Number of Neighbors")
plt.ylabel("Accuracy")
plt.show()

maxAccuracy = max(testAccuracy.values())
maxNeighbor = [value for value in testAccuracy.keys() if maxAccuracy == testAccuracy.get(value)][0]

covidPredict = [[1, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 1, 1, 0],
                [1, 1, 0, 0, 0, 0, 0, 0]]

neighborClass = KNeighborsClassifier(n_neighbors=maxNeighbor)
neighborClass.fit(xTrain, yTrain)
prediction = neighborClass.predict(covidPredict)
prediction
