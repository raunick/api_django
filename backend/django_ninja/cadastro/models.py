from django.db import models

class Usuario(models.Model):
    nome = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    senha = models.CharField(max_length=100)
    telefone = models.CharField(max_length=100)
    cpf = models.CharField(max_length=100)
    data_nascimento = models.DateField()
    cep = models.CharField(max_length=100)
    rua = models.CharField(max_length=100)
    numero = models.CharField(max_length=100)
    
    def __str__(self):
        return self.nome
