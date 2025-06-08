        const featureImportanceData = {
            labels: ['Sales', 'Discount', 'Sub-Category', 'Quantity', 'Category', 'State', 'Region'],
            datasets: [{
                label: 'Importância (%)',
                data: [59.2, 12.1, 8.9, 7.3, 5.8, 4.2, 2.5],
                backgroundColor: [
                    '#4f46e5', '#7c3aed', '#06b6d4', '#10b981', 
                    '#f59e0b', '#ef4444', '#8b5cf6'
                ],
                borderWidth: 0,
                borderRadius: 8
            }]
        };

        const predictionDistributionData = {
            labels: ['Alto Lucro', 'Baixo Lucro'],
            datasets: [{
                data: [23, 77],
                backgroundColor: ['#10b981', '#f59e0b'],
                borderWidth: 0
            }]
        };

        const categoryPerformanceData = {
            labels: ['Technology', 'Office Supplies', 'Furniture'],
            datasets: [{
                label: 'Alto Lucro (%)',
                data: [68, 24, 8],
                backgroundColor: '#10b981',
                borderRadius: 8
            }, {
                label: 'Baixo Lucro (%)',
                data: [32, 76, 92],
                backgroundColor: '#f59e0b',
                borderRadius: 8
            }]
        };

        const classificationMetricsData = {
            labels: ['Precisão', 'Recall', 'F1-Score'],
            datasets: [{
                label: 'Alto Lucro',
                data: [89, 88, 89],
                backgroundColor: '#10b981',
                borderRadius: 8
            }, {
                label: 'Baixo Lucro',
                data: [96, 97, 97],
                backgroundColor: '#4f46e5',
                borderRadius: 8
            }]
        };

        // Configuração dos gráficos
        const chartOptions = {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: {
                        padding: 20,
                        usePointStyle: true
                    }
                }
            }
        };

        // Inicializar gráficos
        function initCharts() {
            // Gráfico de Importância das Features
            new Chart(document.getElementById('featureImportanceChart'), {
                type: 'bar',
                data: featureImportanceData,
                options: {
                    ...chartOptions,
                    indexAxis: 'y',
                    scales: {
                        x: {
                            beginAtZero: true,
                            max: 70
                        }
                    }
                }
            });

            // Gráfico de Distribuição de Previsões
            new Chart(document.getElementById('predictionDistributionChart'), {
                type: 'doughnut',
                data: predictionDistributionData,
                options: {
                    ...chartOptions,
                    cutout: '60%'
                }
            });

            // Gráfico de Performance por Categoria
            new Chart(document.getElementById('categoryPerformanceChart'), {
                type: 'bar',
                data: categoryPerformanceData,
                options: {
                    ...chartOptions,
                    scales: {
                        y: {
                            beginAtZero: true,
                            max: 100
                        }
                    }
                }
            });

            // Gráfico de Métricas de Classificação
            new Chart(document.getElementById('classificationMetricsChart'), {
                type: 'radar',
                data: classificationMetricsData,
                options: {
                    ...chartOptions,
                    scales: {
                        r: {
                            beginAtZero: true,
                            max: 100
                        }
                    }
                }
            });   

        }  

        
        // Funções de interação
        function goToPredictor() {
            window.location.href = '/';
        }   

        

        function showScenarioDetails(scenario) {
            const scenarios = {
                'tech-high': {
                    title: 'Technology + Vendas Altas',
                    details: 'Produtos de tecnologia com vendas acima de $2000 e desconto menor que 10% têm 89% de chance de alto lucro.'
                },
                'furniture-discount': {
                    title: 'Furniture + Desconto Alto',
                    details: 'Móveis com desconto superior a 20% apresentam 76% de probabilidade de baixo lucro devido à menor margem.'
                },
                'office-medium': {
                    title: 'Office Supplies Médio',
                    details: 'Materiais de escritório na faixa de $500-1500 com desconto moderado têm boa probabilidade de lucro.'
                },
                'low-sales': {
                    title: 'Vendas Baixas',
                    details: 'Vendas abaixo de $200 raramente resultam em alto lucro, independente da categoria.'
                }
            };

            const info = scenarios[scenario];
            alert(`${info.title}\n\n${info.details}\n\nClique em "Fazer Previsão" para testar cenários específicos!`);
        }

        // Animações de entrada
        function animateMetrics() {
            const cards = document.querySelectorAll('.metric-card');
            cards.forEach((card, index) => {
                card.style.opacity = '0';
                card.style.transform = 'translateY(20px)';
                
                setTimeout(() => {
                    card.style.transition = 'all 0.6s ease';
                    card.style.opacity = '1';
                    card.style.transform = 'translateY(0)';
                }, index * 100);
            });
        }

        // Inicializar dashboard
        document.addEventListener('DOMContentLoaded', function() {
            initCharts();
            animateMetrics();

        });

        // Atualização automática das métricas a cada 30 segundos (simulação)
        setInterval(() => {
            const processingTime = document.getElementById('processingTime');
            const times = ['0.19s', '0.21s', '0.23s', '0.25s', '0.27s'];
            processingTime.textContent = times[Math.floor(Math.random() * times.length)];
        }, 30000);