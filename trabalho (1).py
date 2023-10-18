import PySimpleGUI as sg


alunos = [
    {
        "Nome": "Gabriel",
        "Nota 1": 7.5,
        "Nota 2": 8.5,
        "Nota 3": 5.6,
        "Situação": "---",
    },
    {
        "Nome": "Angelo",
        "Nota 1": 9.2,
        "Nota 2": 6.0,
        "Nota 3": 8.2,
        "Situação": "---",
    },
    {
        "Nome": "Henrique",
        "Nota 1": 8.0,
        "Nota 2": 5.5,
        "Nota 3": 3.2,
        "Situação": "---",
    },
    {
        "Nome": "Marcos",
        "Nota 1": 1.0,
        "Nota 2": 4.5,
        "Nota 3": 9.2,
        "Situação": "---",
    },
]


# Cabeçalho
notas = ["Nome", "Nota 1", "Nota 2", "Nota 3", "Situação"]

info = [
    [
        aluno["Nome"],
        aluno["Nota 1"],
        aluno["Nota 2"],
        aluno["Nota 3"],
        aluno["Situação"],
    ]
    for aluno in alunos
]

# Tela
sg.theme("LightGray1")
layout = [
    [sg.Text("Buscar"), sg.Input(key="-SEARCH-", enable_events=True)],
    [
        sg.Table(values=info, headings=notas, justification="c", key="Table"),
    ],
    [
        sg.Button("Adicionar Aluno"),
        sg.Button("Editar Aluno"),
        sg.Button("Remover Aluno"),
        sg.Button("Calcular Média"),
        sg.Button("Sair"),
    ],
]
window = sg.Window(" Tabela de Notas", layout)


def atualizar_tabela():
    info = []
    for aluno in alunos:
        row = [
            aluno["Nome"],
            aluno["Nota 1"],
            aluno["Nota 2"],
            aluno["Nota 3"],
        ]
        if "Situação" in aluno:
            row.append(aluno["Situação"])
        info.append(row)
    window["Table"].update(values=info)


def calcular_media_aluno_selecionado(selected_row):
    if selected_row < len(alunos):
        aluno_selecionado = alunos[selected_row].copy()  # Copia o aluno selecionado
        nome = aluno_selecionado["Nome"]
        nota1 = aluno_selecionado["Nota 1"]
        nota2 = aluno_selecionado["Nota 2"]
        nota3 = aluno_selecionado["Nota 3"]
        if nota1 is not None and nota2 is not None and nota3 is not None:
            try:
                nota1 = float(nota1)
                nota2 = float(nota2)
                nota3 = float(nota3)
                media = (nota1 + nota2 + nota3) / 3
                situacao = "Aprovado" if media >= 7 else "Reprovado"
                aluno_selecionado["Situação"] = situacao
                alunos[
                    selected_row
                ] = aluno_selecionado  # Atualiza o aluno na lista de alunos
                sg.popup(f"Média do aluno {nome}: {media:.2f}")
                atualizar_tabela()
            except ValueError:
                sg.popup("Alguma das notas não é um número válido.")
        else:
            sg.popup("Selecione um aluno válido para calcular a média.")


# Loop de Eventos
while True:
    event, values = window.read()
    if event == sg.WINDOW_CLOSED or event == "Sair":
        break

    # Calcular a médoa dos alunos
    if event == "Calcular Média":
        if values["Table"]:
            selected_row = int(
                values["Table"][0]
            )  # Converte o índice para um número inteiro
            calcular_media_aluno_selecionado(selected_row)
        else:
            sg.popup("Selecione um aluno para calcular a média.")

    # Pesquisar o aluno ou a situação
    if event == "-SEARCH-":
        search_term = values["-SEARCH-"]
        filtered_info = [
            [
                aluno["Nome"],
                aluno["Nota 1"],
                aluno["Nota 2"],
                aluno["Nota 3"],
                aluno["Situação"],
            ]
            for aluno in alunos
            if search_term.lower() in aluno["Nome"].lower()
            or search_term.lower() in aluno["Situação"].lower()
        ]
        window["Table"].update(values=filtered_info)

    # Função Adicionar aluno
    if event == "Adicionar Aluno":
        novo_aluno = {
            "Nome": "Novo Aluno",
            "Nota 1": 0.0,
            "Nota 2": 0.0,
            "Nota 3": 0.0,
            "Situação": "---",
        }
        alunos.append(novo_aluno)
        atualizar_tabela()

    # Função para remover aluno
    if event == "Remover Aluno":
        # Lógica para remover um aluno selecionado
        selected_rows = values["Table"]
        if selected_rows:
            selected_row = selected_rows[0]
            # Verifica se uma linha está selecionada
            if selected_row < len(alunos):
                del alunos[selected_row]
                window["Table"].update(
                    values=[
                        [
                            aluno["Nome"],
                            aluno["Nota 1"],
                            aluno["Nota 2"],
                            aluno["Nota 3"],
                            aluno["Situação"],
                        ]
                        for aluno in alunos
                    ]
                )
            else:
                sg.popup("Selecione um aluno válido para remover.")
        else:
            sg.popup("Selecione um aluno para remover.")

    # Edição dos Alunos
    if event == "Editar Aluno":
        selected_rows = values["Table"]
        if selected_rows:
            selected_row = selected_rows[0]
            if selected_row < len(alunos):
                aluno_selecionado = alunos[selected_row]
                # Criar uma nova janela para edição
                layout_edicao = [
                    [
                        sg.Text("Nome Novo:"),
                        sg.InputText(aluno_selecionado["Nome"], key="-NOME_NOVO-"),
                    ],
                    [
                        sg.Text("Nota Nova 1:"),
                        sg.InputText(aluno_selecionado["Nota 1"], key="-NOTA_NOVA1-"),
                    ],
                    [
                        sg.Text("Nota Nova 2:"),
                        sg.InputText(aluno_selecionado["Nota 2"], key="-NOTA_NOVA2-"),
                    ],
                    [
                        sg.Text("Nota Nova 3:"),
                        sg.InputText(aluno_selecionado["Nota 3"], key="-NOTA_NOVA3-"),
                    ],
                    [sg.Button("Salvar"), sg.Button("Cancelar")],
                ]
                window_edicao = sg.Window("Editar Aluno", layout_edicao)

                while True:
                    event_edicao, values_edicao = window_edicao.read()
                    if event_edicao == sg.WINDOW_CLOSED or event_edicao == "Cancelar":
                        break

                    if event_edicao == "Salvar":
                        # Atualizar os dados do aluno com as novas informações
                        aluno_selecionado["Nome"] = values_edicao["-NOME_NOVO-"]
                        aluno_selecionado["Nota 1"] = values_edicao["-NOTA_NOVA1-"]
                        aluno_selecionado["Nota 2"] = values_edicao["-NOTA_NOVA2-"]
                        aluno_selecionado["Nota 3"] = values_edicao["-NOTA_NOVA3-"]
                        atualizar_tabela()
                        break

                window_edicao.close()
                if event_edicao == "Salvar":
                    sg.popup("Aluno editado com sucesso!")
        else:
            sg.popup("Selecione um aluno para editar.")
