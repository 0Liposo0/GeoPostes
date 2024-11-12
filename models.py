import flet as ft
import requests
import flet.map as map
import threading



class Poste:

    def __init__(self, number, ip, situacao, tipo, pontos, bairro, logradouro, lat, long):
        self.number = number
        self.ip = ip
        self.situacao = situacao
        self.tipo = tipo
        self.pontos = pontos
        self.bairro = bairro
        self.logradouro = logradouro
        self.lat = lat
        self.long = long


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
    def create_button(self, on_click, text, color, col, padding, width=150):
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
                                width=width,
                            )
                        )
                    ]    
                 )

    
    def create_call_location_button(self, icon, on_click, color, col, padding, icon_color=ft.colors.RED):
        return ft.Column(
            col=col,
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[
                    ft.Container(
                            alignment=ft.alignment.center,
                            col=col,
                            width=50,
                            height=50,
                            border_radius=ft.border_radius.all(25),
                            padding=padding,
                            bgcolor=color,
                            content=ft.IconButton(
                                icon=icon,
                                icon_color=icon_color,
                                on_click=on_click,
                            )
                        )
                    ]    
                 )

    def create_icon_button(self, icon, on_click, color, col, padding, icon_color):
        return ft.Column(
            col=col,
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[
                    ft.Container(
                            alignment=ft.alignment.center,
                            col=col,
                            width=40,
                            height=40,
                            border_radius=ft.border_radius.all(20),
                            padding=padding,
                            bgcolor=color,
                            content=ft.IconButton(
                                icon=icon,
                                icon_color=icon_color,
                                on_click=on_click,
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
                        no_wrap=True,
                        color=ft.colors.BLACK,
                        size=20,
                        text_align=ft.TextAlign.START,
                        weight=ft.FontWeight.BOLD,
                        visible=True,
                        )
                ]
            )
    
    def create_location_button(self):
        return ft.Column(
                spacing=0,
                controls=[
                    ft.ElevatedButton(
                        on_click=None,
                        width=20,
                        height=20,
                        bgcolor=ft.colors.BLUE,
                        text="",
                        style=ft.ButtonStyle(
                            shape=ft.RoundedRectangleBorder(radius=10),
                        ),
                    ),
                ]
            )
    
    def create_point_marker(self, content, x, y):
        return map.Marker(
                content=content,
                coordinates=map.MapLatitudeLongitude(x, y),
                rotate=True, 
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
        

    def get_poste_image_url(self, numero):
        SUPABASE_URL = "https://ipyhpxhsmyzzkvucdonu.supabase.co"
        SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImlweWhweGhzbXl6emt2dWNkb251Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3Mjc1NjQ3NDIsImV4cCI6MjA0MzE0MDc0Mn0.qA9H-UyAEx2OgihW1d_i2IjqQ5HTt1e4ITr52J5qRsA"


        headers = {
            "apikey": SUPABASE_KEY,
            "Authorization": f"Bearer {SUPABASE_KEY}",
        }
        
        # Faz a requisição GET para buscar pela coluna 'number'
        response = requests.get(f"{SUPABASE_URL}/rest/v1/points_capeladoalto?number=eq.{numero}", headers=headers)
        
        if response.status_code == 200 and response.json():
            # Pegando a URL da imagem a partir da coluna 'url'
            image_url = response.json()[0]["url"]
            return image_url
        else:
            print("Erro ao buscar a imagem.")
            return None


    def create_web_image(self, src):

        return ft.Image(src=src, repeat=None)


class CallText:

    def __init__(self, page):
        self.page = page

    
    def create_calltext(self, text, color, size, font, col, padding, visible):

        textthemes = TextTheme()
        texttheme1 = textthemes.create_text_theme1()

        return  ft.Container(
            visible=visible,
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
                col=12,
                spacing=10,
                horizontal_alignment=ft.CrossAxisAlignment.START,
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


    def create_checkbox(self, text, size, on_change, col, data=None):

        return ft.Column(
            horizontal_alignment = ft.CrossAxisAlignment.START,
            col=col,
            controls=[
                ft.Checkbox(
                    label=text,
                    data = data,
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


    def create_textfield(self,value, text, password):

        return  ft.TextField(
            value=value,
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

    def create_settings_menu(self, color, col, action):

        return ft.Column(
                col=col,
                alignment=ft.MainAxisAlignment.CENTER,
                controls=[
                    ft.Container(
                        width=50,
                        height=50,
                        alignment=ft.alignment.center,
                        bgcolor=color,
                        border_radius=ft.border_radius.all(25),
                        padding=0,
                        content=(
                            ft.IconButton(
                                icon=ft.icons.MENU,
                                icon_color=ft.colors.BLUE,
                                bgcolor=ft.colors.WHITE,
                                on_click=action,
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
            theme=texttheme1,  
            content=ft.DataTable(
                data_row_max_height=50,
                columns=[
                    ft.DataColumn(ft.Text(value="")),  
                    ft.DataColumn(ft.Text(value="")),  
                ],
                rows=[
                    ft.DataRow(cells=[
                        ft.DataCell(ft.Text(value="Latitude", theme_style=ft.TextThemeStyle.TITLE_LARGE)),
                        ft.DataCell(
                            ft.Container(content=ft.Text(value=poste.lat, theme_style=ft.TextThemeStyle.TITLE_MEDIUM), width=200)
                        )
                    ]),
                    ft.DataRow(cells=[
                        ft.DataCell(ft.Text(value="Longitude", theme_style=ft.TextThemeStyle.TITLE_LARGE)),
                        ft.DataCell(
                            ft.Container(content=ft.Text(value=poste.long, theme_style=ft.TextThemeStyle.TITLE_MEDIUM), width=200)
                        )
                    ]),
                    ft.DataRow(cells=[
                        ft.DataCell(ft.Text(value="IP", theme_style=ft.TextThemeStyle.TITLE_LARGE)),
                        ft.DataCell(
                            ft.Container(content=ft.Text(value=poste.ip, theme_style=ft.TextThemeStyle.TITLE_MEDIUM), width=200)
                        )
                    ]),
                    ft.DataRow(cells=[
                        ft.DataCell(ft.Text(value="Situação", theme_style=ft.TextThemeStyle.TITLE_LARGE)),
                        ft.DataCell(
                            ft.Container(content=ft.Text(value=poste.situacao, theme_style=ft.TextThemeStyle.TITLE_MEDIUM), width=200)
                        )
                    ]),
                    ft.DataRow(cells=[
                        ft.DataCell(ft.Text(value="Tipo de Lâmpada", theme_style=ft.TextThemeStyle.TITLE_LARGE)),
                        ft.DataCell(
                            ft.Container(content=ft.Text(value=poste.tipo, theme_style=ft.TextThemeStyle.TITLE_MEDIUM), width=200)
                        )
                    ]),
                    ft.DataRow(cells=[
                        ft.DataCell(ft.Text(value="Pontos", theme_style=ft.TextThemeStyle.TITLE_LARGE)),
                        ft.DataCell(
                            ft.Container(content=ft.Text(value=poste.pontos, theme_style=ft.TextThemeStyle.TITLE_MEDIUM), width=200)
                        )
                    ]),
                    ft.DataRow(cells=[
                        ft.DataCell(ft.Text(value="Bairro", theme_style=ft.TextThemeStyle.TITLE_LARGE)),
                        ft.DataCell(
                            ft.Container(content=ft.Text(value=poste.bairro, theme_style=ft.TextThemeStyle.TITLE_MEDIUM), width=200)
                        )
                    ]),
                    ft.DataRow(cells=[
                        ft.DataCell(ft.Text(value="Logradouro", theme_style=ft.TextThemeStyle.TITLE_LARGE)),
                        ft.DataCell(
                            ft.Container(content=ft.Text(value=poste.logradouro, theme_style=ft.TextThemeStyle.TITLE_MEDIUM), width=200)
                        )
                    ]),
                ],
            ),
        )
    

    def create_os_forms(self, data_criacao, ip, reclamante, function, celular, ordem, origem, obser, materiais, ponto, status, data_andamen, data_conclu, equipe):

        textthemes = TextTheme()
        texttheme1 = textthemes.create_text_theme1()

        return ft.Container(
            padding=0,
            col=12,
            theme=texttheme1,  
            content=ft.DataTable(
                data_row_max_height=50,
                columns=[
                    ft.DataColumn(ft.Text(value="")),  
                    ft.DataColumn(ft.Text(value="")),  
                ],
                rows=[
                    ft.DataRow(cells=[
                        ft.DataCell(ft.Text(value="Criação", theme_style=ft.TextThemeStyle.TITLE_LARGE)),
                        ft.DataCell(
                            ft.Container(content=ft.Text(value=data_criacao, theme_style=ft.TextThemeStyle.TITLE_MEDIUM), width=200)
                        )
                    ]),
                    ft.DataRow(cells=[
                        ft.DataCell(ft.Text(value="IP", theme_style=ft.TextThemeStyle.TITLE_LARGE)),
                        ft.DataCell(
                            ft.Container(content=ft.Text(value=ip, theme_style=ft.TextThemeStyle.TITLE_MEDIUM), width=200)
                        )
                    ]),
                    ft.DataRow(cells=[
                        ft.DataCell(ft.Text(value="Reclamante", theme_style=ft.TextThemeStyle.TITLE_LARGE)),
                        ft.DataCell(
                            ft.Container(content=ft.Text(value=reclamante, theme_style=ft.TextThemeStyle.TITLE_MEDIUM), width=200)
                        )
                    ]),
                    ft.DataRow(cells=[
                        ft.DataCell(ft.Text(value="Usuário", theme_style=ft.TextThemeStyle.TITLE_LARGE)),
                        ft.DataCell(
                            ft.Container(content=ft.Text(value=function, theme_style=ft.TextThemeStyle.TITLE_MEDIUM), width=200)
                        )
                    ]),
                    ft.DataRow(cells=[
                        ft.DataCell(ft.Text(value="Celular", theme_style=ft.TextThemeStyle.TITLE_LARGE)),
                        ft.DataCell(
                            ft.Container(content=ft.Text(value=celular, theme_style=ft.TextThemeStyle.TITLE_MEDIUM), width=200)
                        )
                    ]),
                    ft.DataRow(cells=[
                        ft.DataCell(ft.Text(value="Ordem", theme_style=ft.TextThemeStyle.TITLE_LARGE)),
                        ft.DataCell(
                            ft.Container(content=ft.Text(value=ordem, theme_style=ft.TextThemeStyle.TITLE_MEDIUM), width=200)
                        )
                    ]),
                    ft.DataRow(cells=[
                        ft.DataCell(ft.Text(value="Origem", theme_style=ft.TextThemeStyle.TITLE_LARGE)),
                        ft.DataCell(
                            ft.Container(content=ft.Text(value=origem, theme_style=ft.TextThemeStyle.TITLE_MEDIUM), width=200)
                        )
                    ]),
                    ft.DataRow(cells=[
                        ft.DataCell(ft.Text(value="Observação", theme_style=ft.TextThemeStyle.TITLE_LARGE)),
                        ft.DataCell(
                            ft.Container(content=ft.Text(value=obser, theme_style=ft.TextThemeStyle.TITLE_MEDIUM), width=200)
                        )
                    ]),
                    ft.DataRow(cells=[
                        ft.DataCell(ft.Text(value="Materiais", theme_style=ft.TextThemeStyle.TITLE_LARGE)),
                        ft.DataCell(
                            ft.Container(content=ft.Text(value=materiais, theme_style=ft.TextThemeStyle.TITLE_MEDIUM), width=200)
                        )
                    ]),
                    ft.DataRow(cells=[
                        ft.DataCell(ft.Text(value="Ponto", theme_style=ft.TextThemeStyle.TITLE_LARGE)),
                        ft.DataCell(
                            ft.Container(content=ft.Text(value=ponto, theme_style=ft.TextThemeStyle.TITLE_MEDIUM), width=200)
                        )
                    ]),
                    ft.DataRow(cells=[
                        ft.DataCell(ft.Text(value="Status", theme_style=ft.TextThemeStyle.TITLE_LARGE)),
                        ft.DataCell(
                            ft.Container(content=ft.Text(value=status, theme_style=ft.TextThemeStyle.TITLE_MEDIUM), width=200)
                        )
                    ]),
                    ft.DataRow(cells=[
                        ft.DataCell(ft.Text(value="Data do andamento", theme_style=ft.TextThemeStyle.TITLE_LARGE)),
                        ft.DataCell(
                            ft.Container(content=ft.Text(value=data_andamen, theme_style=ft.TextThemeStyle.TITLE_MEDIUM), width=200)
                        )
                    ]),
                    ft.DataRow(cells=[
                        ft.DataCell(ft.Text(value="Data da conclusão", theme_style=ft.TextThemeStyle.TITLE_LARGE)),
                        ft.DataCell(
                            ft.Container(content=ft.Text(value=data_conclu, theme_style=ft.TextThemeStyle.TITLE_MEDIUM), width=200)
                        )
                    ]),
                    ft.DataRow(cells=[
                        ft.DataCell(ft.Text(value="Equipe", theme_style=ft.TextThemeStyle.TITLE_LARGE)),
                        ft.DataCell(
                            ft.Container(content=ft.Text(value=equipe, theme_style=ft.TextThemeStyle.TITLE_MEDIUM), width=200)
                        )
                    ]),
                ],
            ),
        )


    def create_add_forms(self, lat, long, ip, situ, tipo, pontos, bairro, logra):

        textthemes = TextTheme()
        texttheme1 = textthemes.create_text_theme1()

        textfields = TextField(self.page)
        latitude_field = textfields.create_textfield(value=lat, text=None, password=False)
        longitude_field = textfields.create_textfield(value=long, text=None, password=False)
        ip_field = textfields.create_textfield(value=ip, text=None, password=False)
        situacao_field = textfields.create_textfield(value=situ, text=None, password=False)
        tipo_field = textfields.create_textfield(value=tipo, text=None, password=False)
        pontos_field = textfields.create_textfield(value=pontos, text=None, password=False)
        bairro_field = textfields.create_textfield(value=bairro, text=None, password=False)
        logradouro_field = textfields.create_textfield(value=logra, text=None, password=False)

        return ft.Container(
            padding=0,
            col=12,
            theme=texttheme1,
            content=ft.DataTable(
                data_row_max_height=50,
                columns=[
                    ft.DataColumn(ft.Text(value="")),  # Primeira coluna
                    ft.DataColumn(ft.Text(value="")),  # Segunda coluna
                ],
                rows=[
                    ft.DataRow(cells=[
                        ft.DataCell(ft.Text(value="Latitude", theme_style=ft.TextThemeStyle.TITLE_LARGE)),
                        ft.DataCell(
                            ft.Container(content=latitude_field, width=200)  # Ajuste da largura
                        )
                    ]),
                    ft.DataRow(cells=[
                        ft.DataCell(ft.Text(value="Longitude", theme_style=ft.TextThemeStyle.TITLE_LARGE)),
                        ft.DataCell(
                            ft.Container(content=longitude_field, width=200)
                        )
                    ]),
                    ft.DataRow(cells=[
                        ft.DataCell(ft.Text(value="IP", theme_style=ft.TextThemeStyle.TITLE_LARGE)),
                        ft.DataCell(
                            ft.Container(content=ip_field, width=200)
                        )
                    ]),
                    ft.DataRow(cells=[
                        ft.DataCell(ft.Text(value="Situação", theme_style=ft.TextThemeStyle.TITLE_LARGE)),
                        ft.DataCell(
                            ft.Container(content=situacao_field, width=200)
                        )
                    ]),
                    ft.DataRow(cells=[
                        ft.DataCell(ft.Text(value="Tipo de Lâmpada", theme_style=ft.TextThemeStyle.TITLE_LARGE)),
                        ft.DataCell(
                            ft.Container(content=tipo_field, width=200)
                        )
                    ]),
                    ft.DataRow(cells=[
                        ft.DataCell(ft.Text(value="Pontos", theme_style=ft.TextThemeStyle.TITLE_LARGE)),
                        ft.DataCell(
                            ft.Container(content=pontos_field, width=200)
                        )
                    ]),
                    ft.DataRow(cells=[
                        ft.DataCell(ft.Text(value="Bairro", theme_style=ft.TextThemeStyle.TITLE_LARGE)),
                        ft.DataCell(
                            ft.Container(content=bairro_field, width=200)
                        )
                    ]),
                    ft.DataRow(cells=[
                        ft.DataCell(ft.Text(value="Logradouro", theme_style=ft.TextThemeStyle.TITLE_LARGE)),
                        ft.DataCell(
                            ft.Container(content=logradouro_field, width=200)
                        )
                    ]),
                ],
            ),
        )


    def create_add_os_forms(self, list_os_forms):

        textthemes = TextTheme()
        texttheme1 = textthemes.create_text_theme1()

        textfields = TextField(self.page)
        data_cria_field = textfields.create_textfield(value=list_os_forms[0], text=None, password=False)
        ip_field = textfields.create_textfield(value=list_os_forms[1], text=None, password=False)
        reclamante_field = textfields.create_textfield(value=list_os_forms[2], text=None, password=False)
        usuario_field = textfields.create_textfield(value=list_os_forms[3], text=None, password=False)
        celular_field = textfields.create_textfield(value=list_os_forms[4], text=None, password=False)
        order_field = textfields.create_textfield(value=list_os_forms[5], text=None, password=False)
        origem_field = textfields.create_textfield(value=list_os_forms[6], text=None, password=False)
        observ_field = textfields.create_textfield(value=list_os_forms[7], text=None, password=False)
        materi_field = textfields.create_textfield(value=list_os_forms[8], text=None, password=False)
        pontos_field = textfields.create_textfield(value=list_os_forms[9], text=None, password=False)
        status_field = textfields.create_textfield(value=list_os_forms[10], text=None, password=False)
        data_andamen_field = textfields.create_textfield(value=list_os_forms[11], text=None, password=False)
        data_conclu_field = textfields.create_textfield(value=list_os_forms[12], text=None, password=False)
        equipe_field = textfields.create_textfield(value=list_os_forms[13], text=None, password=False)

        return ft.Container(
            padding=0,
            col=12,
            theme=texttheme1,
            content=ft.DataTable(
                data_row_max_height=50,
                columns=[
                    ft.DataColumn(ft.Text(value="")),  
                    ft.DataColumn(ft.Text(value="")), 
                ],
                rows=[
                    ft.DataRow(cells=[
                        ft.DataCell(ft.Text(value="Data de Criação", theme_style=ft.TextThemeStyle.TITLE_LARGE)),
                        ft.DataCell(
                            ft.Container(content=data_cria_field, width=200)  
                        )
                    ]),
                    ft.DataRow(cells=[
                        ft.DataCell(ft.Text(value="IP", theme_style=ft.TextThemeStyle.TITLE_LARGE)),
                        ft.DataCell(
                            ft.Container(content=ip_field, width=200)  
                        )
                    ]),
                    ft.DataRow(cells=[
                        ft.DataCell(ft.Text(value="Reclamante", theme_style=ft.TextThemeStyle.TITLE_LARGE)),
                        ft.DataCell(
                            ft.Container(content=reclamante_field, width=200)
                        )
                    ]),
                    ft.DataRow(cells=[
                        ft.DataCell(ft.Text(value="Usuário", theme_style=ft.TextThemeStyle.TITLE_LARGE)),
                        ft.DataCell(
                            ft.Container(content=usuario_field, width=200)
                        )
                    ]),
                    ft.DataRow(cells=[
                        ft.DataCell(ft.Text(value="Celular", theme_style=ft.TextThemeStyle.TITLE_LARGE)),
                        ft.DataCell(
                            ft.Container(content=celular_field, width=200)
                        )
                    ]),
                    ft.DataRow(cells=[
                        ft.DataCell(ft.Text(value="Ordem", theme_style=ft.TextThemeStyle.TITLE_LARGE)),
                        ft.DataCell(
                            ft.Container(content=order_field, width=200)
                        )
                    ]),
                    ft.DataRow(cells=[
                        ft.DataCell(ft.Text(value="Origem", theme_style=ft.TextThemeStyle.TITLE_LARGE)),
                        ft.DataCell(
                            ft.Container(content=origem_field, width=200)
                        )
                    ]),
                    ft.DataRow(cells=[
                        ft.DataCell(ft.Text(value="Observação", theme_style=ft.TextThemeStyle.TITLE_LARGE)),
                        ft.DataCell(
                            ft.Container(content=observ_field, width=200)
                        )
                    ]),
                    ft.DataRow(cells=[
                        ft.DataCell(ft.Text(value="Material", theme_style=ft.TextThemeStyle.TITLE_LARGE)),
                        ft.DataCell(
                            ft.Container(content=materi_field, width=200)
                        )
                    ]),
                    ft.DataRow(cells=[
                        ft.DataCell(ft.Text(value="Ponto Queimado", theme_style=ft.TextThemeStyle.TITLE_LARGE)),
                        ft.DataCell(
                            ft.Container(content=pontos_field, width=200)
                        )
                    ]),
                    ft.DataRow(cells=[
                        ft.DataCell(ft.Text(value="Status", theme_style=ft.TextThemeStyle.TITLE_LARGE)),
                        ft.DataCell(
                            ft.Container(content=status_field, width=200)
                        )
                    ]),
                    ft.DataRow(cells=[
                        ft.DataCell(ft.Text(value="Data de Andamento", theme_style=ft.TextThemeStyle.TITLE_LARGE)),
                        ft.DataCell(
                            ft.Container(content=data_andamen_field, width=200)
                        )
                    ]),
                    ft.DataRow(cells=[
                        ft.DataCell(ft.Text(value="Data de Conclusão", theme_style=ft.TextThemeStyle.TITLE_LARGE)),
                        ft.DataCell(
                            ft.Container(content=data_conclu_field, width=200)
                        )
                    ]),
                    ft.DataRow(cells=[
                        ft.DataCell(ft.Text(value="Equipe", theme_style=ft.TextThemeStyle.TITLE_LARGE)),
                        ft.DataCell(
                            ft.Container(content=equipe_field, width=200)
                        )
                    ]),
                ],
            ),
        )


class LoadingPages:

    def __init__(self, page):
        self.page = page

    def new_loading_page(self, page, layout, home=False, anchor=False):

        page.clean()

        page.go("/")

        page.add(layout)

        page.scroll_to(1)

        if home == False:
            page.floating_action_button.visible = False
            page.bottom_appbar.visible = False
            page.appbar.visible = False

        else:
            page.go("/home")
            page.floating_action_button.visible = True
            page.bottom_appbar.visible = True
            page.appbar.visible = True
        
        page.update()

    def first_loading_page(self, page, layout):

        page.clean()

        page.go("/")

        page.add(layout)

        page.scroll_to(1)

        page.update()
 

class GalleryPicker:

    def __init__(self, page, image_temp):

        self.page = page
        self.image_temp = image_temp
        self.fp = ft.FilePicker(on_result=self.on_image_selected) # cria o objeto de seleção de arquivos e adiciona uma chamada de função para quando arquivo for escolhido
        self.page.overlay.append(self.fp) # adiciona o objeto a sebreposição da página


    def open_gallery(self, e):   # e representa o clique do botão que disparou o evento
   
        self.fp.pick_files(               # chama a janela de seleção de arquivos
            allow_multiple=False,
            file_type=ft.FilePickerFileType.IMAGE
        )

    def on_image_selected(self, e: ft.FilePickerResultEvent):

            self.page.snack_bar = ft.SnackBar(
                content=ft.Text(value="Adicionando imagem...", color=ft.colors.BLACK),
                duration=2000,
                bgcolor=ft.colors.AMBER,
            )
            self.page.snack_bar.open = True

            selected_image = e.files[0]
            print(selected_image.path)  

            image_container = ft.Image(src=selected_image.path) 

            self.image_temp.content = image_container 

            self.page.update()


class SupaBase:

    def __init__(self, page):
        self.page = page
        self.supabase_url = "https://ipyhpxhsmyzzkvucdonu.supabase.co"
        self.supabase_key = (
            "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImlweWhweGhzbXl6emt2dWNkb251Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3Mjc1NjQ3NDIsImV4cCI6MjA0MzE0MDc0Mn0.qA9H-UyAEx2OgihW1d_i2IjqQ5HTt1e4ITr52J5qRsA"
        )


    def add_storage(self, numero, image):
        
        headers = {
            'Authorization': f'Bearer {self.supabase_key}',
            'Content-Type': 'image/jpeg'
        }

        storage_path = f'postes_images_points/postes/{numero}.jpg'

        with open(image.src, 'rb') as file:
            bytes = file.read()


        response = requests.post(
                f'{self.supabase_url}/storage/v1/object/{storage_path}',
                headers=headers,
                data=bytes
            )
        
        if response.status_code == 200:
                print("Imagem enviada com sucesso!")
        else:
            print("Erro ao enviar imagem:", response.json())
            return None
        
    def get_storage(self, numero):

        storage_path = f'postes_images_points/postes/{numero}.jpg'
        public_url = f"{self.supabase_url}/storage/v1/object/public/{storage_path}"
        response = requests.get(public_url)
        if response.status_code == 200:
            print(f"Imagem encontrada: {public_url}")
            return public_url 
        else:
            print(f"Erro ao buscar a imagem: {response.status_code} - {response.text}")
            url = "Nulo"
            return url
        
    def delete_storage(self, numero):

        storage_path = f'postes_images_points/postes/{numero}.jpg'
        url = f"{self.supabase_url}/storage/v1/object/{storage_path}"
        headers = {
            "apikey": self.supabase_key,
            "Authorization": f"Bearer {self.supabase_key}",
            'Content-Type': 'image/jpeg'
        }
        response = requests.delete(
            url,
            headers=headers,
        )

        if response.status_code != 200:
            self.page.snack_bar = ft.SnackBar(
                content=ft.Text("Imagem mantida"),
                bgcolor=ft.colors.AMBER,
                duration=4000,
                behavior=ft.SnackBarBehavior.FLOATING,
            )
            self.page

    def get_login(self, username, password):

        headers = {
            "apikey": self.supabase_key,
            "Authorization": f"Bearer {self.supabase_key}",
            "Content-Type": "application/json",
        }

        params = {
            "or": f"(usuario.eq.{username},email.eq.{username})",
            "senha": f"eq.{password}",
            "select": "*"
        }

        response = requests.get(
            f"{self.supabase_url}/rest/v1/login_geopostes",
            headers=headers,
            params=params,
        )

        return response
    
    def register(self, username, email, number, password1, password2):

        headers = {
            "apikey": self.supabase_key,
            "Authorization": f"Bearer {self.supabase_key}",
            "Content-Type": "application/json",
        }

        response = requests.get(
            f"{self.supabase_url}/rest/v1/login_geopostes",
            headers=headers,
            params={"select": "email", "email": f"eq.{email}"}
        )

        if response.status_code == 200 and response.json():
            # Se o e-mail já existir, mostre a mensagem e retorne
            self.page.snack_bar = ft.SnackBar(
                content=ft.Text("E-mail já cadastrado"),
                bgcolor=ft.colors.RED
            )
            self.page.snack_bar.open = True
            self.page.update()

            return 

        response = requests.get(
            f"{self.supabase_url}/rest/v1/login_geopostes",
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
                f"{self.supabase_url}/rest/v1/login_geopostes",
                headers=headers,
                json=data,
            )

            return response

    def add_point(self, list_forms, image):

        numero = int(list_forms[2].split('-')[1])

        headers = {
            "apikey": self.supabase_key,
            "Authorization": f"Bearer {self.supabase_key}",
            "Content-Type": "application/json",
        }

        response = requests.get(
            f"{self.supabase_url}/rest/v1/points_capeladoalto",
            headers=headers,
            params={"select": "name", "name": f"eq.{list_forms[2]}"}
        )

        if response.status_code == 200 and response.json():
            # Se o ponto já existir, mostre a mensagem e retorne
            self.page.snack_bar = ft.SnackBar(
                content=ft.Text(f"{list_forms[2]} já foi cadastrado, ponto não adicionado"),
                bgcolor=ft.colors.RED
            )
            self.page.snack_bar.open = True
            self.page.update()
            return

        image_url = "Nulo"
        if image != None:

            sp = SupaBase(self.page)
            try:
                sp.add_storage(numero=numero, image=image)
                image_url = sp.get_storage(numero=numero)
            except:
                self.page.snack_bar = ft.SnackBar(
                        content=ft.Text(f"O dispositivo negou acesso a imagem"),
                        bgcolor=ft.colors.AMBER,
                        duration=1000,
                    )
                self.page.snack_bar.open = True

        data = {
            "number": numero,
            "coord_x": list_forms[0],
            "coord_y": list_forms[1],
            "name": list_forms[2],
            "situacao": list_forms[3],
            "tipo": list_forms[4],
            "pontos": list_forms[5],
            "bairro": list_forms[6],
            "logradouro": list_forms[7],
            "url": image_url
        }

        response = requests.post(
            f"{self.supabase_url}/rest/v1/points_capeladoalto",
            headers=headers,
            json=data,
        )

        return response
    
    def add_os(self, list_add_os):

        numero = int(list_add_os[1].split('-')[1])

        headers = {
            "apikey": self.supabase_key,
            "Authorization": f"Bearer {self.supabase_key}",
            "Content-Type": "application/json",
        }

        response = requests.get(
            f"{self.supabase_url}/rest/v1/ordens_postes_capeladoalto",
            headers=headers,
            params={"select": "ordem", "ordem": f"eq.{list_add_os[5]}"}
        )

        if response.status_code == 200 and response.json():
            self.page.snack_bar = ft.SnackBar(
                content=ft.Text(f"{list_add_os[5]} já foi cadastrado, ordem não adicionada"),
                bgcolor=ft.colors.RED
            )
            self.page.snack_bar.open = True
            self.page.update()
            return

        data = {
            "created_at": list_add_os[0],
            "ip": list_add_os[1],
            "numero": numero,
            "reclamante": list_add_os[2],
            "function": list_add_os[3],
            "celular": list_add_os[4],
            "ordem": list_add_os[5],
            "origem": list_add_os[6],
            "observacao": list_add_os[7],
            "materiais": list_add_os[8],
            "ponto": list_add_os[9],
            "status": list_add_os[10],
            "data_andamento": list_add_os[11],
            "data_conclusao": list_add_os[12],
            "equipe": list_add_os[13],
        }

        response = requests.post(
            f"{self.supabase_url}/rest/v1/ordens_postes_capeladoalto",
            headers=headers,
            json=data,
        )

        return response
    
    def edit_point(self, image, list_forms, numero_ant):

        numero = int(list_forms[2].split('-')[1])

        headers = {
            "apikey": self.supabase_key,
            "Authorization": f"Bearer {self.supabase_key}",
            "Content-Type": "application/json",
        }

        image_url = "Nulo"
        sp = SupaBase(self.page)
        if "supabase" in image.src:
            data = {
                "number": numero,
                "coord_x": list_forms[0],
                "coord_y": list_forms[1],
                "name": list_forms[2],
                "situacao": list_forms[3],
                "tipo": list_forms[4],
                "pontos": list_forms[5],
                "bairro": list_forms[6],
                "logradouro": list_forms[7],
            }
        else:
            try:
                with open(image.src, 'rb') as file: #verificar com antecedencia se a imagem vai poder ser acessada
                    bytes = file.read()
                sp.delete_storage(numero=numero_ant)
                sp.add_storage(numero=numero, image=image)
                image_url = sp.get_storage(numero=numero)
                data = {
                    "number": numero,
                    "coord_x": list_forms[0],
                    "coord_y": list_forms[1],
                    "name": list_forms[2],
                    "situacao": list_forms[3],
                    "tipo": list_forms[4],
                    "pontos": list_forms[5],
                    "bairro": list_forms[6],
                    "logradouro": list_forms[7],
                    "url": image_url
                }
            except:
                self.page.snack_bar = ft.SnackBar(
                        content=ft.Text(f"O dispositivo negou acesso a imagem"),
                        bgcolor=ft.colors.AMBER,
                        duration=1000,
                    )
                self.page.snack_bar.open = True
                data = {
                    "number": numero,
                    "coord_x": list_forms[0],
                    "coord_y": list_forms[1],
                    "name": list_forms[2],
                    "situacao": list_forms[3],
                    "tipo": list_forms[4],
                    "pontos": list_forms[5],
                    "bairro": list_forms[6],
                    "logradouro": list_forms[7],
                }

        response = requests.patch(
            f"{self.supabase_url}/rest/v1/points_capeladoalto?number=eq.{numero}",
            headers=headers,
            json=data,
        )

        return response

    def get_os(self, order):

        headers = {
            "apikey": self.supabase_key,
            "Authorization": f"Bearer {self.supabase_key}",
            "Content-Type": "application/json",
        }

        params = {
        "ordem": f"eq.{order}",
        "select": "created_at, ip, reclamante, function, celular, ordem, origem, observacao, materiais, ponto, status, data_andamento, data_conclusao, equipe",
        }

        response = requests.get(
            f"{self.supabase_url}/rest/v1/ordens_postes_capeladoalto",
            headers=headers,
            params=params,
        )

        return response

    def edit_os(self, list_edited_os_forms):

        numero = int(list_edited_os_forms[1].split('-')[1])

        headers = {
            "apikey": self.supabase_key,
            "Authorization": f"Bearer {self.supabase_key}",
            "Content-Type": "application/json",
        }


        data = {
            "created_at": list_edited_os_forms[0],
            "ip": list_edited_os_forms[1],
            "numero": numero,
            "reclamante": list_edited_os_forms[2],
            "function": list_edited_os_forms[3],
            "celular": list_edited_os_forms[4],
            "ordem": list_edited_os_forms[5],
            "origem": list_edited_os_forms[6],
            "observacao": list_edited_os_forms[7],
            "materiais": list_edited_os_forms[8],
            "ponto": list_edited_os_forms[9],
            "status": list_edited_os_forms[10],
            "data_andamento": list_edited_os_forms[11],
            "data_conclusao": list_edited_os_forms[12],
            "equipe": list_edited_os_forms[13],
        }

        response = requests.patch(
            f"{self.supabase_url}/rest/v1/ordens_postes_capeladoalto?ordem=eq.{list_edited_os_forms[5]}",
            headers=headers,
            json=data,
        )

        return response

    def delete_os(self, order):

        headers = {
            "apikey": self.supabase_key,
            "Authorization": f"Bearer {self.supabase_key}",
            "Content-Type": "application/json",
        }

        response = requests.delete(
            f"{self.supabase_url}/rest/v1/ordens_postes_capeladoalto?ordem=eq.{order}",
            headers=headers,
        )

        return response



class GeoPosition:

    def __init__(self, page, point_location):
        self.page = page
        self.point_location = point_location



        def handle_position_change(e):

            self.point_location.coordinates = map.MapLatitudeLongitude(e.latitude, e.longitude)
            self.page.update()



        self.gl = ft.Geolocator(
                    location_settings=ft.GeolocatorAppleSettings(
                        distance_filter=0,
                    ),
                    on_position_change=handle_position_change,
                    data = 0,
                    )
        self.page.overlay.append(self.gl)

    async def get_permission(self, e=None):

        status = await self.gl.get_permission_status_async()
        if str(status) == "GeolocatorPermissionStatus.DENIED":
            await self.gl.request_permission_async(wait_timeout=60)
            return status   
        else:
            return status
            


class NavigationDrawer:

    def __init__(self, page):
        self.page = page






    def create_navigation(self, name, action1, action2, action3, action4):

        space = ft.Container(padding=10)

        web_images = Web_Image(self.page)
        url_imagem1 = web_images.get_image_url(name="perfil")

        perfil = ft.Column(
            visible=True,
            col=12,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[ft.Container(
                width=150,
                height=150,
                alignment=ft.alignment.center,
                image_src=url_imagem1,
                bgcolor=ft.colors.GREY,
                border=ft.Border(
                    left=ft.BorderSide(2, ft.colors.BLACK),  
                    top=ft.BorderSide(2, ft.colors.BLACK),    
                    right=ft.BorderSide(2, ft.colors.BLACK), 
                    bottom=ft.BorderSide(2, ft.colors.BLACK) 
                ),
                border_radius=ft.border_radius.all(75),
            )
            ]
        )

        nome = ft.Text(
            value=name,
            text_align=ft.TextAlign.CENTER,
        )


        navigation =  ft.NavigationDrawer(
                position=ft.NavigationDrawerPosition.END,
                on_dismiss=None,
                on_change=None,
                controls=[
                    space,
                    perfil,
                    nome,
                    space,
                    ft.ListTile(
                        title=ft.Text(f"Deslogar"),
                        on_click=action1
                    ),
                    ft.ListTile(
                        title=ft.Text(f"Atualizar"),
                        on_click=action2
                    ),
                    ft.ListTile(
                        title=ft.Text(f"Lista de Postes"),
                        on_click=action3
                    ),
                    ft.ListTile(
                        title=ft.Text(f"Lista de Ordens de serviço"),
                        on_click=action4
                    ),
                ],
            )

        return navigation

        



    



      

