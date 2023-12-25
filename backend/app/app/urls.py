from django.contrib import admin
from django.urls import path
from tarefas.views import atualizar_tarefas,atualizar_tarefa , adicionar_tarefa_form, adicionar_tarefa_form_view, index, lista_tarefas, adicionar_tarefa, completar_tarefa, deletar_tarefa, lista_tarefas_form, lista_tarefas_json

urlpatterns = [
    path('admin/', admin.site.urls),
    path('index',index , name='index'),
    path('', lista_tarefas, name='lista_tarefas'),
    path('lista_tarefas_json/', lista_tarefas_json, name='lista_tarefas_json'),
    path('adicionar_tarefa_form/', adicionar_tarefa_form_view, name='adicionar_tarefa_form'),
    path('adicionar/', adicionar_tarefa, name='adicionar_tarefa'),
    path('adicionar_tarefa_form/', adicionar_tarefa_form, name='adicionar_tarefa_form'),
    path('completar_tarefa/<int:tarefa_id>/', completar_tarefa, name='completar_tarefa'),
    path('deletar_tarefa/<int:tarefa_id>/', deletar_tarefa, name='deletar_tarefa'),
    path('tarefas_form/', lista_tarefas_form, name='lista_tarefas_form'),
    path('tarefas_form/<str:status>/', lista_tarefas_form, name='lista_tarefas_status'),
    path('atualizar_tarefas/',atualizar_tarefas,name='atualizar_tarefas'),
    path('atualizar_tarefa/<int:tarefa_id>/<str:status>',atualizar_tarefa,name='atualizar_tarefa'),
]
