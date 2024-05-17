import streamlit as st
import os
import numpy as np
import pandas as pd
import scipy as sc
import matplotlib.pyplot as plt
import seaborn as sns
import pylab as pl

# from streamlit.components import AgGrid, GridOptionsBuilder  ## Manage grid output


# import mod_styles_app as style_app
import styles_app as styles_app  ## Module local créer pour le style de l'application
from sklearn.impute import KNNImputer
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt

from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix, accuracy_score, precision_score, recall_score, f1_score

# LOAD DATASET
def load_data():
    # Chemin du répertoire courant
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Chemin du dossier "_data" relatif au répertoire courant
    data_dir = os.path.join(current_dir, "_data")
    
    # Chemin complet du fichier de données
    data_file = os.path.join(data_dir, "Tab2.sas7bdat")
    
    # Définir les options d'affichage de Pandas
    pd.set_option('display.max_column', 18)
    
    # Charger les données
    dfp = pd.read_sas(data_file)
    return dfp


# MAIN FUNCTION
def main():
    # st.title("Predicting the creditworthiness of a bank's customers")
    st.markdown("<h1 style='text-align: center; color: grey;'>Predicting the Creditworthiness of Bank Customers</h1>", unsafe_allow_html=True)
    
    dfp = load_data()


    #---------------------------------------------------------------#
    # 1. Data Explorations
    #---------------------------------------------------------------#
    
    # Créer la sidebar
    sidebar = st.sidebar
    
    # Ajouter un grand titre dans la sidebar
    # sidebar.title("Sidebar Panel : ")

    # Ajouter un titre stylisé dans la sidebar
    sidebar.markdown("<h1 style='text-align: left; color: grey;'>Sidebar Panel : </h1>", unsafe_allow_html=True)

    #---------------------------#
    # Insertion de style CSS
    
    css_header = styles_app.input_css("style.css")
    st.markdown(f"<style>{css_header}</style>", unsafe_allow_html=True)
    st.markdown("""
    <div class="container">
        <div class="header">Titre du Conteneur</div>
        <div class="content">
            Ceci est un exemple de conteneur stylisé en utilisant du CSS dans une application Streamlit...
        </div>
    </div>
    """, unsafe_allow_html=True)
    #---------------------------#

    
    
    sidebar.subheader('Load Data')
    st.subheader('Variables Renaming : ')
    if st.sidebar.checkbox('data'):
        st.write("data :")
        st.write(dfp)

    dfp.rename(columns={'varA': 'Incident_r', 'varB': 'Montant_pret', 'varC': 'Montant_hypotheque',
    'varD': 'Val_propriete','varE': 'Motif_pret','varF': 'Profession',
    'varG': 'Nb_annees_travail','varH': 'Nb_report_pret', 'varI': 'Nb_litiges',
    'varJ': 'Age_cred','varK': 'Nb_demandes_cred','varL': 'Ratio_dette_revenu'}, inplace=True)
    
    if st.sidebar.checkbox('data after columns renamed'):
        st.write("data [renamed columns] :")
        st.write(dfp)
    
    sidebar.subheader('Descriptive Statistics')
    st.subheader('Descriptive Statistics : ')
    if st.sidebar.checkbox('shape'):
        st.write("shape :")
        st.write(dfp.shape)

    if st.sidebar.checkbox('dtypes'):
        st.write("dtypes :")
        st.write(dfp.dtypes)

    if st.sidebar.checkbox('value counts'):
        st.write(dfp["Incident_r"].value_counts(dropna = False))
        st.write(dfp["Motif_pret"].value_counts(dropna = False))
        st.write(dfp["Profession"].value_counts(dropna = False))

    dfp['Age_cred'] = round(dfp['Age_cred'] /12 ,2)


    sidebar.subheader('Data Explorations')
    st.subheader('Data Exploration (DE) : ')
    if st.sidebar.checkbox('descriptions'):
        st.write(dfp.describe(include="all"))

    if st.sidebar.checkbox('pie charts'):
        for col in dfp.select_dtypes('object'):
            st.write(f'{col :-<30} {dfp[col].unique()}')
            plt.figure()
            dfp[col].value_counts().plot.pie()
            st.pyplot()

    if st.sidebar.checkbox('count plots'):
        sns.countplot(x='Montant_pret', hue='Incident_r', data=dfp)
        st.pyplot()

    ## -----------------------------------------------------#
    # if st.sidebar.checkbox('missing values'):
    #     st.write(dfp.isna().any())
    #     st.write(dfp.isna().sum())

    if st.sidebar.checkbox('missing values'):
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader('Columns with missing values')
            st.write(dfp.isna().any())
            
        with col2:
            st.subheader('Number of missing values')
            st.write(dfp.isna().sum())
    #-------------------------------------------------------#


    if st.sidebar.checkbox('missing values percentage'):
        dfp_Na=pd.DataFrame({"Pourcentage_Na" : round(dfp.isnull().sum()/(dfp.shape[0])*100,2)})
        st.write(dfp_Na)

    if st.sidebar.checkbox('box plots'):
        for col in dfp.select_dtypes('float'):
            plt.figure()
            sns.boxplot(dfp[col])
            st.pyplot()

    if st.sidebar.checkbox('unique values'):
        for col in dfp.select_dtypes('object'):
            st.write(f'{col :-<30} {dfp[col].unique()}')

    if st.sidebar.checkbox('descriptive statistics before imputation'):
        cat_var_avant=dfp[['Motif_pret', 'Profession']]
        st.write(cat_var_avant.describe())
        st.write(dfp.describe())
        

    # Detection of outliers
    sidebar.subheader('Detection of outliers')
    if st.sidebar.checkbox('box plots for outlier detection'):
        st.subheader('Box Plots for Outlier Detection')
        for col in dfp.select_dtypes(include=np.number):
            st.write(f'Box plot for {col}')
            fig, ax = plt.subplots()
            ax.boxplot(dfp[col].dropna())
            st.pyplot()
    
    # Catching missing variables containing missing values
    sidebar.subheader('Missing values')
    if st.sidebar.checkbox('Missing values frequency'):
        st.subheader('Missing Values Frequency')
        missing_values_freq = dfp.isnull().sum() / len(dfp)
        st.write(missing_values_freq)
    
    if st.sidebar.checkbox('Impute missing values'):
        st.subheader('Imputation of Missing Values')
        st.write('Before imputation:')
        st.write(dfp.isnull().sum())

        # Imputation of missing values for numerical columns
        imputer = KNNImputer(n_neighbors=5)
        dfp[dfp.select_dtypes(include=np.number).columns] = imputer.fit_transform(dfp.select_dtypes(include=np.number))

        # Imputation of missing values for categorical columns
        for col in dfp.select_dtypes(include='object').columns:
            dfp[col].fillna(dfp[col].mode()[0], inplace=True)

        st.write('After imputation:')
        st.write(dfp.isnull().sum())

    sidebar.subheader('Correlation Analysis')
    st.subheader('Variable Correlation Analysis : ') 
    #  Transformation of Categorical Variables into Numeric variables to prepare the CORRELATION MATRIX (CM)
    if st.sidebar.checkbox('Transform categorical variables'):
        st.subheader('Transformation of Categorical Variables into Numeric variables')
        dfp = pd.get_dummies(dfp, drop_first=True)
        dfp.rename(columns=lambda x: x.replace("'", ""), inplace=True)
        st.write(dfp)

    if st.sidebar.checkbox('correlation matrix'):
        st.subheader('Correlation Matrix')
        corr = dfp.corr()
        fig, ax = plt.subplots(figsize=(10, 10))
        sns.heatmap(corr, annot=True, fmt=".2f", ax=ax, cmap='coolwarm')
        st.pyplot()

    if st.sidebar.checkbox('Analyze correlations'):
        st.subheader('Correlation Analysis')
        correlations = dfp.corr()['Incident_r'].sort_values(ascending=False)
        st.write(correlations)
    
    #-----------------------------------------------------------------------------#
    # Separate date into Train and Test datasets : prepraring data for predictions
    #-----------------------------------------------------------------------------#
    sidebar.subheader('Train and Test datasets')
    st.subheader('Dataset preparation: testing and training : ') 
    if st.sidebar.checkbox('Split data into training and test sets'):
        st.subheader('Splitting Data')
        X = dfp.drop('Incident_r', axis=1)
        y = dfp['Incident_r']
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        st.write('Training set:')
        st.write(X_train)
        st.write(y_train)
        st.write('Test set:')
        st.write(X_test)
        st.write(y_test)
        
        
    #------------------------------------------#
    # MODELIZATION : Train and evaluate models
    #-----------------------------------------#
    sidebar.subheader('Modelization : ')
    
    
    # MODELS EXPLANATIONS
    
    # Add a markdown area for the model explanations
    st.subheader('Reminder of models definitions') 
    
    #------------------------------------------------------------------------------------------------------------------------
    css_remind_def = styles_app.input_css("style.css")
    st.markdown(f"<style>{css_remind_def}</style>", unsafe_allow_html=True)
    st.markdown("""
    <div class="container">
        <div class="header">K-NN (K-Nearest Neighbors) : </div>
        <div class="content">
            <br>• Easy to understand and implement.
            <br>• No need to make assumptions about the distribution of data, making it useful for nonlinear data.
            <br>• The model does not require training, which can make learning fast.
            <br>Inconveniences:
            <br>• Prediction time may be slow for large datasets.
            <br>• Sensitive to irrelevant variables and the scale of data.
            <br>• It does not provide information on the importance of features.
        </div>
    </div>
    """, unsafe_allow_html=True)

    #------------------------------------------------------------------------------------------------------------------------
    
    

    ## TRAINING AND EVALUATING MODELS
    
    st.subheader('Training and Evaluating Models : ')
    if st.sidebar.checkbox('Train and evaluate models'):
        # Variable to predict (Or for SCORING ANALYSIS)
        # Separations between predictor and predicted variables.
        X = dfp.drop('Incident_r', axis=1)
        y = dfp['Incident_r']
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        models = {
            
            ### We need to fillna for missing values for (K-NN) and (Logistic Regression)   
            # (2 MODELS : 2 models left to test)
            # 'K-NN': KNeighborsClassifier(),
            # 'Logistic Regression': LogisticRegression(),
            
            'Decision Tree': DecisionTreeClassifier(),
            'Random Forest': RandomForestClassifier()
        }

        
        for name, model in models.items():
            model.fit(X_train, y_train)
            y_pred = model.predict(X_test)
            
            #--------------------------------------------------------------------------------#
            # # st.write(f'Model: {name}')
            # st.write(f'**Model:** {name}')  # Utilisation de ** pour rendre le texte en gras
            # st.write('Confusion matrix:')
            # st.write(confusion_matrix(y_test, y_pred))
            # st.write('Error rate:', 1 - accuracy_score(y_test, y_pred))
            # st.write('Precision:', precision_score(y_test, y_pred))
            # st.write('Recall:', recall_score(y_test, y_pred))
            # st.write('F1 score:', f1_score(y_test, y_pred))
            # st.write('Accuracy:', accuracy_score(y_test, y_pred))
            #--------------------------------------------------------------------------------#
            
            # Utilisation de st.markdown pour insérer du HTML avec le style CSS
            st.markdown(f"""
            <div class="container">
                <div class="header">{name}</div>
                <div class="content">
                    Error rate: {1 - accuracy_score(y_test, y_pred)}<br>
                    Precision: {precision_score(y_test, y_pred)}<br>
                    Recall: {recall_score(y_test, y_pred)}<br>
                    F1 score: {f1_score(y_test, y_pred)}<br>
                    Accuracy: {accuracy_score(y_test, y_pred)}
                </div>
            </div>
            """, unsafe_allow_html=True)
                
            st.write('Confusion matrix:')
            st.write(confusion_matrix(y_test, y_pred))
        

            # # Create a DataFrame for the model results
            # model_results = pd.DataFrame({
            #     'Model': [name],
            #     'Confusion matrix': [confusion_matrix(y_test, y_pred)],
            #     'Error rate': [1 - accuracy_score(y_test, y_pred)],
            #     'Precision': [precision_score(y_test, y_pred)],
            #     'Recall': [recall_score(y_test, y_pred)],
            #     'F1 score': [f1_score(y_test, y_pred)],
            #     'Accuracy': [accuracy_score(y_test, y_pred)]
            # })

            # # Display the DataFrame as a table in Streamlit
            # st.table(model_results)
        
        
        ## Features importances  ##
        sidebar.subheader('Features importances : ')
        st.subheader('Features importances : ')
        if name in ['Decision Tree', 'Random Forest']:
            st.write('Feature importances:')
            feature_importances = pd.Series(model.feature_importances_, index=X.columns)
            st.write(feature_importances.sort_values(ascending=False))
    
        
    #------------------------------------------#
    # MODELS : (Comparisons)
    #-----------------------------------------#
    # Select the best model
    # Explain models features importances
    
    
    #-------------------------------------------------------------------------------------------------#
    # TUNINGS : (Improve model performance by using only those variables that best explain the models)
    #-------------------------------------------------------------------------------------------------#
    # Improve model performance by using only those variables that best explain the models

    #------------------------------------------#
    # SCORING : (Predictions)
    #-----------------------------------------#
        


if __name__ == "__main__":
    main()
    
