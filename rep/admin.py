from django.contrib import admin
from .models import (Departamento, EspecialidadeMedica, Funcionario, Consulta, Paciente, Pagamento,
                    ExameMedico, Post,
                    Equipamento, Fatura, Consumivel, Seguradora, ProcedimentoMedico, Agendamento,
                    DetalheFuncionario,
                    DetalhePaciente, ReceitaMedica, RegistroInternacao, HistoricoConsulta,
                    ProcedimentoCirurgico,
                    RegistroVacinacao, TesteLaboratorial, AlergiaCondicao, HistoricoPagamento,
                    ContatoEmergencia)

# Register your models here.
admin.site.register(Departamento)
admin.site.register(EspecialidadeMedica)
admin.site.register(Funcionario)
admin.site.register(Consulta)
admin.site.register(Paciente)
admin.site.register(Pagamento)
admin.site.register(ExameMedico)
admin.site.register(Equipamento)
admin.site.register(Fatura)
admin.site.register(Consumivel)
admin.site.register(Seguradora)
admin.site.register(ProcedimentoMedico)
admin.site.register(Agendamento)
admin.site.register(DetalheFuncionario)
admin.site.register(DetalhePaciente)
admin.site.register(ReceitaMedica)
admin.site.register(RegistroInternacao)
admin.site.register(HistoricoConsulta)
admin.site.register(ProcedimentoCirurgico)
admin.site.register(RegistroVacinacao)
admin.site.register(TesteLaboratorial)
admin.site.register(AlergiaCondicao)
admin.site.register(HistoricoPagamento)
admin.site.register(ContatoEmergencia)
admin.site.register(Post)
