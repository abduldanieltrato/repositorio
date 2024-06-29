from rest_framework import serializers
from .models import (Paciente, Departamento, Funcionario, Consulta, Pagamento, ExameMedico, Equipamento,
                     Fatura, Consumivel, Seguradora, ProcedimentoMedico, Agendamento, DetalheFuncionario,
                     DetalhePaciente, ReceitaMedica, RegistroInternacao, HistoricoConsulta,
                     ProcedimentoCirurgico,
                     RegistroVacinacao, TesteLaboratorial, AlergiaCondicao, HistoricoPagamento,
                     ContatoEmergencia,
                     Post, EspecialidadeMedica)


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'


class PacienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Paciente
        fields = '__all__'


class DepartamentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Departamento
        fields = '__all__'


class FuncionarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Funcionario
        fields = '__all__'


class ConsultaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Consulta
        fields = '__all__'


class PagamentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pagamento
        fields = '__all__'


class ExameMedicoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExameMedico
        fields = '__all__'


class EquipamentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Equipamento
        fields = '__all__'


class FaturaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fatura
        fields = '__all__'


class ConsumivelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Consumivel
        fields = '__all__'


class SeguradoraSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seguradora
        fields = '__all__'


class ProcedimentoMedicoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProcedimentoMedico
        fields = '__all__'


class AgendamentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Agendamento
        fields = '__all__'


class DetalheFuncionarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetalheFuncionario
        fields = '__all__'


class DetalhePacienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetalhePaciente
        fields = '__all__'


class ReceitaMedicaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReceitaMedica
        fields = '__all__'


class RegistroInternacaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegistroInternacao
        fields = '__all__'


class HistoricoConsultaSerializer(serializers.ModelSerializer):
    class Meta:
        model = HistoricoConsulta
        fields = '__all__'


class ProcedimentoCirurgicoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProcedimentoCirurgico
        fields = '__all__'


class RegistroVacinacaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegistroVacinacao
        fields = '__all__'


class TesteLaboratorialSerializer(serializers.ModelSerializer):
    class Meta:
        model = TesteLaboratorial
        fields = '__all__'


class AlergiaCondicaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = AlergiaCondicao
        fields = '__all__'


class HistoricoPagamentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = HistoricoPagamento
        fields = '__all__'


class ContatoEmergenciaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContatoEmergencia
        fields = '__all__'


class EspecialidadeMedicaSerializer(serializers.ModelSerializer):
    class Meta:
        model = EspecialidadeMedica
        fields = '__all__'
