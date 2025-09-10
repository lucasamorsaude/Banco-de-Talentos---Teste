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
    if response.status_code == 200:
        return response.json()['tasks']
    return None

def get_clickup_task_details(task_id):
    """Busca os detalhes (atributos) de uma tarefa específica."""
    url = f"https://api.clickup.com/api/v2/task/{task_id}"
    headers = {'Authorization': API_TOKEN}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
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
            chosen_id = input("> Cole o ID de uma LISTA ou TAREFA (ou Enter para sair): ").strip()

            if not chosen_id:
                break

            # 1. Tenta buscar como uma LISTA
            if chosen_id in LISTAS.values():
                tasks = get_clickup_list_tasks(chosen_id)
                if tasks:
                    print("\n" + "=" * 50)
                    print(f"  TAREFAS NA LISTA ID: {chosen_id}")
                    print("=" * 50)
                    for task in tasks:
                        print(f"Nome: {task['name']:<15} |  Status: {task['status']['status']:<20} |  ID: {task['id']}")
                    print("\n")
                else:
                    print("Nenhuma tarefa encontrada nesta lista.\n")
            # 2. Se não for uma lista, tenta buscar como uma TAREFA
            else:
                task_details = get_clickup_task_details(chosen_id)
                if task_details:
                    print("\n" + "=" * 50)
                    print(f"  DETALHES DA TAREFA ID: {chosen_id}")
                    print("=" * 50)
                    # Imprime todos os detalhes (atributos) da tarefa
                    for key, value in task_details.items():
                        print(f"- {key}: {json.dumps(value, indent=2, ensure_ascii=False)}")
                    print("\n")
                # 3. Se não encontrar nem lista nem tarefa
                else:
                    print("ID inválido. Não é uma lista conhecida nem uma tarefa válida. Tente novamente.\n")

        except (KeyboardInterrupt, EOFError):
            break

    print("Explorador finalizado.")