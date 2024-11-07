import flet as ft
from models import *
import requests
import threading
import flet.map as map


def create_page_home(page, name, coord_initial_x, coord_initial_y):

    page.clean()

    loading = LoadingPages(page)

    calltexts = CallText(page)
    coord_text_lat = calltexts.create_calltext(
                      visible=False,
                      text=coord_initial_x,
                      color=ft.colors.BLACK,
                      size=15,
                      font=ft.FontWeight.W_600,
                      col=12,
                      padding=0,)
    coord_text_lon = calltexts.create_calltext(
                      visible=False,
                      text=coord_initial_y,
                      color=ft.colors.BLACK,
                      size=15,
                      font=ft.FontWeight.W_600,
                      col=12,
                      padding=0)
    coord_text_zoom = calltexts.create_calltext(
                      visible=False,
                      text="19",
                      color=ft.colors.BLACK,
                      size=15,
                      font=ft.FontWeight.W_600,
                      col=12,
                      padding=0)
    current_text_lat = calltexts.create_calltext(
                      visible=False,
                      text=None,
                      color=ft.colors.BLACK,
                      size=15,
                      font=ft.FontWeight.W_600,
                      col=12,
                      padding=0,)
    current_text_lon = calltexts.create_calltext(
                      visible=False,
                      text=None,
                      color=ft.colors.BLACK,
                      size=15,
                      font=ft.FontWeight.W_600,
                      col=12,
                      padding=0,)

    navigations = NavigationDrawer(page)
    action1 = lambda e: loading.new_loading_page(page=page, layout=create_page_login(page)) 
    action2 = lambda e: loading.new_loading_page(page=page, layout=create_page_home(page, name, coord_initial_x=coord_text_lat.content.value, coord_initial_y=coord_text_lon.content.value), home=True)
    action3 = lambda e: loading.new_loading_page(page=page, layout=create_view_postes_form(page, name, rightmenu)) 
    action4 = lambda e: loading.new_loading_page(page=page, layout=create_view_orders_form(page, name, rightmenu)) 

    rightmenu = navigations.create_navigation(name, action1, action2, action3, action4)

    menus = SettingsMenu(page)
    menu = menus.create_settings_menu(color=ft.colors.WHITE, col=10, action=lambda e: page.open(rightmenu))





    point_location = map.Marker(
                content=ft.Column(
                            spacing=0,
                            controls=[ 
                                ft.Stack(
                                    expand=True,
                                    alignment=ft.alignment.center,
                                    controls=[
                                        ft.ElevatedButton(
                                            on_click=None,
                                            width=20,
                                            height=20,
                                            bgcolor=ft.colors.BLUE,
                                            text=" ",
                                            style=ft.ButtonStyle(
                                                shape=ft.RoundedRectangleBorder(radius=10),
                                                ),
                                            ),
                                        ft.ElevatedButton(
                                            on_click=None,
                                            width=10,
                                            height=10,
                                            bgcolor=ft.colors.WHITE,
                                            text=" ",
                                            style=ft.ButtonStyle(
                                                shape=ft.RoundedRectangleBorder(radius=10),
                                            ),
                                        ),
                                    ]
                                 ),    
                            ]
                        ),
                coordinates=None,
                rotate=True, 
                )


    buttons = Buttons(page)
   

    maps = Map(page, name, point_location, coord_initial_x, coord_initial_y, coord_text_lat, coord_text_lon, coord_text_zoom)
    mapa1 = maps.create_map()
    
    geo = GeoPosition(page, point_location, current_text_lat, current_text_lon)

    maps.update_position
   

    def go_to_location(e=None):

        if point_location.coordinates is not None:
            lat = str(point_location.coordinates.latitude)
            lon = str(point_location.coordinates.longitude)
            loading.new_loading_page(page=page, layout=create_page_home(page, name, coord_initial_x=lat, coord_initial_y=lon), home=True)


    async def location(e=None):
        status = await geo.get_permission()
        print(f" \n {status} \n " )
        print(status)
        if str(status) == "GeolocatorPermissionStatus.WHILE_IN_USE" or "GeolocatorPermissionStatus.ALWAYS":
            go_to_location()

    button_location = buttons.create_call_location_button(
                                                        icon=ft.icons.MY_LOCATION,
                                                        on_click=location,
                                                        color=ft.colors.WHITE,
                                                        col=2,
                                                        padding=0,
                                                        )


    def call_update_map():

        if page.route == "/home":
           
            if point_location.coordinates is not None:
                button_location.controls[0].content.icon_color = ft.colors.GREEN
            else:
                button_location.controls[0].content.icon_color = ft.colors.RED

            maps.update_position()
        
        threading.Timer(1, call_update_map).start()

    
    call_update_map()


    searchs_bars = SearchBar(page)
    lista_postes = searchs_bars.create_list(name)
    anchor = searchs_bars.create_search_bar()


    page.appbar = ft.AppBar(
        bgcolor=ft.colors.BLUE,
        toolbar_height=80,
        actions=[
            ft.Column(controls=[ft.Container(width=15)]),
            anchor,
            ft.Column(controls=[ft.Container(width=40)]),
            menu,
            ft.Column(controls=[ft.Container(width=15)]),
        ],
    )



    page.floating_action_button = ft.FloatingActionButton(
                        content=ft.Icon(name=ft.icons.ADD_LOCATION_ROUNDED, color=ft.colors.BLUE, scale=2),
                        bgcolor=ft.colors.WHITE,
                        shape=ft.RoundedRectangleBorder(radius=50),
                        on_click= lambda e: loading.new_loading_page(page=page, layout=create_page_add_forms(page, name, coord_text_lat.content.value, coord_text_lon.content.value)) 
                    )
    page.floating_action_button_location = ft.FloatingActionButtonLocation.MINI_CENTER_DOCKED
    

    page.bottom_appbar = ft.BottomAppBar(
        bgcolor=ft.colors.BLUE,
        shape=ft.NotchShape.CIRCULAR,
        height=80,
        content=ft.Row(
            controls=[
                button_location,
                ft.Container(expand=True),
            ]
        ),
    )

  
  
    return ft.ResponsiveRow(
        columns=12,
        controls=[
                coord_text_lat,
                coord_text_lon,
                coord_text_zoom,
                mapa1,
                ],
        alignment=ft.MainAxisAlignment.CENTER,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
    )






def create_page_forms(page, name, poste, numero, coord_initial_x, coord_initial_y):

    page.clean()

    loading = LoadingPages(page)

    buttons = Buttons(page)
    ordem_button = buttons.create_button(on_click=lambda e: loading.new_loading_page(page=page, layout=create_adm_page_order(page, name, poste, numero, coord_initial_x, coord_initial_y)),
                                        text="Ordens",
                                        color=ft.colors.RED,
                                        col=6,
                                        padding=5,)
    back_home_button = buttons.create_button(on_click=lambda e: loading.new_loading_page(page=page, layout=create_page_home(page, name, coord_initial_x, coord_initial_y), home=True),
                                            text="Voltar",
                                            color=ft.colors.AMBER,
                                            col=12,
                                            padding=5,)
    edit_button = buttons.create_button(on_click=lambda e: loading.new_loading_page(page=page, layout=create_page_edit_forms(page, name, poste, coord_initial_x, coord_initial_y)),
                                            text="Editar",
                                            color=ft.colors.GREEN,
                                            col=6,
                                            padding=5,)
    
    forms = Forms(page)
    forms1 = forms.create_forms(poste=poste)


    sp = SupaBase(page)
    url_imagem1 = sp.get_storage(numero=numero)

    if url_imagem1 == "Nulo":

        texts = CallText(page)
        text1 = texts.create_calltext(
                                    visible=True,
                                    text="Sem foto",
                                    color=ft.colors.BLACK,
                                    size=15,
                                    font=ft.FontWeight.W_400,
                                    col=12,
                                    padding=0,
                                    )
        foto_poste = ft.Container(col=12,height=400,alignment=ft.alignment.center,content=(text1))  

    else:

        foto = ft.Image(src=url_imagem1, repeat=None)
        foto_poste = ft.Container(col=8,
                            height=400,
                            expand=True,
                            image_fit=ft.ImageFit.FILL,
                            clip_behavior=ft.ClipBehavior.HARD_EDGE,
                            alignment=ft.alignment.center,
                            border=ft.Border(
                                left=ft.BorderSide(2, ft.colors.BLACK),
                                top=ft.BorderSide(2, ft.colors.BLACK),
                                right=ft.BorderSide(2, ft.colors.BLACK),
                                bottom=ft.BorderSide(2, ft.colors.BLACK),
                                ),
                            content=foto
                            )  
        

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


def create_page_os_forms(page, name, order, poste, numero, coord_initial_x, coord_initial_y):

    page.clean()
    loading = LoadingPages(page)
    forms = Forms(page)


    SUPABASE_URL = "https://ipyhpxhsmyzzkvucdonu.supabase.co"
    SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImlweWhweGhzbXl6emt2dWNkb251Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3Mjc1NjQ3NDIsImV4cCI6MjA0MzE0MDc0Mn0.qA9H-UyAEx2OgihW1d_i2IjqQ5HTt1e4ITr52J5qRsA"

    headers = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}",
        "Content-Type": "application/json",
    }


    params = {
        "ordem": f"eq.{order}",
        "select": "created_at, ip, reclamante, function, celular, ordem, origem, observacao, materiais, ponto, status, data_andamento, data_conclusao, equipe",
    }

    # Requisição à API
    response = requests.get(
        f"{SUPABASE_URL}/rest/v1/ordens_postes_capeladoalto",
        headers=headers,
        params=params,
    )

    data = response.json()

    row = data[0]

    data_criacao = row["created_at"]
    ip = row["ip"]
    reclamante = row["reclamante"]
    function = row["function"]
    celular = row["celular"]
    ordem = row["ordem"]
    origem = row["origem"]
    obser = row["observacao"]
    materiais = row["materiais"]
    ponto = row["ponto"]
    status = row["status"]
    data_andamen = row["data_andamento"]
    data_conclu = row["data_conclusao"]
    equipe = row["equipe"]
    

    os_forms = forms.create_os_forms(data_criacao, ip, reclamante, function, celular, ordem, origem, obser, materiais, ponto, status, data_andamen, data_conclu, equipe)


    def go_back(e=None):
        if numero == None:
            loading.new_loading_page(page=page, layout=create_view_orders_form(page, name, menu=None))
        else:
            loading.new_loading_page(page=page, layout=create_adm_page_order(page, name, poste, numero, coord_initial_x, coord_initial_y))


    buttons = Buttons(page)
    back_home_button = buttons.create_button(on_click=go_back,
                                            text="Voltar",
                                            color=ft.colors.AMBER,
                                            col=12,
                                            padding=5,)
    edit_button = buttons.create_button(on_click=None,
                                            text="Editar",
                                            color=ft.colors.GREEN,
                                            col=6,
                                            padding=5,)
          

    return ft.ResponsiveRow(
        columns=12,
        controls=[
            os_forms,
            edit_button,
            back_home_button   
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
    )




def create_page_add_forms(page, name, lat, long):

    page.clean()

    def send_point(name_profile, object, image):

        lat = object.content.rows[0].cells[1].content.content.value
        long = object.content.rows[1].cells[1].content.content.value
        ip = object.content.rows[2].cells[1].content.content.value
        situ = object.content.rows[3].cells[1].content.content.value
        tipo = object.content.rows[4].cells[1].content.content.value
        pontos = object.content.rows[5].cells[1].content.content.value
        bairro = object.content.rows[6].cells[1].content.content.value
        logra = object.content.rows[7].cells[1].content.content.value
        numero = int(ip.split('-')[1])


        add_point(page, name_profile, numero, lat, long, ip, situ, tipo, pontos, bairro, logra, image=image)
     
    loading = LoadingPages(page)

    forms = Forms(page)
    forms1 = forms.create_add_forms(lat, long, ip="IP SOR-", situ=None, tipo=None, pontos=None, bairro=None, logra=None)

    buttons = Buttons(page)
    add_button = buttons.create_button(on_click=lambda e :send_point(name, forms1, image_temp.content),
                                            text="Adicionar",
                                            color=ft.colors.GREEN,
                                            col=6,
                                            padding=15,)
    back_home_button = buttons.create_button(on_click=lambda e: loading.new_loading_page(page=page, layout=create_page_home(page, name, lat, long), home=True),
                                            text="Voltar",
                                            color=ft.colors.AMBER,
                                            col=6,
                                            padding=15,)
    

    image_temp = ft.Container(col=8,
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

    photos = GalleryPicker(page, image_temp)
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
            image_temp,
            add_button, 
            back_home_button   
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,

    )


def create_page_edit_forms(page, name, poste, coord_initial_x, coord_initial_y):

    page.clean()

    def send_point(name_profile, object, image, coord_initial_x, coord_initial_y):

        lat = object.content.rows[0].cells[1].content.content.value
        long = object.content.rows[1].cells[1].content.content.value
        ip = object.content.rows[2].cells[1].content.content.value
        situ = object.content.rows[3].cells[1].content.content.value
        tipo = object.content.rows[4].cells[1].content.content.value
        pontos = object.content.rows[5].cells[1].content.content.value
        bairro = object.content.rows[6].cells[1].content.content.value
        logra = object.content.rows[7].cells[1].content.content.value

        numero_ant = poste.number

        edit_point(page, name_profile, image, coord_initial_x, coord_initial_y, lat, long, ip, situ, tipo, pontos, bairro, logra, numero_ant)
     
    loading = LoadingPages(page)

    forms = Forms(page)
    forms1 = forms.create_add_forms(poste.lat, poste.long, poste.ip, poste.situacao, poste.tipo, poste.pontos, poste.bairro, poste.logradouro)

    buttons = Buttons(page)
    add_button = buttons.create_button(on_click=lambda e :send_point(name, forms1, image_temp.content, coord_initial_x, coord_initial_y),
                                            text="Salvar",
                                            color=ft.colors.GREEN,
                                            col=6,
                                            padding=5,)
    delete_button = buttons.create_button(on_click=lambda e :delete_point(page, name, coord_initial_x, coord_initial_y, poste.number),
                                            text="Excluir",
                                            color=ft.colors.RED,
                                            col=6,
                                            padding=5,)
    back_home_button = buttons.create_button(on_click=lambda e :loading.new_loading_page(page=page, layout=create_page_home(page, name, coord_initial_x, coord_initial_y), home=True),
                                            text="Voltar",
                                            color=ft.colors.AMBER,
                                            col=7,
                                            padding=5,)
    
    sp = SupaBase(page)
    url_imagem1 = sp.get_storage(numero=poste.number)

    if url_imagem1 == "Nulo":
        initial_image = ft.Text(value="Sem Foto", color=ft.colors.BLACK)
    else:
        initial_image = ft.Image(src=url_imagem1, repeat=None)


    image_temp = ft.Container(col=8,
                            height=400,
                            expand=True,
                            image_fit=ft.ImageFit.FILL,
                            clip_behavior=ft.ClipBehavior.HARD_EDGE,
                            alignment=ft.alignment.center,
                            border=ft.Border(
                                left=ft.BorderSide(2, ft.colors.BLACK),
                                top=ft.BorderSide(2, ft.colors.BLACK),
                                right=ft.BorderSide(2, ft.colors.BLACK),
                                bottom=ft.BorderSide(2, ft.colors.BLACK),
                                ),
                            content=initial_image
                            )  

    photos = GalleryPicker(page, image_temp)
    icon_camera = ft.IconButton(
        icon=ft.icons.CAMERA_ALT,
        icon_color=ft.colors.AMBER,
        expand=True,
        scale=2.3,
        on_click=photos.open_gallery,  # Chama a função diretamente
        alignment=ft.alignment.center,
        padding=0,
    )

    return ft.ResponsiveRow(
        columns=12,
        controls=[
            forms1,
            icon_camera,
            image_temp,
            add_button,
            delete_button,
            back_home_button   
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
    )
 

def create_page_order(page, name, poste, numero, coord_initial_x, coord_initial_y):

    page.clean()

    calltexts = CallText(page)
    text1 = calltexts.create_container_calltext2(text=poste.ip)
    text2 = calltexts.create_calltext(
                      visible=True,
                      text="Qual o motivo da ordem de serviço",
                      color=ft.colors.BLACK,
                      size=30,
                      font=ft.FontWeight.W_900,
                      col=12,
                      padding=20)
    text3 = calltexts.create_calltext(
                        visible=True,
                        text="Ordem enviada com sucesso",
                        color=ft.colors.GREEN,
                        size=30,
                        font=None,
                        col=12,
                        padding=None
                        )


    checkboxes = CheckBox(page)
    box_1 = checkboxes.create_checkbox(text="Ponto apagado", size=25, on_change=None, col=12, data="Ponto apagado")
    box_2 = checkboxes.create_checkbox(text="Ponto piscando", size=25, on_change=None, col=12, data="Ponto piscando")
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
    back_forms_button = buttons.create_button(on_click=lambda e: loading.new_loading_page(page=page, layout=create_page_forms(page, name, poste, numero, coord_initial_x, coord_initial_y)),
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


def create_adm_page_order(page, name, poste, numero, coord_initial_x, coord_initial_y):

    page.clean()

    loading = LoadingPages(page)
    buttons = Buttons(page)
    textthemes = TextTheme()
    texttheme1 = textthemes.create_text_theme1()
    calltexts = CallText(page)
    text1 = calltexts.create_container_calltext2(text=poste.ip)
  

    dicio = {}


    SUPABASE_URL = "https://ipyhpxhsmyzzkvucdonu.supabase.co"
    SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImlweWhweGhzbXl6emt2dWNkb251Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3Mjc1NjQ3NDIsImV4cCI6MjA0MzE0MDc0Mn0.qA9H-UyAEx2OgihW1d_i2IjqQ5HTt1e4ITr52J5qRsA"

    headers = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}",
        "Content-Type": "application/json",
    }


    params = {
        "numero": f"eq.{numero}",
        "select": "created_at, ordem, function",
        "order": "ordem.desc"
    }

    # Requisição à API
    response = requests.get(
        f"{SUPABASE_URL}/rest/v1/ordens_postes_capeladoalto",
        headers=headers,
        params=params,
    )

    data = response.json()

    for row in data:

            data = row["created_at"]
            ordem = row["ordem"]
            function = row["function"]

            def forms(ordem):
                return lambda e: loading.new_loading_page(
                    page=page,
                    layout=create_page_os_forms(page, name, ordem, poste, numero, coord_initial_x, coord_initial_y)
                )
         

            linha = ft.DataRow(cells=[
                        ft.DataCell(ft.Text(value=data, theme_style=ft.TextThemeStyle.TITLE_LARGE, text_align=ft.TextAlign.CENTER)),
                        ft.DataCell(ft.Text(value=ordem, theme_style=ft.TextThemeStyle.TITLE_LARGE, text_align=ft.TextAlign.CENTER)),
                        ft.DataCell(ft.Text(value=function, theme_style=ft.TextThemeStyle.TITLE_LARGE, text_align=ft.TextAlign.CENTER)),
                        ft.DataCell(
                            ft.Container(content=
                                         buttons.create_icon_button(
                                                        icon=ft.icons.SEARCH,
                                                        on_click=forms(ordem),
                                                        color=ft.colors.BLUE,
                                                        col=2,
                                                        padding=0,
                                                        icon_color=ft.colors.WHITE,
                                                        ))
                        ),
                    ])

            dicio[ordem] = linha

    lista = list(dicio.values())


    
    forms2 = ft.Container(
            padding=0,
            col=12,
            theme=texttheme1,  
            content=ft.DataTable(
                data_row_max_height=50,
                width=50,
                column_spacing=10,
                columns=[
                    ft.DataColumn(ft.Text(value="Data", color=ft.colors.BLACK)),  
                    ft.DataColumn(ft.Text(value="Ordem", color=ft.colors.BLACK)),  
                    ft.DataColumn(ft.Text(value="Origem", color=ft.colors.BLACK)),  
                    ft.DataColumn(ft.Text(value="")),  
                ],
                rows=lista,
            ),
        )

    send_button = buttons.create_button(on_click=None,
                                        text="Adicionar",
                                        color=ft.colors.GREEN,
                                        col=6,
                                        padding=15,)
    back_forms_button = buttons.create_button(on_click=lambda e: loading.new_loading_page(page=page, layout=create_page_forms(page, name, poste, numero, coord_initial_x, coord_initial_y)),
                                              text="Voltar",
                                              color=ft.colors.AMBER,
                                              col=6,
                                              padding=15,
                                              width=200,
                                              )

    container1 = ft.Container(padding=10)

    return ft.ResponsiveRow(
        columns=12,
        controls=[
            container1,
            text1,  
            container1,
            send_button,
            container1,
            forms2,
            back_forms_button  
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
    )



def create_page_login(page):

    page.clean()

    web_images = Web_Image(page)
    url_imagem1 = web_images.get_image_url(name="titulo_geopostes")
    login_title = web_images.create_web_image(src=url_imagem1) 
    url_imagem2 = web_images.get_image_url(name="icone_facens")
    login_facens = web_images.create_web_image(src=url_imagem2)

    login_title.col = 12
    login_title.height = 120
    login_facens.col = 12
    login_facens.height = 70

    checkboxes = CheckBox(page)
    def visible_password(e):
        password_field.password = not password_field.password
        page.update()
    box_login = checkboxes.create_checkbox(text="Mostrar senha", size=15, on_change=visible_password, col=8)

    textfields = TextField(page)
    username_field = textfields.create_textfield(value=None, text="Usuário ou E-mail", password=False)
    password_field = textfields.create_textfield(value=None, text="Senha", password=True)

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
            container1,
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

    page.clean()

    web_images = Web_Image(page)
    url_imagem1 = web_images.get_image_url(name="titulo_geopostes")
    register_title = web_images.create_web_image(src=url_imagem1)

    register_title.col = 12 
    register_title.height = 120

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






def create_view_postes_form(page, profile_name, menu):

    textthemes = TextTheme()
    texttheme1 = textthemes.create_text_theme1() 
    buttons = Buttons(page)
    loading = LoadingPages(page)
    dicio = {}

    page.close(menu)

    SUPABASE_URL = "https://ipyhpxhsmyzzkvucdonu.supabase.co"
    SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImlweWhweGhzbXl6emt2dWNkb251Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3Mjc1NjQ3NDIsImV4cCI6MjA0MzE0MDc0Mn0.qA9H-UyAEx2OgihW1d_i2IjqQ5HTt1e4ITr52J5qRsA"

    headers = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}",
        "Content-Type": "application/json",
    }


    params = {
        "select": "number, coord_x, coord_y, name, situacao, tipo, pontos, bairro, logradouro",
        "order": "number.asc"
    }

    # Requisição à API
    response = requests.get(
        f"{SUPABASE_URL}/rest/v1/points_capeladoalto",
        headers=headers,
        params=params,
    )

    data = response.json()

    for row in data:

            number = row["number"]
            name = row["name"]
            situacao = row["situacao"]
            tipo = row["tipo"]
            pontos = row["pontos"]
            bairro = row["bairro"]
            logradouro = row["logradouro"]
            Latitude = row["coord_x"]
            Longitude = row["coord_y"]

            loading = LoadingPages(page)
            poste = Poste(number, name, situacao, tipo, pontos, bairro, logradouro, Latitude, Longitude)

            def forms(poste=poste, number=number, Latitude=Latitude, Longitude=Longitude):
                return lambda e: loading.new_loading_page(
                    page=page,
                    layout=create_page_forms(page, profile_name, poste, number, Latitude, Longitude)
                )

            def edit(poste=poste, number=number, Latitude=Latitude, Longitude=Longitude):
                return lambda e: loading.new_loading_page(
                    page=page,
                    layout=create_page_edit_forms(page, profile_name, poste, Latitude, Longitude)
                )

            def delete(poste=poste, number=number, Latitude=Latitude, Longitude=Longitude):
                return lambda e :delete_point(page, profile_name, Latitude, Longitude, number)

            linha = ft.DataRow(cells=[
                        ft.DataCell(ft.Text(value=name, theme_style=ft.TextThemeStyle.TITLE_LARGE)),
                        ft.DataCell(
                            ft.Container(content=
                                         buttons.create_icon_button(
                                                        icon=ft.icons.SEARCH,
                                                        on_click=forms(),
                                                        color=ft.colors.BLUE,
                                                        col=2,
                                                        padding=0,
                                                        icon_color=ft.colors.WHITE,
                                                        ))
                        ),
                        ft.DataCell(
                            ft.Container(content=
                                         buttons.create_icon_button(
                                                        icon=ft.icons.EDIT_ROUNDED,
                                                        on_click=edit(),
                                                        color=ft.colors.BLUE,
                                                        col=2,
                                                        padding=0,
                                                        icon_color=ft.colors.WHITE,
                                                        ))
                        ),
                        ft.DataCell(
                            ft.Container(content=
                                         buttons.create_icon_button(
                                                        icon=ft.icons.DELETE,
                                                        on_click=delete(),
                                                        color=ft.colors.BLUE,
                                                        col=2,
                                                        padding=0,
                                                        icon_color=ft.colors.WHITE,
                                                        ))
                        ),
                    ])

            dicio[number] = linha

    lista = list(dicio.values())


    forms = ft.Container(
            padding=0,
            col=12,
            theme=texttheme1,  
            content=ft.DataTable(
                data_row_max_height=50,
                width=50,
                column_spacing=0,
                columns=[
                    ft.DataColumn(ft.Text(value="")),  
                    ft.DataColumn(ft.Text(value="")),  
                    ft.DataColumn(ft.Text(value="")),  
                    ft.DataColumn(ft.Text(value="")),  
                ],
                rows=lista,
            ),
        )

    back_home_button = buttons.create_button(on_click=lambda e: loading.new_loading_page(page=page, layout=create_page_home(page, profile_name, coord_initial_x="-23.3396", coord_initial_y="-47.8238"), home=True),
                                            text="Voltar",
                                            color=ft.colors.AMBER,
                                            col=12,
                                            padding=5,)

    return ft.ResponsiveRow(
        columns=12,
        controls=[
            forms,
            back_home_button
         
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
    )


def create_view_orders_form(page, profile_name, menu):

    textthemes = TextTheme()
    texttheme1 = textthemes.create_text_theme1() 
    buttons = Buttons(page)
    loading = LoadingPages(page)
    dicio = {}

    if menu != None:
        page.close(menu)


    SUPABASE_URL = "https://ipyhpxhsmyzzkvucdonu.supabase.co"
    SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImlweWhweGhzbXl6emt2dWNkb251Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3Mjc1NjQ3NDIsImV4cCI6MjA0MzE0MDc0Mn0.qA9H-UyAEx2OgihW1d_i2IjqQ5HTt1e4ITr52J5qRsA"

    headers = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}",
        "Content-Type": "application/json",
    }


    params = {
        "select": "ip, ordem, function",
        "order": "ordem.desc"
    }

    # Requisição à API
    response = requests.get(
        f"{SUPABASE_URL}/rest/v1/ordens_postes_capeladoalto",
        headers=headers,
        params=params,
    )

    data = response.json()

    for row in data:

            ip = row["ip"]
            ordem = row["ordem"]
            function = row["function"]

            def forms(ordem):
                return lambda e: loading.new_loading_page(
                    page=page,
                    layout=create_page_os_forms(page, profile_name, ordem, poste=None, numero=None, coord_initial_x=None, coord_initial_y=None)
                )
         

            linha = ft.DataRow(cells=[
                        ft.DataCell(ft.Text(value=ip, theme_style=ft.TextThemeStyle.TITLE_LARGE, text_align=ft.TextAlign.CENTER)),
                        ft.DataCell(ft.Text(value=ordem, theme_style=ft.TextThemeStyle.TITLE_LARGE, text_align=ft.TextAlign.CENTER)),
                        ft.DataCell(ft.Text(value=function, theme_style=ft.TextThemeStyle.TITLE_LARGE, text_align=ft.TextAlign.CENTER)),
                        ft.DataCell(
                            ft.Container(content=
                                         buttons.create_icon_button(
                                                        icon=ft.icons.SEARCH,
                                                        on_click=forms(ordem),
                                                        color=ft.colors.BLUE,
                                                        col=2,
                                                        padding=0,
                                                        icon_color=ft.colors.WHITE,
                                                        ))
                        ),
                    ])

            dicio[ordem] = linha

    lista = list(dicio.values())


    forms = ft.Container(
            padding=0,
            col=12,
            theme=texttheme1,  
            content=ft.DataTable(
                data_row_max_height=50,
                width=50,
                column_spacing=10,
                columns=[
                    ft.DataColumn(ft.Text(value="")),  
                    ft.DataColumn(ft.Text(value="")),  
                    ft.DataColumn(ft.Text(value="")),  
                    ft.DataColumn(ft.Text(value="")),  
                ],
                rows=lista,
            ),
        )

    back_home_button = buttons.create_button(on_click=lambda e: loading.new_loading_page(page=page, layout=create_page_home(page, profile_name, coord_initial_x="-23.3396", coord_initial_y="-47.8238"), home=True),
                                            text="Voltar",
                                            color=ft.colors.AMBER,
                                            col=12,
                                            padding=5,)

    return ft.ResponsiveRow(
        columns=12,
        controls=[
            forms,
            back_home_button
         
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
    )


class Map:

    def __init__(self, page, name, point_location, coord_initial_x, coord_initial_y, coord_text_lat, coord_text_lon, coord_text_zoom):
        self.page = page
        self.name = name
        self.point_location = point_location
        self.coord_initial_x = coord_initial_x
        self.coord_initial_y = coord_initial_y
        self.coord_text_lat = coord_text_lat
        self.coord_text_lon = coord_text_lon
        self.coord_text_zoom = coord_text_zoom

        self.google = None

        self.MarkerLayer = None


    def create_map(self):

        markers = Marker(self.page)
        mappoints = markers.create_points(self.name)
        self.MarkerLayer = mappoints

        def handle_event(e: map.MapEvent):
            self.coord_text_lat.content.value = f"{e.center.latitude:.6f}"
            self.coord_text_lon.content.value = f"{e.center.longitude:.6f}"
            self.coord_text_zoom.content.value = f"{e.zoom:.2f}"
            self.coord_text_lat.update()
            self.coord_text_lon.update()
            self.coord_text_zoom.update()

            self.page.update()


        self.google = map.Map(
                    expand=True,  
                    configuration=map.MapConfiguration(
                        initial_center=map.MapLatitudeLongitude(self.coord_initial_x, self.coord_initial_y),  
                        initial_zoom=19,
                        on_event=handle_event,
                    ),
                    layers=[
                        map.TileLayer(
                            url_template="https://tile.openstreetmap.org/{z}/{x}/{y}.png",
                        ),
                        map.MarkerLayer(self.MarkerLayer),
                        map.RichAttribution(
                            attributions=[map.TextSourceAttribution(text="Teste")]
                        )
                    ],
                )
        

        return ft.Column(
                visible=True,
                spacing=0,
                col=12,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                        ft.Container(
                            width=420,
                            height=800,
                            alignment=ft.alignment.center,
                            bgcolor=ft.colors.GREY,
                            padding=0,
                            expand=True,
                            content=ft.Stack(
                                expand=True,
                                controls=[
                                    self.google,  
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

                ]
            )
           

    def update_position(self):

        if self.point_location.coordinates is not None:

            # Remover marcador antigo se ele já existir na camada
            if self.point_location in self.MarkerLayer:
                self.MarkerLayer.remove(self.point_location)
                self.page.update()

            # Adicionar o marcador atualizado
            else:      
                self.MarkerLayer.append(self.point_location)
                self.page.update()

            self.page.update() 
        
        else:
            None


class Marker:

    def __init__(self, page):
        self.page = page


    def create_points(self, nome_perfil):
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

            def create_on_click(poste=poste, number=number, Latitude=Latitude, Longitude=Longitude):
                return lambda e: loading.new_loading_page(
                    page=self.page,
                    layout=create_page_forms(self.page, nome_perfil, poste, number, Latitude, Longitude)
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
    sp = SupaBase(page)

    if username == "Carlos" and password == "63607120":
        page.snack_bar = ft.SnackBar(
            content=ft.Text("Administrador reconhecido"),
            bgcolor=ft.colors.GREEN,
            duration= 1000,
        )
        page.snack_bar.open = True
        loading.new_loading_page(page=page, layout=create_page_home(page, name="Carlos", coord_initial_x="-23.3396", coord_initial_y="-47.8238"), home=True)

    else:

        response = sp.get_login(username=username, password=password)

        if response.status_code == 200 and len(response.json()) > 0:
            page.snack_bar = ft.SnackBar(
            content=ft.Text("Login realizado"),
            bgcolor=ft.colors.GREEN,
            duration= 1000,
            )
            loading.new_loading_page(page=page, layout=create_page_home(page, username, coord_initial_x="-23.3396", coord_initial_y="-47.8238"), home=True)
            
        else:
            # Exibe mensagem de erro se as credenciais não forem encontradas
            page.snack_bar = ft.SnackBar(
                content=ft.Text("Login ou senha incorretos"),
                bgcolor=ft.colors.RED
            )

        page.snack_bar.open = True
        page.update()


def register(username, email, number, password1, password2, page):

    sp = SupaBase(page)

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
    
    response = sp.register(username, email, number, password1, password2)

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

    page.snack_bar.open = True
    page.update()


def add_point(page, name_profile, numero, lat, long, ip, situ, tipo, pontos, bairro, logra, image):

    sp = SupaBase(page)

    # Verificar se todos os campos estão preenchidos
    if not lat or not long or not ip or not situ or not tipo or not pontos or not bairro or not logra:
        page.snack_bar = ft.SnackBar(
            content=ft.Text("Alguns campos não foram preenchidos"),
            bgcolor=ft.colors.RED
        )
        page.snack_bar.open = True
        page.update()
        return  # Interrompe a execução da função
    
    response = sp.add_point(numero, lat, long, ip, situ, tipo, pontos, bairro, logra, image)

    # Verificar se a inserção foi bem-sucedida
    if response.status_code == 201:
        page.snack_bar = ft.SnackBar(
            content=ft.Text("Ponto adicionado com sucesso"),
            bgcolor=ft.colors.GREEN,
            duration=2500,
        )

        loading = LoadingPages(page)
        loading.new_loading_page(page=page, layout=create_page_home(page, name_profile, lat, long,), home=True)
        
    else:
        print(f"Erro ao inserir ponto: {response.status_code}")
        print(f"Resposta do erro: {response.text}")
        page.snack_bar = ft.SnackBar(
            content=ft.Text(f"Erro ao inserir ponto: {response.text}"),
            bgcolor=ft.colors.RED,
            duration=4000,
        )
 
    page.snack_bar.open = True
    page.update()


def edit_point(page, name_profile, image, coord_initial_x, coord_initial_y, lat, long, ip, situ, tipo, pontos, bairro, logra, numero_ant):

    sp = SupaBase(page)

    page.snack_bar = ft.SnackBar(
        content=ft.Text("Alterando..."),
        bgcolor=ft.colors.ORANGE,
        duration=1000,
    )
    page.snack_bar.open = True
    page.update()

    if not all([lat, long, ip, situ, tipo, pontos, bairro, logra]):
        page.snack_bar = ft.SnackBar(
            content=ft.Text("Alguns campos não foram preenchidos"),
            bgcolor=ft.colors.RED
        )
        page.snack_bar.open = True
        page.update()
        return  # Interrompe a execução da função

    response = sp.edit_point(image, lat, long, ip, situ, tipo, pontos, bairro, logra, numero_ant)
    
    if response.status_code in [200, 204]:  # 204 indica sucesso sem conteúdo
        page.snack_bar = ft.SnackBar(
            content=ft.Text("Alterações Salvas"),
            bgcolor=ft.colors.GREEN,
            duration=2000,
        )
        loading = LoadingPages(page)
        loading.new_loading_page(page=page, layout=create_page_home(page, name_profile, coord_initial_x, coord_initial_y), home=True)

    else:
        print(f"Erro ao editar ponto: {response.status_code}")
        print(f"Resposta do erro: {response.text}")
        page.snack_bar = ft.SnackBar(
            content=ft.Text(f"Erro ao editar ponto: {response.text}"),
            bgcolor=ft.colors.RED
        )


    page.snack_bar.open = True
    page.update()



def delete_point(page, name_profile, coord_initial_x, coord_initial_y, numero):

    page.snack_bar = ft.SnackBar(
        content=ft.Text("Excluindo..."),
        bgcolor=ft.colors.ORANGE,
        duration=1000,
    )
    page.snack_bar.open = True
    page.update()

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

    # Verificar se a exclusão foi bem-sucedida
    if response1.status_code == 204:

        sp = SupaBase(page)
        sp.delete_storage(numero=numero)

        page.snack_bar = ft.SnackBar(
                content=ft.Text("Ponto excluido"),
                bgcolor=ft.colors.GREEN,
                duration=2500,
            )

        loading = LoadingPages(page)
        loading.new_loading_page(page=page, layout=create_page_home(page, name_profile, coord_initial_x, coord_initial_y), home=True)

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


class SearchBar:
    def __init__(self, page):
        self.page = page
        self.list = []

        def handle_tap(e):
            self.anchor.open_view() 

        self.anchor =  ft.SearchBar(
            width=300,
            bar_bgcolor=ft.colors.WHITE,
            bar_hint_text="Procurar",
            view_hint_text="Escolha o número",
            on_change=None,
            on_submit=None,
            on_tap=handle_tap,
            controls=None,
        )

    def create_list(self, name):
        # Configuração da URL e cabeçalho
        SUPABASE_URL = "https://ipyhpxhsmyzzkvucdonu.supabase.co"
        SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImlweWhweGhzbXl6emt2dWNkb251Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3Mjc1NjQ3NDIsImV4cCI6MjA0MzE0MDc0Mn0.qA9H-UyAEx2OgihW1d_i2IjqQ5HTt1e4ITr52J5qRsA"

        headers = {
            "apikey": SUPABASE_KEY,
            "Authorization": f"Bearer {SUPABASE_KEY}",
            "Content-Type": "application/json",
        }

        # Parâmetros da requisição GET
        params = {"select": "number,coord_x,coord_y"}

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

        # Inicializa a lista de itens
        itens = []

        # Loop para criar os botões com base nas linhas da tabela
        for row in data:
            number = row["number"]
            Latitude = row["coord_x"]
            Longitude = row["coord_y"]

            loading = LoadingPages(self.page)

            # Função para criar o evento de clique com coordenadas fixas
            def create_on_click(lat=Latitude, lon=Longitude):

                return lambda e: loading.new_loading_page(
                    page=self.page,
                    layout=create_page_home(self.page, name, coord_initial_x=lat, coord_initial_y=lon),
                    home=True,
                )

            # Adiciona o botão à lista de itens
            itens.append(
                ft.ListTile(
                    title=ft.Text(f"IP SOR-{number}"),
                    on_click=create_on_click()
                )
            )

        self.list = itens
        self.anchor.controls =  self.list        

    def create_search_bar(self):

        if self.anchor.controls is not None:
            return self.anchor



                



