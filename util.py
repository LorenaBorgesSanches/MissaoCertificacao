import datetime


def cpf_validate(numbers: str):
    cpf = [int(char) for char in numbers if char.isdigit()]
    cpfTesto = "".join([char for char in numbers if char.isdigit()])

    if len(cpf) != 11:
        return ""

    if cpf == cpf[::-1]:
        return ""

    for i in range(9, 11):
        value = sum((cpf[num] * ((i+1) - num) for num in range(0, i)))
        digit = ((value * 10) % 11) % 10
        if digit != cpf[i]:
            return ""
    return cpfTesto


def telefone_validate(telefone: str):
    for numero in telefone:
        if numero.isdigit() == False:
            return False

    if len(telefone) != 8 and len(telefone) != 9:
        return False

    return True


def converter_data(data: str):
    parteData = data.split('-')
    parteHora = parteData[2].split(' ')[1].split(':')

    ano = int(parteData[0])
    mes = int(parteData[1])
    dia = int(parteData[2].split(' ')[0])
    hora = int(parteHora[0])
    minuto = int(parteHora[1])
    segundo = int(parteHora[2])

    return datetime.datetime(
        ano, mes, dia, hora, minuto, segundo
    )


def item_formulario(sg, label, tipo, valor='', opcoes=(), bloqueado=False):
    if tipo == 'input':
        return [sg.Text(label + ":", size=(12, 1)), sg.Input(valor, key='-' + label + '-', expand_x=True, disabled=bloqueado)]
    else:
        return [sg.Text(label + ":", size=(12, 1)), sg.Combo(key='-' + label + '-', values=opcoes, default_value=valor, expand_x=True, disabled=bloqueado, readonly=True)],
