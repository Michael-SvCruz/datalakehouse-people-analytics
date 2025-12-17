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

## Arquitetura da Solução

A arquitetura segue o padrão **Medallion (Bronze, Silver, Gold)**, garantindo o refinamento progressivo dos dados.

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

## 🚀 Como Executar (Em breve)
Instruções detalhadas de setup serão adicionadas conforme o desenvolvimento avança.

---
**Desenvolvido por Michael Cruz como parte do portfólio de Engenharia de Dados.**