# 📊 HR Analytics Data Lakehouse

> Um pipeline de dados End-to-End para análise de People Analytics, utilizando arquitetura Medallion, AWS e Databricks.

![Status](https://img.shields.io/badge/Status-Em_Desenvolvimento-yellow)
![Python](https://img.shields.io/badge/Python-14354C?style=flat&logo=python&logoColor=white)
![Terraform](https://img.shields.io/badge/IaC-Terraform-purple)
![AWS](https://img.shields.io/badge/Cloud-AWS-orange)

## 🎯 Objetivo do Projeto
Este projeto visa construir um **Data Lakehouse** para o departamento de Recursos Humanos. O objetivo é monitorar indicadores críticos como:
- Banco de Horas e Horas Extras.
- Frequência e Absenteísmo.
- Escalas de Trabalho.

A solução implementa um pipeline completo, desde a ingestão de dados brutos até a disponibilização de KPIs para dashboards, garantindo governança, qualidade e escalabilidade.

---
## Arquitetura da Solução

O fluxo de dados foi desenhado para simular um ambiente corporativo real:

1.  **Geração de Dados (Source):** Scripts Python geram dados sintéticos complexos (JSON/CSV) simulando sistemas de RH e relógios de ponto IoT.
2.  **Ingestão (Bronze):** Carga dos dados brutos no Data Lake (S3/DBFS).
3.  **Refinamento (Silver):** Limpeza, deduplicação, tratamento de tipos e regras de negócio (ex: cálculo de horas trabalhadas).
4.  **Agregação (Gold):** Tabelas modeladas (Star Schema) prontas para BI e Analytics.

--- 

## 🚀 Roadmap do Projeto

Abaixo, o status atual do desenvolvimento:

- [x] **Módulo de Geração de Dados**
    - [x] Script de Funcionários (Lógica de Pirâmide Hierárquica)
    - [x] Script de Ponto Eletrônico (Simulação de atrasos, faltas e escalas)
    - [x] Script de Carga Incremental (Turnover e Atualização Diária)
- [ ] **Ingestão de Dados (Camada Bronze)**
    - [ ] Configuração do Databricks/S3
    - [ ] Ingestão de CSV e JSON (Autoloader/Copy Into)
- [ ] **Processamento (Camada Silver)**
    - [ ] Tratamento de Schema e Qualidade de Dados
    - [ ] Explode de JSONs aninhados
    - [ ] Regras de Negócio (Cálculo de Jornada)
- [ ] **Modelagem (Camada Gold)**
    - [ ] Criação de Fatos e Dimensões
    - [ ] KPIs de RH
- [ ] **Orquestração & Dataviz**
    - [ ] Dashboards

---
## 🛠️ Tech Stack
|Categoria|Tecnologias|
|---------|-----------|
|Linguagem|Python 3.10, SQL|
|Cloud Provider|AWS (S3, Glue, IAM)
|Infra as Code|Terraform|
|Processamento|Apache Spark (PySpark), Delta Lake|
|Orquestração|Apache Airflow (via Astronomer)|
|Data Warehouse|Snowflake (Planejado)|
|Qualidade de Dados|Great Expectations (Planejado)|

---
## 📂 Estrutura do Repositório
```hr-analytics-pipeline/
├── astro_airflow/      # Orquestração (DAGs do Airflow)
├── infrastructure/     # Código Terraform (IaC)
├── src/                # Scripts Python e Spark
│   ├── data_generator/ # Simulação de dados de RH
│   └── glue_jobs/      # Jobs de ETL
├── notebooks/          # Sandbox para exploração (Databricks)
└── tests/              # Testes unitários
```

## 🎲 Como gerar os dados
Para gerar a massa de dados inicial, acesse a documentação específica do módulo:
[📖 Ir para Documentação do Gerador de Dados](./src/data_generator/README.md)

---
**Desenvolvido por Michael Cruz como parte do portfólio de Engenharia de Dados.**