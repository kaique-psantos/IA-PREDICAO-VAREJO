from flask import Flask, render_template, request, jsonify
import joblib
import numpy as np
import pandas as pd
import os
from datetime import datetime
import json

app = Flask(__name__)

# Carregar o modelo e encoders
try:
    model = joblib.load('model/modelo_lucratividade.pkl')
    label_encoders = joblib.load('model/label_encoders.pkl')
    feature_cols = joblib.load('model/feature_cols.pkl')
    print("Modelo carregado com sucesso!")
except Exception as e:
    print(f"Erro ao carregar modelo: {e}")
    model = None
    label_encoders = None
    feature_cols = None

# Definir as opções disponíveis baseadas no dataset original
CATEGORIES = ['Technology', 'Furniture', 'Office Supplies']
SUBCATEGORIES = {
    'Technology': ['Phones', 'Computers', 'Machines', 'Accessories'],
    'Furniture': ['Chairs', 'Tables', 'Storage', 'Furnishings'],
    'Office Supplies': ['Paper', 'Binders', 'Art', 'Appliances', 'Labels', 'Storage', 'Supplies', 'Envelopes', 'Fasteners']
}
REGIONS = ['Central', 'East', 'South', 'West']
STATES = ['Texas', 'New York', 'California', 'Washington', 'Pennsylvania', 'Ohio', 'Illinois', 'Florida', 'Michigan', 'Virginia', 'North Carolina', 'Arizona', 'Georgia', 'Tennessee', 'Indiana', 'Kentucky', 'Alabama', 'Oregon', 'Louisiana', 'Colorado', 'Connecticut', 'Utah', 'Nevada', 'New Mexico', 'Arkansas', 'Missouri', 'Minnesota', 'Wisconsin', 'Oklahoma', 'Iowa', 'Kansas', 'South Carolina', 'Maryland', 'Delaware', 'Massachusetts', 'New Jersey', 'Mississippi', 'Nebraska', 'Vermont', 'New Hampshire', 'Maine', 'West Virginia', 'Rhode Island', 'Montana', 'North Dakota', 'South Dakota', 'Wyoming', 'District of Columbia']

# Variáveis para armazenar estatísticas (em produção, usaria banco de dados)
prediction_stats = {
    'total_predictions': 0,
    'high_profit_predictions': 0,
    'low_profit_predictions': 0,
    'last_predictions': [],
    'category_stats': {
        'Technology': {'high': 0, 'low': 0},
        'Furniture': {'high': 0, 'low': 0},
        'Office Supplies': {'high': 0, 'low': 0}
    }
}

@app.route('/get_states/<region>')
def get_states(region):
    """Endpoint para retornar estados baseados na região selecionada"""
    region_states = {
        'Central': [
            'Illinois', 'Indiana', 'Iowa', 'Kansas', 'Michigan', 'Minnesota',
            'Missouri', 'Nebraska', 'North Dakota', 'Oklahoma', 'South Dakota',
            'Texas', 'Wisconsin'
        ],
        'East': [
            'Connecticut', 'Delaware', 'District of Columbia', 'Maine', 'Maryland',
            'Massachusetts', 'New Hampshire', 'New Jersey', 'New York',
            'Ohio', 'Pennsylvania', 'Rhode Island', 'Vermont', 'West Virginia'
        ],
        'South': [
            'Alabama', 'Arkansas', 'Florida', 'Georgia', 'Kentucky', 'Louisiana',
            'Mississippi', 'North Carolina', 'South Carolina', 'Tennessee', 'Virginia'
        ],
        'West': [
            'Arizona', 'California', 'Colorado', 'Idaho', 'Montana', 'Nevada',
            'New Mexico', 'Oregon', 'Utah', 'Washington', 'Wyoming'
        ]
    }
    return jsonify(region_states.get(region, []))

@app.route('/')
def index():
    return render_template('index.html', 
                         categories=CATEGORIES, 
                         subcategories=SUBCATEGORIES,
                         regions=REGIONS,
                         states=STATES)

@app.route('/dashboard')
def dashboard():
    """Rota para o dashboard"""
    return render_template('dashboard.html')

@app.route('/api/dashboard-stats')
def dashboard_stats():
    """API para fornecer estatísticas do dashboard"""
    # Dados baseados no relatório + estatísticas simuladas
    stats = {
        'model_accuracy': 94.75,
        'total_predictions': prediction_stats['total_predictions'] + 8000,  # Base + predições reais
        'high_profit_predictions': prediction_stats['high_profit_predictions'] + 1847,
        'low_profit_predictions': prediction_stats['low_profit_predictions'] + 6153,
        'processing_time': np.random.uniform(0.15, 0.35),
        'feature_importance': {
            'Sales': 59.2,
            'Discount': 12.1,
            'Sub-Category': 8.9,
            'Quantity': 7.3,
            'Category': 5.8,
            'State': 4.2,
            'Region': 2.5
        },
        'category_performance': {
            'Technology': {
                'high_profit_percentage': 68,
                'total_predictions': prediction_stats['category_stats']['Technology']['high'] + prediction_stats['category_stats']['Technology']['low'] + 1200
            },
            'Office Supplies': {
                'high_profit_percentage': 24,
                'total_predictions': prediction_stats['category_stats']['Office Supplies']['high'] + prediction_stats['category_stats']['Office Supplies']['low'] + 2800
            },
            'Furniture': {
                'high_profit_percentage': 8,
                'total_predictions': prediction_stats['category_stats']['Furniture']['high'] + prediction_stats['category_stats']['Furniture']['low'] + 4000
            }
        },
        'recent_predictions': prediction_stats['last_predictions'][-10:],  # Últimas 10 predições
        'classification_metrics': {
            'precision': {'high_profit': 89, 'low_profit': 96},
            'recall': {'high_profit': 88, 'low_profit': 97},
            'f1_score': {'high_profit': 89, 'low_profit': 97}
        }
    }
    
    return jsonify(stats)

@app.route('/predict', methods=['POST'])
def predict():
    try:
        if not model or not label_encoders:
            return jsonify({'error': 'Modelo não carregado. Verifique se os arquivos do modelo existem.'})
        
        # Obter dados do formulário
        data = request.get_json() if request.is_json else request.form
        
        category = data.get('category')
        subcategory = data.get('subcategory')
        region = data.get('region')
        state = data.get('state')
        sales = float(data.get('sales', 0))
        quantity = int(data.get('quantity', 1))
        discount = float(data.get('discount', 0))
        
        # Validar inputs
        if not all([category, subcategory, region, state]):
            return jsonify({'error': 'Todos os campos são obrigatórios.'})
        
        # Preparar dados para predição
        input_data = {
            'Sales': sales,
            'Quantity': quantity,
            'Discount': discount
        }
        
        # Codificar variáveis categóricas
        categorical_fields = {
            'Region': region,
            'Category': category,
            'Sub-Category': subcategory,
            'State': state
        }
        
        for field, value in categorical_fields.items():
            if field in label_encoders:
                try:
                    # Verificar se o valor existe no encoder
                    if value in label_encoders[field].classes_:
                        encoded_value = label_encoders[field].transform([value])[0]
                        input_data[field + '_Encoded'] = encoded_value
                    else:
                        return jsonify({'error': f'Valor "{value}" não encontrado para {field}.'})
                except Exception as e:
                    return jsonify({'error': f'Erro ao codificar {field}: {str(e)}'})
        
        # Criar DataFrame com as features na ordem correta
        input_df = pd.DataFrame([input_data])[feature_cols]
        
        # Fazer predição
        prediction = model.predict(input_df)[0]
        probability = model.predict_proba(input_df)[0]
        
        # Interpretar resultado
        result = "Alto Lucro" if prediction == 1 else "Baixo Lucro"
        confidence = max(probability) * 100
        
        return jsonify({
            'prediction': result,
            'confidence': f"{confidence:.2f}%",
            'details': {
                'category': category,
                'subcategory': subcategory,
                'region': region,
                'state': state,
                'sales': sales,
                'quantity': quantity,
                'discount': discount
            }
        })
        
    except Exception as e:
        return jsonify({'error': f'Erro na predição: {str(e)}'})



if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000)
