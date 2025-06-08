# Relatório de Desenvolvimento de um Sistema de Previsão de Lucratividade de uma Loja de Varejo

**Autor:** Kaíque Pereira dos Santos  
**Local:** Paulo Afonso/BA  
**Data:** Maio/2025  
**Instituição:** Centro Universitário do Rio São Francisco - Unirios  
**Disciplina:** Inteligência Artificial  
**Orientador:** Prof. Me. Douglas Costa Braga

---

## Sumário
1. [Introdução](#1-introdução)  
2. [Metodologia](#2-descrição-da-metodologia-adotada)  
3. [Justificativa do Algoritmo](#3-justificativa-para-a-escolha-do-algoritmo)  
4. [Resultados](#4-resultados-obtidos-com-interpretações)  
    - 4.1 [Interpretação dos Resultados](#41-interpretação-dos-resultados)  
5. [Insights de Negócio](#5-insights-de-negócio-extraídos)  
6. [Limitações e Trabalhos Futuros](#6-limitações-e-trabalhos-futuros)

---

## 1. Introdução
Desenvolvimento de um sistema de Machine Learning com interface web para prever a lucratividade de vendas no varejo.

---

## 2. Descrição da Metodologia Adotada

1. **Análise e preparação dos dados**  
   - Dataset: SampleSuperstore.csv (Kaggle)  
   - Limpeza: remoção de valores ausentes  

2. **Engenharia de features**  
   - Criação da variável-alvo binária `High_Profit` com base no 75º percentil do lucro.

3. **Codificação de variáveis categóricas**  
   - Utilização do `LabelEncoder` em atributos como `Region`, `Category`, `Sub-Category` e `State`.

4. **Treinamento e validação do modelo**  
   - Divisão: 80% treino / 20% teste  
   - Features: `Sales`, `Quantity`, `Discount`, variáveis categóricas codificadas

5. **Interface Web (Flask)**  
   - Input de dados pelo usuário e retorno de previsões com confiança.

---

## 3. Justificativa para a Escolha do Algoritmo

- **Modelos de regressão testados:**  
  - Decision Tree Regressor (R²: -0.54 a -0.70)  
  - Random Forest Regressor (R²: -0.12)  
  - Gradient Boosting Regressor (R²: -0.004)  
  - → Resultados ruins (R² negativos)

- **Mudança para Classificação:**  
  - Algoritmo escolhido: **Random Forest Classifier**  
  - Motivos:
    - Robustez contra overfitting
    - Alta acurácia
    - Capacidade de análise de importância das variáveis

---

## 4. Resultados Obtidos com Interpretações

- **Acurácia geral:** 94,75%  
- **Matriz de Confusão:**  
  - Verdadeiros Negativos (0): 1480  
  - Verdadeiros Positivos (1): 414  
  - Falsos Positivos: 49  
  - Falsos Negativos: 56

- **Métricas:**

| Classe | Precisão | Recall | F1-Score | Suporte |
|--------|----------|--------|----------|---------|
| 0 (Baixo Lucro) | 0.96 | 0.97 | 0.97 | 1529 |
| 1 (Alto Lucro)  | 0.89 | 0.88 | 0.89 | 470  |
| Média Ponderada | 0.95 | 0.95 | 0.95 | 1999 |

### 4.1 Interpretação dos Resultados
- **Classe 1 (Alto Lucro):**  
  - Precisão: 89%  
  - Recall: 88%  

- **Classe 0 (Baixo Lucro):**  
  - Excelente performance, crucial para evitar decisões não lucrativas.

---

## 5. Insights de Negócio Extraídos

- **Fatores mais influentes:**  
  - `Sales` (vendas) e `Discount` (desconto)  
  - Sensibilidade da lucratividade aos descontos aplicados

- **Importância de produto e localização:**  
  - `Sub-Category`, `Category` e `State` influenciam a lucratividade

- **Aplicação prática:**  
  - Interface web pode ser usada para simular cenários antes de promoções

---

## 6. Limitações e Trabalhos Futuros

- **Definição relativa de lucro:**  
  - Baseada em percentil; futuro: metas absolutas (KPIs)

- **Ausência de análise temporal:**  
  - Futuro: modelos de séries temporais

- **Features avançadas não incluídas:**  
  - CLV, dados demográficos, concorrência, etc.

---
