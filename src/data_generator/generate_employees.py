import csv
import os
import random
from datetime import datetime, timedelta
from faker import Faker

# Configuração Inicial
fake = Faker('pt_BR')
Faker.seed(42)

# Configurações do Gerador
TOTAL_REGISTROS = 150 # Aumentei um pouco para garantir volume após preencher os obrigatórios
OUTPUT_DIR = "../../data"
OUTPUT_FILE = "employees.csv"

# 
# ESTRUTURA ORGANIZACIONAL COM PESOS
# 
ESTRUTURA_ORGANIZACIONAL = {
    "Engenharia Clínica": {
        "Supervisor de Engenharia Clínica": 5,
        "Gerente de Engenharia Clínica": 1,
        "Engenheiro Clínico": 20,
        "Técnico de Equipamentos III": 15,
        "Técnico de Equipamentos II": 20,
        "Técnico de Equipamentos I": 35,
        "Estagiário de Engenharia": 10
    },
    "TI / Dados": {
        "Coordenador de TI": 5,
        "Engenheiro de Dados Pleno": 10,
        "Engenheiro de Dados Jr": 15,
        "Desenvolvedor Full Stack": 20,
        "Analista de BI": 15,
        "Analista de Infraestrutura": 15,
        "Analista de Suporte": 40
    },
    "Enfermagem": {
        "Enfermeiro Chefe": 1,
        "Supervisor de Enfermagem": 5,
        "Enfermeiro UTI": 10,
        "Enfermeiro CC": 15,
        "Enfermeiro Assistencial": 20,
        "Técnico de Enfermagem": 80,
        "Auxiliar de Enfermagem": 40
    },
    "Administrativo": {
        "Gerente Administrativo": 5,
        "Secretária Executiva": 10,
        "Assistente Administrativo": 50,
        "Recepcionista": 40,
        "Auxiliar de Escritório": 30
    },
    "Financeiro": {
        "Gerente Financeiro": 5,
        "Contador": 10,
        "Analista Financeiro": 20,
        "Auxiliar de Contas a Pagar": 40,
        "Auxiliar de Contas a Receber": 40
    },
    "Recursos Humanos": {
        "Gerente de RH": 5,
        "Business Partner": 10,
        "Analista de RH": 30,
        "Analista de Departamento Pessoal": 30,
        "Recrutador": 20
    },
    "Manutenção Predial": {
        "Supervisor de Manutenção": 5,
        "Oficial de Manutenção": 30,
        "Eletricista": 20,
        "Encanador": 20,
        "Pintor": 15
    }
}

PESOS_DEPARTAMENTOS = {
    "Engenharia Clínica": 10,
    "TI / Dados": 5,
    "Enfermagem": 45,
    "Administrativo": 15,
    "Financeiro": 8,
    "Recursos Humanos": 5,
    "Manutenção Predial": 12
}

def garantir_diretorio(caminho):
    if not os.path.exists(caminho):
        os.makedirs(caminho)

def calcular_salario(cargo):
    c = cargo.lower()
    if "gerente" in c: return random.uniform(15000, 25000)
    elif "chefe" in c or "coordenador" in c or "supervisor" in c: return random.uniform(10000, 16000)
    elif "sr" in c or "senior" in c: return random.uniform(12000, 16000)
    elif "pleno" in c or "contador" in c or "business partner" in c: return random.uniform(7000, 11000)
    elif "jr" in c or "analista" in c or "enfermeiro" in c or "desenvolvedor" in c: return random.uniform(4000, 7000)
    elif "técnico" in c or "eletricista" in c or "encanador" in c: return random.uniform(2800, 5000)
    elif "assistente" in c or "oficial" in c or "secretária" in c: return random.uniform(2200, 3500)
    elif "auxiliar" in c or "recepcionista" in c or "pintor" in c or "recrutador" in c: return random.uniform(1800, 2800)
    elif "estagiário" in c: return random.uniform(1200, 1800)
    else: return random.uniform(2000, 4000)

def criar_dados_funcionario(dept_fixo=None, cargo_fixo=None):
    """
    Gera os dados de um funcionário.
    Se dept_fixo e cargo_fixo forem passados, força esses valores.
    Caso contrário, escolhe aleatoriamente baseado nos pesos.
    """
    
    # 1. Definição de Departamento e Cargo
    if dept_fixo and cargo_fixo:
        departamento = dept_fixo
        cargo = cargo_fixo
    else:
        # Escolha Aleatória Ponderada
        dept_opcoes = list(PESOS_DEPARTAMENTOS.keys())
        dept_pesos = list(PESOS_DEPARTAMENTOS.values())
        departamento = random.choices(dept_opcoes, weights=dept_pesos, k=1)[0]

        cargos_dict = ESTRUTURA_ORGANIZACIONAL[departamento]
        cargos_opcoes = list(cargos_dict.keys())
        cargos_pesos = list(cargos_dict.values())
        cargo = random.choices(cargos_opcoes, weights=cargos_pesos, k=1)[0]

    # 2. Dados Pessoais
    genero = random.choice(['M', 'F'])
    nome = fake.name_male() if genero == 'M' else fake.name_female()
    
    # 3. Lógica de Datas e Status
    data_admissao = fake.date_between(start_date='-5y', end_date='today')
    is_ativo = random.random() > 0.20 
    
    data_demissao = None
    status = "Ativo"
    
    if not is_ativo:
        status = "Inativo"
        dias_trabalhados = random.randint(30, 1400)
        data_calculada = data_admissao + timedelta(days=dias_trabalhados)
        hoje = datetime.now().date()
        if data_calculada > hoje:
            data_demissao = hoje - timedelta(days=random.randint(1, 30))
        else:
            data_demissao = data_calculada

    salario = round(calcular_salario(cargo), 2)

    return {
        "nome": nome,
        "cpf": fake.cpf(),
        "data_nascimento": fake.date_of_birth(minimum_age=18, maximum_age=65).isoformat(),
        "endereco": fake.address().replace('\n', ', '),
        "telefone": fake.phone_number(),
        "departamento": departamento,
        "cargo": cargo,
        "salario": salario,
        "data_admissao": data_admissao.isoformat(),
        "data_demissao": data_demissao.isoformat() if data_demissao else "",
        "status": status
    }

def main():
    caminho_completo_dir = os.path.join(os.path.dirname(__file__), OUTPUT_DIR)
    garantir_diretorio(caminho_completo_dir)
    arquivo_saida = os.path.join(caminho_completo_dir, OUTPUT_FILE)
    
    print(f"🚀 Iniciando geração híbrida (Garantia de Cargos + Pesos)...")
    
    lista_funcionarios_temp = []

    # FASE 1: GARANTIA DE COBERTURA (Pelo menos 1 de cada cargo)
    print("   ...Gerando 1 funcionário para cada cargo existente...")
    for dept, cargos_dict in ESTRUTURA_ORGANIZACIONAL.items():
        for cargo in cargos_dict.keys():
            # Gera forçado
            func = criar_dados_funcionario(dept_fixo=dept, cargo_fixo=cargo)
            lista_funcionarios_temp.append(func)
            
    total_ja_gerado = len(lista_funcionarios_temp)
    print(f"   ✅ {total_ja_gerado} funcionários obrigatórios gerados.")

    # FASE 2: PREENCHIMENTO (O restante respeita os pesos)
    restante = TOTAL_REGISTROS - total_ja_gerado
    if restante > 0:
        print(f"   ...Gerando mais {restante} funcionários aleatórios baseados em pesos...")
        for _ in range(restante):
            func = criar_dados_funcionario() # Sem argumentos = aleatório ponderado
            lista_funcionarios_temp.append(func)

    # FASE 3: EMBARALHAMENTO E ATRIBUIÇÃO DE IDs
    # Embaralhamos para que os chefes (gerados primeiro) não fiquem todos no topo da lista
    random.shuffle(lista_funcionarios_temp)

    # Adiciona o ID sequencial agora que a lista está finalizada
    funcionarios_finais = []
    for i, func in enumerate(lista_funcionarios_temp):
        func_com_id = {"id_funcionario": i + 1}
        func_com_id.update(func) # Adiciona os outros campos
        funcionarios_finais.append(func_com_id)

    # GRAVAÇÃO
    colunas = funcionarios_finais[0].keys()
    with open(arquivo_saida, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=colunas)
        writer.writeheader()
        writer.writerows(funcionarios_finais)
        
    print(f"✅ Arquivo gerado com sucesso: {arquivo_saida}")
    print(f"📊 Total de registros: {len(funcionarios_finais)}")

if __name__ == "__main__":
    main()