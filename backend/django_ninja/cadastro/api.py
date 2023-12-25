from ninja import ModelSchema, NinjaAPI
from .models import Usuario
from django.forms.models import model_to_dict
from ninja.errors import HttpError

api=NinjaAPI()

class UsuarioSchema(ModelSchema):
    class Config:
        model = Usuario
        model_fields = '__all__'

@api.get("usuarios/")
def get_usuarios(request): 
    usuarios = Usuario.objects.all()

    # Verifique se há usuários
    if not usuarios:
        raise HttpError(404, "Nenhum usuário encontrado")

    # Converta os usuários para uma lista de dicionários
    usuarios_data = [model_to_dict(usuario) for usuario in usuarios]

    # Crie a resposta
    response = {"usuarios": usuarios_data}
    return response

@api.get("usuario/{id}")
def get_usuario(request, id):
    try:
        usuario = Usuario.objects.get(id=id)
    except Usuario.DoesNotExist:
        raise HttpError(404, "Usuário não encontrado")
    return model_to_dict(usuario)

@api.post("usuario_dict")
def create_usuario_dict(request, usuario: UsuarioSchema):
    usuario_obj = Usuario.objects.create(
        nome=usuario.nome,
        email=usuario.email,
        senha=usuario.senha,
        data_nascimento = usuario.data_nascimento,
    )
    return model_to_dict(usuario_obj)

@api.post("usuario_schema",response=UsuarioSchema)
def create_usuario_schema(request, usuario: UsuarioSchema):
    l1 = usuario.dict()
    usuario = Usuario(**l1)
    usuario.save()
    return usuario


@api.put("usuario/{id}", response=UsuarioSchema)
def update_usuario(request, id, usuario: UsuarioSchema):
    try:
        usuario_obj = Usuario.objects.get(id=id)
    except Usuario.DoesNotExist:
        raise HttpError(404, "Usuário não encontrado")

    # Atualize os campos do usuário
    usuario_obj.nome = usuario.nome
    usuario_obj.email = usuario.email
    usuario_obj.senha = usuario.senha
    usuario_obj.data_nascimento = usuario.data_nascimento

    # Salve as alterações
    usuario_obj.save()

    return usuario

@api.delete("usuario/{id}")
def delete_usuario(request, id):
    try:
        usuario_obj = Usuario.objects.get(id=id)
    except Usuario.DoesNotExist:
        raise HttpError(404, "Usuário não encontrado")

    # Delete o usuário
    usuario_obj.delete()

    return {"success": True, "message": "Usuário deletado com sucesso"}