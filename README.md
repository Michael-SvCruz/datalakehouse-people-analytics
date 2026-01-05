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

1.  **Geração de Dados (Source):** Scripts Python geram dados sintéticos complexos (JSON/CSV) simulando sistemas de RH e relógios de ponto IoT. Os arquivos são gerados com versionamento por timestamp (`employees_20251217_1000.csv`).
2.  **Ingestão (Bronze):** Ingestão via **Databricks Autoloader** (`cloudFiles`).
    - Utiliza **Spark Structured Streaming** em modo `AvailableNow` (Batch).
    - Schema Evolution e Schema Inference ativados.
    - Armazena histórico completo (Full Snapshot Append-Only).
3.  **Refinamento (Silver):** (Em breve) Limpeza, deduplicação (Merge), tratamento de tipos e regras de negócio.
4.  **Agregação (Gold):** (Em breve) Tabelas modeladas (Star Schema) prontas para BI e Analytics.


--- 

## 🚀 Roadmap do Projeto

Abaixo, o status atual do desenvolvimento:

- [x] **Módulo de Geração de Dados**
    - [x] Script de Funcionários (Lógica de Pirâmide Hierárquica)
    - [x] Script de Ponto Eletrônico (Simulação de atrasos, faltas e escalas)
    - [x] Script de Carga Incremental (Turnover e Atualização Diária)
- [x] **Ingestão de Dados (Camada Bronze)**
    - [x] Configuração do Unity Catalog e Volumes
    - [x] Pipeline de Ingestão com Autoloader (CSV e JSON)
    - [x] Captura de Metadados (`_metadata.file_path`, `data_ingestao`)
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
|Cloud Provider|AWS (S3, Glue, IAM, Databricks Community)
|Infra as Code|Terraform|
|Processamento|Apache Spark (PySpark), Delta Lake|
|Catálogo de Dados|Unity Catalog|
|Orquestração|Apache Airflow (via Astronomer), Databricks Workflows (Planejado)|
|Data Warehouse|Snowflake (Planejado)|
|Qualidade de Dados|Great Expectations (Planejado)|

---
## 📂 Estrutura do Repositório
```hr-analytics-pipeline/
├── astro_airflow/      # (Em breve) Orquestração (DAGs do Airflow)
├── infrastructure/     # Código Terraform (IaC)
├── src/                # Scripts Python e Spark
│   ├── data_generator/ # Simulação de dados de RH
│   ├── 00-bronze/      # Notebooks de Ingestão (Autoloader)
│   ├── 01-silver/      # (Em breve) Notebooks de Tratamento
│   ├── 02-gold/        # (Em breve) Notebooks de Agregação
│   └── glue_jobs/      # (Em breve) Jobs de ETL
├── notebooks/          # Sandbox para exploração (Databricks)
└── tests/              # Testes unitários
```

## 🎲 Como gerar os dados
Para gerar a massa de dados inicial, acesse a documentação específica do módulo:
[📖 Ir para Documentação do Gerador de Dados](./src/data_generator/README.md)

## 🥉 Documentação da Camada Bronze
Para entender os detalhes técnicos da ingestão:
[📖 Ir para Documentação da Bronze](./src/00-bronze/README.md)
---
**Desenvolvido por Michael Cruz como parte do portfólio de Engenharia de Dados.**