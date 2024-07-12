import json
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.http import JsonResponse,HttpResponse,HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from models import (
	Departamento,Funcionario,Consulta,Paciente,Pagamento,ExameMedico,Equipamento,Fatura,
	Consumivel,Seguradora,ProcedimentoMedico,Agendamento,DetalheFuncionario,DetalhePaciente,ReceitaMedica,
	RegistroInternacao,HistoricoConsulta,ProcedimentoCirurgico,RegistroVacinacao,TesteLaboratorial,AlergiaCondicao,
	HistoricoPagamento,ContatoEmergencia,EspecialidadeMedica
	)


def receita_medica_detail ( request,receita_medica_id ):
	receita_medica = get_object_or_404 (ReceitaMedica,pk = receita_medica_id)
	context = {'receita_medica':receita_medica,}
	if request.headers.get ('Accept') == 'application/json':
		data = {
				'receita_medica':{
						'paciente_id': receita_medica.paciente_id,'medicamentos':receita_medica.medicamentos,
						'data_receita':receita_medica.data_receita,
						'outros_dados':receita_medica.outros_dados if receita_medica.outros_dados is not None else ""
						}
				}
		return JsonResponse (data)
	else:
		return render (request,'receita_medica_detail.html',context)


@csrf_exempt
def receita_medica_create ( request ):
	if request.method == 'POST':
		try:
			if request.content_type == 'application/json':
				data = json.loads (request.body)
			else:
				data = request.POST
			
			paciente_id = data.get ('paciente_id')
			medicamentos = data.get ('medicamentos')
			data_receita_str = data.get ('data_receita')
			outros_dados = data.get ('outros_dados','')
			
			# Verifica se os campos obrigatórios estão presentes
			if not paciente_id or not medicamentos or not data_receita_str:
				return JsonResponse ({'mensagem':'Campos obrigatórios não fornecidos'},status = 400)
			
			# Valida o formato da data de receita
			try:
				data_receita = parse_date (data_receita_str)
			except ValueError:
				return JsonResponse ({'mensagem':'Formato de data inválido'},status = 400)
			
			# Cria a receita médica
			receita_medica = ReceitaMedica.objects.create (
					paciente_id = paciente_id,medicamentos = medicamentos,
					data_receita = data_receita,outros_dados = outros_dados
					)
			return JsonResponse ({'mensagem':'Receita médica criada com sucesso!'},status = 201)
		except KeyError:
			return JsonResponse ({'mensagem':'Dados incompletos ou inválidos'},status = 400)
	return HttpResponse (status = 400)


@csrf_exempt
def receita_medica_update ( request,receita_medica_id ):
	receita_medica = get_object_or_404 (ReceitaMedica,pk = receita_medica_id)
	if request.method == 'PUT':
		try:
			if request.content_type == 'application/json':
				data = json.loads (request.body)
			else:
				data = request.POST
			
			paciente_id = data.get ('paciente_id')
			medicamentos = data.get ('medicamentos')
			data_receita_str = data.get ('data_receita')
			outros_dados = data.get ('outros_dados','')
			
			# Verifica se os campos obrigatórios estão presentes
			if not paciente_id or not medicamentos or not data_receita_str:
				return JsonResponse ({'mensagem':'Campos obrigatórios não fornecidos'},status = 400)
			
			# Valida o formato da data de receita
			try:
				data_receita = parse_date (data_receita_str)
			except ValueError:
				return JsonResponse ({'mensagem':'Formato de data inválido'},status = 400)
			
			# Atualiza a receita médica
			receita_medica.paciente_id = paciente_id
			receita_medica.medicamentos = medicamentos
			receita_medica.data_receita = data_receita
			receita_medica.outros_dados = outros_dados
			receita_medica.save ()
			return JsonResponse ({'mensagem':'Receita médica atualizada com sucesso!'})
		except KeyError:
			return JsonResponse ({'mensagem':'Dados incompletos ou inválidos'},status = 400)
	return HttpResponse (status = 400)


def receita_medica_form ( request ):
	return render (request,'receita_medica_form.html')


@csrf_exempt
def receita_medica_delete ( request,receita_medica_id ):
	receita_medica = get_object_or_404 (ReceitaMedica,pk = receita_medica_id)
	if request.method == 'DELETE':
		receita_medica.delete ()
		return HttpResponse ("Receita médica deletada com sucesso!",status = 200)
	return HttpResponse ("Erro ao tentar deletar a receita médica",status = 400)


def registro_internacao_list ( request ):
	registros_internacao = RegistroInternacao.objects.all ()
	return render (request,'registro_internacao_list.html',{'registros_internacao':registros_internacao})


def registro_internacao_detail ( request,registro_internacao_id ):
	registro_internacao = get_object_or_404 (RegistroInternacao,pk = registro_internacao_id)
	return render (request,'registro_internacao_detail.html',{'registro_internacao':registro_internacao})


@csrf_exempt
def registro_internacao_create ( request ):
	if request.method == 'POST':
		try:
			data = request.POST
			registro_internacao = RegistroInternacao.objects.create (
					paciente_id = data [ 'paciente_id' ],
					data_entrada = data [ 'data_entrada' ],data_saida = data [ 'data_saida' ],
					quarto = data [ 'quarto' ],motivo = data [ 'motivo' ],outros_dados = data [ 'outros_dados' ]
					)
			return JsonResponse ({'mensagem':'Registro de internação criado com sucesso!'},status = 201)
		except KeyError:
			return JsonResponse ({'mensagem':'Dados incompletos ou inválidos'},status = 400)
	return HttpResponse (status = 400)


@csrf_exempt
def registro_internacao_update ( request,registro_internacao_id ):
	registro_internacao = get_object_or_404 (RegistroInternacao,pk = registro_internacao_id)
	if request.method == 'PUT':
		data = json.loads (request.body)
		registro_internacao.paciente_id = data [ 'paciente_id' ]
		registro_internacao.data_entrada = data [ 'data_entrada' ]
		registro_internacao.data_saida = data [ 'data_saida' ]
		registro_internacao.quarto = data [ 'quarto' ]
		registro_internacao.motivo = data [ 'motivo' ]
		registro_internacao.outros_dados = data [ 'outros_dados' ]
		registro_internacao.save ()
		return JsonResponse ({'mensagem':'Registro de internação atualizado com sucesso!'})
	elif request.method == 'GET':
		return render (request,'update_registro_internacao.html',{'registro_internacao_id':registro_internacao_id})
	return HttpResponse (status = 400)


@csrf_exempt
def registro_internacao_delete ( request,registro_internacao_id ):
	registro_internacao = get_object_or_404 (RegistroInternacao,pk = registro_internacao_id)
	if request.method == 'DELETE':
		registro_internacao.delete ()
		return HttpResponse (status = 204)
	elif request.method == 'GET':
		return render (request,'delete_registro_internacao.html',{'registro_internacao_id':registro_internacao_id})
	return HttpResponse (status = 400)


@csrf_exempt
def funcionario_list ( request ):
	if request.method == 'GET':
		return render (request,'lista_funcionarios.html')
	else:
		funcionarios = Funcionario.objects.all ()
		data = {'funcionarios':list (funcionarios.values ())}
		return JsonResponse (data)


@csrf_exempt
def funcionario_detail ( request,funcionario_id ):
	if request.method == 'GET':
		return render (request,'detalhe_funcionario.html',{'funcionario_id':funcionario_id})
	else:
		funcionario = get_object_or_404 (Funcionario,pk = funcionario_id)
		data = {
				'funcionario':{
						'nome_funcionario':funcionario.nome_funcionario,
						'data_nascimento': funcionario.data_nascimento,'data_contratacao':funcionario.data_contratacao,
						'departamento':    funcionario.departamento.nome_departamento,
						'outros_dados':    funcionario.outros_dados
						}
				}
		return JsonResponse (data)


@csrf_exempt
def funcionario_create ( request ):
	if request.method == 'POST':
		data = request.POST
		funcionario = Funcionario.objects.create (
				departamento_id = data [ 'departamento_id' ],
				nome_funcionario = data [ 'nome_funcionario' ],data_nascimento = data [ 'data_nascimento' ],
				data_contratacao = data [ 'data_contratacao' ],outros_dados = data [ 'outros_dados' ]
				)
		return JsonResponse ({'mensagem':'Funcionário criado com sucesso!'},status = 201)
	return render (request,'criar_funcionario.html')


@csrf_exempt
def funcionario_update ( request,funcionario_id ):
	funcionario = get_object_or_404 (Funcionario,pk = funcionario_id)
	if request.method == 'PUT':
		data = json.loads (request.body)
		funcionario.departamento_id = data [ 'departamento_id' ]
		funcionario.nome_funcionario = data [ 'nome_funcionario' ]
		funcionario.data_nascimento = data [ 'data_nascimento' ]
		funcionario.data_contratacao = data [ 'data_contratacao' ]
		funcionario.outros_dados = data [ 'outros_dados' ]
		funcionario.save ()
		return JsonResponse ({'mensagem':'Funcionário atualizado com sucesso!'})
	elif request.method == 'GET':
		return render (request,'editar_funcionario.html',{'funcionario':funcionario})
	return HttpResponse (status = 400)


@csrf_exempt
def funcionario_delete ( request,funcionario_id ):
	funcionario = get_object_or_404 (Funcionario,pk = funcionario_id)
	if request.method == 'DELETE':
		funcionario.delete ()
		return HttpResponse (status = 204)
	elif request.method == 'GET':
		return render (request,'excluir_funcionario.html',{'funcionario':funcionario})
	return HttpResponse (status = 400)


def historico_pagamento_list ( request ):
	historico_pagamentos = HistoricoPagamento.objects.all ()
	return render (request,'historico_pagamento_list.html',{'historico_pagamentos':historico_pagamentos})


def historico_pagamento_detail ( request,historico_pagamento_id ):
	historico_pagamento = get_object_or_404 (HistoricoPagamento,pk = historico_pagamento_id)
	return render (request,'historico_pagamento_detail.html',{'historico_pagamento':historico_pagamento})


@csrf_exempt
def historico_pagamento_create ( request ):
	if request.method == 'POST':
		data = request.POST
		historico_pagamento = HistoricoPagamento.objects.create (
				fatura_id = data [ 'fatura_id' ],
				valor_pago = data [ 'valor_pago' ],data_pagamento = data [ 'data_pagamento' ],
				outros_dados = data [ 'outros_dados' ]
				)
		return JsonResponse ({'mensagem':'Registro de histórico de pagamento criado com sucesso!'},status = 201)
	return render (request,'historico_pagamento_create.html')


@csrf_exempt
def historico_pagamento_update ( request,historico_pagamento_id ):
	historico_pagamento = get_object_or_404 (HistoricoPagamento,pk = historico_pagamento_id)
	if request.method == 'PUT':
		data = request.POST
		historico_pagamento.fatura_id = data [ 'fatura_id' ]
		historico_pagamento.valor_pago = data [ 'valor_pago' ]
		historico_pagamento.data_pagamento = data [ 'data_pagamento' ]
		historico_pagamento.outros_dados = data [ 'outros_dados' ]
		historico_pagamento.save ()
		return JsonResponse ({'mensagem':'Registro de histórico de pagamento atualizado com sucesso!'})
	return render (request,'historico_pagamento_update.html',{'historico_pagamento':historico_pagamento})


@csrf_exempt
def historico_pagamento_delete ( request,historico_pagamento_id ):
	historico_pagamento = get_object_or_404 (HistoricoPagamento,pk = historico_pagamento_id)
	if request.method == 'DELETE':
		historico_pagamento.delete ()
		return HttpResponse (status = 204)
	return render (request,'confirmar_exclusao_historico_pagamento.html',{'historico_pagamento':historico_pagamento})


@csrf_exempt
def departamento_list ( request ):
	departamentos = Departamento.objects.all ()
	return render (request,'departamento_list.html',{'departamentos':departamentos})


@csrf_exempt
def departamento_detail ( request,departamento_id ):
	departamento = get_object_or_404 (Departamento,pk = departamento_id)
	return render (request,'departamento_detail.html',{'departamento':departamento})


@csrf_exempt
def departamento_create ( request ):
	if request.method == 'POST':
		data = request.POST
		departamento = Departamento.objects.create (
				nome_departamento = data [ 'nome_departamento' ],
				responsavel_id = data.get ('responsavel_id',None),outros_dados = data.get ('outros_dados',None)
				)
		return render (request,'departamento_create_success.html',{'departamento':departamento})
	return HttpResponse (status = 400)


@csrf_exempt
def departamento_update ( request,departamento_id ):
	departamento = get_object_or_404 (Departamento,pk = departamento_id)
	if request.method == 'PUT':
		data = request.POST  # Usaremos request.POST em vez de request.PUT
		departamento.nome_departamento = data.get ('nome_departamento',departamento.nome_departamento)
		departamento.responsavel_id = data.get ('responsavel_id',departamento.responsavel_id)
		departamento.outros_dados = data.get ('outros_dados',departamento.outros_dados)
		departamento.save ()
		return render (request,'departamento_update_success.html',{'departamento':departamento})
	return HttpResponse (status = 400)


@csrf_exempt
def departamento_delete ( request,departamento_id ):
	departamento = get_object_or_404 (Departamento,pk = departamento_id)
	if request.method == 'DELETE':
		departamento.delete ()
		return redirect ('home')  # Redirecionamento para a página inicial após a exclusão
	return HttpResponse (status = 400)


@csrf_exempt
def especialidade_list ( request ):
	especialidades = EspecialidadeMedica.objects.all ()
	return render (request,'especialidade_list.html',{'especialidades':especialidades})


@csrf_exempt
def especialidade_detail ( request,especialidade_id ):
	especialidade = get_object_or_404 (EspecialidadeMedica,pk = especialidade_id)
	return render (request,'especialidade_detail.html',{'especialidade':especialidade})


@csrf_exempt
def especialidade_create ( request ):
	if request.method == 'POST':
		data = request.POST
		especialidade = EspecialidadeMedica.objects.create (
				nome_especialidade = data [ 'nome_especialidade' ],
				outros_dados = data.get ('outros_dados',None)
				)
		return render (request,'especialidade_create_success.html',{'especialidade':especialidade})
	return HttpResponse (status = 400)


@csrf_exempt
def especialidade_update ( request,especialidade_id ):
	especialidade = get_object_or_404 (EspecialidadeMedica,pk = especialidade_id)
	if request.method == 'PUT':
		data = request.POST
		especialidade.nome_especialidade = data.get ('nome_especialidade',especialidade.nome_especialidade)
		especialidade.outros_dados = data.get ('outros_dados',especialidade.outros_dados)
		especialidade.save ()
		return render (request,'especialidade_update_success.html',{'especialidade':especialidade})
	return HttpResponse (status = 400)


@csrf_exempt
def especialidade_delete ( request,especialidade_id ):
	especialidade = get_object_or_404 (EspecialidadeMedica,pk = especialidade_id)
	if request.method == 'DELETE':
		especialidade.delete ()
		return render (request,'especialidade_delete_success.html')
	return HttpResponse (status = 400)


@csrf_exempt
def paciente_list ( request ):
	pacientes = Paciente.objects.all ()
	serializer = PacienteSerializer (pacientes,many = True)
	return render (request,'paciente_list.html',{'pacientes':serializer.data})


@csrf_exempt
def paciente_detail ( request,paciente_id ):
	paciente = get_object_or_404 (Paciente,pk = paciente_id)
	serializer = PacienteSerializer (paciente)
	return render (request,'paciente_detail.html',{'paciente':serializer.data})


@csrf_exempt
def paciente_create ( request ):
	if request.method == 'POST':
		nome = request.POST.get ('nome')
		data_nascimento = request.POST.get ('data_nascimento')
		endereco = request.POST.get ('endereco')
		telefone = request.POST.get ('telefone')
		outros_dados = request.POST.get ('outros_dados','')
		
		if nome and data_nascimento and endereco and telefone:
			paciente = Paciente.objects.create (
					nome = nome,data_nascimento = data_nascimento,endereco = endereco,
					telefone = telefone,outros_dados = outros_dados
					)
			return render (request,'paciente_create_success.html',{'paciente':paciente})
		else:
			errors = "Todos os campos obrigatórios devem ser preenchidos."
			return render (request,'paciente_create_error.html',{'errors':errors})
	return render (request,'paciente_create_form.html')


@csrf_exempt
def paciente_update ( request,paciente_id ):
	paciente = get_object_or_404 (Paciente,pk = paciente_id)
	if request.method == 'POST':
		nome = request.POST.get ('nome')
		data_nascimento = request.POST.get ('data_nascimento')
		endereco = request.POST.get ('endereco')
		telefone = request.POST.get ('telefone')
		outros_dados = request.POST.get ('outros_dados','')
		
		if nome and data_nascimento and endereco and telefone:
			paciente.nome = nome
			paciente.data_nascimento = data_nascimento
			paciente.endereco = endereco
			paciente.telefone = telefone
			paciente.outros_dados = outros_dados
			paciente.save ()
			return render (request,'paciente_update_success.html',{'paciente':paciente})
		else:
			errors = "Todos os campos obrigatórios devem ser preenchidos."
			return render (request,'paciente_update_error.html',{'errors':errors,'paciente':paciente})
	return render (request,'paciente_update_form.html',{'paciente':paciente})


@csrf_exempt
def paciente_delete ( request,paciente_id ):
	paciente = get_object_or_404 (Paciente,pk = paciente_id)
	if request.method == 'POST':
		paciente.delete ()
		return render (request,'paciente_delete_success.html',{'paciente':paciente})
	return render (request,'paciente_delete_confirm.html',{'paciente':paciente})


def consulta_list ( request ):
	consultas = Consulta.objects.all ()
	return render (request,'consulta_list.html',{'consultas':consultas})


def consulta_detail ( request,consulta_id ):
	consulta = get_object_or_404 (Consulta,pk = consulta_id)
	return render (request,'consulta_detail.html',{'consulta':consulta})


@csrf_exempt
def consulta_create ( request ):
	if request.method == 'POST':
		data = request.POST
		consulta = Consulta (
				paciente_id = data [ 'paciente_id' ],funcionario_id = data [ 'funcionario_id' ],
				data_inicio_consulta = data [ 'data_inicio_consulta' ],
				data_fim_consulta = data [ 'data_fim_consulta' ],diagnostico = data [ 'diagnostico' ],
				outros_dados = data [ 'outros_dados' ]
				)
		consulta.save ()
		return render (request,'consulta_create_success.html',{'consulta':consulta},status = 201)
	return render (request,'consulta_create_error.html',status = 400)


@csrf_exempt
def consulta_update ( request,consulta_id ):
	consulta = get_object_or_404 (Consulta,pk = consulta_id)
	if request.method == 'PUT':
		data = request.PUT
		consulta.paciente_id = data [ 'paciente_id' ]
		consulta.funcionario_id = data [ 'funcionario_id' ]
		consulta.data_inicio_consulta = data [ 'data_inicio_consulta' ]
		consulta.data_fim_consulta = data [ 'data_fim_consulta' ]
		consulta.diagnostico = data [ 'diagnostico' ]
		consulta.outros_dados = data [ 'outros_dados' ]
		consulta.save ()
		return render (request,'consulta_update_success.html',{'consulta':consulta},status = 200)
	return render (request,'consulta_update_error.html',status = 400)


@csrf_exempt
def consulta_delete ( request,consulta_id ):
	consulta = get_object_or_404 (Consulta,pk = consulta_id)
	if request.method == 'DELETE':
		consulta.delete ()
		return render (request,'consulta_delete_success.html',status = 204)
	return render (request,'consulta_delete_error.html',status = 400)


def contato_emergencia_list ( request ):
	contatos = ContatoEmergencia.objects.all ()
	return render (request,'contato_emergencia_list.html',{'contatos':contatos})


def contato_emergencia_detail ( request,contato_id ):
	contato = get_object_or_404 (ContatoEmergencia,pk = contato_id)
	return render (request,'contato_emergencia_detail.html',{'contato':contato})


@csrf_exempt
def contato_emergencia_create ( request ):
	if request.method == 'POST':
		data = request.POST
		contato = ContatoEmergencia (
				nome_contato = data [ 'nome_contato' ],relacionamento = data [ 'relacionamento' ],
				telefone = data [ 'telefone' ],outros_dados = data [ 'outros_dados' ]
				)
		contato.save ()
		return render (request,'contato_emergencia_create_success.html',{'contato':contato},status = 201)
	return render (request,'contato_emergencia_create_error.html',status = 400)


@csrf_exempt
def contato_emergencia_update ( request,contato_id ):
	contato = get_object_or_404 (ContatoEmergencia,pk = contato_id)
	if request.method == 'PUT':
		data = request.PUT
		contato.nome_contato = data [ 'nome_contato' ]
		contato.relacionamento = data [ 'relacionamento' ]
		contato.telefone = data [ 'telefone' ]
		contato.outros_dados = data [ 'outros_dados' ]
		contato.save ()
		return render (request,'contato_emergencia_update_success.html',{'contato':contato})
	return render (request,'contato_emergencia_update_error.html',status = 400)


@csrf_exempt
def contato_emergencia_delete ( request,contato_id ):
	contato = get_object_or_404 (ContatoEmergencia,pk = contato_id)
	if request.method == 'DELETE':
		contato.delete ()
		return render (request,'contato_emergencia_delete.html',{'contato':contato})
	return HttpResponse (status = 400)


@csrf_exempt
def pagamento_list ( request ):
	pagamentos = Pagamento.objects.all ()
	return render (request,'pagamento_list.html',{'pagamentos':pagamentos})


def pagamento_detail ( request,pagamento_id ):
	pagamento = get_object_or_404 (Pagamento,pk = pagamento_id)
	return render (request,'pagamento_detail.html',{'pagamento':pagamento})


@csrf_exempt
def pagamento_create ( request ):
	if request.method == 'POST':
		data = request.POST
		pagamento = Pagamento (
				nome_pagamento = data [ 'nome_pagamento' ],data_pagamento = data [ 'data_pagamento' ],
				outros_dados = data [ 'outros_dados' ]
				)
		try:
			pagamento.save ()
			return render (request,'pagamento_create_success.html')
		except Exception as e:
			return render (request,'pagamento_create_error.html')
	return HttpResponse (status = 400)


@csrf_exempt
def pagamento_update ( request,pagamento_id ):
	pagamento = get_object_or_404 (Pagamento,pk = pagamento_id)
	if request.method == 'PUT':
		data = request.PUT
		pagamento.nome_pagamento = data [ 'nome_pagamento' ]
		pagamento.data_pagamento = data [ 'data_pagamento' ]
		pagamento.outros_dados = data [ 'outros_dados' ]
		pagamento.save ()
		return render (request,'pagamento_update_success.html',{'pagamento':pagamento})
	return HttpResponse (status = 400)


@csrf_exempt
def pagamento_detail ( request,pagamento_id ):
	pagamento = get_object_or_404 (Pagamento,pk = pagamento_id)
	return render (request,'pagamento_detail.html',{'pagamento':pagamento})


@csrf_exempt
def pagamento_create ( request ):
	if request.method == 'POST':
		data = request.POST
		pagamento = Pagamento (
				nome_pagamento = data [ 'nome_pagamento' ],data_pagamento = data [ 'data_pagamento' ],
				outros_dados = data [ 'outros_dados' ]
				)
		pagamento.save ()
		return render (request,'pagamento_create_success.html')
	return render (request,'pagamento_create_error.html')


@csrf_exempt
def pagamento_update ( request,pagamento_id ):
	pagamento = get_object_or_404 (Pagamento,pk = pagamento_id)
	if request.method == 'PUT':
		data = request.PUT
		pagamento.nome_pagamento = data [ 'nome_pagamento' ]
		pagamento.data_pagamento = data [ 'data_pagamento' ]
		pagamento.outros_dados = data [ 'outros_dados' ]
		pagamento.save ()
		return render (request,'pagamento_update_success.html')
	return render (request,'pagamento_update_error.html')


@csrf_exempt
def pagamento_delete ( request,pagamento_id ):
	pagamento = get_object_or_404 (Pagamento,pk = pagamento_id)
	if request.method == 'DELETE':
		pagamento.delete ()
		return render (request,'pagamento_delete_success.html')
	return render (request,'pagamento_delete_error.html')


def exame_medico_list ( request ):
	exames = ExameMedico.objects.all ()
	return render (request,'exame_medico_list.html',{'exames':exames})


def exame_medico_detail ( request,exame_id ):
	exame = get_object_or_404 (ExameMedico,pk = exame_id)
	return render (request,'exame_medico_detail.html',{'exame':exame})


@csrf_exempt
def exame_medico_create ( request ):
	if request.method == 'POST':
		data = request.POST
		exame = ExameMedico (nome_exame = data [ 'nome_exame' ],outros_dados = data [ 'outros_dados' ])
		exame.save ()
		return render (request,'exame_medico_create_success.html')
	return render (request,'exame_medico_create_error.html')


@csrf_exempt
def exame_medico_update ( request,exame_id ):
	exame = get_object_or_404 (ExameMedico,pk = exame_id)
	if request.method == 'PUT':
		data = request.PUT
		exame.nome_exame = data [ 'nome_exame' ]
		exame.outros_dados = data [ 'outros_dados' ]
		exame.save ()
		return render (request,'exame_medico_update_success.html')
	return render (request,'exame_medico_update_error.html')


@csrf_exempt
def exame_medico_delete ( request,exame_id ):
	exame = get_object_or_404 (ExameMedico,pk = exame_id)
	if request.method == 'DELETE':
		exame.delete ()
		return render (request,'exame_medico_delete_success.html')
	return render (request,'exame_medico_delete_error.html')


def equipamento_list ( request ):
	equipamentos = Equipamento.objects.all ()
	return render (request,'equipamento_list.html',{'equipamentos':equipamentos})


def equipamento_detail ( request,equipamento_id ):
	equipamento = get_object_or_404 (Equipamento,pk = equipamento_id)
	return render (request,'equipamento_detail.html',{'equipamento':equipamento})


@csrf_exempt
def equipamento_create ( request ):
	if request.method == 'POST':
		data = request.POST
		equipamento = Equipamento (
				nome_equipamento = data [ 'nome_equipamento' ],
				data_aquisicao = data [ 'data_aquisicao' ],estoque_equipamento = data [ 'estoque_equipamento' ]
				)
		equipamento.save ()
		return render (request,'equipamento_create_success.html')
	return render (request,'equipamento_create_error.html')


@csrf_exempt
def equipamento_update ( request,equipamento_id ):
	equipamento = get_object_or_404 (Equipamento,pk = equipamento_id)
	if request.method == 'PUT':
		data = request.PUT
		equipamento.nome_equipamento = data [ 'nome_equipamento' ]
		equipamento.data_aquisicao = data [ 'data_aquisicao' ]
		equipamento.estoque_equipamento = data [ 'estoque_equipamento' ]
		equipamento.save ()
		return render (request,'equipamento_update_success.html',{'equipamento':equipamento})
	return render (request,'equipamento_update_error.html')


@csrf_exempt
def equipamento_delete ( request,equipamento_id ):
	equipamento = get_object_or_404 (Equipamento,pk = equipamento_id)
	if request.method == 'DELETE':
		equipamento.delete ()
		return render (request,'equipamento_delete_success.html')
	return render (request,'equipamento_delete_error.html')


def fatura_list ( request ):
	faturas = Fatura.objects.all ()
	return render (request,'fatura_list.html',{'faturas':faturas})


def fatura_detail ( request,fatura_id ):
	fatura = get_object_or_404 (Fatura,pk = fatura_id)
	return render (request,'fatura_detail.html',{'fatura':fatura})


@csrf_exempt
def fatura_create ( request ):
	"""
    """
	if request.method == 'POST':
		data = request.POST
		fatura = Fatura (
				nome_fatura = data [ 'nome_fatura' ],data_fatura = data [ 'data_fatura' ],
				pagamento_id = data [ 'pagamento' ],outros_dados = data.get ('outros_dados',None)
				)
		fatura.save ()
		return render (request,'fatura_create_success.html',{'mensagem':'Fatura criada com sucesso!'},status = 201)
	return render (request,'fatura_create_error.html',status = 400)


@csrf_exempt
def fatura_update ( request,fatura_id ):
	fatura = get_object_or_404 (Fatura,pk = fatura_id)
	if request.method == 'POST':
		form = FaturaForm (request.POST,instance = fatura)
		if form.is_valid ():
			form.save ()
			return render (request,'fatura_update_success.html')
		else:
			return render (request,'fatura_update_error.html')
	else:
		form = FaturaForm (instance = fatura)
		return render (request,'fatura_update_form.html',{'form':form})


@csrf_exempt
def fatura_delete ( request,fatura_id ):
	"""
    """
	fatura = get_object_or_404 (Fatura,pk = fatura_id)
	if request.method == 'DELETE':
		fatura.delete ()
		return render (request,'fatura_delete_success.html')
	return render (request,'fatura_delete_error.html')


def consumivel_list ( request ):
	consumiveis = Consumivel.objects.all ()
	return render (request,'consumivel_list.html',{'consumiveis':consumiveis})


def consumivel_detail ( request,consumivel_id ):
	consumivel = get_object_or_404 (Consumivel,pk = consumivel_id)
	return render (request,'consumivel_detail.html',{'consumivel':consumivel})


def consumivel_create ( request ):
	if request.method == 'POST':
		form = ConsumivelForm (request.POST)
		if form.is_valid ():
			form.save ()
			return render (request,'consumivel_create_success.html')
	else:
		form = ConsumivelForm ()
	return render (request,'consumivel_create.html',{'form':form})


@csrf_exempt
def consumivel_update ( request,consumivel_id ):
	"""
    """
	consumivel = get_object_or_404 (Consumivel,pk = consumivel_id)
	if request.method == 'PUT':
		data = request.PUT
		consumivel.nome_consumivel = data [ 'nome_consumivel' ]
		consumivel.estoque_consumivel = data [ 'estoque_consumivel' ]
		consumivel.data_aquisicao = data [ 'data_aquisicao' ]
		consumivel.departamento_id = data [ 'departamento' ]
		consumivel.outros_dados = data.get ('outros_dados',None)
		consumivel.save ()
		return JsonResponse ({'mensagem':'Consumível atualizado com sucesso!'})
	
	# Se não for uma requisição PUT, renderize a página de atualização do consumível
	return render (request,'consumivel_update.html',{'consumivel':consumivel})


@csrf_exempt
def consumivel_delete ( request,consumivel_id ):
	consumivel = get_object_or_404 (Consumivel,pk = consumivel_id)
	if request.method == 'DELETE':
		consumivel.delete ()
		return HttpResponse (status = 204)
	return render (request,'delete_consumivel.html')


def seguradora_list ( request ):
	seguradoras = Seguradora.objects.all ()
	return render (request,'seguradora_list.html',{'seguradoras':seguradoras})


def seguradora_detail ( request,seguradora_id ):
	seguradora = get_object_or_404 (Seguradora,pk = seguradora_id)
	return render (request,'seguradora_detail.html',{'seguradora':seguradora})


@csrf_exempt
def seguradora_create ( request ):
	if request.method == 'POST':
		data = request.POST
		seguradora = Seguradora (
				nome_seguradora = data [ 'nome_seguradora' ],
				outros_dados = data.get ('outros_dados',None)
				)
		seguradora.save ()
		return JsonResponse ({'mensagem':'Seguradora criada com sucesso!'},status = 201)
	return render (request,'seguradora_create.html')


@csrf_exempt
def seguradora_update ( request,seguradora_id ):
	seguradora = get_object_or_404 (Seguradora,pk = seguradora_id)
	if request.method == 'PUT':
		data = request.PUT
		seguradora.nome_seguradora = data [ 'nome_seguradora' ]
		seguradora.outros_dados = data.get ('outros_dados',None)
		seguradora.save ()
		return JsonResponse ({'mensagem':'Seguradora atualizada com sucesso!'})
	return render (request,'seguradora_update.html',{'seguradora':seguradora})


@csrf_exempt
def seguradora_delete ( request,seguradora_id ):
	seguradora = get_object_or_404 (Seguradora,pk = seguradora_id)
	if request.method == 'DELETE':
		seguradora.delete ()
		return JsonResponse ({'mensagem':'Seguradora excluída com sucesso!'},status = 204)
	return render (request,'seguradora_delete.html',{'seguradora':seguradora})


def procedimento_list ( request ):
	procedimentos = ProcedimentoMedico.objects.all ()
	return render (request,'procedimento_list.html',{'procedimentos':procedimentos})


def procedimento_detail ( request,procedimento_id ):
	procedimento = get_object_or_404 (ProcedimentoMedico,pk = procedimento_id)
	return render (request,'procedimento_detail.html',{'procedimento':procedimento})


@csrf_exempt
def procedimento_create ( request ):
	if request.method == 'POST':
		data = request.POST
		procedimento = ProcedimentoMedico (
				nome_procedimento = data [ 'nome_procedimento' ],
				outros_dados = data.get ('outros_dados',None)
				)
		procedimento.save ()
		return JsonResponse ({'mensagem':'Procedimento médico criado com sucesso!'},status = 201)
	return render (request,'procedimento_create.html')


@csrf_exempt
def procedimento_update ( request,procedimento_id ):
	procedimento = get_object_or_404 (ProcedimentoMedico,pk = procedimento_id)
	if request.method == 'PUT':
		data = request.POST  # Aqui, request.PUT não é uma propriedade; estamos usando request.POST para obter os dados do formulário
		procedimento.nome_procedimento = data [ 'nome_procedimento' ]
		procedimento.outros_dados = data.get ('outros_dados',None)
		procedimento.save ()
		return JsonResponse ({'mensagem':'Procedimento médico atualizado com sucesso!'})
	return render (request,'procedimento_update.html',{'procedimento':procedimento})


@csrf_exempt
def procedimento_delete ( request,procedimento_id ):
	procedimento = get_object_or_404 (ProcedimentoMedico,pk = procedimento_id)
	if request.method == 'DELETE':
		procedimento.delete ()
		return JsonResponse ({'mensagem':'Procedimento médico excluído com sucesso!'},status = 204)
	return render (request,'procedimento_delete.html',{'procedimento':procedimento})


def agendamento_list ( request ):
	agendamentos = Agendamento.objects.all ()
	return render (request,'agendamento_list.html',{'agendamentos':agendamentos})


def agendamento_detail ( request,agendamento_id ):
	agendamento = get_object_or_404 (Agendamento,pk = agendamento_id)
	return render (request,'agendamento_detail.html',{'agendamento':agendamento})


@csrf_exempt
def agendamento_create ( request ):
	if request.method == 'POST':
		try:
			data = request.POST
			agendamento = Agendamento (
					especialidade_id = data [ 'especialidade_id' ],
					funcionario_id = data [ 'funcionario_id' ],exame_id = data.get ('exame_id',None),
					nome_agendamento = data [ 'nome_agendamento' ],data_agendamento = data [ 'data_agendamento' ],
					procedimento_id = data.get ('procedimento_id',None),outros_dados = data.get ('outros_dados',None)
					)
			agendamento.save ()
			return JsonResponse ({'mensagem':'Agendamento criado com sucesso!'},status = 201)
		except KeyError:
			return render (request,'agendamento_create.html',{'error_message':'Erro: Campos inválidos!'})
	return render (request,'agendamento_create.html')


@csrf_exempt
def agendamento_update ( request,agendamento_id ):
	agendamento = get_object_or_404 (Agendamento,pk = agendamento_id)
	if request.method == 'PUT':
		data = request.POST  # Aqui, request.PUT não é uma propriedade; estamos usando request.POST para obter os dados do formulário
		agendamento.especialidade_id = data [ 'especialidade_id' ]
		agendamento.funcionario_id = data [ 'funcionario_id' ]
		agendamento.exame_id = data.get ('exame_id',None)
		agendamento.nome_agendamento = data [ 'nome_agendamento' ]
		agendamento.data_agendamento = data [ 'data_agendamento' ]
		agendamento.procedimento_id = data.get ('procedimento_id',None)
		agendamento.outros_dados = data.get ('outros_dados',None)
		agendamento.save ()
		return JsonResponse ({'mensagem':'Agendamento atualizado com sucesso!'})
	return render (request,'agendamento_update.html',{'agendamento':agendamento})


@csrf_exempt
def agendamento_delete ( request,agendamento_id ):
	agendamento = get_object_or_404 (Agendamento,pk = agendamento_id)
	if request.method == 'POST':
		agendamento.delete ()
		return JsonResponse ({'mensagem':'Agendamento excluído com sucesso!'},status = 204)
	return render (request,'agendamento_confirm_delete.html',{'agendamento':agendamento})


def detalhe_funcionario_list ( request ):
	detalhes_funcionario = DetalheFuncionario.objects.all ()
	return render (request,'detalhe_funcionario_list.html',{'detalhes_funcionario':detalhes_funcionario})


def detalhe_funcionario_detail ( request,detalhe_funcionario_id ):
	detalhe_funcionario = get_object_or_404 (DetalheFuncionario,pk = detalhe_funcionario_id)
	return render (request,'detalhe_funcionario_detail.html',{'detalhe_funcionario':detalhe_funcionario})


@csrf_exempt
def detalhe_funcionario_create ( request ):
	if request.method == 'POST':
		data = request.POST
		detalhe_funcionario = DetalheFuncionario (
				funcionario_id = data [ 'funcionario_id' ],
				nacionalidade = data [ 'nacionalidade' ]
				)
		detalhe_funcionario.save ()
		return JsonResponse ({'mensagem':'Detalhe de funcionário criado com sucesso!'},status = 201)
	return render (request,'detalhe_funcionario_create.html')


@csrf_exempt
def detalhe_funcionario_update ( request,detalhe_funcionario_id ):
	detalhe_funcionario = get_object_or_404 (DetalheFuncionario,pk = detalhe_funcionario_id)
	if request.method == 'POST':
		data = request.POST
		detalhe_funcionario.funcionario_id = data [ 'funcionario_id' ]
		detalhe_funcionario.nacionalidade = data [ 'nacionalidade' ]
		detalhe_funcionario.save ()
		return JsonResponse ({'mensagem':'Detalhe de funcionário atualizado com sucesso!'})
	return render (request,'detalhe_funcionario_update.html',{'detalhe_funcionario':detalhe_funcionario})


@csrf_exempt
def detalhe_funcionario_delete ( request,detalhe_funcionario_id ):
	detalhe_funcionario = get_object_or_404 (DetalheFuncionario,pk = detalhe_funcionario_id)
	if request.method == 'POST':
		detalhe_funcionario.delete ()
		return JsonResponse ({'mensagem':'Detalhe de funcionário excluído com sucesso!'},status = 204)
	return render (request,'detalhe_funcionario_delete.html',{'detalhe_funcionario':detalhe_funcionario})


def detalhe_paciente_list ( request ):
	detalhes_paciente = DetalhePaciente.objects.all ()
	return render (request,'detalhe_paciente_list.html',{'detalhes_paciente':detalhes_paciente})


def detalhe_paciente_detail ( request,detalhe_paciente_id ):
	detalhe_paciente = get_object_or_404 (DetalhePaciente,pk = detalhe_paciente_id)
	return render (request,'detalhe_paciente_detail.html',{'detalhe_paciente':detalhe_paciente})


@csrf_exempt
def detalhe_paciente_create ( request ):
	if request.method == 'POST':
		data = request.POST
		detalhe_paciente = DetalhePaciente (
				paciente_id = data [ 'paciente_id' ],
				nacionalidade = data [ 'nacionalidade' ]
				)
		detalhe_paciente.save ()
		return JsonResponse ({'mensagem':'Detalhe de paciente criado com sucesso!'},status = 201)
	return render (request,'detalhe_paciente_create.html')


@csrf_exempt
def detalhe_paciente_update ( request,detalhe_paciente_id ):
	detalhe_paciente = get_object_or_404 (DetalhePaciente,pk = detalhe_paciente_id)
	if request.method == 'POST':
		data = request.POST
		detalhe_paciente.paciente_id = data [ 'paciente_id' ]
		detalhe_paciente.nacionalidade = data [ 'nacionalidade' ]
		detalhe_paciente.save ()
		return JsonResponse ({'mensagem':'Detalhe de paciente atualizado com sucesso!'})
	return render (request,'detalhe_paciente_update.html',{'detalhe_paciente':detalhe_paciente})


@csrf_exempt
def detalhe_paciente_delete ( request,detalhe_paciente_id ):
	detalhe_paciente = get_object_or_404 (DetalhePaciente,pk = detalhe_paciente_id)
	if request.method == 'POST':
		detalhe_paciente.delete ()
		return HttpResponse (status = 204)
	return render (request,'detalhe_paciente_delete.html',{'detalhe_paciente':detalhe_paciente})


def receita_medica_list ( request ):
	receitas_medicas = ReceitaMedica.objects.all ()
	return render (request,'receita_medica_list.html',{'receitas_medicas':receitas_medicas})


def receita_medica_detail ( request,receita_medica_id ):
	receita_medica = get_object_or_404 (ReceitaMedica,pk = receita_medica_id)
	return render (request,'receita_medica_detail.html',{'receita_medica':receita_medica})


def receita_medica_create ( request ):
	if request.method == 'POST':
		form = ReceitaMedicaForm (request.POST)
		if form.is_valid ():
			form.save ()
			return render (request,'receita_medica_create_success.html')
	else:
		form = ReceitaMedicaForm ()
	return render (request,'receita_medica_create.html',{'form':form})


def receita_medica_update ( request,receita_medica_id ):
	receita_medica = get_object_or_404 (ReceitaMedica,pk = receita_medica_id)
	if request.method == 'POST':
		form = ReceitaMedicaForm (request.POST,instance = receita_medica)
		if form.is_valid ():
			form.save ()
			return render (request,'receita_medica_update_success.html')
	else:
		form = ReceitaMedicaForm (instance = receita_medica)
	return render (request,'receita_medica_update.html',{'form':form})


def receita_medica_delete ( request,receita_medica_id ):
	receita_medica = get_object_or_404 (ReceitaMedica,pk = receita_medica_id)
	if request.method == 'POST':
		receita_medica.delete ()
		return render (request,'receita_medica_delete_success.html')
	return render (request,'receita_medica_delete_confirm.html',{'receita_medica':receita_medica})


def historico_consulta_list ( request ):
	historicos_consulta = HistoricoConsulta.objects.all ()
	return render (request,'historico_consulta_list.html',{'historicos_consulta':historicos_consulta})


def historico_consulta_detail ( request,historico_consulta_id ):
	historico_consulta = get_object_or_404 (HistoricoConsulta,pk = historico_consulta_id)
	return render (request,'historico_consulta_detail.html',{'historico_consulta':historico_consulta})


@csrf_exempt
def historico_consulta_create ( request ):
	if request.method == 'POST':
		form = HistoricoConsultaForm (request.POST)
		if form.is_valid ():
			form.save ()
			return render (request,'historico_consulta_create_success.html')
	else:
		form = HistoricoConsultaForm ()
	return render (request,'historico_consulta_create.html',{'form':form})


@csrf_exempt
def historico_consulta_update ( request,historico_consulta_id ):
	historico_consulta = get_object_or_404 (HistoricoConsulta,pk = historico_consulta_id)
	if request.method == 'POST':
		form = HistoricoConsultaForm (request.POST,instance = historico_consulta)
		if form.is_valid ():
			form.save ()
			return render (request,'historico_consulta_update_success.html')
	else:
		form = HistoricoConsultaForm (instance = historico_consulta)
	return render (request,'historico_consulta_update.html',{'form':form})


@csrf_exempt
def historico_consulta_delete ( request,historico_consulta_id ):
	historico_consulta = get_object_or_404 (HistoricoConsulta,pk = historico_consulta_id)
	if request.method == 'POST':
		historico_consulta.delete ()
		return HttpResponseRedirect ('/historico_consulta/deleted/')
	return render (request,'historico_consulta_delete.html',{'historico_consulta':historico_consulta})


def procedimento_cirurgico_list ( request ):
	procedimentos_cirurgicos = ProcedimentoCirurgico.objects.all ()
	return render (request,'procedimento_cirurgico_list.html',{'procedimentos_cirurgicos':procedimentos_cirurgicos})


def procedimento_cirurgico_detail ( request,procedimento_cirurgico_id ):
	procedimento_cirurgico = get_object_or_404 (ProcedimentoCirurgico,pk = procedimento_cirurgico_id)
	return render (request,'procedimento_cirurgico_detail.html',{'procedimento_cirurgico':procedimento_cirurgico})


@csrf_exempt
def procedimento_cirurgico_create ( request ):
	if request.method == 'POST':
		data = request.POST
		procedimento_cirurgico = ProcedimentoCirurgico (
				paciente_id = data [ 'paciente_id' ],
				tipo_procedimento = data [ 'tipo_procedimento' ],medico_cirurgiao = data [ 'medico_cirurgiao' ],
				data_cirurgia = data [ 'data_cirurgia' ],outros_dados = data [ 'outros_dados' ]
				)
		procedimento_cirurgico.save ()
		return HttpResponseRedirect ('/procedimento_cirurgico/success/')
	return render (request,'procedimento_cirurgico_create.html')


@csrf_exempt
def procedimento_cirurgico_update ( request,procedimento_cirurgico_id ):
	procedimento_cirurgico = get_object_or_404 (ProcedimentoCirurgico,pk = procedimento_cirurgico_id)
	if request.method == 'POST':
		data = request.POST
		procedimento_cirurgico.paciente_id = data [ 'paciente_id' ]
		procedimento_cirurgico.tipo_procedimento = data [ 'tipo_procedimento' ]
		procedimento_cirurgico.medico_cirurgiao = data [ 'medico_cirurgiao' ]
		procedimento_cirurgico.data_cirurgia = data [ 'data_cirurgia' ]
		procedimento_cirurgico.outros_dados = data [ 'outros_dados' ]
		procedimento_cirurgico.save ()
		return HttpResponseRedirect ('/procedimento_cirurgico/success/')
	return render (request,'procedimento_cirurgico_update.html',{'procedimento_cirurgico':procedimento_cirurgico})


from django.shortcuts import render


@csrf_exempt
def procedimento_cirurgico_delete ( request,procedimento_cirurgico_id ):
	procedimento_cirurgico = get_object_or_404 (ProcedimentoCirurgico,pk = procedimento_cirurgico_id)
	if request.method == 'DELETE':
		procedimento_cirurgico.delete ()
		return HttpResponse (status = 204)
	return render (request,'procedimento_cirurgico_delete.html')


def registro_vacinacao_list ( request ):
	registros_vacinacao = RegistroVacinacao.objects.all ()
	context = {'registros_vacinacao':registros_vacinacao}
	return render (request,'registro_vacinacao_list.html',context)


def registro_vacinacao_detail ( request,registro_vacinacao_id ):
	registro_vacinacao = get_object_or_404 (RegistroVacinacao,pk = registro_vacinacao_id)
	return render (request,'registro_vacinacao_detail.html',{'registro_vacinacao':registro_vacinacao})


@csrf_exempt
def registro_vacinacao_create ( request ):
	"""
    Create a new vaccination record.
    """
	if request.method == 'POST':
		data = request.POST
		try:
			registro_vacinacao = RegistroVacinacao.objects.create (
					paciente_id = data [ 'paciente_id' ],
					tipo_vacina = data [ 'tipo_vacina' ],data_vacinacao = data [ 'data_vacinacao' ],
					lote_vacina = data [ 'lote_vacina' ],outros_dados = data.get ('outros_dados',None)
					)
			return JsonResponse ({'mensagem':'Registro de vacinação criado com sucesso!'},status = 201)
		except ValidationError as e:
			return JsonResponse ({'erro':'Erro de validação: {}'.format (e)},status = 400)
	return render (request,'registro_vacinacao_create.html')


@csrf_exempt
def registro_vacinacao_update ( request,registro_vacinacao_id ):
	"""
    Update a vaccination record.
    """
	registro_vacinacao = get_object_or_404 (RegistroVacinacao,pk = registro_vacinacao_id)
	if request.method == 'POST':
		data = request.POST
		try:
			registro_vacinacao.paciente_id = data [ 'paciente_id' ]
			registro_vacinacao.tipo_vacina = data [ 'tipo_vacina' ]
			registro_vacinacao.data_vacinacao = data [ 'data_vacinacao' ]
			registro_vacinacao.lote_vacina = data [ 'lote_vacina' ]
			registro_vacinacao.outros_dados = data [ 'outros_dados' ]
			registro_vacinacao.save ()
			return JsonResponse ({'mensagem':'Registro de vacinação atualizado com sucesso!'})
		except ValidationError as e:
			return JsonResponse ({'erro':'Erro de validação: {}'.format (e)},status = 400)
	return render (request,'registro_vacinacao_update.html')


@csrf_exempt
def registro_vacinacao_delete ( request,registro_vacinacao_id ):
	"""
    """
	registro_vacinacao = get_object_or_404 (RegistroVacinacao,pk = registro_vacinacao_id)
	if request.method == 'DELETE':
		registro_vacinacao.delete ()
		return HttpResponse (status = 204)
	return render (request,'registro_vacinacao_delete.html')


def teste_laboratorial_list ( request ):
	testes_laboratoriais = TesteLaboratorial.objects.all ()
	return render (request,'teste_laboratorial_list.html',{'testes_laboratoriais':testes_laboratoriais})


def teste_laboratorial_detail ( request,teste_laboratorial_id ):
	teste_laboratorial = get_object_or_404 (TesteLaboratorial,pk = teste_laboratorial_id)
	return render (request,'teste_laboratorial_detail.html',{'teste_laboratorial':teste_laboratorial})


@csrf_exempt
def teste_laboratorial_create ( request ):
	if request.method == 'POST':
		form = TesteLaboratorialForm (request.POST)
		if form.is_valid ():
			form.save ()
			return JsonResponse ({'mensagem':'Teste laboratorial criado com sucesso!'},status = 201)
	else:
		form = TesteLaboratorialForm ()
	return render (request,'teste_laboratorial_create.html',{'form':form})


@csrf_exempt
def teste_laboratorial_update ( request,teste_laboratorial_id ):
	teste_laboratorial = get_object_or_404 (TesteLaboratorial,pk = teste_laboratorial_id)
	if request.method == 'POST':
		form = TesteLaboratorialForm (request.POST,instance = teste_laboratorial)
		if form.is_valid ():
			form.save ()
			return JsonResponse ({'mensagem':'Teste laboratorial atualizado com sucesso!'})
	else:
		form = TesteLaboratorialForm (instance = teste_laboratorial)
	return render (request,'teste_laboratorial_update.html',{'form':form})


@csrf_exempt
def teste_laboratorial_delete ( request,teste_laboratorial_id ):
	teste_laboratorial = get_object_or_404 (TesteLaboratorial,pk = teste_laboratorial_id)
	if request.method == 'POST':
		teste_laboratorial.delete ()
		return HttpResponse (status = 204)
	return HttpResponse (status = 400)


def alergia_condicao_list ( request ):
	alergias_condicoes = AlergiaCondicao.objects.all ()
	return render (request,'alergia_condicao_list.html',{'alergias_condicoes':alergias_condicoes})


def alergia_condicao_detail ( request,alergia_condicao_id ):
	alergia_condicao = get_object_or_404 (AlergiaCondicao,pk = alergia_condicao_id)
	return render (request,'alergia_condicao_detail.html',{'alergia_condicao':alergia_condicao})


@csrf_exempt
def alergia_condicao_create ( request ):
	if request.method == 'POST':
		data = request.POST
		alergia_condicao = AlergiaCondicao (
				paciente_id = data [ 'paciente_id' ],
				alergia_condicao = data [ 'alergia_condicao' ],outros_dados = data [ 'outros_dados' ]
				)
		alergia_condicao.save ()
		return JsonResponse ({'mensagem':'Alergia ou condição criada com sucesso!'},status = 201)
	# Renderizando a página HTML do formulário
	return render (request,'alergia_condicao_create.html')


@csrf_exempt
def alergia_condicao_update ( request,alergia_condicao_id ):
	alergia_condicao = get_object_or_404 (AlergiaCondicao,pk = alergia_condicao_id)
	if request.method == 'PUT':
		data = request.PUT
		alergia_condicao.paciente_id = data [ 'paciente_id' ]
		alergia_condicao.alergia_condicao = data [ 'alergia_condicao' ]
		alergia_condicao.outros_dados = data [ 'outros_dados' ]
		alergia_condicao.save ()
		return JsonResponse ({'mensagem':'Alergia ou condição atualizada com sucesso!'})
	# Renderizando a página HTML do formulário de atualização
	return render (request,'alergia_condicao_update.html',{'alergia_condicao':alergia_condicao})


def alergia_condicao_delete ( request,alergia_condicao_id ):
	alergia_condicao = get_object_or_404 (AlergiaCondicao,pk = alergia_condicao_id)
	if request.method == 'POST':
		alergia_condicao.delete ()
		return HttpResponse (status = 204)
	return render (request,'delete_alergia_condicao.html',{'alergia_condicao':alergia_condicao})
