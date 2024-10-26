import flet as ft
import requests
import threading
import flet.map as map


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
    def create_button(self, on_click, text, color, col, padding, on_long_press=None):
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
                                on_long_press=on_long_press,
                                width=150,
                            )
                        )
                    ]    
                 )
    
    def create_call_location_button(self, on_click, text, color, col, padding, on_long_press=None):
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
                                icon=ft.icons.MY_LOCATION,
                                icon_color=ft.colors.GREEN,
                                bgcolor=color,
                                color=ft.colors.WHITE,
                                on_click=on_click,
                                on_long_press=on_long_press,
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

    def create_settings_menu(self, color, itens, col):

        return ft.Column(
                col=col,
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


class LoadingPages:

    def __init__(self, page):
        self.page = page

    def new_loading_page(self, page, layout):

        page.clean()

        page.add(layout)

        page.scroll_to(1)

        page.update()
 

class GalleryPicker:

    def __init__(self, page, image_temp, image_bytes):

        self.page = page
        self.image_temp = image_temp
        self.image_bytes = image_bytes
        self.file_picker = ft.FilePicker(on_result=self.on_image_selected) # cria o objeto de seleção de arquivos e adiciona uma chamada de função para quando arquivo for escolhido
        self.page.overlay.append(self.file_picker) # adiciona o objeto a sebreposição da página


    def open_gallery(self, e):   # e representa o clique do botão que disparou o evento
        self.file_picker.pick_files(               # chama a janela de seleção de arquivos
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

            image_container = ft.Image(src=selected_image.path) 
            with open(image_container.src, 'rb') as file:
                bytes = file.read() 


            self.image_temp.content = image_container 
            self.image_bytes[0] = bytes 
            self.page.update()


class SendImage:
    def __init__(self):
        self.supabase_url = "https://ipyhpxhsmyzzkvucdonu.supabase.co"
        self.supabase_key = (
            "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImlweWhweGhzbXl6emt2dWNkb251Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3Mjc1NjQ3NDIsImV4cCI6MjA0MzE0MDc0Mn0.qA9H-UyAEx2OgihW1d_i2IjqQ5HTt1e4ITr52J5qRsA"
        )

    def upload_image(self, image, numero):
        # O caminho onde a imagem será armazenada no Supabase
        storage_path = f'postes_images_points/postes/{numero}.jpg'

        # Cabeçalhos para a requisição de upload
        headers = {
            'Authorization': f'Bearer {self.supabase_key}',
            'Content-Type': 'image/jpeg'
        }

        # Fazendo a requisição POST para enviar a imagem
        response = requests.post(
            f'{self.supabase_url}/storage/v1/object/{storage_path}',
            headers=headers,
            data=image
        )

        if response.status_code == 200:
            print("Imagem enviada com sucesso!")

            # Construindo a URL pública correta da imagem
            public_url = f"{self.supabase_url}/storage/v1/object/public/{storage_path}"
            
            # Verificando se a imagem é acessível
            response = requests.get(public_url)

            if response.status_code == 200:
                print(f"Imagem encontrada: {public_url}")
                return public_url  # Retorna a URL pública da imagem

            else:
                print(f"Erro ao buscar a imagem: {response.status_code} - {response.text}")
                return None

        else:
            print("Erro ao enviar imagem:", response.json())
            return None
