import csv
import json
import os
import random
import uuid
from datetime import datetime, timedelta, time

# ==========================================
# CONFIGURAÇÕES GERAIS
# ==========================================
INPUT_FILE = "../../data/employees.csv"
OUTPUT_FILE = "../../data/attendance.json"
DATA_INICIO = datetime(2023, 1, 1)
DATA_FIM = datetime.now()

# Probabilidades (Comportamento Humano)
PROB_ESQUECER_PONTO = 0.02   # 2% de chance de esquecer UMA das batidas (gera ímpar)
PROB_ATRASO = 0.05           # 5% de chance de atraso na entrada
PROB_HORA_EXTRA = 0.10       # 10% de chance de sair mais tarde
PROB_TRABALHO_FDS = 0.15     # 15% de chance de trabalhar Sábado ou Domingo (Gera escala > 7 dias)
PROB_FALTA = 0.01            # 1% de chance de faltar em dia normal (Absenteísmo)

def carregar_funcionarios():
    """Lê o arquivo CSV gerado anteriormente."""
    caminho = os.path.join(os.path.dirname(__file__), INPUT_FILE)
    funcionarios = []
    if not os.path.exists(caminho):
        print(f"❌ Erro: Arquivo {INPUT_FILE} não encontrado. Rode o generate_employees.py primeiro.")
        return []
    with open(caminho, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            funcionarios.append(row)
    return funcionarios

def gerar_horario_com_ruido(hora_base, ruido_minutos=10):
    """Adiciona variação de minutos para não ficar horário robótico (ex: 08:00:00)."""
    delta = random.randint(-ruido_minutos, ruido_minutos)
    data_base = datetime(2000, 1, 1, hora_base.hour, hora_base.minute)
    nova_hora = data_base + timedelta(minutes=delta)
    return nova_hora.strftime("%H:%M:%S")

def gerar_marcacoes_do_dia():
    """Gera as batidas do dia simulando a rotina real."""
    marcacoes = []
    
    # 1. Entrada
    if random.random() < PROB_ATRASO:
        # Atraso entre 15 e 90 minutos
        hora_entrada = datetime(2000, 1, 1, 8, 0) + timedelta(minutes=random.randint(15, 90))
        marcacoes.append(hora_entrada.strftime("%H:%M:%S"))
    else:
        marcacoes.append(gerar_horario_com_ruido(time(8, 0)))

    # 2. Saída Almoço
    marcacoes.append(gerar_horario_com_ruido(time(12, 0)))

    # 3. Volta Almoço
    marcacoes.append(gerar_horario_com_ruido(time(13, 0)))

    # 4. Saída
    if random.random() < PROB_HORA_EXTRA:
        # Hora extra entre 30 min e 2 horas
        hora_saida = datetime(2000, 1, 1, 17, 0) + timedelta(minutes=random.randint(30, 120))
        marcacoes.append(hora_saida.strftime("%H:%M:%S"))
    else:
        marcacoes.append(gerar_horario_com_ruido(time(17, 0)))
        
    # Simula esquecimento (Remove 1 batida aleatória, gerando inconsistência)
    if random.random() < PROB_ESQUECER_PONTO:
        if marcacoes:
            marcacoes.pop(random.randint(0, len(marcacoes)-1))
        
    return marcacoes

def main():
    funcionarios = carregar_funcionarios()
    if not funcionarios:
        return

    print(f"🚀 Iniciando geração de pontos para {len(funcionarios)} funcionários...")
    print(f"📅 Período: {DATA_INICIO.date()} até {DATA_FIM.date()}")

    registros_ponto = []
    
    data_atual = DATA_INICIO
    while data_atual <= DATA_FIM:
        
        eh_fim_de_semana = data_atual.weekday() >= 5 # 5=Sábado, 6=Domingo
        
        for func in funcionarios:
            # --- VERIFICAÇÕES DE CONTRATO ---
            dt_admissao = datetime.strptime(func['data_admissao'], "%Y-%m-%d")
            if data_atual < dt_admissao: continue # Ainda não contratado

            if func['data_demissao']:
                dt_demissao = datetime.strptime(func['data_demissao'], "%Y-%m-%d")
                if data_atual > dt_demissao: continue # Já demitido

            # --- LÓGICA DE TRABALHO NO DIA ---
            vai_trabalhar = False
            
            if not eh_fim_de_semana:
                # Dia de semana normal: Trabalha, a menos que falte (absenteísmo)
                if random.random() > PROB_FALTA:
                    vai_trabalhar = True
            else:
                # Fim de semana: Só trabalha se cair na probabilidade de escala (15%)
                # Isso permite criar sequências longas (ex: Seg-Sex + Sab-Dom + Seg...)
                if random.random() < PROB_TRABALHO_FDS:
                    vai_trabalhar = True
            
            # Se decidiu que trabalha hoje, gera o registro
            if vai_trabalhar:
                registro = {
                    "id_ponto": str(uuid.uuid4()),
                    "id_funcionario": int(func['id_funcionario']),
                    "data": data_atual.strftime("%Y-%m-%d"),
                    "dia_semana": data_atual.strftime("%A"),
                    "marcacoes": gerar_marcacoes_do_dia()
                }
                registros_ponto.append(registro)
        
        data_atual += timedelta(days=1)

    # Salva JSON
    caminho_saida = os.path.join(os.path.dirname(__file__), OUTPUT_FILE)
    with open(caminho_saida, 'w', encoding='utf-8') as f:
        json.dump(registros_ponto, f, indent=2, ensure_ascii=False)

    print(f"✅ Arquivo gerado com sucesso: {OUTPUT_FILE}")
    print(f"📊 Total de registros de ponto gerados: {len(registros_ponto)}")

if __name__ == "__main__":
    main()