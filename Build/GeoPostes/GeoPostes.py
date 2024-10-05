import flet as ft
from views import *
from models import *

def main(page: ft.Page):
    # Configurações da janela
    page.title = 'Flet App'
    page.window.always_on_top = True
    page.window.height = 960
    page.window.width = 540 
    page.window.resizable = False  
    page.bgcolor = ft.colors.WHITE  
    page.scroll = "auto"  # Habilitar rolagem automática na página

    # Estado inicial do poste
    poste = Poste("IP SOR-0010", "Com iluminação", "Lâmpada LED", 1, "Centro", "Rua Raimundo Malta")
    poste2 = Poste("IP SOR-0020", "Com iluminação", "Lâmpada Química", 1, "Centro", "Rua Raimundo Malta")


    # Define o nome da rota inicial como "Home"
    def go_home(e):
        page.go("/")


    # Botão flutuante para reiniciar a tela
    def action_btn(page):
        page.floating_action_button = ft.FloatingActionButton(
            icon=ft.icons.HOUSE,
            on_click=go_home
        )

    def update_floating_button(page):
        if page.route != "/login" and page.route != "/register" :
            action_btn(page)
        else:
            page.floating_action_button = None  # Remove o botão se na página de login

    # Definindo as rotas
    def route_change(route):

        if page.route == "/form" or page.route == "/order":
            None
        else:

            page.clean()  # Limpa os controles da página
            update_floating_button(page)

            # Se a rota for "/", carrega a home
            if page.route == "/":
                titulo = create_titulo()
                mapa = create_mapa(
                    page,
                    btn1_action=lambda e: page_forms(e, page, poste, foto1),
                    btn2_action=lambda e: page_forms(e, page, poste2, foto2),
                )
                container1 = ft.Container(padding=10)
                container2 = ft.Container(padding=5)

                layout = ft.ResponsiveRow(
                    columns=12,
                    controls=[
                        titulo,
                        mapa,
                        container2,
                        texto_chamada,
                        container1,
                        facens
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                )
                page.add(layout)


            # Se a rota for "/order", carrega login
            elif page.route == "/login":
                page_login(None, page)  # Chama a função para carregar login

            # Se a rota for "/order", carrega login
            elif page.route == "/register":
                page_register(None, page)  # Chama a função para carregar login


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

    # Evento para gerenciar o ciclo de vida do aplicativo
    def event(e):
        if e.data == 'detach' and page.platform == ft.PagePlatform.ANDROID:
            on_back()  # Chama a função on_back ao invés de encerrar

    # Associa os eventos
    page.on_app_lifecycle_state_change = event
    page.on_keyboard_event = on_keyboard_event



    # Registra a função para lidar com mudança de rota
    page.on_route_change = route_change

    # Registra a função para detectar eventos de teclado
    page.on_keyboard_event = on_keyboard_event

    # Define a rota inicial como "/"
    page.go("/login")





# Executa a aplicação
if __name__ == "__main__":
    ft.app(target=main, assets_dir="assets")
