# -*- coding: utf-8 -*-
"""Predictive_Analysis_Liver_Disease.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/15b_n1B_nGwrpKwOE4DXSTJ-KNI-qKc5j
"""

from google.colab import files
files.upload()

!ls

!pip install lifelines

# Commented out IPython magic to ensure Python compatibility.
import pandas as pd
import numpy as np
import missingno
from sklearn.preprocessing import LabelEncoder,OneHotEncoder
#from lifelines import KaplanMeierFitter
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier, BaggingClassifier
from sklearn.svm import SVC, LinearSVC
from sklearn.tree import DecisionTreeClassifier
import matplotlib.pyplot as plt
import seaborn as sns
# %matplotlib inline
plt.style.use('ggplot')

from sklearn.metrics import classification_report,confusion_matrix

df = pd.read_csv('datasets_2607_4342_indian_liver_patient.csv')
df.head()

"""**EDA**"""

df.info()

df.describe(include='all')

df.Gender.unique()

df.nunique() #gender and target is categorical.

df.rename(columns={'Dataset':'Target'}, inplace=True)
df['Target'] = df['Target'].apply(lambda x: 0 if x==2 else 1)
df['Gender'] = df['Gender'].apply(lambda x: 0 if x=='Male' else 1)

df.iloc[0,:]

df.columns[df.isnull().any()].tolist()

sns.distplot(df['Albumin_and_Globulin_Ratio'])
plt.show()

df['Albumin_and_Globulin_Ratio'] = df['Albumin_and_Globulin_Ratio'].fillna(df['Albumin_and_Globulin_Ratio'].mean())

df.isna().sum()

df.Target.value_counts()

df.corr()["Target"]

pd.crosstab(df.Gender, df.Target).plot(kind="bar",figsize=(15,6))
plt.title('Liver Disease Frequency by Gender')
plt.xlabel('Sex ( 0 = Male , 1 = Female)')
plt.legend(["Liver Disease : No", "Liver Disease : Yes"])
plt.ylabel('Frequency')
plt.show()

pd.crosstab(df.Age, df.Target).plot(kind="bar",figsize=(20,6))
plt.title('Liver Disease Frequency by Age')
plt.xlabel('Age')
plt.legend(["Liver Disease : No", "Liver Disease : Yes"])
plt.ylabel('Frequency')
plt.show()

pd.crosstab(df.Gender, df.Target, aggfunc='mean', values=df['Total_Protiens']).plot(kind="bar",figsize=(20,6))
#plt.title('Liver Disease Frequency by Gender')
plt.xlabel('Gender')
plt.legend(["Liver Disease : No", "Liver Disease : Yes"])
plt.ylabel('Mean Protein')
plt.show()

df.columns

pd.crosstab(df.Gender, df.Target, aggfunc='mean', values=df['Total_Bilirubin']).plot(kind="bar",figsize=(20,6))
plt.xlabel('Gender')
plt.legend(["Liver Disease : No", "Liver Disease : Yes"])
plt.ylabel('Mean Total Bilirubin')
plt.show()

pd.crosstab(df.Gender, df.Target, aggfunc='mean', values=df['Alamine_Aminotransferase']).plot(kind="bar",figsize=(20,6))
plt.xlabel('Gender')
plt.legend(["Liver Disease : No", "Liver Disease : Yes"])
plt.ylabel('Mean Alamine_Aminotransferase')
plt.show()

pd.crosstab(df.Gender, df.Target, aggfunc='mean', values=df['Albumin_and_Globulin_Ratio']).plot(kind="bar",figsize=(20,6))
plt.xlabel('Gender')
plt.legend(["Liver Disease : No", "Liver Disease : Yes"])
plt.ylabel('Mean Albumin_and_Globulin_Ratio')
plt.show()

df.head(2)

df.columns

cols = ['Total_Bilirubin', 'Direct_Bilirubin',
       'Alkaline_Phosphotase', 'Alamine_Aminotransferase',
       'Aspartate_Aminotransferase', 'Total_Protiens', 'Albumin',
       'Albumin_and_Globulin_Ratio']

fig, ax = plt.subplots(4, 2, figsize=(15, 20))
d=0

for i in range(len(ax)):
  for j in range(2):
    sns.scatterplot(x='Age', y=cols[d], hue='Target', data=df, ax=ax[i][j])
    d+=1
plt.show()

df_corr = df.corr()
plt.figure(figsize=(20, 10))
sns.heatmap(df_corr, cbar = True,  square = True,  annot=True, fmt= '.2f',annot_kws={'size': 10},
           cmap= 'coolwarm')
plt.title('Correlation between features')

df.columns

df.drop(columns=["Total_Bilirubin","Alamine_Aminotransferase","Albumin"],axis=1,inplace=True) # high correlation hence removed

plt.figure(figsize=(25,7))
sns.boxplot(data=df,)

df["log_Alkaline_Phosphotase"]=np.log10(df["Alkaline_Phosphotase"])
df["log_Aspartate_Aminotransferase"]=np.log10(df["Aspartate_Aminotransferase"])

plt.figure(figsize=(25,7))
sns.boxplot(data=df,)

df.drop(columns=["Aspartate_Aminotransferase","Alkaline_Phosphotase"],axis=1,inplace=True)

plt.figure(figsize=(25,7))
sns.boxplot(data=df,)

X = df.drop('Target',axis=1)
y = df['Target']
df.head(2)

X.head(2)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=123)
print (X_train.shape)
print (y_train.shape)
print (X_test.shape)
print (y_test.shape)

from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

def model_fit(m):
  
  pipe = Pipeline(steps=[('Scaler', StandardScaler()), ('Classifier', m)])
  pipe.fit(X_train, y_train)

  preds = pipe.predict(X_test)
  
  try :
    for name, importance in zip(X_train.columns, m.feature_importances_):
        print(name, "=", importance)
  except :
    print("Not applicable")
  print("-------")    
  print('Classification Report: \n', classification_report(y_test, preds))
  tn, fp, fn, tp = confusion_matrix(y_test, preds).ravel()
  print((tn, fp, fn, tp))
  sns.heatmap(confusion_matrix(y_test,preds),annot=True,fmt="d")

model_fit(LogisticRegression(class_weight='balanced', random_state=42))

model_fit(RandomForestClassifier(n_estimators=100, random_state=42,class_weight="balanced"))

#adaboost, baggingclf, DT, SVC, LinearSVC
model_fit(AdaBoostClassifier(n_estimators=1000, random_state=123))
#tn, fp, fn, tp

model_fit(BaggingClassifier(n_estimators=100, random_state=123))
#tn, fp, fn, tp

model_fit(SVC(random_state=123))
#tn, fp, fn, tp

model_fit(LinearSVC(max_iter=5000,random_state=123))

# can tune and choose model or just select from choices above

