# 🎲 Gerador de Dados (Data Generator)

Este módulo é responsável por gerar dados sintéticos realistas para simular um ambiente corporativo de RH e Ponto Eletrônico. Utilizando a biblioteca `Faker` com lógicas de negócio complexas para garantir que os dados tenham "sujeira" e padrões reais (atrasos, faltas, turnover, hierarquia de cargos).

## 📂 Estrutura dos Scripts

| Script | Função | Output |
|--------|--------|--------|
| `generate_employees.py` | Gera a carga inicial de funcionários (Dimensão). Utiliza pesos ponderados para criar uma pirâmide hierárquica realista (muitos técnicos, poucos gerentes). | `data/employees.csv` |
| `generate_attendance.py` | Gera o histórico de ponto (Fato) retroativo. Inclui lógica de dias úteis, escalas de fim de semana, atrasos e esquecimento de marcação. | `data/attendance.json` |
| `update_data.py` | Simula a passagem do tempo (Carga Incremental). Gera novos pontos a partir da última data e processa Turnover (demissões/contratações) baseado em taxa de Churn. | Atualiza os arquivos acima |

## 🛠️ Pré-requisitos

Certifique-se de ter o Python instalado e a biblioteca `Faker`:
```bash
pip install faker
```
## 🚀 Como Executar
A ordem de execução é crítica para manter a integridade referencial dos dados.

#### 1. Carga Inicial (Full Load)
Execute nesta ordem para criar a base do zero:

```bash
# 1. Gerar Funcionários
python src/data_generator/generate_employees.py

# 2. Gerar Histórico de Ponto
python src/data_generator/generate_attendance.py
```

#### 2. Simulação de Dia a Dia (Incremental)
Para simular a chegada de novos dados (D+1) e movimentações de RH:

```bash
# Atualiza pontos e processa demissões/contratações
python src/data_generator/update_data.py
```

## 🧠 Lógicas de Negócio Implementadas
- Pirâmide Hierárquica: A distribuição de cargos respeita pesos estatísticos (ex: 1 Gerente para cada 20 Operacionais).
- Salários Inteligentes: Faixas salariais compatíveis com o nível do cargo (Jr, Pleno, Sr, Gestão).
- Ruído de Dados:
	- Ponto: Ninguém bate ponto exatamente às 08:00:00. Há variações de minutos.
	- Falhas: **%** de chance de esquecer uma batida, pode ser ajustada na variável ```PROB_ESQUECER_PONTO = 0.02```. Atualmente em 2%.
	- Turnover: O script update_data.py demite funcionários ativos e contrata substitutos, mantendo o histórico para análises de SCD (Slowly Changing Dimensions).
Caso Somente a atualização de ponto seja necessária e o Turnover não, deve-se zerar a variável ```CHURN_RATE = 0.00```.
	- Escalas: **%** de chance de trabalho aos fins de semana, permitindo simular escalas longas (>7 dias), podendo ser ajustado na variável ```PROB_TRABALHO_FDS = 0.15```. Atualmente em 15%.

## 📊 Formatos de Saída
- Employees (.csv): Formato tabular padrão de sistemas legados de RH.
- Attendance (.json): Formato semi-estruturado simulando logs de relógios de ponto IoT ou APIs modernas.