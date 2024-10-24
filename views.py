import flet as ft
from models import *
import requests
import threading
import flet.map as map
from PIL import Image
import io




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
    menu = menus.create_settings_menu(color=ft.colors.BLUE_900, itens=itens, col=10)

    loading = LoadingPages(page)

    calltexts = CallText(page)
    texto_chamada = calltexts.create_container_calltext1()
    coord_text_lat = calltexts.create_calltext(text="-23.339500000000",
                      color=ft.colors.BLACK,
                      size=15,
                      font=ft.FontWeight.W_600,
                      col=12,
                      padding=0)
    coord_text_lon = calltexts.create_calltext(text="-47.823750000000",
                      color=ft.colors.BLACK,
                      size=15,
                      font=ft.FontWeight.W_600,
                      col=12,
                      padding=0)
    coord_text_zoom = calltexts.create_calltext(text="19",
                      color=ft.colors.BLACK,
                      size=15,
                      font=ft.FontWeight.W_600,
                      col=12,
                      padding=0)
    
    maps = Map(page, coord_text_lat, coord_text_lon, coord_text_zoom)
    mapa1 = maps.create_map()

    buttons = Buttons(page)
    add_button = buttons.create_add_button(on_click=lambda e: loading.new_loading_page(page=page, layout=create_page_add_forms(page, coord_text_lat.content.value, coord_text_lon.content.value)),
                                           col=2)
    

    container1 = ft.Container(padding=10)
    container2 = ft.Container(padding=5)

    return ft.ResponsiveRow(
        columns=12,
        controls=[
                container2,
                menu,
                add_button,
                coord_text_lat,
                coord_text_lon,
                coord_text_zoom,
                mapa1,
                texto_chamada,
                container1,
                home_facens,
                ],
        alignment=ft.MainAxisAlignment.CENTER,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
    )


def create_page_forms(page, poste, numero):


    loading = LoadingPages(page)

    buttons = Buttons(page)
    ordem_button = buttons.create_button(on_click=lambda e: loading.new_loading_page(page=page, layout=create_page_order(page, poste, numero)),
                                        text="Chamado",
                                        color=ft.colors.RED,
                                        col=6,
                                        padding=5,)
    back_home_button = buttons.create_button(on_click=lambda e: loading.new_loading_page(page=page, layout=create_page_home(page)),
                                            text="Voltar",
                                            color=ft.colors.AMBER,
                                            col=12,
                                            padding=5,)
    edit_button = buttons.create_button(on_click=lambda e: loading.new_loading_page(page=page, layout=create_page_edit_forms(page, poste)),
                                            text="Editar",
                                            color=ft.colors.GREEN,
                                            col=6,
                                            padding=5,)
    
    forms = Forms(page)
    forms1 = forms.create_forms(poste=poste)

    web_images = Web_Image(page)
    url_imagem1 = web_images.get_poste_image_url(numero)

    if url_imagem1 == "Nulo":

        texts = CallText(page)
        text1 = texts.create_calltext(text="Sem foto",
                                      color=ft.colors.BLACK,
                                      size=15,
                                      font=ft.FontWeight.W_400,
                                      col=12,
                                      padding=0,
                                      )
        foto_poste = ft.Container(col=12,height=400,alignment=ft.alignment.center,content=(text1))  

    else:

        foto_poste = web_images.create_web_image(src=url_imagem1, col=12, height=400)



    return ft.ResponsiveRow(
        columns=12,
        controls=[
            forms1,
            foto_poste,  
            ordem_button,
            edit_button,
            back_home_button   
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
    )


def create_page_add_forms(page, lat, long):

    def send_point(object, image):

        print(f"Testando a imagem 1: {image}")

        lat = object.content.rows[0].cells[1].content.content.value
        long = object.content.rows[1].cells[1].content.content.value
        ip = object.content.rows[2].cells[1].content.content.value
        situ = object.content.rows[3].cells[1].content.content.value
        tipo = object.content.rows[4].cells[1].content.content.value
        pontos = object.content.rows[5].cells[1].content.content.value
        bairro = object.content.rows[6].cells[1].content.content.value
        logra = object.content.rows[7].cells[1].content.content.value
        numero = int(ip.split('-')[1])


        add_point(page, numero, lat, long, ip, situ, tipo, pontos, bairro, logra, image=image)
     
    loading = LoadingPages(page)

    forms = Forms(page)
    forms1 = forms.create_add_forms(lat, long, ip="IP SOR-", situ=None, tipo=None, pontos=None, bairro=None, logra=None)

    buttons = Buttons(page)
    add_button = buttons.create_button(on_click=lambda e :send_point(forms1, container_foto.content),
                                            text="Adicionar",
                                            color=ft.colors.GREEN,
                                            col=6,
                                            padding=15,)
    back_home_button = buttons.create_button(on_click=lambda e: loading.new_loading_page(page=page, layout=create_page_home(page)),
                                            text="Voltar",
                                            color=ft.colors.AMBER,
                                            col=6,
                                            padding=15,)
    

    container_foto = ft.Container(col=8,
                                  height=400,
                                  expand=True,
                                  alignment=ft.alignment.center,
                                    border=ft.Border(
                                        left=ft.BorderSide(2, ft.colors.BLACK),
                                        top=ft.BorderSide(2, ft.colors.BLACK),
                                        right=ft.BorderSide(2, ft.colors.BLACK),
                                        bottom=ft.BorderSide(2, ft.colors.BLACK),
                                        ),
                                    content=None
                                  )  
    photos = GalleryPicker(page, container_foto)
    icon_camera = ft.IconButton(
        icon=ft.icons.CAMERA_ALT,
        icon_color=ft.colors.AMBER,
        expand=True,
        scale=2.3,
        on_click=photos.open_gallery,  # Chama a função diretamente
        alignment=ft.alignment.center,
        padding=0,
    )

    container1 = ft.Container(padding=10)
 

    return ft.ResponsiveRow(
        columns=12,
        controls=[
            forms1,
            container1,
            icon_camera,
            container_foto,
            add_button, 
            back_home_button   
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,

    )


def create_page_edit_forms(page, poste):

    def send_point(object):

        lat = object.content.rows[0].cells[1].content.content.value
        long = object.content.rows[1].cells[1].content.content.value
        ip = object.content.rows[2].cells[1].content.content.value
        situ = object.content.rows[3].cells[1].content.content.value
        tipo = object.content.rows[4].cells[1].content.content.value
        pontos = object.content.rows[5].cells[1].content.content.value
        bairro = object.content.rows[6].cells[1].content.content.value
        logra = object.content.rows[7].cells[1].content.content.value

        edit_point(page, lat, long, ip, situ, tipo, pontos, bairro, logra)
     
    loading = LoadingPages(page)

    forms = Forms(page)
    forms1 = forms.create_add_forms(poste.lat, poste.long, poste.ip, poste.situacao, poste.tipo, poste.pontos, poste.bairro, poste.logradouro)

    buttons = Buttons(page)
    add_button = buttons.create_button(on_click=lambda e :send_point(forms1),
                                            text="Salvar",
                                            color=ft.colors.GREEN,
                                            col=6,
                                            padding=5,)
    delete_button = buttons.create_button(on_click=lambda e :delete_point(page, poste.number),
                                            text="Excluir",
                                            color=ft.colors.RED,
                                            col=6,
                                            padding=5,)
    back_home_button = buttons.create_button(on_click=lambda e :loading.new_loading_page(page=page, layout=create_page_home(page)),
                                            text="Voltar",
                                            color=ft.colors.AMBER,
                                            col=7,
                                            padding=5,)
    


    return ft.ResponsiveRow(
        columns=12,
        controls=[
            forms1,
            add_button,
            delete_button,
            back_home_button   
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
    )
 



def create_page_order(page, poste, numero):

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
    back_forms_button = buttons.create_button(on_click=lambda e: loading.new_loading_page(page=page, layout=create_page_forms(page, poste, numero)),
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
    username_field = textfields.create_textfield(value=None, text="Usuário ou E-mail", password=False)
    password_field = textfields.create_textfield(value=None, text="Senha", password=True)

    menus = SettingsMenu(page)
    itens = []
    exit = menus.itens_settings_menu(text="Sair da aplicação",
                                       color=ft.colors.AMBER,
                                       action=lambda e: page.window_close())
    itens.append(exit)
    menu = menus.create_settings_menu(color=ft.colors.BLUE_900, itens=itens, col=12)

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
    username_field = textfields.create_textfield(value=None, text="Primeiro Nome", password=False)
    email_field = textfields.create_textfield(value=None, text="Email", password=False)
    number_field = textfields.create_textfield(value=None, text="Celular  Ex: 15912345678", password=False)
    password_field1 = textfields.create_textfield(value=None, text="Senha", password=True)
    password_field2 = textfields.create_textfield(value=None, text="Confirmar senha", password=False)

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

    def __init__(self, page, coord_text_lat, coord_text_lon, coord_text_zoom):
        self.page = page
        self.coord_text_lat = coord_text_lat
        self.coord_text_lon = coord_text_lon
        self.coord_text_zoom = coord_text_zoom


    def create_map(self):

        markers = Marker(self.page)
        mappoints = markers.create_points()
        MarkerLayer = mappoints



        def handle_event(e: map.MapEvent):
            self.coord_text_lat.content.value = f"{e.center.latitude:.6f}"
            self.coord_text_lon.content.value = f"{e.center.longitude:.6f}"
            self.coord_text_zoom.content.value = f"{e.zoom:.2f}"
            self.coord_text_lat.update()
            self.coord_text_lon.update()
            self.coord_text_zoom.update()
            self.page.update()
            


        google = map.Map(
                    expand=True,  
                    configuration=map.MapConfiguration(
                        initial_center=map.MapLatitudeLongitude(-23.3396, -47.8238),  
                        initial_zoom=19,
                        on_event=handle_event,
                    ),
                    layers=[
                        map.TileLayer(
                            url_template="https://tile.openstreetmap.org/{z}/{x}/{y}.png",
                        ),
                        map.MarkerLayer(MarkerLayer),
                        map.RichAttribution(
                            attributions=[map.TextSourceAttribution(text="Teste")]
                        )
                    ],
                )

        return ft.Column(
                visible=True,
                col=12,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Container(
                        width=400,
                        height=400,
                        alignment=ft.alignment.center,
                        bgcolor=ft.colors.GREY,
                        border=ft.Border(
                            left=ft.BorderSide(2, ft.colors.BLACK),
                            top=ft.BorderSide(2, ft.colors.BLACK),
                            right=ft.BorderSide(2, ft.colors.BLACK),
                            bottom=ft.BorderSide(2, ft.colors.BLACK),
                        ),
                        border_radius=ft.border_radius.all(250),
                        content=ft.Container(
                            width=395,
                            height=395,
                            alignment=ft.alignment.center,
                            bgcolor=ft.colors.GREY,
                            border_radius=ft.border_radius.all(250),
                            content=ft.Stack(
                                expand=True,
                                controls=[
                                    google,  
                                    ft.TransparentPointer( 
                                            content=ft.Container(
                                                alignment=ft.alignment.center,  
                                                content=ft.Icon(
                                                    name=ft.icons.CONTROL_POINT,
                                                    size=40,
                                                    color=ft.colors.BLACK,
                                                ),
                                            ),
                                        ),
                                ],
                            ),
                        ),
                    )
                ]
            )


class Marker:

    def __init__(self, page):
        self.page = page


    def create_points(self):
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
        FinalPoints = []

        # Classe Buttons usada para criar botões e marcadores
        buttons = Buttons(self.page)

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
            Latitude = row["coord_x"]
            Longitude = row["coord_y"]

            loading = LoadingPages(self.page)
            poste = Poste(number, name, situacao, tipo, pontos, bairro, logradouro, Latitude, Longitude)

            def create_on_click(poste=poste, number=number):
                return lambda e: loading.new_loading_page(
                    page=self.page,
                    layout=create_page_forms(self.page, poste, number)
                )

            # Cria o botão com o valor correspondente de 'number'
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
            marker = buttons.create_point_marker(
                content=button_data["element"],
                x=button_data["x"],
                y=button_data["y"],
            )
            FinalPoints.append(marker)

        # Retorna a lista de marcadores
        return FinalPoints








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


def add_point(page, numero, lat, long, ip, situ, tipo, pontos, bairro, logra, image):


    page.snack_bar = ft.SnackBar(
            content=ft.Text("Adicionando ponto..."),
            bgcolor=ft.colors.ORANGE,
            duration=2000,
        )
    page.snack_bar.open = True
    page.update()

    def pause_and_continue(image):


        def image_path_to_bytes(image_path):
            # Abre a imagem a partir do caminho
            with Image.open(image_path) as img:
                # Rotaciona a imagem 90 graus para a direita
                rotated_img = img.rotate(-90, expand=True)  # -90 graus para sentido horário
                
                # Cria um fluxo de bytes
                byte_stream = io.BytesIO()
                # Salva a imagem rotacionada no fluxo de bytes
                rotated_img.save(byte_stream, format='JPEG')  # ou 'PNG' se necessário
                
                # Move o ponteiro do fluxo de bytes para o início
                byte_stream.seek(0)
                
                # Retorna os bytes da imagem
                return byte_stream.read()



        # Verificar se todos os campos estão preenchidos
        if not lat or not long or not ip or not situ or not tipo or not pontos or not bairro or not logra:
            page.snack_bar = ft.SnackBar(
                content=ft.Text("Alguns campos não foram preenchidos"),
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


        # Verificar se o ponto já foi cadastrado
        response = requests.get(
            f"{SUPABASE_URL}/rest/v1/points_capeladoalto",
            headers=headers,
            params={"select": "name", "name": f"eq.{ip}"}
        )

        if response.status_code == 200 and response.json():
            # Se o ponto já existir, mostre a mensagem e retorne
            page.snack_bar = ft.SnackBar(
                content=ft.Text(f"{ip} já foi cadastrado, ponto não adicionado"),
                bgcolor=ft.colors.RED
            )
            page.snack_bar.open = True
            page.update()
            return
        

        image_url = "Nulo"
        # ..............................
        #Inicia o processamento da imagem
        # ..............................
        if image != None:
            im_path = image.src
            image_bytes = image_path_to_bytes(im_path)
            send_images = SendImage()
            image_url = send_images.upload_image(image_bytes, numero)



        # Obter o maior valor de user_id na tabela
        response = requests.get(
            f"{SUPABASE_URL}/rest/v1/points_capeladoalto",
            headers=headers,
            params={"select": "id", "order": "id.desc", "limit": 1},
        )

        if response.status_code == 200:
            max_user_id = response.json()[0]["id"] if response.json() else 0
            new_user_id = max_user_id + 1

            # Dados para inserir no Supabase
            data = {
                "number": numero,
                "coord_x": lat,
                "coord_y": long,
                "name": ip,
                "situacao": situ,
                "tipo": tipo,
                "pontos": pontos,
                "bairro": bairro,
                "logradouro": logra,
                "url": image_url
            }

            # Fazer a solicitação POST para inserir o novo registro
            response = requests.post(
                f"{SUPABASE_URL}/rest/v1/points_capeladoalto",
                headers=headers,
                json=data,
            )

            # Verificar se a inserção foi bem-sucedida
            if response.status_code == 201:
                page.snack_bar = ft.SnackBar(
                    content=ft.Text("Ponto adicionado com sucesso"),
                    bgcolor=ft.colors.GREEN
                )

                loading = LoadingPages(page)
                loading.new_loading_page(page=page, layout=create_page_home(page))
                
            else:
                print(f"Erro ao inserir ponto: {response.status_code}")
                print(f"Resposta do erro: {response.text}")
                page.snack_bar = ft.SnackBar(
                    content=ft.Text(f"Erro ao inserir ponto: {response.text}"),
                    bgcolor=ft.colors.RED
                )
        else:
            print(f"Erro ao obter o maior user_id: {response.status_code}")
            print(f"Resposta do erro: {response.text}")
            page.snack_bar = ft.SnackBar(
                content=ft.Text(f"Erro ao obter id: {response.text}"),
                bgcolor=ft.colors.RED
            )

        # Abrir o snack bar e atualizar a página
        page.snack_bar.open = True
        page.update()

    # Iniciar o temporizador
    threading.Timer(2.0, pause_and_continue(image)).start()


def edit_point(page, lat, long, ip, situ, tipo, pontos, bairro, logra):


    numero = int(ip.split('-')[1])

    # Mostrar snack bar de "Editando ponto..."
    page.snack_bar = ft.SnackBar(
        content=ft.Text("Editando ponto..."),
        bgcolor=ft.colors.ORANGE,
        duration=2000,
    )
    page.snack_bar.open = True
    page.update()

    def pause_and_continue():
        # Verificar se todos os campos estão preenchidos
        if not all([lat, long, ip, situ, tipo, pontos, bairro, logra]):
            page.snack_bar = ft.SnackBar(
                content=ft.Text("Alguns campos não foram preenchidos"),
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
            return  # Interrompe se não houver conexão

        # URL e chave da API do Supabase
        SUPABASE_URL = "https://ipyhpxhsmyzzkvucdonu.supabase.co"
        SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImlweWhweGhzbXl6emt2dWNkb251Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3Mjc1NjQ3NDIsImV4cCI6MjA0MzE0MDc0Mn0.qA9H-UyAEx2OgihW1d_i2IjqQ5HTt1e4ITr52J5qRsA"

        # Cabeçalhos com a API Key
        headers = {
            "apikey": SUPABASE_KEY,
            "Authorization": f"Bearer {SUPABASE_KEY}",
            "Content-Type": "application/json",
        }

        # Dados a serem atualizados
        data = {
            "coord_x": lat,
            "coord_y": long,
            "name": ip,
            "situacao": situ,
            "tipo": tipo,
            "pontos": pontos,
            "bairro": bairro,
            "logradouro": logra,
        }

        # Realiza a requisição PATCH para atualizar o registro onde "number" é igual a `numero`
        response = requests.patch(
            f"{SUPABASE_URL}/rest/v1/points_capeladoalto?number=eq.{numero}",
            headers=headers,
            json=data,
        )

        # Verificar se a atualização foi bem-sucedida
        if response.status_code in [200, 204]:  # 204 indica sucesso sem conteúdo
            page.snack_bar = ft.SnackBar(
                content=ft.Text("Alterações Salvas"),
                bgcolor=ft.colors.GREEN
            )
        else:
            print(f"Erro ao editar ponto: {response.status_code}")
            print(f"Resposta do erro: {response.text}")
            page.snack_bar = ft.SnackBar(
                content=ft.Text(f"Erro ao editar ponto: {response.text}"),
                bgcolor=ft.colors.RED
            )

        # Exibir o snack bar e atualizar a página
        page.snack_bar.open = True
        page.update()

    # Iniciar o temporizador
    threading.Timer(2.0, pause_and_continue).start()


def delete_point(page, numero):

    page.snack_bar = ft.SnackBar(
        content=ft.Text("Excluindo ponto..."),
        bgcolor=ft.colors.ORANGE,
        duration=2000,
    )
    page.snack_bar.open = True
    page.update()

    def pause_and_continue():
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
            return  # Interrompe a execução se não há conexão

        # URL e chave do Supabase
        SUPABASE_URL = "https://ipyhpxhsmyzzkvucdonu.supabase.co"
        SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImlweWhweGhzbXl6emt2dWNkb251Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3Mjc1NjQ3NDIsImV4cCI6MjA0MzE0MDc0Mn0.qA9H-UyAEx2OgihW1d_i2IjqQ5HTt1e4ITr52J5qRsA"

        headers = {
            "apikey": SUPABASE_KEY,
            "Authorization": f"Bearer {SUPABASE_KEY}",
            "Content-Type": "application/json",
        }

        # Excluir o ponto cujo número seja igual à variável `numero`
        response1 = requests.delete(
            f"{SUPABASE_URL}/rest/v1/points_capeladoalto?number=eq.{numero}",
            headers=headers,
        )

        storage_path = f'postes_images_points/postes/{numero}.jpg'

        response2 = requests.delete(
            f"{SUPABASE_URL}/storage/v1/object/{storage_path}",
            headers=headers,
        )

        # Verificar se a exclusão foi bem-sucedida
        if response1.status_code == 204:

            headers2 = {
            "apikey": SUPABASE_KEY,
            "Authorization": f"Bearer {SUPABASE_KEY}",
            'Content-Type': 'image/jpeg'
            }

            storage_path = f'postes_images_points/postes/{numero}.jpg'

            response2 = requests.delete(
                f"{SUPABASE_URL}/storage/v1/object/{storage_path}",
                headers=headers2,
            )            

            if response2.status_code == 200:

                page.snack_bar = ft.SnackBar(
                    content=ft.Text("Ponto e imagem excluidos com sucesso"),
                    bgcolor=ft.colors.GREEN
                )
                loading = LoadingPages(page)
                loading.new_loading_page(page=page, layout=create_page_home(page))

            else:

                page.snack_bar = ft.SnackBar(
                    content=ft.Text("Ponto excluido mas imagem mantida"),
                    bgcolor=ft.colors.AMBER
                )
                loading = LoadingPages(page)
                loading.new_loading_page(page=page, layout=create_page_home(page))

        else:
            print(f"Erro ao excluir ponto: {response1.status_code}")
            print(f"Resposta do erro: {response1.text}")
            page.snack_bar = ft.SnackBar(
                content=ft.Text(f"Erro ao excluir ponto: {response1.text}"),
                bgcolor=ft.colors.RED
            )

        # Exibir a mensagem e atualizar a página
        page.snack_bar.open = True
        page.update()

    # Iniciar o temporizador
    threading.Timer(2.0, pause_and_continue).start()
