import flet as ft
from models import *
import requests
import threading
import flet.map as map






def create_page_home(page):

    web_images = Web_Image(page)
    url_imagem1 = web_images.get_image_url(name="titulo_geopostes")
    home_title = web_images.create_web_image(src=url_imagem1, col=12, height=120)
    url_imagem2 = web_images.get_image_url(name="icone_facens")
    home_facens = web_images.create_web_image(src=url_imagem2, col=12, height=70)

    menus = SettingsMenu(page)
    itens = []
    logout = menus.itens_settings_menu(text="Deslogar",
                                       color=ft.colors.AMBER,
                                       action=lambda e: loading.new_loading_page(page=page, layout=create_page_login(page)))
    exit = menus.itens_settings_menu(text="Sair da aplicação",
                                       color=ft.colors.AMBER,
                                       action=lambda e: page.window_close())
    itens.append(logout)
    itens.append(exit)
    menu = menus.create_settings_menu(color=ft.colors.BLUE_900, itens=itens)

    loading = LoadingPages(page)

    maps = Map(page)
    mapa1 = maps.create_map(page)

    calltexts = CallText(page)
    texto_chamada = calltexts.create_container_calltext1()

    container1 = ft.Container(padding=10)
    container2 = ft.Container(padding=5)

    return ft.ResponsiveRow(
        columns=12,
        controls=[
                container2,
                menu,
                home_title,
                mapa1,
                texto_chamada,
                container1,
                home_facens,
                ],
        alignment=ft.MainAxisAlignment.CENTER,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
    )


def create_page_forms(page, poste, foto):


    loading = LoadingPages(page)

    buttons = Buttons(page)
    ordem_button = buttons.create_button(on_click=lambda e: loading.new_loading_page(page=page, layout=create_page_order(page, poste, foto)),
                                        text="Chamado",
                                        color=ft.colors.RED,
                                        col=6,
                                        padding=15,)
    back_home_button = buttons.create_button(on_click=lambda e: loading.new_loading_page(page=page, layout=create_page_home(page)),
                                            text="Voltar",
                                            color=ft.colors.AMBER,
                                            col=6,
                                            padding=15,)
    
    forms = Forms(page)
    forms1 = forms.create_forms(poste=poste)

    web_images = Web_Image(page)
    url_imagem1 = web_images.get_poste_image_url(number=foto)
    foto_poste = web_images.create_web_image(src=url_imagem1, col=12, height=400)

    return ft.ResponsiveRow(
        columns=12,
        controls=[
            forms1,
            foto_poste,  
            ordem_button,
            back_home_button   
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
    )
 

def create_page_order(page, poste, foto):

    calltexts = CallText(page)
    text1 = calltexts.create_container_calltext2(text=poste.ip)
    text2 = calltexts.create_calltext(text="Qual o motivo da ordem de serviço",
                      color=ft.colors.BLACK,
                      size=30,
                      font=ft.FontWeight.W_900,
                      col=12,
                      padding=20)
    text3 = calltexts.create_calltext(text="Ordem enviada com sucesso",
                                           color=ft.colors.GREEN,
                                           size=30,
                                           font=None,
                                           col=12,
                                           padding=None
                                           )


    checkboxes = CheckBox(page)
    box_1 = checkboxes.create_checkbox(text="Ponto apagado", size=25, on_change=None, col=12)
    box_2 = checkboxes.create_checkbox(text="Ponto piscando", size=25, on_change=None, col=12)
    box_3 = checkboxes.create_checkbox(text="Rachadura", size=25, on_change=None, col=12)
    box_4 = checkboxes.create_checkbox(text="Queda", size=25, on_change=None, col=12)
    box_5 = checkboxes.create_checkbox(text="Incêndia elétrico", size=25, on_change=None, col=12)
    box_6 = checkboxes.create_checkbox(text="Adicionar ponto", size=25, on_change=None, col=12)

    textfields = TextField(page)
    text_field_order = textfields.create_description_textfield(text="Adicionar comentário")

    loading = LoadingPages(page)

    buttons = Buttons(page)
    send_button = buttons.create_button(on_click=lambda e: (page.add(text3), page.scroll_to(9999)),
                                        text="Enviar",
                                        color=ft.colors.GREEN,
                                        col=6,
                                        padding=15,)
    back_forms_button = buttons.create_button(on_click=lambda e: loading.new_loading_page(page=page, layout=create_page_forms(page, poste, foto)),
                                              text="Voltar",
                                              color=ft.colors.AMBER,
                                              col=6,
                                              padding=15,)

    container1 = ft.Container(padding=10)

    return ft.ResponsiveRow(
        columns=12,
        controls=[
            container1,
            text1,  
            text2,
            box_1,
            box_2,
            box_3,
            box_4,
            box_5,
            box_6,
            text_field_order,
            send_button,
            back_forms_button  
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
    )


def create_page_login(page):

    web_images = Web_Image(page)
    url_imagem1 = web_images.get_image_url(name="titulo_geopostes")
    login_title = web_images.create_web_image(src=url_imagem1, col=12, height=120) 
    url_imagem2 = web_images.get_image_url(name="icone_facens")
    login_facens = web_images.create_web_image(src=url_imagem2, col=12, height=70)

    checkboxes = CheckBox(page)
    def visible_password(e):
        password_field.password = not password_field.password
        page.update()
    box_login = checkboxes.create_checkbox(text="Mostrar senha", size=15, on_change=visible_password, col=8)

    textfields = TextField(page)
    username_field = textfields.create_textfield(text="Usuário ou E-mail", password=False)
    password_field = textfields.create_textfield(text="Senha", password=True)

    menus = SettingsMenu(page)
    itens = []
    exit = menus.itens_settings_menu(text="Sair da aplicação",
                                       color=ft.colors.AMBER,
                                       action=lambda e: page.window_close())
    itens.append(exit)
    menu = menus.create_settings_menu(color=ft.colors.BLUE_900, itens=itens)

    loading = LoadingPages(page)

    buttons = Buttons(page)
    btn_login = buttons.create_button(on_click=lambda e: verificar(username_field.value, password_field.value, page),
                                      text="Entrar",
                                      color=ft.colors.BLUE_700,
                                      col=7,
                                      padding=10,)
    btn_register = buttons.create_button(on_click=lambda e: loading.new_loading_page(page=page, layout=create_page_register(page)),
                                         text="Cadastrar",
                                         color=ft.colors.AMBER,
                                         col=7,
                                         padding=10,)

    container1 = ft.Container(padding=10)
    container2 = ft.Container(padding=5)


    return ft.ResponsiveRow(
        columns=12,
        controls=[
            container2,
            menu,
            login_title,
            container1,  
            username_field,  
            password_field,
            box_login,
            container2,
            btn_login,
            btn_register, 
            container2,
            login_facens,
             
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
    )


def create_page_register(page):

    web_images = Web_Image(page)
    url_imagem1 = web_images.get_image_url(name="titulo_geopostes")
    register_title = web_images.create_web_image(src=url_imagem1, col=12, height=120)

    textfields = TextField(page)
    username_field = textfields.create_textfield(text="Primeiro Nome", password=False)
    email_field = textfields.create_textfield(text="Email", password=False)
    number_field = textfields.create_textfield(text="Celular  Ex: 15912345678", password=False)
    password_field1 = textfields.create_textfield(text="Senha", password=True)
    password_field2 = textfields.create_textfield(text="Confirmar senha", password=False)

    container1 = ft.Container(
      padding=5
    )

    loading = LoadingPages(page)

    buttons = Buttons(page)
    btn_register = buttons.create_button(on_click=lambda e: register(username_field.value.strip(), email_field.value.strip(), number_field.value.strip(), password_field1.value.strip(), password_field2.value.strip(), page),
                                         text="Registrar",
                                         color=ft.colors.BLUE_700,
                                         col=7,
                                         padding=10,)
    btn_back = buttons.create_button(on_click=lambda e: loading.new_loading_page(page=page, layout=create_page_login(page)),
                                     text="Voltar",
                                     color=ft.colors.AMBER,
                                     col=7,
                                     padding=10)

    return ft.ResponsiveRow(
        columns=12,
        controls=[
            container1,
            register_title, 
            container1, 
            username_field, 
            email_field,
            number_field, 
            password_field1,
            password_field2,
            container1,
            btn_register,
            btn_back,         
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
    )


class Map:

    def __init__(self, page):
        self.page = page

    def create_map(self, page):

        markers = Marker(page)
        mapmarkers = markers.create_markers(page)


        google = map.Map(
                    expand=True,  
                    configuration=map.MapConfiguration(
                        initial_center=map.MapLatitudeLongitude(-23.339500000000, -47.823750000000),  
                        initial_zoom=19 
                    ),
                    layers=[
                        map.TileLayer(
                            url_template="https://tile.openstreetmap.org/{z}/{x}/{y}.png"
                        ),
                        map.MarkerLayer(markers=mapmarkers),
                    ],
                )

        return ft.Column(
            visible=True,
            col=12,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[ft.Container(
                width=400,
                height=400,
                alignment=ft.alignment.center,
                bgcolor=ft.colors.GREY,
                border=ft.Border(
                    left=ft.BorderSide(2, ft.colors.BLACK),  
                    top=ft.BorderSide(2, ft.colors.BLACK),    
                    right=ft.BorderSide(2, ft.colors.BLACK), 
                    bottom=ft.BorderSide(2, ft.colors.BLACK) 
                ),
                border_radius=ft.border_radius.all(250),
                content=ft.Container(
                    width=395,
                    height=395,
                    alignment=ft.alignment.center,
                    bgcolor=ft.colors.GREY,
                    border_radius=ft.border_radius.all(250),
                    content=google,
                ))]
        )


class Marker:

    def __init__(self, page):
        self.page = page


    def create_markers(self, page):
        # Configuração da URL e cabeçalho
        SUPABASE_URL = "https://ipyhpxhsmyzzkvucdonu.supabase.co"
        SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImlweWhweGhzbXl6emt2dWNkb251Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3Mjc1NjQ3NDIsImV4cCI6MjA0MzE0MDc0Mn0.qA9H-UyAEx2OgihW1d_i2IjqQ5HTt1e4ITr52J5qRsA"

        headers = {
            "apikey": SUPABASE_KEY,
            "Authorization": f"Bearer {SUPABASE_KEY}",
            "Content-Type": "application/json",
        }

        # Parâmetros da requisição GET
        params = {"select": "number,coord_x,coord_y,name,situacao,tipo,pontos,bairro,logradouro"}

        # Requisição à API
        response = requests.get(
            f"{SUPABASE_URL}/rest/v1/points_capeladoalto",
            headers=headers,
            params=params,
        )

        # Verifica se a requisição foi bem-sucedida
        if response.status_code != 200:
            print("Erro ao buscar dados:", response.text)
            return []

        data = response.json()

        # Inicializa o dicionário de botões e a lista de marcadores
        InitialButtons = {}
        Markers = []

        # Classe Buttons usada para criar botões e marcadores
        buttons = Buttons(page)

        # Loop para criar os botões com base nas linhas da tabela
        for row in data:
            number = row["number"]
            coord_x = row["coord_x"]
            coord_y = row["coord_y"]
            name = row["name"]
            situacao = row["situacao"]
            tipo = row["tipo"]
            pontos = row["pontos"]
            bairro = row["bairro"]
            logradouro = row["logradouro"]

            loading = LoadingPages(page)
            poste = Poste(number, name, situacao, tipo, pontos, bairro, logradouro)

            def create_on_click(poste=poste, number=number):
                return lambda e: loading.new_loading_page(
                    page=page,
                    layout=create_page_forms(page, poste, foto=number)
                )

            # Cria o botão com o valor correspondente de 'number'
            btn_name = f"btn{number}"
            InitialButtons[number] = {
                "element": buttons.create_point_button(
                    on_click=create_on_click(),  # Usa a função auxiliar
                    text=str(number)
                ),
                "x": coord_x,
                "y": coord_y,
            }

        # Cria marcadores com base nos botões criados
        for number, button_data in InitialButtons.items():
            marker_name = f"marker{number}"
            marker = buttons.create_point_marker(
                content=button_data["element"],
                x=button_data["x"],
                y=button_data["y"],
            )
            Markers.append(marker)

        # Retorna a lista de marcadores
        return Markers








# Função para verificar as credenciais no Supabase
def verificar(username, password, page):

    loading = LoadingPages(page)

    if username == "Carlos" and password == "63607120":
        page.snack_bar = ft.SnackBar(
            content=ft.Text("Administrador reconhecido"),
            bgcolor=ft.colors.GREEN,
            duration= 1000,
        )
        page.snack_bar.open = True
        loading.new_loading_page(page=page, layout=create_page_home(page))
    
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
            return 

        # URL da API do seu projeto no Supabase
        SUPABASE_URL = "https://ipyhpxhsmyzzkvucdonu.supabase.co" 
        SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImlweWhweGhzbXl6emt2dWNkb251Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3Mjc1NjQ3NDIsImV4cCI6MjA0MzE0MDc0Mn0.qA9H-UyAEx2OgihW1d_i2IjqQ5HTt1e4ITr52J5qRsA"  # Substitua pela API Key gerada pelo Supabase

        # Cabeçalho com a API Key
        headers = {
            "apikey": SUPABASE_KEY,
            "Authorization": f"Bearer {SUPABASE_KEY}",
            "Content-Type": "application/json",
        }

        # Adicione os filtros de consulta nos parâmetros da URL
        params = {
            "or": f"(usuario.eq.{username},email.eq.{username})",
            "senha": f"eq.{password}",
            "select": "*"
        }

        response = requests.get(
            f"{SUPABASE_URL}/rest/v1/login_geopostes",
            headers=headers,
            params=params,
        )

        if response.status_code == 200 and len(response.json()) > 0:
            page.snack_bar = ft.SnackBar(
            content=ft.Text("Login realizado"),
            bgcolor=ft.colors.GREEN,
            duration= 1000,
            )
            page.snack_bar.open = True
            loading.new_loading_page(page=page, layout=create_page_home(page))  # Vai para a página inicial se o login for bem-sucedido
            
        else:
            # Exibe mensagem de erro se as credenciais não forem encontradas
            page.snack_bar = ft.SnackBar(
                content=ft.Text("Login ou senha incorretos"),
                bgcolor=ft.colors.RED
            )
            page.snack_bar.open = True
            page.update()


# Função para inserir um registro no Supabase
def register(username, email, number, password1, password2, page):

    page.snack_bar = ft.SnackBar(
            content=ft.Text("Realizando Cadastro..."),
            bgcolor=ft.colors.ORANGE,
            duration=2000,
        )
    page.snack_bar.open = True
    page.update()

    def pause_and_continue():

        # Verificar se todos os campos estão preenchidos
        if not username or not email or not number or not password1 or not password2:
            page.snack_bar = ft.SnackBar(
                content=ft.Text("Alguns campos não foram preenchidos"),
                bgcolor=ft.colors.RED
            )
            page.snack_bar.open = True
            page.update()
            return  # Interrompe a execução da função
        
        #Verificar se as senhas coincidem
        if password1 != password2:
            page.snack_bar = ft.SnackBar(
                content=ft.Text("As senhas não coincidem"),
                bgcolor=ft.colors.RED
            )
            page.snack_bar.open = True
            page.update()
            return  # Interrompe a execução da função 
        

        # Verificar conexão com a internet
        try:
            requests.get("https://www.google.com", timeout=5)
        except requests.ConnectionError:
            page.snack_bar = ft.SnackBar(
                content=ft.Text("Sem conexão com a internet"),
                bgcolor=ft.colors.RED
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


        # Verificar se o email já foi cadastrado
        response = requests.get(
            f"{SUPABASE_URL}/rest/v1/login_geopostes",
            headers=headers,
            params={"select": "email", "email": f"eq.{email}"}
        )

        if response.status_code == 200 and response.json():
            # Se o e-mail já existir, mostre a mensagem e retorne
            page.snack_bar = ft.SnackBar(
                content=ft.Text("E-mail já cadastrado"),
                bgcolor=ft.colors.RED
            )
            page.snack_bar.open = True
            page.update()
            return


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
                "senha": password1,
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

    # Iniciar o temporizador
    threading.Timer(2.0, pause_and_continue).start()
