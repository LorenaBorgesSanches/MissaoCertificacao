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


def item_formulario(sg, label, tipo, valor='', opcoes=(), bloqueado=False):
    if tipo == 'input':
        return [sg.Text(label + ":", size=(12, 1)), sg.Input(valor, key='-' + label + '-', expand_x=True, disabled=bloqueado)]
    else:
        return [sg.Text(label + ":", size=(12, 1)), sg.Combo(key='-' + label + '-', values=opcoes, default_value=valor, expand_x=True, disabled=bloqueado)],
