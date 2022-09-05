import csv

from modelo import Ferramenta, Tecnico


class DB:

    def __init__(self) -> None:
        self.Tecnicos: list[Tecnico] = []
        self.Ferramentas: list[Ferramenta] = []

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
