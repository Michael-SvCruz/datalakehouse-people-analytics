import csv
import json
import os
import glob
import random
import uuid
from datetime import datetime, timedelta, time
from faker import Faker

# --- CONFIGURAÇÕES ---
DATA_DIR = "../../data"
CHURN_RATE = 0.05  # 5% dos ativos serão substituídos nesta atualização
PROB_ESQUECER_PONTO = 0.02
PROB_ATRASO = 0.05
PROB_HORA_EXTRA = 0.10
PROB_TRABALHO_FDS = 0.15
PROB_FALTA = 0.01

fake = Faker('pt_BR')
Faker.seed(random.randint(0, 9999)) # Seed aleatória para variar a cada execução

def carregar_dados_mais_recentes():
    """Busca os arquivos employees_*.csv e attendance_*.json mais recentes."""
    
    # Busca Employees
    padrao_emp = os.path.join(os.path.dirname(__file__), DATA_DIR, "employees_*.csv")
    arqs_emp = glob.glob(padrao_emp)
    if not arqs_emp:
        print("❌ Erro: Nenhum arquivo employees encontrado.")
        exit()
    path_emp_recente = max(arqs_emp, key=os.path.getctime)
    
    # Busca Attendance
    padrao_att = os.path.join(os.path.dirname(__file__), DATA_DIR, "attendance_*.json")
    arqs_att = glob.glob(padrao_att)
    if not arqs_att:
        print("❌ Erro: Nenhum arquivo attendance encontrado.")
        exit()
    path_att_recente = max(arqs_att, key=os.path.getctime)

    print(f"📂 Carregando base: {os.path.basename(path_emp_recente)} e {os.path.basename(path_att_recente)}")

    with open(path_emp_recente, 'r', encoding='utf-8') as f:
        employees = list(csv.DictReader(f))
        
    with open(path_att_recente, 'r', encoding='utf-8') as f:
        attendance = json.load(f)
        
    return employees, attendance

def obter_ultima_data_ponto(attendance_list):
    """Descobre qual foi o último dia processado no JSON"""
    if not attendance_list:
        return datetime(2024, 1, 1)
    
    # Ordena as datas e pega a última
    datas = [x['data'] for x in attendance_list]
    ultima_str = max(datas)
    return datetime.strptime(ultima_str, "%Y-%m-%d")

def processar_turnover(employees):
    """Simula demissões e contratações recentes"""
    
    # Se a taxa for 0, não faz nada e retorna a lista original
    if CHURN_RATE <= 0:
        print("🔄 Turnover desativado (CHURN_RATE = 0). Nenhuma demissão processada.")
        return employees

    print("🔄 Processando Turnover (Demissões e Contratações)...")
    
    # 1. Identificar ativos e último ID
    ativos = [e for e in employees if e['status'] == 'Ativo']
    max_id = max([int(e['id_funcionario']) for e in employees])
    
    # 2. Definir quantos vão rodar
    qtd_trocas = int(len(ativos) * CHURN_RATE)
    
    # Só garante mínimo de 1 se a taxa for positiva, mas o cálculo matemático der 0 (ex: 0.01 * 50 = 0.5 -> 0)
    if qtd_trocas < 1 and CHURN_RATE > 0: 
        qtd_trocas = 1
    
    if qtd_trocas == 0:
        print("   ℹ️ Nenhuma troca necessária baseada na taxa atual.")
        return employees
    
    demitidos_agora = random.sample(ativos, qtd_trocas)
    novos_funcionarios = []
    
    data_base_troca = datetime.now() - timedelta(days=random.randint(10, 30))
    
    for demitido in demitidos_agora:
        # A. Processa Demissão
        demitido['status'] = 'Inativo'
        # Demitido entre 10 e 30 dias atrás
        dt_demissao = data_base_troca + timedelta(days=random.randint(0, 5))
        demitido['data_demissao'] = dt_demissao.strftime("%Y-%m-%d")
        
        # B. Processa Contratação (Substituto)
        max_id += 1
        # Contratado alguns dias após a demissão do anterior
        dt_admissao = dt_demissao + timedelta(days=random.randint(2, 10))
        if dt_admissao > datetime.now(): dt_admissao = datetime.now() # Não contratar no futuro
        
        genero = random.choice(['M', 'F'])
        nome = fake.name_male() if genero == 'M' else fake.name_female()
        
        novo_func = {
            "id_funcionario": max_id,
            "nome": nome,
            "cpf": fake.cpf(),
            "data_nascimento": fake.date_of_birth(minimum_age=18, maximum_age=50).isoformat(),
            "endereco": f"{fake.street_address()}, São Paulo - SP, CEP {fake.postcode()}",
            "telefone": fake.phone_number(),
            "departamento": demitido['departamento'], # Mantém setor
            "cargo": demitido['cargo'],               # Mantém cargo (reposição)
            "salario": demitido['salario'],           # Mantém faixa salarial
            "data_admissao": dt_admissao.strftime("%Y-%m-%d"),
            "data_demissao": "",
            "status": "Ativo"
        }
        novos_funcionarios.append(novo_func)
        print(f"   📉 Saiu: {demitido['nome']} ({demitido['cargo']}) | 📈 Entrou: {novo_func['nome']}")

    employees.extend(novos_funcionarios)
    return employees

# --- FUNÇÕES AUXILIARES DE PONTO (Reutilizadas) ---
def gerar_horario_ruido(hora_base):
    delta = random.randint(-10, 10)
    dt = datetime(2000,1,1, hora_base.hour, hora_base.minute) + timedelta(minutes=delta)
    return dt.strftime("%H:%M:%S")

def gerar_marcacoes():
    marcacoes = []
    # Entrada
    if random.random() < PROB_ATRASO:
        ent = datetime(2000,1,1,8,0) + timedelta(minutes=random.randint(15,90))
        marcacoes.append(ent.strftime("%H:%M:%S"))
    else:
        marcacoes.append(gerar_horario_ruido(time(8,0)))
    
    marcacoes.append(gerar_horario_ruido(time(12,0)))
    marcacoes.append(gerar_horario_ruido(time(13,0)))
    
    # Saída
    if random.random() < PROB_HORA_EXTRA:
        sai = datetime(2000,1,1,17,0) + timedelta(minutes=random.randint(30,120))
        marcacoes.append(sai.strftime("%H:%M:%S"))
    else:
        marcacoes.append(gerar_horario_ruido(time(17,0)))
        
    if random.random() < PROB_ESQUECER_PONTO and marcacoes:
        marcacoes.pop(random.randint(0, len(marcacoes)-1))
    return marcacoes

def gerar_ponto_incremental(employees, attendance_list):
    ultima_data = obter_ultima_data_ponto(attendance_list)
    inicio_incremental = ultima_data + timedelta(days=1)
    hoje = datetime.now()
    
    if inicio_incremental > hoje:
        print("✅ Dados de ponto já estão atualizados até hoje.")
        return attendance_list

    print(f"⏰ Gerando pontos de {inicio_incremental.date()} até {hoje.date()}...")
    
    novos_pontos = []
    curr_date = inicio_incremental
    
    while curr_date <= hoje:
        eh_fds = curr_date.weekday() >= 5
        
        for func in employees:
            # Regras de Data
            dt_adm = datetime.strptime(func['data_admissao'], "%Y-%m-%d")
            if curr_date < dt_adm: continue # Ainda não entrou
            
            if func['data_demissao']:
                dt_dem = datetime.strptime(func['data_demissao'], "%Y-%m-%d")
                if curr_date > dt_dem: continue # Já saiu
            
            # Regras de Trabalho
            trabalha = False
            if not eh_fds:
                if random.random() > PROB_FALTA: trabalha = True
            else:
                if random.random() < PROB_TRABALHO_FDS: trabalha = True
                
            if trabalha:
                registro = {
                    "id_ponto": str(uuid.uuid4()),
                    "id_funcionario": int(func['id_funcionario']),
                    "data": curr_date.strftime("%Y-%m-%d"),
                    "dia_semana": curr_date.strftime("%A"),
                    "marcacoes": gerar_marcacoes()
                }
                novos_pontos.append(registro)
        
        curr_date += timedelta(days=1)
        
    print(f"   ➕ {len(novos_pontos)} novos registros de ponto gerados.")
    attendance_list.extend(novos_pontos)
    return attendance_list

def main():
    # 1. Carrega os dados mais recentes
    emps, atts = carregar_dados_mais_recentes()
    
    # 2. Atualiza Funcionários (Turnover)
    emps_atualizados = processar_turnover(emps)
    
    # 3. Atualiza Pontos (Incremental)
    atts_atualizados = gerar_ponto_incremental(emps_atualizados, atts)
    
    timestamp_str = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    novo_nome_emp = f"employees_{timestamp_str}.csv"
    novo_nome_att = f"attendance_{timestamp_str}.json"
    
    path_novo_emp = os.path.join(os.path.dirname(__file__), DATA_DIR, novo_nome_emp)
    path_novo_att = os.path.join(os.path.dirname(__file__), DATA_DIR, novo_nome_att)
    

    
    # 4. Salva Funcionários (Arquivo Novo)
    with open(path_novo_emp, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=emps_atualizados[0].keys())
        writer.writeheader()
        writer.writerows(emps_atualizados)
        
    with open(path_novo_att, 'w', encoding='utf-8') as f:
        json.dump(atts_atualizados, f, indent=2, ensure_ascii=False)
        
    print(f"🚀 Atualização concluída!")
    print(f"💾 Novos arquivos gerados:\n   -> {novo_nome_emp}\n   -> {novo_nome_att}")

if __name__ == "__main__":
    main()