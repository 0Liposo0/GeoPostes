import flet as ft
from views import *
from models import *

def main(page: ft.Page):
    # Configurações da janela
    page.title = 'GeoPostes'
    page.window.always_on_top = True
    page.window.height = 960
    page.window.width = 440 
    page.window.resizable = False  
    page.bgcolor = ft.colors.WHITE  
    page.scroll = "auto"  # Habilitar rolagem automática na página


    # Definindo as rotas
    def route_change(route):
        # Verifica se já estamos na rota atual, evitando re-executar o carregamento
        if page.route == route:
            return
        
        if page.route == "/form" or page.route == "/order":
            return

        # Limpa a página apenas quando a rota for alterada
        page.clean()

        # Se a rota for "/", carrega a home
        if page.route == "/":
            page.add(create_page_home(page))

        # Se a rota for "/login", carrega login
        elif page.route == "/login":
            page.add(create_page_login(page))

        # Se a rota for "/register", carrega o registro
        elif page.route == "/register":
            page.add(create_page_register(page))

        page.update()



    # Função para fechar o aplicativo
    def sair_da_aplicacao(e):
        page.window_close()  # Fecha a janela do aplicativo

    # Função para abrir o diálogo de confirmação
    def confirmar_saida(e=None):
        print("Chamando alerta")
        page.dialog = dialog  # Define o dialog como o diálogo da página
        dialog.open = True
        page.update()
 
    # Função para fechar o diálogo
    def close_dialog(e):
        dialog.open = False
        page.update()

    dialog = ft.AlertDialog(
        modal=True,  # Torna o diálogo modal
        title=ft.Text("Deseja sair da aplicação?"),
        actions=[
            ft.TextButton("Sim", on_click=sair_da_aplicacao),  # Botão para sair
            ft.TextButton("Não", on_click=close_dialog),  # Botão para cancelar
        ],
    )




    # Função que detecta o evento de voltar do celular ou tecla "Esc" no desktop
    def on_back():
        if page.route == "/form":
            page.go("/")  # Vai para a página inicial "Home"

        elif page.route == "/order":
            page.go("/")  # Vai para a página inicial "Home"

        elif page.route == "/register":
            page.go("/login")

        elif page.route == "/":
            page.go("/login")

        elif page.route == "/login":
            confirmar_saida() 

    # Função para lidar com eventos de teclado
    def on_keyboard_event(e: ft.KeyboardEvent):
        if e.key == "Escape":  # Se a tecla pressionada for "Esc"
            on_back()



    # Registra a função para lidar com mudança de rota
    page.on_route_change = route_change

    # Registra a função para detectar eventos de teclado
    page.on_keyboard_event = on_keyboard_event

    # Define a rota inicial como "/"
    page.go("/login")





# Executa a aplicação
if __name__ == "__main__":
    ft.app(target=main)
