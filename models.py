import flet as ft
import requests
import flet.map as map
from datetime import datetime




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
                size=12,
                color=ft.colors.BLACK,
                weight=ft.FontWeight.W_900,
            ),
            title_medium=ft.TextStyle(
                size=12,
                color=ft.colors.BLACK,
                weight=ft.FontWeight.W_400,
            ),
            title_small=ft.TextStyle(
                size=13,
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
    
          
    
    def create_point_button(self, on_click, text, color, size, visible):
        return ft.Column( 
                spacing=0,
                wrap=True,
                controls=[
                    ft.ElevatedButton(
                        on_click=on_click,
                        width=size,
                        height=size,
                        bgcolor=color,
                        text=" ",
                        style=ft.ButtonStyle(
                            shape=ft.RoundedRectangleBorder(radius=10),
                        ),
                    ),
                    ft.Text(
                        value=text,
                        no_wrap=True,
                        color=ft.colors.BLACK,
                        size=size,
                        text_align=ft.TextAlign.START,
                        weight=ft.FontWeight.BOLD,
                        visible=visible,
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


    def create_checkbox(self, text, size, on_change, col, data=None, value=False):

        return ft.Column(
            horizontal_alignment = ft.CrossAxisAlignment.START,
            col=col,
            controls=[
                ft.Checkbox(
                    value=value,
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

    def create_checkbox2(self, text, size, on_change, col, data=None, value=False):

        return ft.Column(
            horizontal_alignment = ft.CrossAxisAlignment.START,
            col=col,
            controls=[
                ft.Checkbox(
                    value=value,
                    label=text,
                    data = data,
                    on_change=on_change,
                    label_style=ft.TextStyle(
                        color=ft.colors.WHITE,
                        size=size,    
                        )
                    )
            ]
        )


class TextField:

    def __init__(self, page):
        self.page = page


    def create_textfield(self,value, text, password, read=False, input_filter=None, keyboard_type=None):

        return  ft.TextField(
            value=value,
            label= text,
            password=password,
            label_style= ft.TextStyle(color=ft.colors.BLACK, size=12),
            text_style= ft.TextStyle(color=ft.colors.BLACK, size=12),
            col=8,
            read_only=read,
            input_filter=input_filter,
            keyboard_type=keyboard_type
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

    def create_post_form(self, list_post_form):

        textthemes = TextTheme()
        texttheme1 = textthemes.create_text_theme1()

        return ft.Container(
            padding=0,
            col=12,
            theme=texttheme1,  
            content=ft.DataTable(
                data_row_max_height=60,
                column_spacing=10,
                columns=[
                    ft.DataColumn(ft.Text(value="")),  
                    ft.DataColumn(ft.Text(value="")),  
                ],
                rows=[
                    ft.DataRow(cells=[
                        ft.DataCell(ft.Text(value="IP", theme_style=ft.TextThemeStyle.TITLE_LARGE)),
                        ft.DataCell(
                            ft.Container(content=ft.Text(value=list_post_form[0], theme_style=ft.TextThemeStyle.TITLE_MEDIUM), width=200)
                        )
                    ]),
                    ft.DataRow(cells=[
                        ft.DataCell(ft.Text(value="Situação", theme_style=ft.TextThemeStyle.TITLE_LARGE)),
                        ft.DataCell(
                            ft.Container(content=ft.Text(value=list_post_form[1], theme_style=ft.TextThemeStyle.TITLE_MEDIUM), width=200)
                        )
                    ]),
                    ft.DataRow(cells=[
                        ft.DataCell(ft.Text(value="Tipo de Lâmpada", theme_style=ft.TextThemeStyle.TITLE_LARGE)),
                        ft.DataCell(
                            ft.Container(content=ft.Text(value=list_post_form[2], theme_style=ft.TextThemeStyle.TITLE_MEDIUM), width=200)
                        )
                    ]),
                    ft.DataRow(cells=[
                        ft.DataCell(ft.Text(value="Pontos", theme_style=ft.TextThemeStyle.TITLE_LARGE)),
                        ft.DataCell(
                            ft.Container(content=ft.Text(value=list_post_form[3], theme_style=ft.TextThemeStyle.TITLE_MEDIUM), width=200)
                        )
                    ]),
                    ft.DataRow(cells=[
                        ft.DataCell(ft.Text(value="Bairro", theme_style=ft.TextThemeStyle.TITLE_LARGE)),
                        ft.DataCell(
                            ft.Container(content=ft.Text(value=list_post_form[4], theme_style=ft.TextThemeStyle.TITLE_MEDIUM), width=200)
                        )
                    ]),
                    ft.DataRow(cells=[
                        ft.DataCell(ft.Text(value="Logradouro", theme_style=ft.TextThemeStyle.TITLE_LARGE)),
                        ft.DataCell(
                            ft.Container(content=ft.Text(value=list_post_form[5], theme_style=ft.TextThemeStyle.TITLE_MEDIUM), width=200)
                        )
                    ]),
                ],
            ),
        )
    
    def create_user_form(self, list_user_form):

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
                        ft.DataCell(ft.Text(value="ID", theme_style=ft.TextThemeStyle.TITLE_LARGE)),
                        ft.DataCell(
                            ft.Container(content=ft.Text(value=list_user_form[0], theme_style=ft.TextThemeStyle.TITLE_MEDIUM), width=200)
                        )
                    ]),
                    ft.DataRow(cells=[
                        ft.DataCell(ft.Text(value="Usuário", theme_style=ft.TextThemeStyle.TITLE_LARGE)),
                        ft.DataCell(
                            ft.Container(content=ft.Text(value=list_user_form[1], theme_style=ft.TextThemeStyle.TITLE_MEDIUM), width=200)
                        )
                    ]),
                    ft.DataRow(cells=[
                        ft.DataCell(ft.Text(value="E-mail", theme_style=ft.TextThemeStyle.TITLE_LARGE)),
                        ft.DataCell(
                            ft.Container(content=ft.Text(value=list_user_form[2], theme_style=ft.TextThemeStyle.TITLE_SMALL), width=200)
                        )
                    ]),
                    ft.DataRow(cells=[
                        ft.DataCell(ft.Text(value="Numero", theme_style=ft.TextThemeStyle.TITLE_LARGE)),
                        ft.DataCell(
                            ft.Container(content=ft.Text(value=list_user_form[3], theme_style=ft.TextThemeStyle.TITLE_MEDIUM), width=200)
                        )
                    ]),
                    ft.DataRow(cells=[
                        ft.DataCell(ft.Text(value="Senha", theme_style=ft.TextThemeStyle.TITLE_LARGE)),
                        ft.DataCell(
                            ft.Container(content=ft.Text(value=list_user_form[4], theme_style=ft.TextThemeStyle.TITLE_MEDIUM), width=200)
                        )
                    ]),
                    ft.DataRow(cells=[
                        ft.DataCell(ft.Text(value="Permissão", theme_style=ft.TextThemeStyle.TITLE_LARGE)),
                        ft.DataCell(
                            ft.Container(content=ft.Text(value=list_user_form[5], theme_style=ft.TextThemeStyle.TITLE_MEDIUM), width=200)
                        )
                    ]),
                ],
            ),
        )
    
    def create_os_forms(self, data_criacao, ip, reclamante, function, celular, order, origem, obser, materiais, ponto, status, data_andamen, data_conclu, equipe):

        textthemes = TextTheme()
        texttheme1 = textthemes.create_text_theme1()

        return ft.Container(
            padding=0,
            col=12,
            theme=texttheme1,  
            content=ft.DataTable(
                data_row_max_height=60,
                column_spacing=10,
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
                            ft.Container(content=ft.Text(value=order, theme_style=ft.TextThemeStyle.TITLE_MEDIUM), width=200)
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

    def create_add_forms(self, ip, situ, tipo, pontos, bairro, logra):

        textthemes = TextTheme()
        texttheme1 = textthemes.create_text_theme1()

        textfields = TextField(self.page)
        ip_field = textfields.create_textfield(value=ip, text=None, password=False, read=None, input_filter=ft.NumbersOnlyInputFilter(), keyboard_type=ft.KeyboardType.NUMBER)
        bairro_field = textfields.create_textfield(value=bairro, text=None, password=False)
        logradouro_field = textfields.create_textfield(value=logra, text=None, password=False)

        def drop_down_menu(value=None, opt1=None, opt2=None, opt3=None, opt4=None, opt5=None, opt6=None):

            list = [opt1, opt2, opt3, opt4, opt5, opt6]
            list_option = []
            for opt in list:
                if opt != None:
                    list_option.append(ft.dropdown.Option(opt))

            menu = ft.Dropdown(
                options=list_option,
                value=value,
                label_style=ft.TextStyle(color=ft.colors.BLACK, size=12),
                bgcolor=ft.colors.WHITE,
                options_fill_horizontally=True,
                text_style= ft.TextStyle(size=12, color=ft.colors.BLACK)
            )
            return menu
    

        return ft.Container(
            padding=0,
            col=12,
            theme=texttheme1,
            content=ft.DataTable(
                data_row_max_height=60,
                column_spacing=10,
                columns=[
                    ft.DataColumn(ft.Text(value="")),  # Primeira coluna
                    ft.DataColumn(ft.Text(value="")),  # Segunda coluna
                ],
                rows=[
                    ft.DataRow(cells=[
                        ft.DataCell(ft.Text(value="IP", theme_style=ft.TextThemeStyle.TITLE_LARGE)),
                        ft.DataCell(
                            ft.Container(content=ip_field, width=240)
                        )
                    ]),
                    ft.DataRow(cells=[
                        ft.DataCell(ft.Text(value="Situação", theme_style=ft.TextThemeStyle.TITLE_LARGE)),
                        ft.DataCell(
                            ft.Container(content=drop_down_menu(situ, "Com iluminação", "Sem iluminação"), width=240)
                        )
                    ]),
                    ft.DataRow(cells=[
                        ft.DataCell(ft.Text(value="Tipo de Lâmpada", theme_style=ft.TextThemeStyle.TITLE_LARGE)),
                        ft.DataCell(
                            ft.Container(content=drop_down_menu(tipo, ".", "Lâmpada LED", "Lâmpada de vapor de sódio"), width=240)
                        )
                    ]),
                    ft.DataRow(cells=[
                        ft.DataCell(ft.Text(value="Pontos", theme_style=ft.TextThemeStyle.TITLE_LARGE)),
                        ft.DataCell(
                            ft.Container(content=drop_down_menu(pontos, "0","1", "2", "3", "4", "5"), width=240)
                        )
                    ]),
                    ft.DataRow(cells=[
                        ft.DataCell(ft.Text(value="Bairro", theme_style=ft.TextThemeStyle.TITLE_LARGE)),
                        ft.DataCell(
                            ft.Container(content=bairro_field, width=240)
                        )
                    ]),
                    ft.DataRow(cells=[
                        ft.DataCell(ft.Text(value="Logradouro", theme_style=ft.TextThemeStyle.TITLE_LARGE)),
                        ft.DataCell(
                            ft.Container(content=logradouro_field, width=240)
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
                data_row_max_height=60,
                column_spacing=10,
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
    
    def create_add_user_forms(self, list_user_forms, new=False):

        textthemes = TextTheme()
        texttheme1 = textthemes.create_text_theme1()
        textfields = TextField(self.page)

        user_name_field = textfields.create_textfield(value=list_user_forms[0], text=None, password=False)
        user_email_field = textfields.create_textfield(value=list_user_forms[1], text=None, password=False, read=True)
        if new == True:
            user_email_field = textfields.create_textfield(value=list_user_forms[1], text=None, password=False, read=False)
        user_phone_field = textfields.create_textfield(value=list_user_forms[2], text=None, password=False)
        user_password_field = textfields.create_textfield(value=list_user_forms[3], text=None, password=False)
        user_permission_field = textfields.create_textfield(value=list_user_forms[4], text=None, password=False)

        def drop_down_menu(value=None, opt1=None, opt2=None, opt3=None, opt4=None, opt5=None, opt6=None):
            list = [opt1, opt2, opt3, opt4, opt5, opt6]
            list_option = []
            for opt in list:
                if opt != None:
                    list_option.append(ft.dropdown.Option(opt))

            menu = ft.Dropdown(
                options=list_option,
                value=value,
                label_style=ft.TextStyle(color=ft.colors.BLACK, size=12),
                bgcolor=ft.colors.WHITE,
                options_fill_horizontally=True,
                text_style= ft.TextStyle(size=12, color=ft.colors.BLACK)
            )
            return menu
       
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
                        ft.DataCell(ft.Text(value="Usuário", theme_style=ft.TextThemeStyle.TITLE_LARGE)),
                        ft.DataCell(
                            ft.Container(content=user_name_field, width=200)  
                        )
                    ]),
                    ft.DataRow(cells=[
                        ft.DataCell(ft.Text(value="E-mail", theme_style=ft.TextThemeStyle.TITLE_LARGE)),
                        ft.DataCell(
                            ft.Container(content=user_email_field, width=200)  
                        )
                    ]),
                    ft.DataRow(cells=[
                        ft.DataCell(ft.Text(value="Numero", theme_style=ft.TextThemeStyle.TITLE_LARGE)),
                        ft.DataCell(
                            ft.Container(content=user_phone_field, width=200)
                        )
                    ]),
                    ft.DataRow(cells=[
                        ft.DataCell(ft.Text(value="Senha", theme_style=ft.TextThemeStyle.TITLE_LARGE)),
                        ft.DataCell(
                            ft.Container(content=user_password_field, width=200)
                        )
                    ]),
                    ft.DataRow(cells=[
                        ft.DataCell(ft.Text(value="Permissão", theme_style=ft.TextThemeStyle.TITLE_LARGE)),
                        ft.DataCell(
                            ft.Container(content=drop_down_menu(list_user_forms[4], "adm", "invited"), width=200)
                        )
                    ]),
                   
                ],
            ),
        )


class LoadingPages:

    def __init__(self, page):
        self.page = page

    def new_loading_page(self, page, layout):

        page.add(layout)

        page.scroll_to(1)
        
        page.update()


class SupaBase:

    def __init__(self, page):
        self.page = page
        self.supabase_url = "https://ipyhpxhsmyzzkvucdonu.supabase.co"
        self.supabase_key = (
            "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImlweWhweGhzbXl6emt2dWNkb251Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3Mjc1NjQ3NDIsImV4cCI6MjA0MzE0MDc0Mn0.qA9H-UyAEx2OgihW1d_i2IjqQ5HTt1e4ITr52J5qRsA"
        )

    def get_url(self):
        return self.supabase_url
    
    def get_key(self):
        return self.supabase_key



    def get_point_post(self):

        headers = {
            "apikey": self.supabase_key,
            "Authorization": f"Bearer {self.supabase_key}",
            "Content-Type": "application/json",
        }

        params = {"select": "name, x, y, color"}

        response = requests.get(
            f"{self.supabase_url}/rest/v1/point_post_capela",
            headers=headers,
            params=params,
        )

        return response

    def get_form_user(self, user):

        headers = {
            "apikey": self.supabase_key,
            "Authorization": f"Bearer {self.supabase_key}",
            "Content-Type": "application/json",
        }

        params = {
        "usuario": f"eq.{user}",
        "select": "user_id, usuario, email, numero, senha, permission",
        }

        response = requests.get(
            f"{self.supabase_url}/rest/v1/login_geopostes",
            headers=headers,
            params=params,
        )

        return response
    
    def get_form_post(self, name):

        headers = {
            "apikey": self.supabase_key,
            "Authorization": f"Bearer {self.supabase_key}",
            "Content-Type": "application/json",
        }

        params = {
        "name": f"eq.{name}",
        "select": "name, situation, type, point, hood, address",
        }

        response = requests.get(
            f"{self.supabase_url}/rest/v1/form_post_capela",
            headers=headers,
            params=params,
        )

        return response

    def get_storage_post(self, name):
        storage_path = f'capela/post/{name}.jpg'
        public_url = f"{self.supabase_url}/storage/v1/object/public/{storage_path}"
        response = requests.get(public_url)
        if response.status_code == 200:
            return public_url 
        else:
            url = "Nulo"
            return url

    def get_os(self, order):

        headers = {
            "apikey": self.supabase_key,
            "Authorization": f"Bearer {self.supabase_key}",
            "Content-Type": "application/json",
        }

        params = {
        "order_id": f"eq.{order}",
        "select": "created_at, ip, reclamante, function, celular, order_id, origem, observacao, materiais, ponto, status, data_andamento, data_conclusao, equipe",
        }

        response = requests.get(
            f"{self.supabase_url}/rest/v1/ordens_postes_capeladoalto",
            headers=headers,
            params=params,
        )

        return response

    def get_os_id(self):

        headers = {
            "apikey": self.supabase_key,
            "Authorization": f"Bearer {self.supabase_key}",
            "Content-Type": "application/json",
        }

        params = {
        "select": "order_id", "order": "order_id.desc", "limit": 1,
        }

        response = requests.get(
            f"{self.supabase_url}/rest/v1/ordens_postes_capeladoalto",
            headers=headers,
            params=params,
        )

        next_id = response.json()[0]["order_id"] if response.json() else 0
        new_id = int(next_id) + 1

        return new_id
    
    def get_last_form_post(self):

        headers = {
            "apikey": self.supabase_key,
            "Authorization": f"Bearer {self.supabase_key}",
            "Content-Type": "application/json",
        }

        params = {
        "select": "name", 
        }
    
        response = requests.get(
            f"{self.supabase_url}/rest/v1/form_post_capela",
            headers=headers,
            params=params,
        )

        data = response.json()

        if not data:
            return "1"

        numbers = []
        for item in data:
            try:
                # Extrai o número após o hífen
                numero = int(item["name"].split('-')[1])
                numbers.append(numero)
            except (IndexError, ValueError):
                # Ignora entradas inválidas
                continue

        max_number = max(numbers) if numbers else 0
        new_number = str(max_number+1)

        return new_number
    
    def get_user_id(self):

        headers = {
            "apikey": self.supabase_key,
            "Authorization": f"Bearer {self.supabase_key}",
            "Content-Type": "application/json",
        }

        params = {
        "select": "user_id", "order": "user_id.desc", "limit": 1,
        }

        response = requests.get(
            f"{self.supabase_url}/rest/v1/login_geopostes",
            headers=headers,
            params=params,
        )

        next_id = response.json()[0]["user_id"] if response.json() else 0
        new_id = int(next_id) + 1

        return new_id



    def add_storage(self, name, image, angle_image, new=True):
        
        headers = {
            'Authorization': f'Bearer {self.supabase_key}',
            'Content-Type': 'image/jpeg'
        }

        storage_path = f'capela/post/{name}.jpg'

        if new == True:
            with open(image, 'rb') as file:
                bytes = file.read() 
        else:
            bytes = image

        response = requests.post(
                f'{self.supabase_url}/storage/v1/object/{storage_path}',
                headers=headers,
                data=bytes
            )
        
        if response.status_code != 200: 
            print("Erro ao enviar imagem:", response.json())
            return None

    def add_point(self, list_profile, list_forms, list_initial_coordinates, image, angle):

        sp = SupaBase(self.page)
        number = str(list_forms[0])
        new_number = number.zfill(4)
        ip = f"IP SOR-{new_number}"

        point_color = None
        if list_forms[2] == "Lâmpada LED":
            point_color = "white"
        if list_forms[2] == "Lâmpada de vapor de sódio":
            point_color = "yellow"
        if list_forms[2] == ".":
            point_color = "blue"


        headers = {
            "apikey": self.supabase_key,
            "Authorization": f"Bearer {self.supabase_key}",
            "Content-Type": "application/json",
        }

        response1 = requests.get(
            f"{self.supabase_url}/rest/v1/point_post_capela",
            headers=headers,
            params={"select": "name", "name": f"eq.{ip}"}
        )

        if response1.status_code == 200 and response1.json():
            # Se o ponto já existir, mostre a mensagem e retorne
            snack_bar = ft.SnackBar(
                content=ft.Text(f"{ip} já foi cadastrado, ponto não adicionado"),
                bgcolor=ft.colors.RED
            )
            self.page.overlay.append(snack_bar)
            snack_bar.open = True
            response1.status_code = 199
            return response1

        if image != None:
            try:
                sp.add_storage(ip, image.src, angle)
            except:
                snack_bar = ft.SnackBar(
                        content=ft.Text(f"O dispositivo negou acesso a imagem"),
                        bgcolor=ft.colors.AMBER,
                        duration=1000,
                    )
                self.page.overlay.append(snack_bar)
                snack_bar.open = True

        data = {
                "name": ip,
                "situation": list_forms[1],
                "type": list_forms[2],
                "point": list_forms[3],
                "hood": list_forms[4],
                "address": list_forms[5],
            }

        response2 = requests.post(
            f"{self.supabase_url}/rest/v1/form_post_capela",
            headers=headers,
            json=data,
        )

        data_atual = datetime.now()
        data_formatada = data_atual.strftime("%d/%m/%Y")

        data2 = {
                "name": ip,
                "x": list_initial_coordinates[0],
                "y": list_initial_coordinates[1],
                "color": point_color,
                "changed_at": data_formatada,
                "changed_by": list_profile[0],
            }
        
        response3 = requests.post(
            f"{self.supabase_url}/rest/v1/point_post_capela",
            headers=headers,
            json=data2,
        )
        
        return response3
    
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
            params={"select": "order_id", "order_id": f"eq.{list_add_os[5]}"}
        )

        if response.status_code == 200 and response.json():
            snack_bar = ft.SnackBar(
                content=ft.Text(f"{list_add_os[5]} já foi cadastrado, ordem {list_add_os[5]} não adicionada"),
                bgcolor=ft.colors.RED
            )
            self.page.overlay.append(snack_bar)
            snack_bar.open = True
            self.page.update()
            return

        data = {
            "created_at": list_add_os[0],
            "ip": list_add_os[1],
            "numero": numero,
            "reclamante": list_add_os[2],
            "function": list_add_os[3],
            "celular": list_add_os[4],
            "order_id": list_add_os[5],
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
    
    def add_user(self, list_add_user, id):

        headers = {
            "apikey": self.supabase_key,
            "Authorization": f"Bearer {self.supabase_key}",
            "Content-Type": "application/json",
        }

        response1 = requests.get(
            f"{self.supabase_url}/rest/v1/login_geopostes",
            headers=headers,
            params={"select": "email", "email": f"eq.{list_add_user[0]}"}
        )

        if response1.status_code == 200 and response1.json():
            # Se o e-mail já existir, mostre a mensagem e retorne
            snack_bar = ft.SnackBar(
                content=ft.Text("E-mail já cadastrado"),
                bgcolor=ft.colors.RED
            )
            self.page.overlay.append(snack_bar)
            snack_bar.open = True
            self.page.update()
            response1.status_code == 199
            return response1
         
        response2 = requests.get(
            f"{self.supabase_url}/rest/v1/login_geopostes",
            headers=headers,
            params={"select": "usuario", "usuario": f"eq.{list_add_user[1]}"}
        )

        if response2.status_code == 200 and response2.json():
            # Se o usuario já existir, mostre a mensagem e retorne
            snack_bar = ft.SnackBar(
                content=ft.Text("Nome de usuario já cadastrado"),
                bgcolor=ft.colors.RED
            )
            self.page.overlay.append(snack_bar)
            snack_bar.open = True
            self.page.update()

            return 

        data = {
            "user_id": id,
            "usuario": list_add_user[0],
            "email": list_add_user[1],
            "numero": list_add_user[2],
            "senha": list_add_user[3],
            "permission": list_add_user[4],  
        }

        response3 = requests.post(
            f"{self.supabase_url}/rest/v1/login_geopostes",
            headers=headers,
            json=data,
        )

        return response3



    def edit_point(self, image, list_forms, previous_data):

        sp = SupaBase(self.page)
        number = str(list_forms[0])
        new_number = number.zfill(4)
        ip = f"IP SOR-{new_number}"

        headers = {
            "apikey": self.supabase_key,
            "Authorization": f"Bearer {self.supabase_key}",
            "Content-Type": "application/json",
        }

        data = {
                "name": ip,
                "situation": list_forms[1],
                "type": list_forms[2],
                "point": list_forms[3],
                "hood": list_forms[4],
                "address": list_forms[5],
            }

        changed = False

        if list_forms[2] != previous_data["type"]:

            if list_forms[2] == "Lâmpada LED":
                point_color = "white"
            if list_forms[2] == "Lâmpada de vapor de sódio":
                point_color = "yellow"
            if list_forms[2] == ".":
                point_color = "blue"

            response1 = requests.get(
                f"{self.supabase_url}/rest/v1/point_post_capela",
                headers=headers,
                params={"select": "name", "name": f'eq.{previous_data["name"]}'}
            )

            data2 = { "color": point_color}

            response2 = requests.patch(
                f'{self.supabase_url}/rest/v1/point_post_capela?name=eq.{previous_data["name"]}',
                headers=headers,
                json=data2,
            )

        if previous_data["name"] != ip:

            response1 = requests.get(
                f"{self.supabase_url}/rest/v1/point_post_capela",
                headers=headers,
                params={"select": "name", "name": f"eq.{ip}"}
            )

            if response1.status_code == 200 and response1.json():
                snack_bar = ft.SnackBar(
                    content=ft.Text(f"{ip} já foi cadastrado, ponto não editado"),
                    bgcolor=ft.colors.RED
                )
                self.page.overlay.append(snack_bar)
                snack_bar.open = True
                response1.status_code = 199
                return response1

            data3 = { "name": ip}

            response2 = requests.patch(
                f'{self.supabase_url}/rest/v1/point_post_capela?name=eq.{previous_data["name"]}',
                headers=headers,
                json=data3,
            )

            if image.data == "foto":
                changed = True
                try:
                    headers2 = {
                        "apikey": self.supabase_key,
                        "Authorization": f"Bearer {self.supabase_key}",
                    }
                    url = sp.get_storage_post(previous_data["name"])
                    get_bytes = requests.get(url, headers=headers2)
                    bytes = get_bytes.content
                    if url != "Nulo":
                        sp.delete_storage(previous_data["name"])
                    if "supabase" not in image.src:
                        sp.add_storage(ip, image.src, angle_image=0)
                    else:
                        sp.add_storage(ip, bytes, angle_image=0, new=False)

                except:
                    snack_bar = ft.SnackBar(
                            content=ft.Text(f"O dispositivo negou acesso a imagem"),
                            bgcolor=ft.colors.AMBER,
                            duration=1000,
                        )
                    self.page.overlay.append(snack_bar)
                    snack_bar.open = True

        if image.data == "foto" and changed == False:
            if "supabase" not in image.src:
                try:
                    url = sp.get_storage_post(previous_data["name"])
                    if url != "Nulo":
                        sp.delete_storage(previous_data["name"])
                    sp.add_storage(ip, image.src, angle_image=0, new=True)    
                except:
                    snack_bar = ft.SnackBar(
                            content=ft.Text(f"O dispositivo negou acesso a imagem"),
                            bgcolor=ft.colors.AMBER,
                            duration=1000,
                        )
                    self.page.overlay.append(snack_bar)
                    snack_bar.open = True

        response3 = requests.patch(
            f'{self.supabase_url}/rest/v1/form_post_capela?name=eq.{previous_data["name"]}',
            headers=headers,
            json=data,
        )

        return response3

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
            "order_id": list_edited_os_forms[5],
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
            f"{self.supabase_url}/rest/v1/ordens_postes_capeladoalto?order_id=eq.{list_edited_os_forms[5]}",
            headers=headers,
            json=data,
        )

        return response
    
    def edit_user(self, list_edited_user_forms, previus_name):

        headers = {
            "apikey": self.supabase_key,
            "Authorization": f"Bearer {self.supabase_key}",
            "Content-Type": "application/json",
        }
      
        if list_edited_user_forms[0] != previus_name:

            response1 = requests.get(
                f"{self.supabase_url}/rest/v1/login_geopostes",
                headers=headers,
                params={"select": "usuario", "usuario": f"eq.{list_edited_user_forms[0]}"}
            )

            if response1.status_code == 200 and response1.json():
                # Se o usuario já existir, mostre a mensagem e retorne
                snack_bar = ft.SnackBar(
                    content=ft.Text("Nome de usuario já cadastrado"),
                    bgcolor=ft.colors.RED
                )
                self.page.overlay.append(snack_bar)
                snack_bar.open = True
                self.page.update()

                return

        data = {
            "usuario": list_edited_user_forms[0],
            "numero": list_edited_user_forms[2],
            "senha": list_edited_user_forms[3],
            "permission": list_edited_user_forms[4],
        }

        response = requests.patch(
            f"{self.supabase_url}/rest/v1/login_geopostes?usuario=eq.{previus_name}",
            headers=headers,
            json=data,
        )

        return response



    def delete_point_post(self, name):

        headers = {
            "apikey": self.supabase_key,
            "Authorization": f"Bearer {self.supabase_key}",
            "Content-Type": "application/json",
        }

        response1 = requests.delete(
            f"{self.supabase_url}/rest/v1/point_post_capela?name=eq.{name}",
            headers=headers,
        )

        response2 = requests.delete(
            f"{self.supabase_url}/rest/v1/form_post_capela?name=eq.{name}",
            headers=headers,
        )


        storage_path = f'capela/post/{name}.jpg'
        headers2 = {
            "apikey": self.supabase_key,
            "Authorization": f"Bearer {self.supabase_key}",
            "Content-Type": "image/jpeg",
        }
        url = f"{self.supabase_url}/storage/v1/object/{storage_path}"
        response3 = requests.delete(
            url,
            headers=headers2,
        )

        list_response = [response1, response2, response3]

        return list_response

    def delete_storage(self, name):

        headers = {
            "apikey": self.supabase_key,
            "Authorization": f"Bearer {self.supabase_key}",
            "Content-Type": "image/jpeg",
        }

        storage_path = f'capela/post/{name}.jpg'
        
        url = f"{self.supabase_url}/storage/v1/object/{storage_path}"

        response = requests.delete(
            url,
            headers=headers,
        )

        return response

    def delete_os(self, order):

        headers = {
            "apikey": self.supabase_key,
            "Authorization": f"Bearer {self.supabase_key}",
            "Content-Type": "application/json",
        }

        response = requests.delete(
            f"{self.supabase_url}/rest/v1/ordens_postes_capeladoalto?order_id=eq.{order}",
            headers=headers,
        )

        return response
    
    def delete_user(self, user):

        headers = {
            "apikey": self.supabase_key,
            "Authorization": f"Bearer {self.supabase_key}",
            "Content-Type": "application/json",
        }

        response = requests.delete(
            f"{self.supabase_url}/rest/v1/login_geopostes?usuario=eq.{user}",
            headers=headers,
        )

        return response



    def check_login(self, username, password):

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

        response1 = requests.get(
            f"{self.supabase_url}/rest/v1/login_geopostes",
            headers=headers,
            params={"select": "email", "email": f"eq.{email}"}
        )

        if response1.status_code == 200 and response1.json():
            # Se o e-mail já existir, mostre a mensagem e retorne
            snack_bar = ft.SnackBar(
                content=ft.Text("E-mail já cadastrado"),
                bgcolor=ft.colors.RED
            )
            self.page.overlay.append(snack_bar)
            snack_bar.open = True
            self.page.update()

            return
         
        response2 = requests.get(
            f"{self.supabase_url}/rest/v1/login_geopostes",
            headers=headers,
            params={"select": "usuario", "usuario": f"eq.{username}"}
        )

        if response2.status_code == 200 and response2.json():
            # Se o usuario já existir, mostre a mensagem e retorne
            snack_bar = ft.SnackBar(
                content=ft.Text("Nome de usuario já cadastrado"),
                bgcolor=ft.colors.RED
            )
            self.page.overlay.append(snack_bar)
            snack_bar.open = True
            self.page.update()

            return 

        response3 = requests.get(
            f"{self.supabase_url}/rest/v1/login_geopostes",
            headers=headers,
            params={"select": "user_id", "order": "user_id.desc", "limit": 1},
        )

        if response3.status_code == 200:
            max_user_id = response3.json()[0]["user_id"] if response3.json() else 0
            new_user_id = max_user_id + 1

            # Dados para inserir no Supabase
            data = {
                "user_id": new_user_id,
                "usuario": username,
                "email": email,
                "numero": number,
                "senha": password1,
                "permission": "invited",
            }

            # Fazer a solicitação POST para inserir o novo registro
            response4 = requests.post(
                f"{self.supabase_url}/rest/v1/login_geopostes",
                headers=headers,
                json=data,
            )

            return response4
   
    
class NavigationDrawer:

    def __init__(self, page):
        self.page = page






    def create_navigation(self, list_profile, action1, action2, action3, action4, action5):

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
                image=ft.Image(
                src=url_imagem1,  
                ),
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
            value=list_profile[0],
            text_align=ft.TextAlign.CENTER,
            color=ft.colors.WHITE,
        )

        listtiles = [

            ft.ListTile(
                        title=ft.Text(f"Deslogar", color=ft.colors.WHITE),
                        on_click=action1,
                    ),
            ft.ListTile(
                title=ft.Text(f"Atualizar", color=ft.colors.WHITE),
                on_click=action2
            ),
        ]

        if list_profile[1] == "adm":

            listtiles.append(
                ft.ListTile(
                        title=ft.Text(f"Lista de postes", color=ft.colors.WHITE),
                        on_click=action3
                    )
            )
            listtiles.append(
                ft.ListTile(
                        title=ft.Text(f"Lista de ordens de serviço", color=ft.colors.WHITE),
                        on_click=action4
                    )
            )
            listtiles.append(
                ft.ListTile(
                        title=ft.Text(f"Gestão de usuários", color=ft.colors.WHITE),
                        on_click=action5
                    )
            )


        navigation =  ft.NavigationDrawer(
                position=ft.NavigationDrawerPosition.END,
                on_dismiss=None,
                on_change=None,
                bgcolor=ft.colors.BLUE_600,
                controls=[
                    space,
                    perfil,
                    nome,
                    space,
                    *listtiles,
                ],
            )

        return navigation

        



    



      

