# Infraestrutura AWS com Terraform

Este módulo cria a estrutura de Data Lake no S3.

## Recursos Criados
- 4 Buckets S3:
  - `landing`: Dados brutos transitórios (CSV/JSON)
  - `bronze`: Dados brutos históricos (Delta)
  - `silver`: Dados limpos e tratados
  - `gold`: Dados agregados para negócio

## Como rodar
1. `terraform init`
2. `terraform plan`
3. `terraform apply`