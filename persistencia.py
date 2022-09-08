import csv
import uuid

from modelo import Ferramenta, Reserva, Tecnico
from dateutil.relativedelta import relativedelta

class DB:

    def __init__(self) -> None:
        self.Tecnicos: list[Tecnico] = []
        self.Ferramentas: list[Ferramenta] = []
        self.Reservas: list[Reserva] = []

    def inicializarDB(self):
        file = open('db_tecnicos.csv', encoding='utf-8')
        csvreader = csv.reader(file)

        self.Tecnicos = []
        for row in csvreader:
            tecnico = Tecnico(row[0])
            tecnico.setNome(row[1])
            tecnico.setTelefone(row[2])
            tecnico.setTurno(row[3])
            tecnico.setEquipe(row[4])

            self.Tecnicos.append(tecnico)

        file = open('db_ferramentas.csv', encoding='utf-8')
        csvreader = csv.reader(file)

        self.Ferramentas = []
        for row in csvreader:
            ferramenta = Ferramenta(row[0])
            ferramenta.setDescricao(row[1])
            ferramenta.setFabricante(row[2])
            ferramenta.setVoltagem(row[3])
            ferramenta.setPartNumber(row[4])
            ferramenta.setTamanho(row[5])
            ferramenta.setUnidadeMedida(row[6])
            ferramenta.setTipo(row[7])
            ferramenta.setMaterial(row[8])
            ferramenta.setTempoMaximoReserva(row[9])

            self.Ferramentas.append(ferramenta)

        file = open('db_reservas.csv', encoding='utf-8')
        csvreader = csv.reader(file)

        self.Reservas = []
        for row in csvreader:
            reserva = Reserva(row[1], row[2], row[0])
            reserva.setDescricao(row[3])
            reserva.setDataRetirada(row[4])
            reserva.setDataDevolucao(row[5])

            self.Reservas.append(reserva)

    def persistirTecnicos(self):
        data = []
        for tecnico in self.Tecnicos:
            data.append([tecnico.CPF, tecnico.Nome, tecnico.Telefone,
                        tecnico.Turno, tecnico.Equipe])

        with open('db_tecnicos.csv', 'w', newline="", encoding='utf-8') as file:
            csvwriter = csv.writer(file)
            csvwriter.writerows(data)

    def persistirFerramentas(self):
        data = []
        for ferramenta in self.Ferramentas:
            data.append([ferramenta.Id, ferramenta.Descricao, ferramenta.Fabricante,
                        ferramenta.Voltagem, ferramenta.PartNumber, ferramenta.Tamanho,
                        ferramenta.UnidadeMedida, ferramenta.Tipo, ferramenta.Material,
                        ferramenta.TempoMaximoReserva])

        with open('db_ferramentas.csv', 'w', newline="", encoding='utf-8') as file:
            csvwriter = csv.writer(file)
            csvwriter.writerows(data)

    def persistirReservas(self):
        data = []
        for reserva in self.Reservas:
            data.append([reserva.Id, reserva.IdFerramenta, reserva.CpfTecnico, reserva.Descricao,
                        reserva.DataRetirada, reserva.DataDevolucao])

        with open('db_reservas.csv', 'w', newline="", encoding='utf-8') as file:
            csvwriter = csv.writer(file)
            csvwriter.writerows(data)

    def getTabelaTecnicos(self):
        dadosTecnicos = []
        for tecnico in self.Tecnicos:
            dadosTecnicos.append([tecnico.CPF, tecnico.getNome(), tecnico.getTelefone(),
                                  tecnico.getTurno(), tecnico.getEquipe()])
        return dadosTecnicos

    def getTabelaFerramentas(self):
        dadosFerramentas = []
        for ferramenta in self.Ferramentas:
            dadosFerramentas.append([ferramenta.Id, ferramenta.getDescricao(), ferramenta.getFabricante(),
                                    ferramenta.getVoltagem(), ferramenta.getPartNumber(), ferramenta.getTamanho(),
                                    ferramenta.getUnidadeMedida(), ferramenta.getTipo(), ferramenta.getMaterial(),
                                    ferramenta.getTempoMaximoReserva()])
        return dadosFerramentas

    def getTabelaReservas(self):
        dadosReservas = []
        for reserva in self.Reservas:
            dadosReservas.append([reserva.Id, reserva.IdFerramenta, reserva.CpfTecnico, reserva.Descricao,
                                  reserva.DataRetirada, reserva.DataDevolucao])
        return dadosReservas
    
    def getTecnicosParaCampo(self):
        dados = []
        for tecnico in self.Tecnicos:
            dados.append([tecnico.CPF, tecnico.Nome])
        return dados

    def getFerramentasParaCampo(self):
        dados = []
        for ferramenta in self.Ferramentas:
            dados.append([ferramenta.Id, ferramenta.Descricao])
        return dados
    
    
    def validarReserva(self, Reserva: Reserva, IdFerramenta: uuid):
        for ferramenta in self.Ferramentas:
            if ferramenta.Id == IdFerramenta:
                Ferramenta = ferramenta
                break
            
        dataMaxima = Reserva.DataRetirada + relativedelta(hours = Ferramenta.TempoMaximoReserva)
        
        if Reserva.DataDevolucao > dataMaxima:
            raise AttributeError(f'Deve devolver até no máximo {dataMaxima}')
        
        for reserva in self.Reservas:
            if reserva.IdFerramenta == IdFerramenta and reserva.Id != Reserva.Id:
                if Reserva.DataRetirada >= reserva.DataRetirada and Reserva.DataRetirada <= reserva.DataDevolucao:
                     raise AttributeError(f'Ferramenta está indisponível para esse horário')
                
                if Reserva.DataDevolucao <= reserva.DataDevolucao and Reserva.DataDevolucao >= reserva.DataRetirada:
                     raise AttributeError(f'Ferramenta está indisponível para esse horário')