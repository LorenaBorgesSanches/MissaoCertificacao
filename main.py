import PySimpleGUI as sg
from modelo import Ferramenta, Reserva, Tecnico
from persistencia import DB
from util import item_formulario

db = DB()
db.inicializarDB()

# ---- TECNICOS ----
cabecalhoTecnicos = ["CPF", "Nome", "Telefone", "Turno", "Equipe"]

layoutTecnicos = [[sg.Button("Novo", key='-NEW-TEC-'), sg.Button("Editar",  key='-EDIT-TEC-'), sg.Button("Excluir",  key='-DEL-TEC-'), sg.Button("Pesquisar", key='-FILTER-TEC-', size=(100, 1))],
                  [sg.Text("Filtro"), sg.Input(key='-FILTER-TEC-INPUT-')],
                  [sg.Table(values=db.getTabelaTecnicos(), headings=cabecalhoTecnicos, max_col_width=25,
                            background_color='black',
                            auto_size_columns=True,
                            display_row_numbers=True,
                            justification='right',
                            num_rows=20,
                            alternating_row_color='black',
                            key='-TABLE-TEC-',
                            row_height=25, expand_x=True, expand_y=True)]]

# ---- FERRAMENTAS ----
cabecalhoFerramentas = ["Id", "Descrição", "Fabricante", "Voltagem", "Part Number", "Tamanho", "Unidade Medida",
                        "Tipo", "Material", "Tempo Máximo Reserva"]

layoutFerramentas = [[sg.Button("Novo", key='-NEW-TOOL-'), sg.Button("Editar",  key='-EDIT-TOOL-'), sg.Button("Excluir",  key='-DEL-TOOL-'), sg.Button("Pesquisar", key='-FILTER-TOOL-', size=(100, 1))],
                     [sg.Text("Filtro"), sg.Input(key='-FILTER-TOOL-INPUT-')],
                     [sg.Table(values=db.getTabelaFerramentas(), headings=cabecalhoFerramentas, max_col_width=25,
                               background_color='black',
                               auto_size_columns=True,
                               display_row_numbers=True,
                               justification='right',
                               num_rows=20,
                               alternating_row_color='black',
                               key='-TABLE-TOOL-',
                               row_height=25, expand_x=True, expand_y=True)]]

# ---- RESERVAS ----
cabecalhoReservas = ["Id", "Ferramenta", "Técnico", "Descrição", "Data de Retirada", "Data de Devolução"]

layoutReservas = [[sg.Button("Novo", key='-NEW-RES-'), sg.Button("Editar",  key='-EDIT-RES-'), sg.Button("Excluir",  key='-DEL-RES-'), sg.Button("Pesquisar", key='-FILTER-RES-', size=(100, 1))],
                  [sg.Text("Filtro"), sg.Input(key='-FILTER-RES-INPUT-')],
                  [sg.Table(values=db.getTabelaReservas(), headings=cabecalhoReservas, max_col_width=25,
                            background_color='black',
                            auto_size_columns=True,
                            display_row_numbers=True,
                            justification='right',
                            num_rows=20,
                            alternating_row_color='black',
                            key='-TABLE-RES-',
                            row_height=25, expand_x=True, expand_y=True)]]

# ---- TELA PRINCIPAL ----
layout = [[sg.TabGroup(
    [[sg.Tab('Técnicos', layoutTecnicos),
      sg.Tab('Ferramentas', layoutFerramentas), 
      sg.Tab('Reservas', layoutReservas)]],
    key='-TAB GROUP-', expand_x=True, expand_y=True)]]

window = sg.Window('Sistema', layout, location=(0, 0),
                   finalize=True, resizable=True)


while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED and window.Title == "Sistema":
        break

    if event == '-NEW-TEC-':
        col_layout = [[sg.Button('Cancelar'), sg.Button('OK')]]
        layout = [
            item_formulario(sg, "CPF", "input"),
            item_formulario(sg, "Nome", "input"),
            item_formulario(sg, "Telefone", "input"),
            item_formulario(sg, "Turno", "combo", '',
                            ('', 'Manhã', 'Tarde', 'Noite')),
            item_formulario(sg, "Equipe", "input"),
            [sg.Text("Erro: ", visible=False, expand_x=True,
                     key="-ERRO-", text_color='red')],
            [sg.Column(col_layout, expand_x=True,
                       element_justification='right')],
        ]
        popup = sg.Window("Novo Técnico", layout,
                          use_default_focus=False, finalize=True, modal=True)

        while True:
            event, values = popup.read()

            if event == sg.WIN_CLOSED or event == "Cancelar":
                popup.close()
                break

            if event == "OK":
                if any(tecnico.CPF == values['-CPF-'] for tecnico in db.Tecnicos):
                    popup['-ERRO-'].update(visible=True)
                    popup['-ERRO-'].update('CPF já existe na base')
                    continue

                try:
                    tecnico = Tecnico(values['-CPF-'])
                    tecnico.setNome(values['-Nome-'])
                    tecnico.setTelefone(values['-Telefone-'])
                    tecnico.setTurno(values['-Turno-'])
                    tecnico.setEquipe(values['-Equipe-'])
                    db.Tecnicos.append(tecnico)

                    window['-TABLE-TEC-'].update(db.getTabelaTecnicos())

                    db.persistirTecnicos()
                    popup.close()
                    break

                except AttributeError as e:
                    popup['-ERRO-'].update(visible=True)
                    popup['-ERRO-'].update("Erro: " + str(e))

    if event == '-EDIT-TEC-':
        if len(window['-TABLE-TEC-'].SelectedRows) == 0:
            sg.popup("Nenhum item selecionado", keep_on_top=True, modal=True)
            continue

        if len(window['-TABLE-TEC-'].SelectedRows) > 1:
            sg.popup("Selecione apenas um item", keep_on_top=True, modal=True)
            continue

        indexLinha = window['-TABLE-TEC-'].SelectedRows[0]
        linha = window['-TABLE-TEC-'].Values[indexLinha]

        col_layout = [[sg.Button('Cancelar'), sg.Button('OK')]]
        layout = [
            item_formulario(sg, "CPF", "input", linha[0], bloqueado=True),
            item_formulario(sg, "Nome", "input", linha[1]),
            item_formulario(sg, "Telefone", "input", linha[2]),
            item_formulario(sg, "Turno", "combo",
                            linha[3], ('', 'Manhã', 'Tarde', 'Noite')),
            item_formulario(sg, "Equipe", "input", linha[4]),
            [sg.Text("Erro: ", visible=False, expand_x=True,
                     key="-ERRO-", text_color='red')],
            [sg.Column(col_layout, expand_x=True,
                       element_justification='right')],
        ]
        popup = sg.Window("Editar Técnico", layout,
                          use_default_focus=False, finalize=True, modal=True)

        while True:
            event, values = popup.read()

            if event == sg.WIN_CLOSED or event == "Cancelar":
                popup.close()
                break

            if event == "OK":
                for item in db.Tecnicos:
                    if item.CPF == linha[0]:
                        tecnico = item
                        break

                try:
                    tecnico.setNome(values['-Nome-'])
                    tecnico.setTelefone(values['-Telefone-'])
                    tecnico.setTurno(values['-Turno-'])
                    tecnico.setEquipe(values['-Equipe-'])

                    window['-TABLE-TEC-'].update(db.getTabelaTecnicos())

                    db.persistirTecnicos()
                    popup.close()
                    break

                except AttributeError as e:
                    popup['-ERRO-'].update(visible=True)
                    popup['-ERRO-'].update("Erro: " + str(e))

    if event == '-DEL-TEC-':
        if len(window['-TABLE-TEC-'].SelectedRows) == 0:
            sg.popup("Nenhum item selecionado", keep_on_top=True, modal=True)

        for indexLinha in window['-TABLE-TEC-'].SelectedRows[::-1]:
            linha = window['-TABLE-TEC-'].Values[indexLinha]

            for tecnico in db.Tecnicos:
                if tecnico.CPF == linha[0]:
                    db.Tecnicos.remove(tecnico)

        window['-TABLE-TEC-'].update(db.getTabelaTecnicos())
        db.persistirTecnicos()

    if event == '-FILTER-TEC-':
        filtro = values['-FILTER-TEC-INPUT-'].lower()
        dadosTecnicosFiltrados = []

        if filtro == None or filtro == '':
            dadosTecnicosFiltrados = db.getTabelaTecnicos()

        else:
            for tecnico in db.Tecnicos:
                if (filtro in tecnico.CPF or
                   filtro in tecnico.Nome.lower() or
                   filtro in tecnico.Telefone or
                   filtro in tecnico.Turno.lower() or
                   filtro in tecnico.Equipe.lower()):
                    dadosTecnicosFiltrados.append([tecnico.CPF, tecnico.getNome(), tecnico.getTelefone(),
                                                   tecnico.getTurno(), tecnico.getEquipe()])

        window['-TABLE-TEC-'].update(dadosTecnicosFiltrados)

    if event == '-NEW-TOOL-':
        col_layout = [[sg.Button('Cancelar'), sg.Button('OK')]]
        layout = [
            item_formulario(sg, "Id", "input", bloqueado=True),
            item_formulario(sg, "Descrição", "input"),
            item_formulario(sg, "Fabricante", "input"),
            item_formulario(sg, "Voltagem", "input"),
            item_formulario(sg, "Part Number", "input"),
            item_formulario(sg, "Tamanho", "input"),
            item_formulario(sg, "Unidade Medida", "combo", '',
                            ('', 'CM', 'Polegadas', 'Metros', 'Outro')),
            item_formulario(sg, "Tipo", "combo", '',
                            ('', 'Elétrica', 'Mecânica', 'Segurança', 'Outro')),
            item_formulario(sg, "Material", "combo", '', ('', 'Ferro',
                            'Madeira', 'Borracha', 'Plástico', 'Outro')),
            item_formulario(sg, "Tempo Máximo Reserva", "input"),
            [sg.Text("Erro: ", visible=False, expand_x=True,
                     key="-ERRO-", text_color='red')],
            [sg.Column(col_layout, expand_x=True,
                       element_justification='right')],
        ]
        popup = sg.Window("Nova Ferramenta", layout,
                          use_default_focus=False, finalize=True, modal=True)

        while True:
            event, values = popup.read()

            if event == sg.WIN_CLOSED or event == "Cancelar":
                popup.close()
                break

            if event == "OK":
                try:
                    ferramenta = Ferramenta()
                    ferramenta.setDescricao(values['-Descrição-'])
                    ferramenta.setFabricante(values['-Fabricante-'])
                    ferramenta.setVoltagem(values['-Voltagem-'])
                    ferramenta.setPartNumber(values['-Part Number-'])
                    ferramenta.setTamanho(values['-Tamanho-'])
                    ferramenta.setUnidadeMedida(values['-Unidade Medida-'])
                    ferramenta.setTipo(values['-Tipo-'])
                    ferramenta.setMaterial(values['-Material-'])
                    ferramenta.setTempoMaximoReserva(
                        values['-Tempo Máximo Reserva-'])
                    db.Ferramentas.append(ferramenta)

                    window['-TABLE-TOOL-'].update(db.getTabelaFerramentas())

                    db.persistirFerramentas()
                    popup.close()
                    break

                except AttributeError as e:
                    popup['-ERRO-'].update(visible=True)
                    popup['-ERRO-'].update("Erro: " + str(e))

    if event == '-EDIT-TOOL-':
        if len(window['-TABLE-TOOL-'].SelectedRows) == 0:
            sg.popup("Nenhum item selecionado", keep_on_top=True, modal=True)
            continue

        if len(window['-TABLE-TOOL-'].SelectedRows) > 1:
            sg.popup("Selecione apenas um item", keep_on_top=True, modal=True)
            continue

        indexLinha = window['-TABLE-TOOL-'].SelectedRows[0]
        linha = window['-TABLE-TOOL-'].Values[indexLinha]

        col_layout = [[sg.Button('Cancelar'), sg.Button('OK')]]
        layout = [
            item_formulario(sg, "Id", "input", linha[0], bloqueado=True),
            item_formulario(sg, "Descrição", "input", linha[1]),
            item_formulario(sg, "Fabricante", "input", linha[2]),
            item_formulario(sg, "Voltagem", "input", linha[3]),
            item_formulario(sg, "Part Number", "input", linha[4]),
            item_formulario(sg, "Tamanho", "input", linha[5]),
            item_formulario(sg, "Unidade Medida", "combo", linha[6],
                            ('', 'CM', 'Polegadas', 'Metros', 'Outro')),
            item_formulario(sg, "Tipo", "combo", linha[7],
                            ('', 'Elétrica', 'Mecânica', 'Segurança', 'Outro')),
            item_formulario(sg, "Material", "combo", linha[8], ('', 'Ferro',
                            'Madeira', 'Borracha', 'Plástico', 'Outro')),
            item_formulario(sg, "Tempo Máximo Reserva", "input", linha[9]),
            [sg.Text("Erro: ", visible=False, expand_x=True,
                     key="-ERRO-", text_color='red')],
            [sg.Column(col_layout, expand_x=True,
                       element_justification='right')],
        ]
        popup = sg.Window("Editar Ferramenta", layout,
                          use_default_focus=False, finalize=True, modal=True)

        while True:
            event, values = popup.read()

            if event == sg.WIN_CLOSED or event == "Cancelar":
                popup.close()
                break

            if event == "OK":
                for item in db.Ferramentas:
                    if item.Id == linha[0]:
                        ferramenta = item
                        break

                try:
                    ferramenta.setDescricao(values['-Descrição-'])
                    ferramenta.setFabricante(values['-Fabricante-'])
                    ferramenta.setVoltagem(values['-Voltagem-'])
                    ferramenta.setPartNumber(values['-Part Number-'])
                    ferramenta.setTamanho(values['-Tamanho-'])
                    ferramenta.setUnidadeMedida(values['-Unidade Medida-'])
                    ferramenta.setTipo(values['-Tipo-'])
                    ferramenta.setMaterial(values['-Material-'])
                    ferramenta.setTempoMaximoReserva(
                        values['-Tempo Máximo Reserva-'])

                    window['-TABLE-TOOL-'].update(db.getTabelaFerramentas())

                    db.persistirFerramentas()
                    popup.close()
                    break

                except AttributeError as e:
                    popup['-ERRO-'].update(visible=True)
                    popup['-ERRO-'].update("Erro: " + str(e))

    if event == '-DEL-TOOL-':
        if len(window['-TABLE-TOOL-'].SelectedRows) == 0:
            sg.popup("Nenhum item selecionado", keep_on_top=True, modal=True)

        for indexLinha in window['-TABLE-TOOL-'].SelectedRows[::-1]:
            linha = window['-TABLE-TOOL-'].Values[indexLinha]

            for ferramenta in db.Ferramentas:
                if ferramenta.Id == linha[0]:
                    db.Ferramentas.remove(ferramenta)

        window['-TABLE-TOOL-'].update(db.getTabelaFerramentas())
        db.persistirFerramentas()

    if event == '-FILTER-TOOL-':
        filtro = values['-FILTER-TOOL-INPUT-'].lower()
        dadosFerramentasFiltrados = []

        if filtro == None or filtro == '':
            dadosFerramentasFiltrados = db.getTabelaFerramentas()

        else:
            for ferramenta in db.Ferramentas:
                if (filtro in ferramenta.Id or
                   filtro in ferramenta.Descricao.lower() or
                   filtro in ferramenta.PartNumber.lower() or
                   filtro in ferramenta.Tipo.lower()):
                    dadosFerramentasFiltrados.append([ferramenta.Id, ferramenta.getDescricao(), ferramenta.getFabricante(),
                                    ferramenta.getVoltagem(), ferramenta.getPartNumber(), ferramenta.getTamanho(),
                                    ferramenta.getUnidadeMedida(), ferramenta.getTipo(), ferramenta.getMaterial(),
                                    ferramenta.getTempoMaximoReserva()])

        window['-TABLE-TOOL-'].update(dadosFerramentasFiltrados)

    if event == '-NEW-RES-':
        col_layout = [[sg.Button('Cancelar'), sg.Button('OK')]]
        layout = [
            item_formulario(sg, "Id", "input", bloqueado=True),
            item_formulario(sg, "Ferramenta", "combo", "", db.getFerramentasParaCampo()),
            item_formulario(sg, "Técnico", "combo", "", db.getTecnicosParaCampo()),
            item_formulario(sg, "Descrição", "input"),
            [sg.Text('Data Retirada :', size=(12, 1)), sg.Input(key='-Data Retirada-', expand_x=True), sg.CalendarButton('Data Retirada',  target='-Data Retirada-', locale='pt_BR', begin_at_sunday_plus=1, size=(14,1) )],
            [sg.Text('Data Devolução :', size=(12, 1)), sg.Input(key='-Data Devolução-', expand_x=True), sg.CalendarButton('Data Devolução',  target='-Data Devolução-', locale='pt_BR', begin_at_sunday_plus=1, size=(14,1) )],
            [sg.Text("Erro: ", visible=False, expand_x=True,
                     key="-ERRO-", text_color='red')],
            [sg.Column(col_layout, expand_x=True,
                       element_justification='right')],
        ]
        popup = sg.Window("Nova Reserva", layout,
                          use_default_focus=False, finalize=True, modal=True)

        while True:
            event, values = popup.read()

            if event == sg.WIN_CLOSED or event == "Cancelar":
                popup.close()
                break

            if event == "OK":
                
                try:
                    if values['-Ferramenta-'] == '':
                        reserva = Reserva('', '')
                        
                    if values['-Técnico-'] == '':
                        reserva = Reserva(values['-Ferramenta-'][0], '')
                        
                    reserva = Reserva(values['-Ferramenta-'][0], values['-Técnico-'][0])
                    reserva.setDescricao(values['-Descrição-'])
                    reserva.setDataRetirada(values['-Data Retirada-'])
                    reserva.setDataDevolucao(values['-Data Devolução-'])
                    db.validarReserva(reserva, values['-Ferramenta-'][0])
                    db.Reservas.append(reserva)
                    
                    window['-TABLE-RES-'].update(db.getTabelaReservas())

                    db.persistirReservas()
                    popup.close()
                    break

                except AttributeError as e:
                    popup['-ERRO-'].update(visible=True)
                    popup['-ERRO-'].update("Erro: " + str(e))
                    
    if event == '-EDIT-RES-':
        if len(window['-TABLE-RES-'].SelectedRows) == 0:
            sg.popup("Nenhum item selecionado", keep_on_top=True, modal=True)
            continue

        if len(window['-TABLE-RES-'].SelectedRows) > 1:
            sg.popup("Selecione apenas um item", keep_on_top=True, modal=True)
            continue

        indexLinha = window['-TABLE-RES-'].SelectedRows[0]
        linha = window['-TABLE-RES-'].Values[indexLinha]

        col_layout = [[sg.Button('Cancelar'), sg.Button('OK')]]
        layout = [
            item_formulario(sg, "Id", "input", linha[0], bloqueado=True),
            item_formulario(sg, "Ferramenta", "combo", linha[1], db.getFerramentasParaCampo(), bloqueado=True),
            item_formulario(sg, "Técnico", "combo", linha[2], db.getTecnicosParaCampo(), bloqueado=True),
            item_formulario(sg, "Descrição", "input", linha[3]),
            [sg.Text('Data Retirada :', size=(12, 1)), sg.Input(linha[4], key='-Data Retirada-', expand_x=True), sg.CalendarButton('Data Retirada',  target='-Data Retirada-', locale='pt_BR', begin_at_sunday_plus=1, size=(14,1) )],
            [sg.Text('Data Devolução :', size=(12, 1)), sg.Input(linha[5], key='-Data Devolução-', expand_x=True), sg.CalendarButton('Data Devolução',  target='-Data Devolução-', locale='pt_BR', begin_at_sunday_plus=1, size=(14,1) )],
            [sg.Text("Erro: ", visible=False, expand_x=True,
                     key="-ERRO-", text_color='red')],
            [sg.Column(col_layout, expand_x=True,
                       element_justification='right')],
        ]
        popup = sg.Window("Editar Reserva", layout,
                          use_default_focus=False, finalize=True, modal=True)

        while True:
            event, values = popup.read()

            if event == sg.WIN_CLOSED or event == "Cancelar":
                popup.close()
                break

            if event == "OK":
                for item in db.Reservas:
                    if item.Id == linha[0]:
                        reserva = item
                        break

                try:
                    reserva.setDescricao(values['-Descrição-'])
                    reserva.setDataRetirada(values['-Data Retirada-'])
                    reserva.setDataDevolucao(values['-Data Devolução-'])
                    db.validarReserva(reserva, values['-Ferramenta-'])

                    window['-TABLE-RES-'].update(db.getTabelaReservas())

                    db.persistirReservas()
                    popup.close()
                    break

                except AttributeError as e:
                    popup['-ERRO-'].update(visible=True)
                    popup['-ERRO-'].update("Erro: " + str(e))

    if event == '-DEL-RES-':
        if len(window['-TABLE-RES-'].SelectedRows) == 0:
            sg.popup("Nenhum item selecionado", keep_on_top=True, modal=True)

        for indexLinha in window['-TABLE-RES-'].SelectedRows[::-1]:
            linha = window['-TABLE-RES-'].Values[indexLinha]

            for reserva in db.Reservas:
                if reserva.Id == linha[0]:
                    db.Reservas.remove(reserva)

        window['-TABLE-RES-'].update(db.getTabelaReservas())
        db.persistirReservas()

    if event == '-FILTER-RES-':
        filtro = values['-FILTER-RES-INPUT-'].lower()
        dadosReservasFiltradas = []

        if filtro == None or filtro == '':
            dadosReservasFiltradas = db.getTabelaReservas()

        else:
            for reserva in db.Reservas:
                if (filtro in reserva.Id or
                   filtro in reserva.IdFerramenta or
                   filtro in reserva.CpfTecnico.lower() or
                   filtro in reserva.Descricao.lower() or
                   filtro in str(reserva.DataDevolucao) or
                   filtro in str(reserva.DataRetirada)):
                    dadosReservasFiltradas.append([reserva.Id, reserva.IdFerramenta, reserva.CpfTecnico, reserva.Descricao,
                                                   reserva.DataRetirada, reserva.DataDevolucao])

        window['-TABLE-RES-'].update(dadosReservasFiltradas)
        
window.close()

