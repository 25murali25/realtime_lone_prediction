import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split,GridSearchCV
from sklearn.preprocessing import MinMaxScaler,OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score,precision_score,recall_score,f1_score
import joblib

file_path = r"loan_dataset.csv"

class LoadDataset:
    def __init__(self,file_path):
        self.file_path = file_path
        
    def load_data(self):
        try:
            data = pd.read_csv(self.file_path)
            print('File is Sucessfullt loaded')
            return data
        except Exception as e:
            print('File is not Sucessfully loaded',e)
            return None 
        
class DataPreprocessing:
    def __init__(self,data):
        self.data = data 
        
    def preprocess_data(self):
        try:
            drop_columns = self.data.drop(columns = ['Loan_ID'],inplace = True)  
            print('Data is Sucessfully Preprocessed')
            return self.data
        except Exception as e:
            print('Data is not Sucessfully Preprocessed',e)
            return None
        
class TrainModel:
    def __init__(self,data):
        self.data = data
        
    def train_model(self):
        try:
            x = self.data.drop(['Loan_Status'], axis=1)
            y = self.data['Loan_Status'].str.strip().map({'Y':1,'N':0})
            
            x_train,x_test,y_train,y_test = train_test_split(x,y,test_size = 0.2,random_state = 42)
            num_cols = x.select_dtypes(include="number").columns
            cat_cols = x.select_dtypes(include="object").columns
            num_pipe = Pipeline([
                ('imputer', SimpleImputer(strategy='mean')),
                ('scaler',MinMaxScaler())
            ])
            
            cet_pipe = Pipeline([
                ('imputer', SimpleImputer(strategy='most_frequent')),
                ('encoder', OneHotEncoder(handle_unknown='ignore',sparse_output=False))
            ])
            
            preprocessor = ColumnTransformer([
                ('num',num_pipe,num_cols),
                ('cat',cet_pipe,cat_cols)
            ])
            
            pipe = Pipeline([
                ('preprocessor',preprocessor),
                ('model',LogisticRegression())
            ])
            
            para_grid = [
                {
                    'model':[LogisticRegression()],
                    'model__C':[0.1,1,10]
                },
                {
                    'model':[DecisionTreeClassifier()],
                    'model__max_depth':[3,5,7]
                },
                {
                    'model':[RandomForestClassifier()],
                    'model__n_estimators':[100,200],
                    'model__max_depth':[3,5,7]
                }
            ]
            
            grid = GridSearchCV(pipe,para_grid,cv = 5,n_jobs = -1,verbose = 2,scoring = 'accuracy')
            grid.fit(x_train,y_train)
            predict = grid.predict(x_test)
            import pickle
            with open("model.pkl", "wb") as f:
                pickle.dump(grid.best_estimator_, f)
            return self.data,predict,y_test
        except Exception as e:
            print('Model is not Sucessfully trained',e)
            return None, None, None, None
        
class Evalution:
    def __init__(self,predict,y_test):
        self.predict = predict
        self.y_test = y_test
        
    def evaltion(self):
        try:
            acc = accuracy_score(self.y_test,self.predict)
            pre = precision_score(self.y_test,self.predict)
            rec = recall_score(self.y_test,self.predict)
            f1 = f1_score(self.y_test,self.predict)
            return acc,pre,rec,f1
        except Exception as e:
            print('Evalution is not Sucessfully done',e)
            return None, None, None, None        
                                     
if __name__ == "__main__":
    result = LoadDataset(file_path).load_data()
    data_preprocessing = DataPreprocessing(result).preprocess_data()
    data,predict,y_test = TrainModel(data_preprocessing).train_model()
    print('no of columns',data.info())
    acc,pre,rec,f1 = Evalution(predict,y_test).evaltion()
    
