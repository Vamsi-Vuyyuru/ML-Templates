# -*- coding: utf-8 -*-
"""ML Templates.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1RumGQrx_KrvJsvLCikacENp7s5GOCtQ_

# 0. Dependencies

- Below is for importing the dependencies
"""

# Commented out IPython magic to ensure Python compatibility.
import numpy as np                      # Implements multi-dimensional array and matrices
import pandas as pd                     # For data manipulation and analysis
import pandas_profiling
import matplotlib.pyplot as plt         # Plotting library for Python programming language and it's numerical mathematics extension NumPy
import seaborn as sns                   # Provides a high level interface for drawing attractive and informative statistical graphics
# %matplotlib inline
sns.set()

from subprocess import check_output

"""# 1. Feature Engineering
## 1.1 Removing skewness from the list of categorical columns

### 1.1.1 For continuous Data

- Below is the function for removing the skewness in each column from the provided list of columns of a dataset.
- The function  ```FtEngCon``` takes the inputs:
    - Target Dataset
    - List of all the skewed columns
    - Multiplier (what % of skewness of a column is allowed)
    - Prefix of the newly created balanced category.

- The function will find the value_counts of a column and then, take the lowest count categories based on the argument multiplier to form a new category.
- The newly created category will have prefix as per the input.
"""

hd = pd.read_csv('https://raw.githubusercontent.com/insaid2018/Term-2/master/Projects/house_data.csv')

# df is the target DataFrame
# lst is the list of columns that we want to be unskewed or equally distributed
# k is the multiplier by which skewness to be considered - range(0.01 to 0.99)
# pfx is the prefix for the newly created category


def FtEngCon(df,lst,k,pfx):
    for col in lst:
        pf = pfx
        ln = len(df[col])
        vlc = pd.DataFrame(df[col].value_counts())
        vlc['cats']=vlc.index
        
        
        for r in vlc[col]:
            if (r<(k*ln)):
                pf = pf + vlc[vlc[col]==r]['cats'][0]



        if (len(pf)<20):
            for t in vlc[col]:
                if (t<(k*ln)):
                    u = vlc[vlc[col]==t]['cats'][0]
                    df.loc[df[col]==u, col] = pf
            print('The new category of '+ col +' is '+ pf)


        elif (len(pf)>20):
            for e in vlc[col]:
                if (e<(k*ln)):
                    v = vlc[vlc[col]==e]['cats'][0]
                    df.loc[df[col]==v, col] = 'Others'
            print('The new category of '+ col +' is Others')

    return df

CatColList = ['MSZoning','Street','LotShape','LandContour','Utilities','LotConfig','LandSlope','Neighborhood',
              'Condition1','BldgType','HouseStyle','RoofStyle']

hdC_Dist = FtEngCon(df=hd,lst=CatColList, k=0.10, pfx='Skw_')

"""### 1.1.2 For Categorical Data

- Below is the function for removing the skewness in each column from the provided list of columns of a dataset.
- The function '''FtEngCat''' takes the inputs:
   - Target Dataset
   - List of all the skewed columns
   - Multiplier (what % of skewness of a column is allowed)
   - Supervision or Target Column.
- The function will find the value_counts of a column and then, take the lowest count categories based on the argument: multiplier.
- Next, It will check if that low count category is having supervision of only one class or both the classes(Ex: 0->Not Survived and 1-> Survived).

- The same will be applied on all the categories of that column.
- After the completion of one column, all the class-1 category are marked with respective supervision suffix and vice versa for class-2 category.
- If the category of a column is having supervision as both the classes then, It will be ignored.
- So The newly created categories will have sufix as combination of target column name and class (Ex: Sur0,Sur1).
"""

tt =pd.read_csv("https://raw.githubusercontent.com/insaid2018/Term-3/master/Data/CaseStudy/titanic_train.csv")
ttsplt=tt['Name'].str.split(", ", n=-1, expand = True)

ttsplt=ttsplt[1].str.split(".", n=-1, expand = True)
ttsplt[0].value_counts()
tt['Salutation']=ttsplt[0]

# df is the target DataFrame
# lst is the list of columns that we want to have unskewed or equally distributed
# k is the multiplier by which skewness to be considered - range(0.01 to 0.99)
# suprvsd - The Supervised column or the target column

def FtEngCat(df,lst,k,suprvsd):
    lsting1 = []
    lsting2= []
    for col in lst:
        #pf = pfx
        #print(pfx)
        ln = len(df[col])
        vlc = pd.DataFrame(df[col].value_counts())
        vlc['cats']=vlc.index
        #print(vlc.head(10))
        #for i in range(0,len(df[suprvsd].unique())-1):
         #   +str(i) = df[suprvsd].unique()[0]
            
        #spr1 = df[suprvsd].unique()[0]
        #spr2 = df[suprvsd].unique()[1]
        


        for r,y in zip(vlc[col],vlc['cats']):
            if (r<(k*ln)):
                dep = y
                if ((df[df[col]==dep][suprvsd].value_counts().count())==1):
                    if ((df[df[col]==dep][suprvsd].value_counts().index[0])==(df[suprvsd].unique()[0])):
                        lsting1.append(dep)
        
                    elif ((df[df[col]==dep][suprvsd].value_counts().index[0])==(df[suprvsd].unique()[1])):
                        lsting2.append(dep)
                        
                elif ((df[df[col]==dep][suprvsd].value_counts().count())==2):
                    pass
                    
        
        a = suprvsd[:3]+ str(df[suprvsd].unique()[1])
        b = suprvsd[:3]+ str(df[suprvsd].unique()[0])
        
        for i in lsting2:
            
            df[col] = df[col].replace(i,a)
            
        for j in lsting1:
            df[col] = df[col].replace(j,b)   
    
        print('The list of categories in the column ['+ col +'] with the supervision: '+ str(df[suprvsd].unique()[1])+' are '+str(lsting2))
        print('The list of categories in the column ['+ col +'] with the supervision: '+ str(df[suprvsd].unique()[0])+' are '+str(lsting1))
    return lsting1,lsting2, df

lsting1,lsting2, df = FtEngCat(df=tt,lst=['Salutation'],k=0.10,suprvsd='Survived')

df['Salutation'].value_counts()

"""## 1.2 Splitting the values of a column and adding all of them to a single column"""

md = pd.read_csv("https://raw.githubusercontent.com/insaid2018/Term-1/master/Data/Projects/1000%20movies%20data.csv")

# df is the target DataFrame
# col is the target column
# splitby - with what you want to split Ex: "," , ";" , "."


def splt(df,col,splitby):
  GenSplt = pd.DataFrame()
  GenSplt=df[col].str.split(splitby, n=-1, expand = True)
  

  GenOne = [] #pd.DataFrame() #columns=['SplitGenre']
  for clm in GenSplt.columns:
    GenOne.extend(GenSplt[clm])
  
  GenOne = pd.DataFrame(GenOne, columns=['Individual_'+col])
  GenOne = GenOne.dropna(axis = 0, how ='any')
  return GenOne

g = splt(df=md,col='Genre',splitby=",")

g





"""## Spare"""

def FtEng(df,lst,k,pfx):
  for col in lst:
    pf = pfx
    print(pfx)
    ln = len(df[col])
    vlc = pd.DataFrame(df[col].value_counts())
    vlc['cats']=vlc.index

    for r in vlc[col]:
      if (r<(k*ln)):
        pf = pf + vlc[vlc[col]==r]['cats'][0]

    
    print(pf)

    if (len(pf)<20):
      for t in vlc[col]:
        if (t<(k*ln)):
          u = vlc[vlc[col]==t]['cats'][0]
          df.loc[df[col]==u, col] = pf
    
    elif (len(pf)>20):
      for e in vlc[col]:
        if (e<(k*ln)):
          v = vlc[vlc[col]==e]['cats'][0]
          df.loc[df[col]==v, col] = 'Others'

  return df