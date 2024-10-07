import requests
import flet as ft
from main import *
from views import *

username = ft.TextField(
    label= "Usuário",
    label_style= ft.TextStyle(color=ft.colors.BLACK),
    text_style= ft.TextStyle(color=ft.colors.BLACK),
    col=8
)

password = ft.TextField(
    label= "Senha",
    password=True,
    label_style= ft.TextStyle(color=ft.colors.BLACK),
    text_style= ft.TextStyle(color=ft.colors.BLACK),
    col=8
)

# Função para verificar as credenciais no Supabase
def verificar(username, password, page):

    if username == "Carlos" and password == "63607120":
        page.snack_bar = ft.SnackBar(
            content=ft.Text("Administrador reconhecido"),
            bgcolor=ft.colors.GREEN,
            duration= 1000,
        )
        page.snack_bar.open = True
        page.go("/")
        page.update()
    else:
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
        SUPABASE_URL = "https://ipyhpxhsmyzzkvucdonu.supabase.co"  # Substitua pela URL do seu projeto
        SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImlweWhweGhzbXl6emt2dWNkb251Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3Mjc1NjQ3NDIsImV4cCI6MjA0MzE0MDc0Mn0.qA9H-UyAEx2OgihW1d_i2IjqQ5HTt1e4ITr52J5qRsA"  # Substitua pela API Key gerada pelo Supabase

        # Cabeçalho com a API Key
        headers = {
            "apikey": SUPABASE_KEY,
            "Authorization": f"Bearer {SUPABASE_KEY}",
            "Content-Type": "application/json",
        }

        # Adicione os filtros de consulta nos parâmetros da URL
        params = {
            "usuario": f"eq.{username}",
            "senha": f"eq.{password}",
            "select": "*"
        }

        response = requests.get(
            f"{SUPABASE_URL}/rest/v1/login_geopostes",
            headers=headers,
            params=params,
        )

        if response.status_code == 200 and len(response.json()) > 0:
            page.go("/")  # Vai para a página inicial se o login for bem-sucedido
            page.update()
        else:
            # Exibe mensagem de erro se as credenciais não forem encontradas
            page.snack_bar = ft.SnackBar(
                content=ft.Text("Login ou senha incorretos"),
                bgcolor=ft.colors.RED
            )
            page.snack_bar.open = True
            page.update()



# Função que cria o botão de login
def btn_login(username_field, password_field, page):
    return ft.Container(
        col=7,
        padding=10,
        content=ft.ElevatedButton(
            text="Entrar",
            bgcolor=ft.colors.BLUE_700,
            color=ft.colors.WHITE,
            on_click=lambda e: verificar(username_field.value, password_field.value, page),
            
        ),
    )


# Função que cria o botão de registro
def btn_register(register_action):
    return ft.Container(
        col=7,
        padding=10,
        content=ft.ElevatedButton(
            text="Cadastrar",
            bgcolor=ft.colors.AMBER,
            color=ft.colors.WHITE,
            on_click=register_action,
            
        ),
    )
