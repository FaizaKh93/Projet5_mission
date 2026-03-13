import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split,cross_validate
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.metrics import ConfusionMatrixDisplay, confusion_matrix, precision_recall_curve, average_precision_score, PrecisionRecallDisplay, roc_auc_score, classification_report,average_precision_score

#========================================================================================================
#========================================================================================================
#========================================================================================================
#========================================================================================================
def data_analyse(data: pd.DataFrame):

    #=========================================================
    # Fonction qui permet de faire une première analyse des fichiers de données
    #=========================================================
    
    print('Affichage des 5 premières lignes')
    display(data.head())    

    print('=============================================')
    print('Taille du fichier SIRH :',data.shape)
    
    print('=============================================')
    print('Analyse descriptive')
    display(data.describe())
    
    print('=============================================')
    print('Types de colonnes')
    display(data.info())

    cat_features = list(data.select_dtypes(include=['str']).columns)
    
    print('=============================================')
    print('Valeurs manquates :')
    print(data.isna().sum())

    return(cat_features)

 

#========================================================================================================
#========================================================================================================
#========================================================================================================
#========================================================================================================

def prepare_data(X: pd.DataFrame,
                 y: pd.Series,
                 num_features: list,
                 scale_X: bool = False, 
                 scale_y: bool = False,
                 scaler_type: str = "standard",   # "standard" ou "minmax"
                 test_size: float = 0.2,
                 random_state: int = 42,
                 stratify=None):
    
    #=========================================================
    # Fonction de préparation de données avec un scale des features numérique et split train/test
    #=========================================================
 
    # Toutes les autres colonnes déjà encodées
    OneHot_features = [col for col in X.columns if col not in num_features]
    
    # split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=random_state,stratify = stratify)
    
    
    # initialisation du scale
    Scaler = MinMaxScaler if scaler_type.lower() == "minmax" else StandardScaler
    scaler_X = Scaler() if scale_X else None
    scaler_y = Scaler() if scale_y else None

    # scale X
    if scale_X:
        #X_train_num = pd.DataFrame(scaler_X.fit_transform(X_train[num_features]))
        #X_test_num = pd.DataFrame(scaler_X.transform(X_test[num_features]))
        X_train_num =scaler_X.fit_transform(X_train[num_features])
        X_train_num = pd.DataFrame(X_train_num, columns=num_features,index=X_train.index)
        
        X_test_num = scaler_X.transform(X_test[num_features])
        X_test_num = pd.DataFrame(X_test_num,columns=num_features,index=X_test.index)

    else:
        X_train_num = X_train[num_features].copy()
        X_test_num = X_test[num_features].copy()

    # Reconstruction de X final
    X_train_final = pd.concat([X_train_num, X_train[OneHot_features]], axis=1)
    X_test_final = pd.concat([X_test_num, X_test[OneHot_features]], axis=1)
    

    # scale y
    if scale_y:
        y_train_final = scaler_y.fit_transform(y_train.values.reshape(-1, 1)).ravel()
        y_test_final = scaler_y.transform(y_test.values.reshape(-1, 1)).ravel()
    else:
        y_train_final = y_train.values
        y_test_final = y_test.values

    return X_train_final, X_test_final, y_train_final, y_test_final, scaler_X, scaler_y


#========================================================================================================
#========================================================================================================
#========================================================================================================
#========================================================================================================

def train_evaluate_model(model,
                         X_train,
                         X_test,
                         y_train,
                         y_test,
                         scaler_y=None,
                         plot=True,
                         title = None,
                         sample_weights=None):
    #=========================================================
    # Fonction d'entrainement et d'évaluation du modèle 
    #=========================================================
    
    # fit
    model.fit(X_train,y_train, sample_weight=sample_weights)
    
    #=================================
    # predict
    y_pred_train = model.predict(X_train) 
    y_pred_test = model.predict(X_test)    
    
    #=================================
    # y real inverse of y scale
    if scaler_y is not None:
        if scaler_y is np.log1p:
            y_train_real = np.expm1(np.array(y_train))
            y_test_real = np.expm1(np.array(y_test))
            y_pred_train_real = np.expm1(np.array(y_pred_train))
            y_pred_test_real = np.expm1(np.array(y_pred_test)) 
        else:
            y_train_real = scaler_y.inverse_transform(np.array(y_train).reshape(-1, 1)).ravel()
            y_test_real  = scaler_y.inverse_transform(np.array(y_test).reshape(-1, 1)).ravel()
            y_pred_train_real = scaler_y.inverse_transform(np.array(y_pred_train).reshape(-1, 1)).ravel()
            y_pred_test_real  = scaler_y.inverse_transform(np.array(y_pred_test).reshape(-1, 1)).ravel()
    else:
        y_train_real = np.array(y_train)
        y_test_real  = np.array(y_test)
        y_pred_train_real = np.array(y_pred_train)
        y_pred_test_real  = np.array(y_pred_test)
        
    #=================================
    #=================================
    # metrics
    #=================================
    #=================================
    
    #=================================
    # matrice de confusion
    #=================================
    cm = confusion_matrix(y_test_real, y_pred_test_real)
    disp = ConfusionMatrixDisplay(confusion_matrix=cm)
     
    # plot 
    fig1, ax1 = plt.subplots(figsize=(6, 5))
    disp.plot(values_format='d', 
          cmap='viridis',          
          colorbar=True,
          ax = ax1)
    ax1.set_title(f"Matrice de confusion - {model.__class__.__name__}")
    #plt.title(title if title else f"Matrice de confusion — {model.__class__.__name__}") 
    plt.grid(False)
    plt.savefig(f"matrice_confusion_{model.__class__.__name__}.png", dpi=300)
    #plt.show()

    #=================================
    # PR curve
    #=================================
    y_proba_test = model.predict_proba(X_test)[:, 1]
    y_proba_train = model.predict_proba(X_train)[:, 1]

    precision_test, recall_test, thresholds_test = precision_recall_curve(y_test_real, y_proba_test)
    #ap_score_test = average_precision_score(y_test, y_proba_test)
    precision_train, recall_train, thresholds_train = precision_recall_curve(y_train_real, y_proba_train)
    #ap_score_train = average_precision_score(y_train, y_proba_train)

    fig2, ax2 = plt.subplots(figsize=(6, 5))

   # plt.figure(figsize=(6, 5))
    ax2.plot(recall_test, precision_test,label='Test')
    ax2.plot(recall_train, precision_train,label='Train')
    plt.xlabel("Recall")
    plt.ylabel("Precision")
    ax2.set_title(f"Courbe Precision-Recall - {model.__class__.__name__}")
    #plt.title(plt.title(title if title else f"Courbe Precision-Recall — {model.__class__.__name__}")) 
    plt.legend()
    plt.grid(True)
    plt.savefig(f"PR_curve_{model.__class__.__name__}.png", dpi=300)

    #plt.show()

    #=================================
    # Classification report
    #=================================
    print('classification_report_train')
    print(classification_report(y_train_real, y_pred_train_real))
    print('classification_report_test')
    print(classification_report(y_test_real, y_pred_test_real))

    report_df = pd.DataFrame(classification_report(y_test_real, y_pred_test_real, output_dict=True)).transpose()
    #=================================
    # # plot tableau
    # fig, ax = plt.subplots(figsize=(6,3))
    # ax.axis('tight')
    # ax.axis('off')

    # # largeur des colonnes
    # col_widths = [0.1] * len(report_df.columns)

    # table = ax.table(cellText=report_df.round(2).values,
    #              colLabels=report_df.columns,
    #              rowLabels=report_df.index,
    #              colWidths=col_widths,
    #              loc='center')
    # table.scale(1.2, 1.5) 
    # plt.title("Classification Report")
    # plt.savefig(f"classification_report_{model.__class__.__name__}.png", dpi=300)
    # plt.show()
    #=================================
    print("ROC-AUC:", roc_auc_score(y_test_real, y_pred_test))
    print("PR-AUC:", average_precision_score(y_test_real, y_pred_test))


    #=================================
    #=================================
    # results    
    #=================================
    #=================================
    results = {'model': model}
               #'precision (test)': precision_test,
               #'precision (train)': precision_train,
               #'recall (test)': recall_test,
               #'recall (train)': recall_train}
    #=================================   
    return results, y_pred_test_real

#========================================================================================================
#========================================================================================================
#========================================================================================================
#========================================================================================================

def perform_cross_validation(
    X: pd.DataFrame,
    y: pd.Series,
    model,
    cross_val_type, # La variante de validation croisée que nous souhaitons utiliser
    scoring_metrics, # Metriques de notre choix
    return_estimator=False, # Si nous souhaitons stocker les modèles de chaque fold
    groups=None, # Nous verrons l’utilité de cet argument juste après 
    ):
#=========================================================
# Fonction qui implémente la fonction cross_validate et qui calcule les moyennes et écart-types des métriques choisies
#=========================================================    
    scores = cross_validate(
        model,
        X,
        y,
        cv=cross_val_type,
        return_train_score=True,
        return_estimator=return_estimator,
        scoring=scoring_metrics,
        groups=groups,
    )

    for metric in scoring_metrics:
        print(
            "Average Train {metric} : {metric_value}".format(
                metric=metric,
                metric_value=np.mean(scores["train_" + metric]),
            )
        )
        print(f"\n==========================================================")
        print(
            "Train {metric} Standard Deviation : {metric_value}".format(
                metric=metric, metric_value=np.std(scores["train_" + metric])
            )
        )
        print(f"\n==========================================================")

        print(
            "Average Test {metric} : {metric_value}".format(
                metric=metric, metric_value=np.mean(scores["test_" + metric])
            )
        )
        print(f"\n==========================================================")
        print(
            "Test {metric} Standard Deviation : {metric_value}".format(
                metric=metric, metric_value=np.std(scores["test_" + metric])
            )
        )
        print(f"\n==========================================================")

    return scores



def grid_around_best(value,step):
    #=========================================================
    # Fonction qui crée une petite grille autour d'une valeur donnée par RandomSearchCV
    #=========================================================
    if value is None:
        return [None]

    #step = 10 if value > 100 else 5

    grid = np.arange(max(1, value - step), value + step + 1,1)
    
    if value == 'min_samples_split':
        grid = np.arange(max(2, value - step), value + step + 1,1)
    
    if value == 'subsample':
        grid = np.arange(max(0, value - step/10), min(1,value + step/10),0.05)
    

    return grid
    