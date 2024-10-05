import requests
import flet as ft
from GeoPostes import *
from views import *

username_register = ft.TextField(
    label= "Nome de usuário",
    label_style= ft.TextStyle(color=ft.colors.BLACK),
    text_style= ft.TextStyle(color=ft.colors.BLACK),
    col=8
)

email_register = ft.TextField(
    label= "E-mail",
    label_style= ft.TextStyle(color=ft.colors.BLACK),
    text_style= ft.TextStyle(color=ft.colors.BLACK),
    col=8
)

number_register = ft.TextField(
    label= "Celular",
    label_style= ft.TextStyle(color=ft.colors.BLACK),
    text_style= ft.TextStyle(color=ft.colors.BLACK),
    col=8
)

password_register = ft.TextField(
    label= "Senha",
    label_style= ft.TextStyle(color=ft.colors.BLACK),
    text_style= ft.TextStyle(color=ft.colors.BLACK),
    col=8
)

# Função para inserir um registro no Supabase
def register(username, email, number, password, page):
    # Verificar se todos os campos estão preenchidos
    if not username or not email or not number or not password:
        page.snack_bar = ft.SnackBar(
            content=ft.Text("Alguns campos não foram preenchidos"),
            bgcolor=ft.colors.RED
        )
        page.snack_bar.open = True
        page.update()
        return  # Interrompe a execução da função se houver campos em branco

    # Verificar conexão com a internet
    try:
        requests.get("https://www.google.com", timeout=5)
    except requests.ConnectionError:
        page.snack_bar = ft.SnackBar(
            content=ft.Text("Sem conexão com a internet"),
            bgcolor=ft.colors.ORANGE
        )
        page.snack_bar.open = True
        page.update()
        return  # Impede que o código continue caso não haja conexão

    # URL da API do seu projeto no Supabase
    SUPABASE_URL = "https://ipyhpxhsmyzzkvucdonu.supabase.co"
    SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImlweWhweGhzbXl6emt2dWNkb251Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3Mjc1NjQ3NDIsImV4cCI6MjA0MzE0MDc0Mn0.qA9H-UyAEx2OgihW1d_i2IjqQ5HTt1e4ITr52J5qRsA"

    # Cabeçalho com a API Key
    headers = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}",
        "Content-Type": "application/json",
    }

    # Obter o maior valor de user_id na tabela
    response = requests.get(
        f"{SUPABASE_URL}/rest/v1/login_geopostes",
        headers=headers,
        params={"select": "user_id", "order": "user_id.desc", "limit": 1},
    )

    if response.status_code == 200:
        max_user_id = response.json()[0]["user_id"] if response.json() else 0
        new_user_id = max_user_id + 1

        # Dados para inserir no Supabase
        data = {
            "user_id": new_user_id,
            "usuario": username,
            "email": email,
            "numero": number,
            "senha": password,
        }

        # Fazer a solicitação POST para inserir o novo registro
        response = requests.post(
            f"{SUPABASE_URL}/rest/v1/login_geopostes",
            headers=headers,
            json=data,
        )

        # Verificar se a inserção foi bem-sucedida
        if response.status_code == 201:
            page.snack_bar = ft.SnackBar(
                content=ft.Text("Usuário registrado com sucesso"),
                bgcolor=ft.colors.GREEN
            )
        else:
            print(f"Erro ao inserir registro: {response.status_code}")
            print(f"Resposta do erro: {response.text}")
            page.snack_bar = ft.SnackBar(
                content=ft.Text(f"Erro ao registrar usuário: {response.text}"),
                bgcolor=ft.colors.RED
            )
    else:
        print(f"Erro ao obter o maior user_id: {response.status_code}")
        print(f"Resposta do erro: {response.text}")
        page.snack_bar = ft.SnackBar(
            content=ft.Text(f"Erro ao obter user_id: {response.text}"),
            bgcolor=ft.colors.RED
        )

    # Abrir o snack bar e atualizar a página
    page.snack_bar.open = True
    page.update()




# Função que cria o botão de login
def btn_register_2(username_field, email_field, number_field, password_field, page):
    return ft.Container(
        col=7,
        padding=10,
        content=ft.ElevatedButton(
            text="Registrar",
            bgcolor=ft.colors.BLUE_700,
            color=ft.colors.WHITE,
            on_click=lambda e: register(username_field.value, email_field.value, number_field.value, password_field.value, page),
            
        ),
    )


# Função que volta a página de login
def btn_back(action_back):
    return ft.Container(
        col=7,
        padding=10,
        content=ft.ElevatedButton(
            text="Voltar",
            bgcolor=ft.colors.AMBER,
            color=ft.colors.WHITE,
            on_click=action_back
            
        ),
    )
