import flet as ft
from models import *
from login import *
from register import *
import threading
import requests


# Estado inicial do poste
poste = Poste("IP SOR-0010", "Com iluminação", "Lâmpada LED", 1, "Centro", "Rua Raimundo Malta")
poste2 = Poste("IP SOR-0020", "Com iluminação", "Lâmpada Química", 1, "Centro", "Rua Raimundo Malta")




# Função que cria o título da ordem de serviço
def create_titulo_2(poste):
    titulo2 = ft.Column(
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        controls=[ ft.Container(
                    visible=True,
                    padding=10,
                    col=12,
                    bgcolor=ft.colors.BLUE_700,
                    border_radius=10,
                    content= ft.Text(
                            value=poste.ip,
                            color=ft.colors.WHITE,
                            size=40,
                            weight=ft.FontWeight.W_600,
                            font_family="Tahoma",
                            ),)
                ]
                )
    return titulo2


# Função que cria o mapa com as ações dos botões passadas como parâmetro
def create_mapa(page, btn1_action, btn2_action):
    btn1 = ft.Column(
    spacing=0,
    controls=[
        ft.ElevatedButton(
            on_click=btn1_action,
            width=20,
            height=20,
            bgcolor=ft.colors.AMBER,
            text=" ",
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=10),
            ),
        ),
        ft.Text(value="10", color=ft.colors.BLACK, size=20, text_align=ft.TextAlign.START, weight=ft.FontWeight.BOLD),
    ]
)

    btn2 = ft.Column(
        spacing=0,
        controls=[
            ft.ElevatedButton(
                on_click=btn2_action,
                width=20,
                height=20,
                bgcolor=ft.colors.AMBER,
                text=" ",
                style=ft.ButtonStyle(
                    shape=ft.RoundedRectangleBorder(radius=10),
                ),
            ),
            ft.Text(value="20", color=ft.colors.BLACK, size=20, text_align=ft.TextAlign.START,weight=ft.FontWeight.BOLD),
        ]
    )

    # Função de animação
    def animate_button():
        # Acessar os botões dentro das colunas btn1 e btn2
        button_1 = btn1.controls[0]
        button_2 = btn2.controls[0]

        if button_1.width == 24:
            # Diminuir tamanho
            button_1.width = 20
            button_1.height = 20
            button_1.style.shape = ft.RoundedRectangleBorder(radius=10)

            button_2.width = 20
            button_2.height = 20
            button_2.style.shape = ft.RoundedRectangleBorder(radius=10)
        else:
            # Aumentar tamanho
            button_1.width = 24
            button_1.height = 24
            button_1.style.shape = ft.RoundedRectangleBorder(radius=11)

            button_2.width = 24
            button_2.height = 24
            button_2.style.shape = ft.RoundedRectangleBorder(radius=11)

        page.update()  # Atualiza a página para refletir as mudanças

        # Chama a função novamente após 500ms
        threading.Timer(0.5, animate_button).start()


    # Inicia a animação
    animate_button()


    imagem3 = "mapa"
    mapa_home = get_image_url(imagem3)

    imagem4 = "seta"
    icone_seta = get_image_url(imagem4)

    seta = ft.Image(
    data=0,
    src=icone_seta,
    repeat=ft.ImageRepeat.NO_REPEAT,
    height=70,
)


    mapa = ft.Column(
        visible=True,
        col=12,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        controls=[ft.Container(
            width=400,
            height=400,
            alignment=ft.alignment.center,
            image_src=mapa_home,
            bgcolor=ft.colors.GREY,
            border=ft.Border(
                left=ft.BorderSide(2, ft.colors.BLACK),  
                top=ft.BorderSide(2, ft.colors.BLACK),    
                right=ft.BorderSide(2, ft.colors.BLACK), 
                bottom=ft.BorderSide(2, ft.colors.BLACK) 
            ),
            border_radius=ft.border_radius.all(250),
            content=ft.Column(
                spacing=0,
                alignment=ft.MainAxisAlignment.CENTER,
                controls=[
                    ft.Row(
                        alignment=ft.MainAxisAlignment.CENTER,
                        spacing=80,
                        controls=[btn1, seta, btn2]  # seta importada do models.py
                    ),
                ],
            )
        )]
    )
    return mapa


# Função que cria o formulário para exibir os dados do poste
def create_forms(poste):
    forms = ft.Container(
        padding=0,
        col=12,
        content=ft.DataTable(
            data_row_max_height=50,
            columns=[
                ft.DataColumn(ft.Text(value="")),
                ft.DataColumn(ft.Text(value="")),
            ],
            rows=[
                ft.DataRow(cells=[ft.DataCell(ft.Text(value="IP", theme_style=ft.TextThemeStyle.TITLE_LARGE)),
                                  ft.DataCell(ft.Text(value=poste.ip, theme_style=ft.TextThemeStyle.TITLE_MEDIUM))]),
                ft.DataRow(cells=[ft.DataCell(ft.Text(value="Situação", theme_style=ft.TextThemeStyle.TITLE_LARGE)),
                                  ft.DataCell(ft.Text(value=poste.situacao, theme_style=ft.TextThemeStyle.TITLE_MEDIUM))]),
                ft.DataRow(cells=[ft.DataCell(ft.Text(value="Tipo de Lâmpada", theme_style=ft.TextThemeStyle.TITLE_LARGE)),
                                  ft.DataCell(ft.Text(value=poste.tipo, theme_style=ft.TextThemeStyle.TITLE_MEDIUM))]),
                ft.DataRow(cells=[ft.DataCell(ft.Text(value="Pontos", theme_style=ft.TextThemeStyle.TITLE_LARGE)),
                                  ft.DataCell(ft.Text(value=poste.pontos, theme_style=ft.TextThemeStyle.TITLE_MEDIUM))]),
                ft.DataRow(cells=[ft.DataCell(ft.Text(value="Bairro", theme_style=ft.TextThemeStyle.TITLE_LARGE)),
                                  ft.DataCell(ft.Text(value=poste.bairro, theme_style=ft.TextThemeStyle.TITLE_MEDIUM))]),
                ft.DataRow(cells=[ft.DataCell(ft.Text(value="Logradouro", theme_style=ft.TextThemeStyle.TITLE_LARGE)),
                                  ft.DataCell(ft.Text(value=poste.logradouro, theme_style=ft.TextThemeStyle.TITLE_MEDIUM))]),
            ],
        ),
        theme=theme1,
    )
    return forms


# Função que cria o botão de ordem de serviço
def btn_ordem(btn3_action):
    ordem = ft.Container(
        alignment=ft.alignment.center,
        col=6,
        padding=15,
        content=ft.ElevatedButton(
            text="Abrir chamado",
            bgcolor=ft.colors.GREEN,
            color=ft.colors.WHITE,
            on_click=btn3_action,
        )
    )
    return ordem


# Função que cria o botão de envio
def btn_send(btn4_action):
    ordem = ft.Container(
        col=6,
        padding=20,
        content=ft.ElevatedButton(
            text="Enviar ordem",
            bgcolor=ft.colors.GREEN,
            color=ft.colors.WHITE,
            on_click=btn4_action,
        )
    )
    return ordem


# Função que cria o botão de retorno ao formulário
def btn_back_forms(btn5_action):
    ordem = ft.Container(
        col=6,
        padding=20,
        content=ft.ElevatedButton(
            text="Voltar",
            bgcolor=ft.colors.AMBER,
            color=ft.colors.WHITE,
            on_click=btn5_action,
        )
    )
    return ordem


# Função que cria o botão de retorno a Home
def btn_back_home(btn6_action):
    ordem = ft.Container(
        alignment=ft.alignment.center,
        padding=5,
        col=6,
        expand=True,
        content=ft.ElevatedButton(
            text="       Voltar       ",
            bgcolor=ft.colors.AMBER,
            color=ft.colors.WHITE,
            on_click=btn6_action,
        )
    )
    return ordem


#Função que cria o texto de envio
def send_text(e, page):
    texto = ft.Text(
    value="Ordem enviada com sucesso",
    text_align=ft.TextAlign.CENTER,
    size=30,
    color=ft.colors.GREEN,
    weight=ft.FontWeight.W_400,   
    )
  
    page.add(texto)
    page.update()  # Atualiza a página
    page.scroll_to(9999)

    
#Função que cria o menu lateral
def create_menu(page):
    def logout(e):
        page.go("/login") 

    return ft.Column(
                controls=[
                    ft.Container(
                        width=50,
                        height=50,
                        alignment=ft.alignment.center,
                        bgcolor=ft.colors.BLUE_900,
                        border_radius=ft.border_radius.all(25),
                        padding=0,
                        content=(
                            ft.PopupMenuButton(
                                icon=ft.icons.MENU,
                                icon_color=ft.colors.AMBER,
                                bgcolor=ft.colors.BLUE_900,
                                items=[ft.PopupMenuItem(
                                    on_click=logout,
                                    content=(
                                        ft.Text(value="Deslogar", color = ft.colors.AMBER)
                                    )  
                                )]
                            )
                        )
                    )
                ]
            )


def get_image_url(name):
    SUPABASE_URL = "https://ipyhpxhsmyzzkvucdonu.supabase.co"
    SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImlweWhweGhzbXl6emt2dWNkb251Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3Mjc1NjQ3NDIsImV4cCI6MjA0MzE0MDc0Mn0.qA9H-UyAEx2OgihW1d_i2IjqQ5HTt1e4ITr52J5qRsA"
    TABLE_NAME = "assets_geopostes"
    COLUMN_NAME = name

    headers = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}",
    }
    
    # Faz a requisição GET para buscar pela coluna 'nome'
    response = requests.get(f"{SUPABASE_URL}/rest/v1/{TABLE_NAME}?nome=eq.{COLUMN_NAME}", headers=headers)
    
    if response.status_code == 200 and response.json():
        # Pegando a URL da imagem a partir da coluna 'imagem_url'
        image_url = response.json()[0]["imagem_url"]
        return image_url
    else:
        print("Erro ao buscar a imagem.")
        return None














# Função que carrega a página de formulario
def page_forms(e, page, poste, foto):
   
    box_1.value=False
    box_2.value=False
    box_3.value=False
    box_4.value=False
    box_5.value=False
    box_6.value=False
    text_field_order.controls[0].content.value = ""

    # Limpa a página atual
    page.clean()

    # Cria o novo layout com forms, foto e ordem
    novo_layout = create_page_forms(poste, page, foto)

    # Adiciona o novo layout à página
    page.add(novo_layout)

    page.go("/form")

    # Atualiza a página
    page.update()

    page.scroll_to(9999)


# Função que carrega a página ordem de serviço
def page_ordem(e, poste, page, foto):
    # Limpa a página atual
    page.clean()

    novo_layout = create__page_ordem(poste, page, foto)

    # Adiciona o novo layout à página
    page.add(novo_layout)

    page.go("/order")

    # Atualiza a página
    page.update()
    page.scroll_to(1)








# Função que cria a página de home
def create_page_home(page):

    imagem1 = "titulo_geopostes"
    titulo = get_image_url(imagem1)

    geopostes = ft.Image(
    src=titulo,
    repeat=ft.ImageRepeat.NO_REPEAT,
    height=120,
    )

    home_title = ft.Container(
        visible=True,
        col=12,
        alignment=ft.alignment.center,
        padding=0,
        content=ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=0,
            controls=[
                geopostes,
            ]
        )
    )


    imagem2 = "icone_facens"
    icone = get_image_url(imagem2)

    facens = ft.Image(
    src=icone,
    repeat=ft.ImageRepeat.NO_REPEAT,
    height=70,
    )

    facens_icon = ft.Container(
        visible=True,
        col=12,
        alignment=ft.alignment.center,
        content=ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=0,
            controls=[
                facens 
            ]
        )
    )


    imagem3 = "poste1"
    poste1_url = get_image_url(imagem3)

    poste1_img = ft.Image(
    src=poste1_url,
    repeat=ft.ImageRepeat.NO_REPEAT,
    height=400,
    )

    foto1= ft.Container(
        col=12,
        padding=0,
        content=ft.Column(
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Divider(height=10, thickness=0.1, color=ft.colors.BLACK),
                ft.Text(value="Foto", theme_style=ft.TextThemeStyle.TITLE_LARGE),
                poste1_img, 
            ]
        ),
        theme=theme1,)
    

    imagem4 = "poste2"
    poste2_url = get_image_url(imagem4)

    poste2_img = ft.Image(
    src=poste2_url,
    repeat=ft.ImageRepeat.NO_REPEAT,
    height=400,
    )

    foto2= ft.Container(
        col=12,
        padding=0,
        content=ft.Column(
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Divider(height=10, thickness=0.1, color=ft.colors.BLACK),
                ft.Text(value="Foto", theme_style=ft.TextThemeStyle.TITLE_LARGE),
                poste2_img, 
            ]
        ),
        theme=theme1,)


    menu = create_menu(page)
    mapa = create_mapa(
        page,
        btn1_action=lambda e: page_forms(e, page, poste, foto1),
        btn2_action=lambda e: page_forms(e, page, poste2, foto2),
    )
    container1 = ft.Container(padding=10)
    container2 = ft.Container(padding=5)
    return ft.ResponsiveRow(
        columns=12,
        controls=[menu, home_title, mapa, container2, texto_chamada, container1, facens_icon],
        alignment=ft.MainAxisAlignment.CENTER,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
    )


# Função para criar a página de formulario
def create_page_forms(poste, page, foto):
    return ft.ResponsiveRow(
        columns=12,
        controls=[
            create_forms(poste),  # Carregar o formulário
            foto,  # Carregar a foto
            btn_ordem(btn3_action=lambda e: page_ordem(e, poste, page, foto)),
            btn_back_home(btn6_action=lambda e: page.go("/"))   
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
    )
 

# Função para criar a página de ordem de serviço
def create__page_ordem(poste, page, foto):
    container1 = ft.Container(padding=10)
    return ft.ResponsiveRow(
        columns=12,
        controls=[
            container1,
            create_titulo_2(poste),  # Carregar o titulo
            chamda_ordem,
            box_1,
            box_2,
            box_3,
            box_4,
            box_5,
            box_6,
            text_field_order,
            btn_send(btn4_action=lambda e: send_text(e, e.page)),
            btn_back_forms(btn5_action=lambda e: page_forms(e, page, poste, foto))  
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
    )


# Função para criar a página de login
def create_page_login(page):

    imagem1 = "titulo_geopostes"
    titulo = get_image_url(imagem1)

    geopostes = ft.Image(
    src=titulo,
    repeat=ft.ImageRepeat.NO_REPEAT,
    height=120,
    )

    home_title = ft.Container(
        visible=True,
        col=12,
        alignment=ft.alignment.center,
        padding=0,
        content=ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=0,
            controls=[
                geopostes,
            ]
        )
    )

    imagem2 = "icone_facens"
    icone = get_image_url(imagem2)

    facens = ft.Image(
    src=icone,
    repeat=ft.ImageRepeat.NO_REPEAT,
    height=70,
    )

    facens_icon = ft.Container(
        visible=True,
        col=12,
        alignment=ft.alignment.center,
        content=ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=0,
            controls=[
                facens 
            ]
        )
    )


    username_field = username
    password_field = password

    container1 = ft.Container(
      padding=10
    )
    container2 = ft.Container(
      padding=50
    )

    return ft.ResponsiveRow(
        columns=12,
        controls=[
            container1,
            home_title,
            container1,  
            username,  
            password,
            container1,
            btn_login(username_field, password_field, page),
            btn_register(register_action=lambda e: page.go("/register")), 
            container2,
            facens_icon,
             
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
    )


# Função para criar a página de registro
def create_page_register(page):

    imagem1 = "titulo_geopostes"
    titulo = get_image_url(imagem1)

    geopostes = ft.Image(
    src=titulo,
    repeat=ft.ImageRepeat.NO_REPEAT,
    height=120,
    )

    home_title = ft.Container(
        visible=True,
        col=12,
        alignment=ft.alignment.center,
        padding=0,
        content=ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=0,
            controls=[
                geopostes,
            ]
        )
    )

    imagem2 = "icone_facens"
    icone = get_image_url(imagem2)

    facens = ft.Image(
    src=icone,
    repeat=ft.ImageRepeat.NO_REPEAT,
    height=70,
    )

    facens_icon = ft.Container(
        visible=True,
        col=12,
        alignment=ft.alignment.center,
        content=ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=0,
            controls=[
                facens 
            ]
        )
    )



    username_field = username_register
    email_field = email_register
    number_field = number_register
    password_field = password_register

    container1 = ft.Container(
      padding=10
    )
    container2 = ft.Container(
      padding=50
    )

    return ft.ResponsiveRow(
        columns=12,
        controls=[
            container1,
            home_title, 
            container1, 
            username_register, 
            email_register,
            number_register, 
            password_register,
            container1,
            btn_register_2(username_field, email_field, number_field, password_field, page),
            btn_back(action_back=lambda e: page.go("/login")),
            container2,
            facens_icon,


             
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
    )