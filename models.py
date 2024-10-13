import flet as ft
import requests
import threading

class Poste:
    def __init__(self, ip, situacao, tipo, pontos, bairro, logradouro):
        self.ip = ip
        self.situacao = situacao
        self.tipo = tipo
        self.pontos = pontos
        self.bairro = bairro
        self.logradouro = logradouro


class TextTheme:

    def __init__(self):
        None

    def create_text_theme1(self):
        
        return ft.Theme(
        text_theme=ft.TextTheme(
            title_large=ft.TextStyle(
                size=15,
                color=ft.colors.BLACK,
                weight=ft.FontWeight.W_900,
            ),
            title_medium=ft.TextStyle(
                size=15,
                color=ft.colors.BLACK,
                weight=ft.FontWeight.W_400,
            ),
            )
        )


class Buttons:
    
    def __init__(self, page):
        self.page = page
    
    # Método base para criar os botões
    def create_button(self, on_click, text, color, col, padding):
        return ft.Column(
            horizontal_alignment = ft.CrossAxisAlignment.CENTER,
            col=col,
            controls=[
                    ft.Container(
                            alignment=ft.alignment.center,
                            col=col,
                            padding=padding,
                            expand=True,
                            content=ft.ElevatedButton(
                                text=text,
                                bgcolor=color,
                                color=ft.colors.WHITE,
                                on_click=on_click,
                                width=150,
                            )
                        )
                    ]    
                 )
    
    def create_point_button(self, on_click, text):
        return ft.Column(
                spacing=0,
                controls=[
                    ft.ElevatedButton(
                        on_click=on_click,
                        width=20,
                        height=20,
                        bgcolor=ft.colors.AMBER,
                        text=" ",
                        style=ft.ButtonStyle(
                            shape=ft.RoundedRectangleBorder(radius=10),
                        ),
                    ),
                    ft.Text(
                        value=text,
                        color=ft.colors.BLACK,
                        size=20,
                        text_align=ft.TextAlign.START,
                        weight=ft.FontWeight.BOLD,
                        visible=True,
                        )
                ]
            )


class Web_Image:

    def __init__(self, page):
        self.page = page

    def get_image_url(self, name):
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


    def create_web_image(self, src, col, height):
        return ft.Container(
                visible=True,
                col=col,
                alignment=ft.alignment.center,
                padding=0,
                content=ft.Row(
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=0,
                    controls=[
                        ft.Image(
                        src=src,
                        repeat=ft.ImageRepeat.NO_REPEAT,
                        height=height,
                        ),
                    ]
                )
            )    


class CallText:

    def __init__(self, page):
        self.page = page

    
    def create_calltext(self, text, color, size, font, col, padding):

        textthemes = TextTheme()
        texttheme1 = textthemes.create_text_theme1()

        return  ft.Container(
            visible=True,
            col=col,
            padding=padding,
            content=ft.Text(
                value=text,
                text_align=ft.TextAlign.CENTER,
                size=size,
                color=color,
                weight=font,
            ),
            theme=texttheme1,
        )
    
    def create_container_calltext1(self):

        buttons = Buttons(self.page)
        btn_null = buttons.create_point_button(on_click=None, text=None)
        btn_null.controls[1].visible = False

        return  ft.Column(
                col=10,
                spacing=10,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[ ft.Container(
                            visible=True,
                            padding=10,
                            col=7,
                            bgcolor=ft.colors.BLUE_900,
                            border_radius=10,
                            content=ft.Column(    
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER, 
                            controls=[
                            ft.Row(
                            alignment=ft.MainAxisAlignment.CENTER,
                            wrap=True,    
                            controls=[  
                            ft.Text(
                                    text_align=ft.TextAlign.CENTER,
                                    value="No mapa acima, clique em um",
                                    color=ft.colors.WHITE,
                                    size=15,
                                    weight=ft.FontWeight.W_600,
                                    font_family="Tahoma",
                                    ),]),
                            ft.Row(
                            alignment=ft.MainAxisAlignment.CENTER,      
                            controls=[  
                            ft.Text(
                                    text_align=ft.TextAlign.CENTER,
                                    value="Ponto de poste:",
                                    color=ft.colors.WHITE,
                                    size=15,
                                    weight=ft.FontWeight.W_600,
                                    font_family="Tahoma",
                                    ),btn_null]),

                                    ])
                        )
                        ]
                        )
    
    def create_container_calltext2(self, text):

        return ft.Column(
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        controls=[ ft.Container(
                    visible=True,
                    padding=10,
                    col=12,
                    bgcolor=ft.colors.BLUE_700,
                    border_radius=10,
                    content= ft.Text(
                            value=text,
                            color=ft.colors.WHITE,
                            size=40,
                            weight=ft.FontWeight.W_600,
                            font_family="Tahoma",
                            ),)
                ]
                )
        

class CheckBox:

    def __init__(self, page):
        self.page = page


    def create_checkbox(self, text, size, on_change, col):

        return ft.Column(
            horizontal_alignment = ft.CrossAxisAlignment.START,
            col=col,
            controls=[
                ft.Checkbox(
                    label=text,
                    on_change=on_change,
                    label_style=ft.TextStyle(
                        color=ft.colors.BLACK,
                        size=size,    
                        )
                    )
            ]
        )


class TextField:

    def __init__(self, page):
        self.page = page


    def create_textfield(self, text, password):

        return  ft.TextField(
            label= text,
            password=password,
            label_style= ft.TextStyle(color=ft.colors.BLACK),
            text_style= ft.TextStyle(color=ft.colors.BLACK),
            col=8
            )
    
    def create_description_textfield(self, text):

        return  ft.Column(
                controls=[
                    ft.Container(
                        col=12,
                        alignment=ft.alignment.center,
                        content=ft.TextField(
                            label=text,
                            text_align=ft.TextAlign.CENTER,
                            min_lines=3,
                            label_style=ft.TextStyle(size=20),
                            text_style=ft.TextStyle(color=ft.colors.BLACK),
                            )
                        )
                    ]
                )


class SettingsMenu:

    def __init__(self, page):
        self.page = page


    def itens_settings_menu(self, text, color, action):

        return ft.PopupMenuItem(
                on_click=action,
                content=(
                    ft.Text(value=text, color=color)
                ))

    def create_settings_menu(self, color, itens):

        return ft.Column(
                controls=[
                    ft.Container(
                        width=50,
                        height=50,
                        alignment=ft.alignment.center,
                        bgcolor=color,
                        border_radius=ft.border_radius.all(25),
                        padding=0,
                        content=(
                            ft.PopupMenuButton(
                                icon=ft.icons.MENU,
                                icon_color=ft.colors.AMBER,
                                bgcolor=ft.colors.BLUE_900,
                                items=itens
                            )
                        )
                    )
                ]
            )    


class Forms:

    def __init__(self, page):
        self.page = page

    def create_forms(self, poste):

        textthemes = TextTheme()
        texttheme1 = textthemes.create_text_theme1()

        return ft.Container(
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
        theme=texttheme1,
    )


class Map:

    def __init__(self, page):
        self.page = page

    def create_map(self, page, btn1_action, btn2_action):

        buttons = Buttons(page)
        btn1 = buttons.create_point_button(on_click=btn1_action, text="10")
        btn2 = buttons.create_point_button(on_click=btn2_action, text="20")


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

        web_images = Web_Image(page)
        url_imagem1 = web_images.get_image_url(name="mapa")
        home_map = url_imagem1 
        url_imagem2 = web_images.get_image_url(name="seta")
        home_seta = web_images.create_web_image(src=url_imagem2, col=None, height=70)

        return ft.Column(
            visible=True,
            col=12,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[ft.Container(
                width=400,
                height=400,
                alignment=ft.alignment.center,
                image_src=home_map,
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
                            controls=[btn1, home_seta, btn2]  # seta importada do models.py
                        ),
                    ],
                )
            )]
        )


class LoadingPages:

    def __init__(self, page):
        self.page = page

    def new_loading_page(self, page, layout):

        page.clean()

        page.add(layout)

        page.update()

        page.scroll_to(1)    

