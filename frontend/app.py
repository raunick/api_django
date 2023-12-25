import streamlit as st
import requests

# URL do seu servidor Django local
DJANGO_SERVER_URL = "http://127.0.0.1:8000"
# Função para obter o token CSRF
def obter_token_csrf():
    response_get = requests.get(f"{DJANGO_SERVER_URL}/adicionar_tarefa_form/")
    csrf_token = response_get.cookies.get('csrftoken')
    return csrf_token


st.title("Aplicativo de Tarefas")

# Sidebar para opções
opcao = st.sidebar.selectbox("Selecione uma opção:", ["Criar Tarefa", "Listar Tarefas", "Atualizar Tarefa", "Deletar Tarefa"], index=0, key="opcao", help=None)

# Página para adicionar uma nova tarefa
if opcao == "Criar Tarefa":
    st.subheader("Nova Tarefa")
    nova_tarefa = st.text_input("Digite o título da tarefa:")
    if st.button("Salvar"):
        # Obter o token CSRF
        csrf_token = obter_token_csrf()

        # Inclua o token CSRF no cabeçalho da solicitação POST
        headers = {'X-CSRFToken': csrf_token}
        response = requests.post(
            f"{DJANGO_SERVER_URL}/adicionar_tarefa_form/",
            data={"titulo": nova_tarefa},
            headers=headers,
            cookies={'csrftoken': csrf_token}  # opcional: inclua o token CSRF nos cookies também
        )
        st.success("Tarefa adicionada com sucesso!")
# Página para exibir a lista de tarefas
elif opcao == "Listar Tarefas":
    st.subheader("Lista de Tarefas")
    status_filter = st.selectbox("Filtrar por status:", ["Todos", "Aberto", "Em Processo", "Concluído"])

    if status_filter == "Todos":
        tarefas = requests.get(f"{DJANGO_SERVER_URL}/lista_tarefas_json/").json()
    else:
        tarefas = requests.get(f"{DJANGO_SERVER_URL}/lista_tarefas_json/{status_filter}").json()

    # Criar uma lista de dicionários para exibir em uma tabela
    data = [{'Codigo': tarefa['id'],
             'Título': tarefa['titulo'], 
             'Status': tarefa['status'],
             'Concluida':tarefa['concluida'],
             } for tarefa in tarefas['tarefas']]
    
    # Exibir a tabela usando st.dataframe
    st.dataframe(data)
    #st.data_editor(data, num_rows="dynamic")
    for tarefa in tarefas['tarefas']:
        if not tarefa['concluida']:
            if st.button(f"Completar Tarefa: {tarefa['titulo']}"):
                # Obter o token CSRF
                csrf_token = obter_token_csrf()

                # Inclua o token CSRF no cabeçalho da solicitação POST
                headers = {'X-CSRFToken': csrf_token}
                response = requests.post(
                    f"{DJANGO_SERVER_URL}/completar_tarefa/{tarefa['id']}/",
                    headers=headers,
                    cookies={'csrftoken': csrf_token}  # opcional: inclua o token CSRF nos cookies também
                    )
                if response.status_code == 200:
                    st.success("Tarefa concluída com sucesso!")
                    st.rerun()
                else:
                    st.error(f"Erro ao completar a tarefa: {response.text}")


# Página para atualizar uma tarefa
elif opcao == "Atualizar Tarefa":  
    # Obter tarefas do Django
    tarefas = requests.get(f"{DJANGO_SERVER_URL}/lista_tarefas_json/").json()
    
    # Criar uma lista de dicionários para exibir em uma tabela
    data = [{'id': tarefa['id'],
             'titulo': tarefa['titulo'], 
             'status': tarefa['status'],
             'concluida': tarefa['concluida'],
             } for tarefa in tarefas['tarefas']]
    
    st.subheader("Atualizar Tarefa")
    titulos = [tarefa['titulo'] for tarefa in data]
    tarefa_selecionada = st.selectbox('Selecione uma tarefa:', titulos)

    # Encontrar o ID da tarefa selecionada
    tarefa_id = None
    for tarefa in data:
        if tarefa['titulo'] == tarefa_selecionada:
            tarefa_id = tarefa['id']
            break

    # Verificar se encontrou o ID
    if tarefa_id is not None:
        st.write(f'Tarefa selecionada: {tarefa_selecionada} (ID: {tarefa_id})')

        # Agora você pode exibir os dados da tarefa selecionada e permitir a atualização
        st.text(f'Status atual: {tarefa["status"]}')
        
        # Mapear rótulos para códigos
        mapeamento_status = {'Aberto': 'AB', 'Em Processo': 'PR', 'Concluído': 'CO'}
        novo_status_rotulo = st.selectbox('Selecione um novo status:', ["Aberto", "Em Processo", "Concluído"])
        novo_status_codigo = mapeamento_status.get(novo_status_rotulo)

        # Obter o token CSRF
        csrf_token = obter_token_csrf()

        # Inclua o token CSRF no cabeçalho da solicitação POST
        headers = {'X-CSRFToken': csrf_token}

        if st.button("Atualizar"):
            # Enviar a atualização para o Django
            response = requests.post(
                f"{DJANGO_SERVER_URL}/atualizar_tarefa/{tarefa_id}/{novo_status_codigo}",
                headers=headers,
                json={"novo_status": novo_status_codigo},
                cookies={'csrftoken': csrf_token}  # opcional: inclua o token CSRF nos cookies também
            )

            if response.status_code == 200:
                st.success("Tarefa atualizada com sucesso!")
            else:
                st.error(f"Erro ao atualizar a tarefa: {response.text}")
    else:
        st.warning("Tarefa não encontrada.")

# Página para deletar uma tarefa
elif opcao == "Deletar Tarefa":
    # Obter tarefas do Django
    tarefas = requests.get(f"{DJANGO_SERVER_URL}/lista_tarefas_json/").json()
    
    # Criar uma lista de dicionários para exibir em uma tabela
    data = [{'id': tarefa['id'],
             'titulo': tarefa['titulo'], 
             'status': tarefa['status'],
             'concluida': tarefa['concluida'],
             } for tarefa in tarefas['tarefas']]

    # Criar um dicionário de mapeamento entre nome e ID
    mapa_tarefas = {tarefa['titulo']: tarefa['id'] for tarefa in data}

    st.subheader("Deletar Tarefa")
    # Obter o token CSRF
    csrf_token = obter_token_csrf()

    # Inclua o token CSRF no cabeçalho da solicitação POST
    headers = {'X-CSRFToken': csrf_token}

    # Criar uma lista de nomes para o selectbox
    nomes_tarefas = [tarefa['titulo'] for tarefa in data]

    # Selecionar uma tarefa pelo nome
    tarefa_selecionada = st.selectbox('Selecione uma tarefa:', nomes_tarefas)

    # Obter o ID correspondente ao nome selecionado
    tarefa_id = mapa_tarefas.get(tarefa_selecionada)

    if st.button("Deletar"):
        if tarefa_id is not None:
            requests.post(
                f"{DJANGO_SERVER_URL}/deletar_tarefa/{tarefa_id}/",
                headers=headers,
                cookies={'csrftoken': csrf_token}  # opcional: inclua o token CSRF nos cookies também
            )
            st.success("Tarefa deletada com sucesso!")
        else:
            st.warning("ID da tarefa não encontrado.")

# Página padrão quando nenhuma opção é selecionada
else:
    st.subheader("Bem-vindo! Selecione uma opção no menu lateral.")

# Adicione um botão para recarregar a página
if st.button("Recarregar Página"):
    st.rerun()
