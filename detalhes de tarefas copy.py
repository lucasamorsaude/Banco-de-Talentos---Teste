import requests
import json

# --- CONFIGURAÇÕES ---
# Cole seu Token da API do ClickUp aqui
API_TOKEN = 'pk_230462181_14A3YYWKI305R4NFCXNRB1PFH6S8JZ91'

LISTAS = {
    'Tarefas Semanais': '901319331136',
    'Teleconsulta': '901319225949',
    'Tarefas Diárias': '901319330021',
    'Projetos': '901319331078'
}

# --- FUNÇÕES DA API ---
def get_clickup_list_tasks(list_id):
    """Busca as tarefas de uma lista específica."""
    url = f"https://api.clickup.com/api/v2/list/{list_id}/task"
    headers = {'Authorization': API_TOKEN}
    response = requests.get(url, headers=headers)
    return response.json()['tasks'] if response.status_code == 200 else None

def get_clickup_task_details(task_id):
    """Busca os detalhes de uma tarefa específica."""
    url = f"https://api.clickup.com/api/v2/task/{task_id}"
    headers = {'Authorization': API_TOKEN}
    response = requests.get(url, headers=headers)
    return response.json() if response.status_code == 200 else None

def create_clickup_task(list_id, task_data):
    """Cria uma nova tarefa em uma lista específica."""
    url = f"https://api.clickup.com/api/v2/list/{list_id}/task"
    headers = {
        'Authorization': API_TOKEN,
        'Content-Type': 'application/json'
    }
    response = requests.post(url, headers=headers, data=json.dumps(task_data))
    
    if response.status_code == 200:
        print("\n✅ Tarefa criada com sucesso!")
        return response.json()
    else:
        print(f"\n❌ Erro ao criar tarefa: {response.status_code} - {response.text}")
        return None

# --- EXECUÇÃO PRINCIPAL ---
if __name__ == "__main__":
    print(" LISTAS 'SOLTAS' NO SPACE")
    print("=" * 50)
    for nome, list_id in LISTAS.items():
        print(f"Nome: {nome:<18} |  ID: {list_id}")
    print("=" * 50)

    while True:
        try:
            choice = input("> Digite 'criar', cole um ID ou pressione Enter para sair: ").strip().lower()

            if not choice:
                break
            
            # Opção para CRIAR uma nova tarefa
            if choice == 'criar':
                list_id_to_add = input("  > Em qual ID de LISTA deseja criar a tarefa? ").strip()
                if list_id_to_add not in LISTAS.values():
                    print("  > ID de lista inválido. Operação cancelada.")
                    continue
                
                task_name = input("  > Qual o nome da nova tarefa? ").strip()
                tags_input = input("  > Adicionar quais tags (separadas por vírgula)? Ex: psiquiatria, urgente\n  > ").strip()
                
                # Prepara os dados para enviar para a API
                tags_list = [tag.strip() for tag in tags_input.split(',') if tag.strip()]
                
                new_task_data = {
                    "name": task_name,
                    "tags": tags_list
                }
                
                create_clickup_task(list_id_to_add, new_task_data)
                print("-" * 50)
                continue

            # Opção para VER detalhes (lista ou tarefa)
            if choice in LISTAS.values():
                tasks = get_clickup_list_tasks(choice)
                if tasks:
                    print("\n" + "=" * 50)
                    print(f"  TAREFAS NA LISTA ID: {choice}")
                    print("=" * 50)
                    for task in tasks:
                        print(f"Nome: {task['name']:<15} |  Status: {task['status']['status']:<20} |  ID: {task['id']}")
                    print("\n")
            else:
                task_details = get_clickup_task_details(choice)
                if task_details:
                    print("\n" + "=" * 50)
                    print(f"  DETALHES DA TAREFA ID: {choice}")
                    print("=" * 50)
                    print(json.dumps(task_details, indent=2, ensure_ascii=False))
                    print("\n")
                else:
                    print("ID inválido. Não é uma lista, tarefa ou comando válido.\n")

        except (KeyboardInterrupt, EOFError):
            break

    print("Explorador finalizado.")