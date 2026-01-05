# Camada Bronze (Ingestão)

Responsável por ingerir os dados brutos (Raw) do Data Lake para tabelas Delta.

## 🛠 Tecnologias
- **Spark Structured Streaming**
- **Databricks Autoloader (`cloudFiles`)**
- **Delta Lake**

## 📋 Tabelas

| Tabela | Origem | Formato | Descrição |
| :--- | :--- | :--- | :--- |
| `bronze_employees` | `employees_*.csv` | CSV | Carga Full diária de funcionários. Contém histórico de alterações. |
| `bronze_attendance` | `attendance_*.json` | JSON | Registros de ponto eletrônico. Ingestão incremental de arquivos novos. |

## ⚙️ Detalhes de Implementação

### Autoloader & Schema Evolution
Utilizando o Autoloader para detecção automática de novos arquivos na pasta de origem (`00_source`).
- **Schema Inference:** Ativado para detectar mudanças nos tipos de dados.
- **Rescue Data:** (Opcional) Dados corrompidos são salvos na coluna `_rescued_data`.
- **Metadados:** Adicionamos `data_ingestao` e `arquivo_origem` (`_metadata.file_path`) para rastreabilidade.

### Estratégia de Arquivos
A origem envia arquivos com timestamp (`nome_YYYYMMDD_HHMMSS.ext`).
O Autoloader usa o padrão glob `*` (ex: `employees*.csv`) para ingerir todas as versões, mantendo o histórico completo na tabela Bronze.

## 🔄 Como Rodar
Execute o notebook `01_ingestion_bronze.ipynb`. O job está configurado com `.trigger(availableNow=True)`, ou seja, processa tudo o que está pendente e desliga o cluster (Batch mode).