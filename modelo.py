import uuid
from util import converter_data, cpf_validate, telefone_validate
import datetime


class Ferramenta:
    def __init__(self, Id: uuid = None):
        self.Id = Id
        if Id == None:
            self.Id = uuid.uuid4()
        self.Descricao = ""
        self.Fabricante = ""
        self.Voltagem = ""
        self.PartNumber = ""
        self.Tamanho = ""
        self.UnidadeMedida = ""
        self.Tipo = ""
        self.Material = ""
        self.TempoMaximoReserva = ""

    def setDescricao(self, Descricao: str):
        if Descricao != None and Descricao != '' and len(Descricao) > 60:
            raise AttributeError("Descricao deve conter até 60 caracteres")
        self.Descricao = Descricao

    def getDescricao(self):
        return self.Descricao

    def setFabricante(self, Fabricante: str):
        if Fabricante != None and Fabricante != '' and len(Fabricante) > 30:
            raise AttributeError("Fabricante deve conter até 30 caracteres")
        self.Fabricante = Fabricante

    def getFabricante(self):
        return self.Fabricante

    def setVoltagem(self, Voltagem: str):
        if Voltagem != None and Voltagem != '' and len(Voltagem) > 15:
            raise AttributeError("Voltagem deve conter até 30 caracteres")
        self.Voltagem = Voltagem

    def getVoltagem(self):
        return self.Voltagem

    def setPartNumber(self, PartNumber: str):
        if PartNumber != None and PartNumber != '' and len(PartNumber) > 25:
            raise AttributeError("PartNumber deve conter até 25 caracteres")
        self.PartNumber = PartNumber

    def getPartNumber(self):
        return self.PartNumber

    def setTamanho(self, Tamanho: str):
        if Tamanho != None and Tamanho != '' and len(Tamanho) > 20:
            raise AttributeError("Tamanho deve conter até 20 caracteres")
        self.Tamanho = Tamanho

    def getTamanho(self):
        return self.Tamanho

    def setUnidadeMedida(self, UnidadeMedida: str):
        if UnidadeMedida != None and UnidadeMedida != '' and len(UnidadeMedida) > 15:
            raise AttributeError("UnidadeMedida deve conter até 15 caracteres")
        self.UnidadeMedida = UnidadeMedida

    def getUnidadeMedida(self):
        return self.UnidadeMedida

    def setTipo(self, Tipo: str):
        if Tipo != None and Tipo != '' and len(Tipo) > 15:
            raise AttributeError("Tipo deve conter até 15 caracteres")
        self.Tipo = Tipo

    def getTipo(self):
        return self.Tipo

    def setMaterial(self, Material: str):
        if Material != None and Material != '' and len(Material) > 15:
            raise AttributeError("Material deve conter até 15 caracteres")
        self.Material = Material

    def getMaterial(self):
        return self.Material

    def setTempoMaximoReserva(self, TempoMaximoReserva: int):
        if TempoMaximoReserva != None and TempoMaximoReserva != '':
            try:
                self.TempoMaximoReserva = int(TempoMaximoReserva)
            except ValueError:
                raise AttributeError("O tempo máximo de reserva deve ser somente números!")
                
    def getTempoMaximoReserva(self):
        return self.TempoMaximoReserva


class Tecnico:
    def __init__(self, CPF: str):
        if CPF == None or CPF == '':
            raise AttributeError("Obrigatório informar o CPF")

        cpf_validado = cpf_validate(CPF)
        if cpf_validado == "":
            raise AttributeError("CPF informado inválido")

        self.CPF = cpf_validado
        self.Nome = ""
        self.Telefone = ""
        self.Turno = ""
        self.Equipe = ""

    def setNome(self, Nome: str):
        if Nome != None and Nome != '' and len(Nome) > 40:
            raise AttributeError("Nome deve conter até 40 caracteres")
        self.Nome = Nome

    def getNome(self):
        return self.Nome

    def setTelefone(self, Telefone: str):
        if Telefone != None and Telefone != '' and telefone_validate(Telefone) == False:
            raise AttributeError("Telefone informado inválido")
        self.Telefone = Telefone

    def getTelefone(self):
        return self.Telefone

    def setTurno(self, Turno: str):
        if (Turno != None and Turno != '' and
           Turno.capitalize() != "Manhã" and
           Turno.capitalize() != "Tarde" and
           Turno.capitalize() != "Noite"):
            raise AttributeError("Turno informado inválido")
        self.Turno = Turno

    def getTurno(self):
        return self.Turno

    def setEquipe(self, Equipe: str):
        if Equipe != None and Equipe != '' and len(Equipe) > 30:
            raise AttributeError("Equipe deve conter até 30 caracteres")
        self.Equipe = Equipe

    def getEquipe(self):
        return self.Equipe

class Reserva:
    def __init__(self, IdFerramenta: uuid, CpfTecnico: str, Id: uuid = None):
        if IdFerramenta == None or IdFerramenta == '':
            raise AttributeError("Obrigatório informar a Ferramenta")
    
        if CpfTecnico == None or CpfTecnico == '':
            raise AttributeError("Obrigatório informar o Técnico")
        
        self.Id = Id
        if Id == None:
            self.Id = uuid.uuid4()   
        
        self.IdFerramenta = IdFerramenta
        self.CpfTecnico = CpfTecnico
        self.Descricao = ""
        self.DataRetirada = ""
        self.DataDevolucao = ""
        
    def setDescricao(self, Descricao: str):
        if Descricao != None and Descricao != '' and len(Descricao) > 60:
            raise AttributeError("Descricao deve conter até 60 caracteres")
        self.Descricao = Descricao
        
    def getDescricao(self):
        return self.Descricao

    def setDataRetirada(self, DataRetirada: datetime.datetime):
        if DataRetirada == None or DataRetirada == '':
            raise AttributeError("Obrigatório informar a Data de Retirada")
        
        try:
            self.DataRetirada = converter_data(DataRetirada)
        except:
            raise AttributeError("Data de Retirada inválida!")
        
    def getDataRetirada(self):
        return self.DataRetirada
    
    def setDataDevolucao(self, DataDevolucao: datetime.datetime):
        if DataDevolucao == None or DataDevolucao == '':
            raise AttributeError("Obrigatório informar a Data de Devolução")
        
        try:
            self.DataDevolucao = converter_data(DataDevolucao)
        except ValueError:
            raise AttributeError("Data de Devolução inválida!")
        
    def getDataDevolucao(self):
        return self.DataDevolucao
    