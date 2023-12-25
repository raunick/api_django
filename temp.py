import json
from faker import Faker
import random

# Configurar a biblioteca Faker
fake = Faker()

# Função para gerar um JSON aleatório
def generate_random_json():
    random_json = {
        "nome": fake.name(),
        "email": fake.email(),
        "senha": fake.password(),
        "data_nascimento": fake.date_of_birth().strftime("%Y-%m-%d")
    }
    return random_json

# Gerar uma lista de JSONs aleatórios
num_users = 5  # Número de usuários que você deseja gerar
random_users = [generate_random_json() for _ in range(num_users)]

# Nome do arquivo de saída
output_file = "usuarios.json"

# Escrever o JSON no arquivo
with open(output_file, "w") as file:
    json.dump(random_users, file, indent=2)

print(f"JSON gerado e salvo em {output_file}")
