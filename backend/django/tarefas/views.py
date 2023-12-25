# views.py
from datetime import timezone
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.shortcuts import render, redirect
from .models import Tarefa
from .forms import TarefaForm
from django.views.decorators.http import require_POST

def index(request):
    return HttpResponse('Olá mundo!')

def adicionar_tarefa_form_view(request):
    if request.method == 'POST':
        form = TarefaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_tarefas')
    else:
        form = TarefaForm()

    return render(request, 'tarefas/adicionar_tarefa.html', {'form': form})

def adicionar_tarefa_form(request):
    if request.method == 'POST':
        form = TarefaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_tarefas')
    else:
        form = TarefaForm()

    return render(request, 'tarefas/adicionar_tarefa.html', {'form': form})


def lista_tarefas_form(request, status=None):
    if status:
        tarefas = Tarefa.objects.filter(status=status)
    else:
        tarefas = Tarefa.objects.all()

    return render(request, 'tarefas/adicionar_tarefa.html', {'tarefas': tarefas})

def lista_tarefas(request):
    tarefas = Tarefa.objects.all()
    return render(request, 'tarefas/lista_tarefas.html', {'tarefas': tarefas})

def lista_tarefas_json(request):
    tarefas = Tarefa.objects.all()
    
    # Criar uma lista de dicionários representando as tarefas
    tarefas_json = []
    for tarefa in tarefas:
        tarefa_dict = {
            'id': tarefa.id,
            'titulo': tarefa.titulo,
            'concluida': tarefa.concluida,
            'data_criacao': tarefa.data_criacao.strftime('%Y-%m-%d %H:%M:%S'),
            'data_conclusao': tarefa.data_conclusao.strftime('%Y-%m-%d %H:%M:%S') if tarefa.data_conclusao else None,
            'status': tarefa.get_status_display(),  # Usa a representação legível do status
        }
        tarefas_json.append(tarefa_dict)

    # Retorna a resposta como JSON
    return JsonResponse({'tarefas': tarefas_json})

def completar_tarefa(request, tarefa_id):
    tarefa = get_object_or_404(Tarefa, pk=tarefa_id)

    # Verifica se a tarefa já está concluída
    if tarefa.concluida:
        return JsonResponse({'error': 'Tarefa já concluída.'}, status=400)

    # Atualiza o status e a data de conclusão
    tarefa.concluida = True
    tarefa.data_conclusao = timezone.now()  # Importe timezone do django
    tarefa.save()

    return JsonResponse({'success': 'Tarefa concluída com sucesso.'})

@require_POST
def adicionar_tarefa(request):
    titulo = request.POST['titulo']
    
    nova_tarefa = Tarefa(titulo=titulo)
    nova_tarefa.save()
    return redirect('lista_tarefas')

@require_POST
def completar_tarefa(request, tarefa_id):
    tarefa = get_object_or_404(Tarefa, pk=tarefa_id)
    tarefa.concluida = True
    tarefa.status = 'CO'
    tarefa.save()
    return redirect('lista_tarefas')

def atualizar_tarefa(request, tarefa_id, status):
    tarefa = Tarefa.objects.get(pk=tarefa_id)
    tarefa.status = status
    tarefa.save()
    return redirect('lista_tarefas')

def deletar_tarefa(request, tarefa_id):
    tarefa = Tarefa.objects.get(pk=tarefa_id)
    tarefa.delete()
    return redirect('lista_tarefas')

def atualizar_tarefas(request):
    if request.method == 'POST':
        data = request.POST.get('tarefas')
        print(data)

        # Retorna uma resposta para indicar que a atualização foi bem-sucedida
        return JsonResponse({'status': 'Atualização bem-sucedida'})

    # Retorna uma resposta indicando que a solicitação não foi bem-sucedida (método não permitido)
    return JsonResponse({'status': 'Método não permitido'}, status=405)