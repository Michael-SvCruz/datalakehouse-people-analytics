locals {
  # definition of the data lake layers
  # landing: onde os dados brutos chegam
  # bronze: onde o arquivo vira Delta Lake com metadados
  # silver: dados limpos
  # gold: dados agregados para BI
  layers = ["landing", "bronze", "silver", "gold"]
}

# 1. Create S3 buckets for each layer
resource "aws_s3_bucket" "datalake" {
  for_each = toset(local.layers)
  
  bucket = "${var.bucket_prefix}-${each.value}-${var.env}"
  
  # force_destroy = true permite deletar o bucket mesmo com arquivos dentro
  # (PERIGOSO em produção, mas ótimo para estudos/dev)
  force_destroy = true
}

# 2. Segurança: Bloquear acesso público (Obrigatório por segurança)
resource "aws_s3_bucket_public_access_block" "public_acess" {
  for_each = aws_s3_bucket.datalake

  bucket = each.value.id

  block_public_acls	      = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

# 3. Versionamento (Backup automático de arquivos deletados/alterados para layers landing)
resource "aws_s3_bucket_versioning" "versioning" {
  for_each = aws_s3_bucket.datalake

  bucket = each.value.id
  versioning_configuration {
  # Lógica Condicional (Ternário):
  # Condição ? Valor_se_Verdadeiro : Valor_se_Falso
  # Se a chave do loop (each.key) for "landing", ativa. Senão, suspende.
    status = each.key == "landing" ? "Enabled" : "Suspended"
  }
}
