from django.db import models


class Departamento(models.Model):
    nome = models.CharField(max_length = 100)

    def __str__(self):
        return self.nome


class EspecialidadeMedica(models.Model):
    nome = models.CharField(max_length = 100)

    def __str__(self):
        return self.nome


class Funcionario(models.Model):
    nome = models.CharField(max_length = 100)
    departamento = models.ForeignKey(Departamento, on_delete = models.SET_NULL, null = True, blank = True)

    def __str__(self):
        return self.nome


class Paciente(models.Model):
    nome = models.CharField(max_length = 100)
    data_nascimento = models.DateField()

    def __str__(self):
        return self.nome


class Consulta(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete = models.CASCADE)
    funcionario = models.ForeignKey(Funcionario, on_delete = models.CASCADE)
    data_consulta = models.DateTimeField()

    def __str__(self):
        return self.paciente


class Pagamento(models.Model):
    consulta = models.ForeignKey(Consulta, on_delete = models.CASCADE)
    valor = models.DecimalField(max_digits = 10, decimal_places = 2)
    data_pagamento = models.DateField()

    def __str__(self):
        return self.nome


class ExameMedico(models.Model):
    tipo_exame = models.CharField(max_length = 200)
    paciente = models.ForeignKey(Paciente, on_delete = models.CASCADE)
    descricao = models.TextField()
    data_exame = models.DateField()

    def __str__(self):
        return self.tipo_exame


class Equipamento(models.Model):
    nome = models.CharField(max_length = 100)
    descricao = models.TextField()

    def __str__(self):
        return self.nome


class Fatura(models.Model):
    nome_fatura = models.CharField(max_length = 100)
    paciente = models.ForeignKey(Paciente, on_delete = models.CASCADE)
    valor = models.DecimalField(max_digits = 10, decimal_places = 2)
    data_fatura = models.DateField()

    def __str__(self):
        return self.nome_fatura


class Consumivel(models.Model):
    nome = models.CharField(max_length = 100)
    descricao = models.TextField()

    def __str__(self):
        return self.nome


class Seguradora(models.Model):
    nome = models.CharField(max_length = 100)
    contato = models.CharField(max_length = 100)

    def __str__(self):
        return self.nome


class ProcedimentoMedico(models.Model):
    nome = models.CharField(max_length = 100)
    descricao = models.TextField()

    def __str__(self):
        return self.nome


class Agendamento(models.Model):
    nome_agendamento = models.CharField(max_length = 100)
    paciente = models.ForeignKey(Paciente, on_delete = models.CASCADE)
    data_agendamento = models.DateTimeField()

    def __str__(self):
        return self.nome


class DetalheFuncionario(models.Model):
    funcionario = models.ForeignKey(Funcionario, on_delete = models.CASCADE)
    detalhes = models.TextField()

    def __str__(self):
        return self.detalhes


class DetalhePaciente(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete = models.CASCADE)
    detalhes = models.TextField()

    def __str__(self):
        return self.detalhes


class ReceitaMedica(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete = models.CASCADE)
    medicamentos = models.TextField()
    data_receita = models.DateField()
    dosagem = models.TextField(500)

    def __str__(self):
        return self.medicamentos, dosagem


class RegistroInternacao(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete = models.CASCADE)
    data_entrada = models.DateField()
    data_saida = models.DateField(null = True, blank = True)
    quarto = models.CharField(max_length = 100)
    motivo = models.TextField()
    outros_dados = models.TextField(blank = True, null = True)

    def __str__(self):
        return self.motivo


class HistoricoConsulta(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete = models.CASCADE)
    consulta = models.ForeignKey(Consulta, on_delete = models.CASCADE)
    historico = models.TextField()

    def __str__(self):
        return self.historico


class ProcedimentoCirurgico(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete = models.CASCADE)
    tipo_procedimento = models.CharField(max_length = 100)
    medico_cirurgiao = models.ForeignKey(Funcionario, on_delete = models.CASCADE)
    data_cirurgia = models.DateField()
    outros_dados = models.TextField(blank = True, null = True)

    def __str__(self):
        return self.tipo_procedimento


class RegistroVacinacao(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete = models.CASCADE)
    vacina = models.CharField(max_length = 100)
    data_vacinacao = models.DateField()

    def __str__(self):
        return self.vacina


class TesteLaboratorial(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete = models.CASCADE)
    tipo_teste = models.CharField(max_length = 100)
    resultado = models.TextField()
    data_teste = models.DateField()

    def __str__(self):
        return self.tipo_teste


class AlergiaCondicao(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete = models.CASCADE)
    descricao = models.TextField()

    def __str__(self):
        return self.descricao


class HistoricoPagamento(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete = models.CASCADE)
    valor = models.DecimalField(max_digits = 10, decimal_places = 2)
    data_pagamento = models.DateField()

    def __str__(self):
        return self.data_pagamento


class ContatoEmergencia(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete = models.CASCADE)
    nome = models.CharField(max_length = 100)
    telefone = models.CharField(max_length = 15)

    def __str__(self):
        return self.telefone


class Post(models.Model):
    objects = None
    title = models.CharField(max_length = 200)
    content = models.TextField()
    author = models.ForeignKey(Funcionario, on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return self.title

# Certifique-se de remover a função index() do models.py, pois ela não pertence a este arquivo.
