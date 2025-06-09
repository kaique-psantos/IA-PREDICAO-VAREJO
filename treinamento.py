import os
import base64
from io import StringIO
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from IPython.display import Image
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier, plot_tree, export_graphviz
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
import joblib

# Carregar o dataset
print("Carregando o dataset...")
file_path = 'data/SampleSuperstore.csv'
df = pd.read_csv(file_path)

# Exibir primeiras linhas do dataset
print("\nPrimeiras linhas do dataset:")
print(df.head())

# Preparar os dados
print("\nPreparando os dados...")

df_clean = df.dropna() # Remove linhas com valores nulos


# Criar variável binária de alta lucratividade com base no 75º percentil do lucro
threshold = df['Profit'].quantile(0.75)
df['High_Profit'] = (df['Profit'] >= threshold).astype(int)

# Codificar variáveis categóricas
categorical_cols = ['Region', 'Category', 'Sub-Category', 'State']
label_encoders = {}

for col in categorical_cols:
    le = LabelEncoder()
    df[col + '_Encoded'] = le.fit_transform(df[col])
    label_encoders[col] = le
    print(f"{col} - Mapeamento de códigos:")
    for key, val in zip(le.classes_, le.transform(le.classes_)):
        print(f"  {key}: {val}")
    print()

# Selecionar features para o modelo
feature_cols = ['Sales', 'Quantity', 'Discount'] + [col + '_Encoded' for col in categorical_cols]
X = df[feature_cols]
y = df['High_Profit']

# Dividir dados em treino e teste
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Treinar modelo Random Forest
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Previsões e avaliação
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
report = classification_report(y_test, y_pred)

# Exibir resultados
print(f"Acurácia do modelo: {accuracy:.4f}\n")
print("Relatório de Classificação:")
print(report)

# Importância das features
feature_importance = pd.DataFrame({
    'Feature': X.columns,
    'Importance': model.feature_importances_
}).sort_values('Importance', ascending=False)

# Plotar importância das features
plt.figure(figsize=(10, 6))
sns.barplot(x='Importance', y='Feature', data=feature_importance, palette='viridis')
plt.title('Importância das Features')
plt.xlabel('Importância')
plt.ylabel('Features')
plt.tight_layout()
plt.savefig('images/features_dt.png')
#plt.show()


plt.figure(figsize=(8, 6))
cm = confusion_matrix(y_test, y_pred)
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
            xticklabels=model.classes_, 
            yticklabels=model.classes_)
plt.xlabel('Previsão')
plt.ylabel('Valor Real')
plt.title('Matriz de Confusão')
plt.tight_layout()
plt.savefig('images/confusion_matrix_dt.png')
print("\nMatriz de confusão salva como 'images/confusion_matrix_dt.png'")


# Extrair uma árvore individual da floresta
estimator = model.estimators_[0]  # Pega a primeira árvore da floresta

# Visualizar a árvore de decisão individual
plt.figure(figsize=(20, 10))
plot_tree(estimator, filled=True, feature_names=X.columns, 
          class_names=['Baixo Lucro', 'Alto Lucro'], rounded=True)
plt.title('Árvore de Decisão - Estimador 0 da Random Forest')
plt.tight_layout()
plt.savefig('images/decision_tree.png')
print("\nÁrvore de decisão salva como 'images/decision_tree.png'")


# 8. Exportar a árvore para visualização gráfica usando graphviz
dot_data = export_graphviz(
    estimator, 
    out_file=None, 
    feature_names=X.columns,
    class_names=['Baixo Lucro', 'Alto Lucro'],
    filled=True, 
    rounded=True,
    special_characters=True
)

# Salvar como arquivo DOT
with open('images/decision_tree.dot', 'w') as f:
    f.write(dot_data)
    
    
    # Exportar o modelo
joblib.dump(model, 'model/modelo_lucratividade.pkl')

# Exportar os codificadores
joblib.dump(label_encoders, 'model/label_encoders.pkl')

# Exportar as colunas utilizadas como features
joblib.dump(feature_cols, 'model/feature_cols.pkl')

print("Modelo e codificadores salvos com sucesso!")