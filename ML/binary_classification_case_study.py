# Ch 21
# Binary Classification Machine Learning Case Study Project

# 1. Import Libraries
import pandas
import numpy as np
import matplotlib.pyplot as plt
from pandas.tools.plotting import scatter_matrix
from sklearn import cross_validation
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
from sklearn.pipeline import Pipeline
from sklearn.grid_search import GridSearchCV
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
from sklearn.ensemble import AdaBoostClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import ExtraTreesClassifier

# 2. Load Data
url = "https://goo.gl/NXoJfR"
# no column names because variables do not have meaningful names
dataset = pandas.read_csv(url, header=None)

# 3. Analyze Data
## Descriptive Statistics
print ('Descriptive Statistics')
print ('Dataset Dimensions ' + str(dataset.shape)) # 208 rows, 61 attributes including class

## Data types of each attribute
pandas.set_option('display.max_rows', 500)
print ('Data Types of each Attribute\n' + str(dataset.dtypes))

## Peek at first 20 rows of data
pandas.set_option('display.width', 100)
print ('First 20 rows of data\n' + str(dataset.head(20)))

## Summarize the distribution of each attribute
pandas.set_option('precision', 3)
print ('Distribution of each Attribute\n' + str(dataset.describe()))

## Distribution of Class Values
print ('Class Distribution\n' + str(dataset.groupby(60).size()))

## Unimodal Data Visualizations
### Histograms
dataset.hist(sharex=False, sharey=False, xlabelsize=1, ylabelsize=1)
# plt.show()

### Density Plots
dataset.plot(kind='density', subplots=True, layout=(8,8), sharex=False, legend=False, fontsize=1)
# plt.show()

### box and whisker plots
dataset.plot(kind='box', subplots=True, layout=(8,8), sharex=False, sharey=False, fontsize=1)
# plt.show()

## Multimodal Data Visualizations
### correlation matrix
fig = plt.figure()
ax = fig.add_subplot(111)
cax = ax.matshow(dataset.corr(), vmin=-1, vmax=1, interpolation='none')
fig.colorbar(cax)
# plt.show()

# 4. Validation Dataset
array = dataset.values
X = array[:,0:60].astype(float)
Y = array[:,60]
validation_size = 0.20
seed = 7
X_train, X_validation, Y_train, Y_validation = cross_validation.train_test_split(X, Y, test_size=validation_size, random_state=seed)

# 5. Evaluate Algorithms: Baseline
## Test options and evaluation metric
num_folds = 10
num_instances = len(X_train)
seed = 7
scoring = 'accuracy'

## Spot Check Algorithms
models = [] 
models.append(('LR', LogisticRegression())) 
models.append(('LDA', LinearDiscriminantAnalysis())) 
models.append(('KNN', KNeighborsClassifier())) 
models.append(('CART', DecisionTreeClassifier())) 
models.append(('NB', GaussianNB())) 
models.append(('SVM', SVC()))

results = []
names = []
for name, model in models:
    kfold = cross_validation.KFold(n=num_instances, n_folds=num_folds, random_state=seed)
    cv_results = cross_validation.cross_val_score(model, X_train, Y_train, cv=kfold, scoring=scoring)
    results.append(cv_results)
    names.append(name)
    msg = "%s: %f (%f)" % (name, cv_results.mean(), cv_results.std())
    print(msg)

# Visual Comparison of Algorithms 
fig = plt.figure()
fig.suptitle('Algorithm Comparison')
ax = fig.add_subplot(111)
plt.boxplot(results)
ax.set_xticklabels(names)
plt.show()