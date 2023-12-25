from django.db import models

class Tarefa(models.Model):
    STATUS_CHOICES = (
        ('AB', 'Aberto'),
        ('PR', 'Em Processo'),
        ('CO', 'Concluído'),
    )

    titulo = models.CharField(max_length=200)
    concluida = models.BooleanField(default=False)
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_conclusao = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=2, choices=STATUS_CHOICES, default='AB')

    def __str__(self):
        return self.titulo
