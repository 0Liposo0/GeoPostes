import flet as ft
from models import *
import requests
import flet.map as map
from datetime import datetime
import math
import time
import asyncio


def create_page_home(page, list_profile, list_initial_coordinates):

    page.go("/home")
    page.clean()
    page.overlay.clear()
    page.controls.clear()

    loading = LoadingPages(page)
    buttons = Buttons(page)
    menus = SettingsMenu(page)
    navigations = NavigationDrawer(page)
    chk = CheckBox(page)

    list_center_map_coordinates = [list_initial_coordinates[0], list_initial_coordinates[1], list_initial_coordinates[2], list_initial_coordinates[3], list_initial_coordinates[4], list_initial_coordinates[5]]

    navigations = NavigationDrawer(page)
    action1 = lambda e: loading.new_loading_page(page=page, layout=create_page_login(page)) 
    action2 = lambda e: loading.new_loading_page(page=page, layout=create_page_home(page, list_profile, list_center_map_coordinates))
    action3 = lambda e: loading.new_loading_page(page=page, layout=create_view_postes_form(page, list_profile, list_center_map_coordinates, menu=rightmenu)) 
    action4 = lambda e: loading.new_loading_page(page=page, layout=create_view_orders_form(page, list_profile, list_center_map_coordinates, menu=rightmenu)) 
    action5 = lambda e: loading.new_loading_page(page=page, layout=create_view_users_form(page, list_profile, list_center_map_coordinates, menu=rightmenu)) 
    rightmenu = navigations.create_navigation(list_profile, action1, action2, action3, action4, action5)
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
                coordinates=list_initial_coordinates[3],
                rotate=True, 
                )


    maps = Map(page, list_profile, point_location, list_initial_coordinates, list_center_map_coordinates)
    mapa1 = maps.create_map()
    




    def handle_position_change(e):
        point_location.coordinates = map.MapLatitudeLongitude(e.latitude, e.longitude)
        list_initial_coordinates[3] =  map.MapLatitudeLongitude(e.latitude, e.longitude)
        list_center_map_coordinates[3] = map.MapLatitudeLongitude(e.latitude, e.longitude)
        page.update() 

    gl = ft.Geolocator(
                    location_settings=ft.GeolocatorSettings(
                        accuracy=ft.GeolocatorPositionAccuracy.BEST,
                        distance_filter=1,
                    ),
                    on_position_change=handle_position_change,
                    data = 0,
                    )
    page.overlay.insert(0, gl)

    def go_to_location(e=None):
        if point_location.coordinates is not None:
            lat = str(point_location.coordinates.latitude)
            long = str(point_location.coordinates.longitude)
            list_initial_coordinates = [lat, long, list_center_map_coordinates[2], list_center_map_coordinates[3], list_center_map_coordinates[4], 18.4]
            loading.new_loading_page(page=page, layout=create_page_home(page, list_profile, list_initial_coordinates))

    async def location(e=None):

        snack_bar = ft.SnackBar(
                content=ft.Text(value="Buscando...", color=ft.colors.BLACK),
                duration=1000,
                bgcolor=ft.colors.AMBER,
            )
        page.overlay.append(snack_bar)
        snack_bar.open = True

        status = await gl.get_permission_status_async()

        if str(status) == "GeolocatorPermissionStatus.DENIED":
            await gl.request_permission_async(wait_timeout=60)
        else:
            go_to_location()

    button_location = buttons.create_call_location_button(
                                                        icon=ft.icons.MY_LOCATION,
                                                        on_click=location,
                                                        color=ft.colors.WHITE,
                                                        col=2,
                                                        padding=0,
                                                        )

    async def update_map(page, point_location, button_location, maps):

        while True:
            if point_location.coordinates is not None:
                button_location.controls[0].content.icon_color = ft.colors.GREEN
            else:
                button_location.controls[0].content.icon_color = ft.colors.RED
            maps.update_position()
            page.update()
            await asyncio.sleep(1)  

    page.run_task(update_map, page, point_location, button_location, maps)





    searchs = Search(page, list_profile, list_initial_coordinates)
    search_text_fild = searchs.create_search_text()
    search_container = searchs.create_search_container()
    search_container.visible = False

    containers = Container(page, list_profile, list_center_map_coordinates)
    map_layer_container = containers.create_maps_container()
    map_filter_container = containers.create_filter_container()
    map_layer_container.visible = False
    map_filter_container.visible = False

    def show_map_layer_container(e):
        try:
            page.overlay.pop(1)
        except:
            None
        if not map_layer_container in page.overlay:
            page.overlay.append(map_layer_container)    
            map_layer_container.visible = not map_layer_container.visible
        else:
            page.overlay.remove(map_layer_container)
            map_layer_container.visible = not map_layer_container.visible
        page.update()

    def show_filter_container(e):
        try:
            page.overlay.pop(1)
        except:
            None
        if not map_filter_container in page.overlay:
            page.overlay.append(map_filter_container)    
            map_filter_container.visible = not map_filter_container.visible
        else:
            page.overlay.remove(map_filter_container)
            map_filter_container.visible = not map_filter_container.visible
        page.update()

    button_map_layer = buttons.create_call_location_button(
                                                        icon=ft.icons.LAYERS,
                                                        on_click=show_map_layer_container,
                                                        color=ft.colors.WHITE,
                                                        col=2,
                                                        padding=0,
                                                        icon_color=ft.colors.BLUE
                                                        )
    
    button_map_filter = buttons.create_call_location_button(
                                                        icon=ft.icons.FILTER_ALT_OUTLINED,
                                                        on_click=show_filter_container,
                                                        color=ft.colors.WHITE,
                                                        col=2,
                                                        padding=0,
                                                        icon_color=ft.colors.BLUE
                                                        )

    button_map_rotate = buttons.create_call_location_button(
                                                        icon=ft.icons.ROTATE_RIGHT_OUTLINED,
                                                        on_click=lambda e: loading.new_loading_page(page=page, layout=create_page_home(page, list_profile, list_center_map_coordinates)),
                                                        color=ft.colors.WHITE,
                                                        col=2,
                                                        padding=0,
                                                        icon_color=ft.colors.BLUE
                                                        )


    page.appbar = ft.AppBar(
        bgcolor=ft.colors.BLUE,
        toolbar_height=80,
        actions=[
            ft.Column(controls=[ft.Container(width=15)]),
            search_text_fild,
            ft.Column(controls=[ft.Container(width=40)]),
            menu,
            ft.Column(controls=[ft.Container(width=15)]),
        ],
    )

    if list_profile[1] == "adm":
        page.floating_action_button = ft.FloatingActionButton(
                            content=ft.Icon(name=ft.icons.ADD_LOCATION_ROUNDED, color=ft.colors.BLUE, scale=2),
                            bgcolor=ft.colors.WHITE,
                            shape=ft.RoundedRectangleBorder(radius=50),
                            on_click= lambda e: loading.new_loading_page(page=page,
                            layout=create_page_add_forms(page, list_profile,
                            list_initial_coordinates=[list_center_map_coordinates[0], list_center_map_coordinates[1], list_center_map_coordinates[2],list_center_map_coordinates[3], list_center_map_coordinates[4], list_center_map_coordinates[5]])) 
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
                button_map_rotate,
                ft.Container(expand=True),
                ft.Container(expand=True),
                ft.Container(expand=True),
                ft.Container(expand=True),
                ft.Container(expand=True),
                button_map_filter,
                ft.Container(expand=True),
                button_map_layer
            ]
        ),
    )

  
  
    return ft.ResponsiveRow(
        columns=12,
        controls=[
                mapa1,
                ],
        alignment=ft.MainAxisAlignment.CENTER,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
    )




def create_page_forms(page, list_profile, list_initial_coordinates, name, local=False):

    page.go("/")
    page.floating_action_button = None
    page.bottom_appbar = None
    page.appbar = None
    page.clean()
    page.controls.clear()
    page.overlay.clear()

    loading = LoadingPages(page)
    forms = Forms(page)
    sp = SupaBase(page)
    buttons = Buttons(page)
      
    point = sp.get_form_post(name)
    data = point.json()
    row = data[0]
    list_post_form= [
        row["name"],
        row["situation"],
        row["type"],
        row["point"],
        row["hood"],
        row["address"]
    ]

    form = forms.create_post_form(list_post_form)

    url_imagem1 = sp.get_storage_post(name)

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
                            image=ft.Image(
                                fit=ft.ImageFit.FILL  
                                ),
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

    def go_back(e=None):
        if local ==False:
            loading.new_loading_page(page=page, layout=create_page_home(page, list_profile, list_initial_coordinates))
        else:
            loading.new_loading_page(page=page, layout=create_view_postes_form(page, list_profile, list_initial_coordinates, menu=None))       

    order_layout = lambda e: loading.new_loading_page(page=page, layout=create_invited_page_order(page, list_profile, list_initial_coordinates, name))
    if list_profile[1] == "adm":
        order_layout = lambda e: loading.new_loading_page(page=page, layout=create_adm_page_order(page, list_profile, list_initial_coordinates, name))

    order_button = buttons.create_button(on_click=order_layout,
                                            text="Ordens",
                                            color=ft.colors.RED,
                                            col=6,
                                            padding=5,)
        
    back_home_button = buttons.create_button(on_click=go_back,
                                            text="Voltar",
                                            color=ft.colors.AMBER,
                                            col=12,
                                            padding=5,)
    
    edit_button = ft.Container(height=2)
    if list_profile[1] == "adm":
        edit_button = buttons.create_button(on_click=lambda e: loading.new_loading_page(page=page, layout=create_page_edit_forms(page, list_profile, list_initial_coordinates, name)),
                                                text="Editar",
                                                color=ft.colors.GREEN,
                                                col=6,
                                                padding=5,)    
        

    return ft.ResponsiveRow(
        columns=12,
        controls=[
            form,
            foto_poste,  
            order_button,
            edit_button,
            back_home_button   
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
    )

def create_page_os_forms(page, list_profile, list_initial_coordinates, name, order):

    page.go("/")
    page.floating_action_button = None
    page.bottom_appbar = None
    page.appbar = None
    page.clean()
    page.controls.clear()
    page.overlay.clear()

    loading = LoadingPages(page)
    forms = Forms(page)
    sp = SupaBase(page)


    os = sp.get_os(order)

    data = os.json()

    row = data[0]

    data_criacao = row["created_at"]
    ip = row["ip"]
    reclamante = row["reclamante"]
    function = row["function"]
    celular = row["celular"]
    order = row["order_id"]
    origem = row["origem"]
    obser = row["observacao"]
    materiais = row["materiais"]
    ponto = row["ponto"]
    status = row["status"]
    data_andamen = row["data_andamento"]
    data_conclu = row["data_conclusao"]
    equipe = row["equipe"]
    

    os_forms = forms.create_os_forms(data_criacao, ip, reclamante, function, celular, order, origem, obser, materiais, ponto, status, data_andamen, data_conclu, equipe)


    def go_back(e=None):
        if name == None:
            loading.new_loading_page(page=page, layout=create_view_orders_form(page, list_profile, list_initial_coordinates, menu=None))
        else:
            loading.new_loading_page(page=page, layout=create_adm_page_order(page, list_profile, list_initial_coordinates, name))


    buttons = Buttons(page)
    back_home_button = buttons.create_button(on_click=go_back,
                                            text="Voltar",
                                            color=ft.colors.AMBER,
                                            col=12,
                                            padding=5,)
    edit_button = buttons.create_button(on_click=lambda e: loading.new_loading_page(page=page, layout=create_page_edit_os_forms(page, list_profile, list_initial_coordinates, name, order)),
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

def create_page_user_forms(page, list_profile, list_initial_coordinates, user):

    page.go("/")
    page.floating_action_button = None
    page.bottom_appbar = None
    page.appbar = None
    page.clean()
    page.controls.clear()
    page.overlay.clear()

    loading = LoadingPages(page)
    forms = Forms(page)
    sp = SupaBase(page)
    buttons = Buttons(page)
     
    user_data = sp.get_form_user(user)
    data = user_data.json()
    row = data[0]
    list_user_form = [
        row["user_id"],
        row["usuario"],
        row["email"],
        row["numero"],
        row["senha"],
        row["permission"]
    ]

    form = forms.create_user_form(list_user_form)


    back_home_button = buttons.create_button(on_click= lambda e: loading.new_loading_page(page=page, layout=create_view_users_form(page, list_profile, list_initial_coordinates, menu=None)),
                                            text="Voltar",
                                            color=ft.colors.AMBER,
                                            col=12,
                                            padding=5,)
    

    edit_button = buttons.create_button(on_click=lambda e: loading.new_loading_page(page=page, layout=create_page_edit_user_forms(page, list_profile, list_initial_coordinates, user)),
                                            text="Editar",
                                            color=ft.colors.GREEN,
                                            col=6,
                                            padding=5,)    
        

    return ft.ResponsiveRow(
        columns=12,
        controls=[
            form,
            edit_button,
            back_home_button   
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
    )



def create_page_add_forms(page, list_profile, list_initial_coordinates):

    page.go("/")
    page.floating_action_button = None
    page.bottom_appbar = None
    page.appbar = None
    page.clean()
    page.controls.clear()
    page.overlay.clear()

    loading = LoadingPages(page)
    forms = Forms(page)
    buttons = Buttons(page)
    sp = SupaBase(page)

    def send_point(object, image):

        snack_bar = ft.SnackBar(
                        content=ft.Text(f"Adicionando..."),
                        bgcolor=ft.colors.AMBER,
                        duration=1000,
                    )
        page.overlay.append(snack_bar)
        snack_bar.open = True
        page.update()

        time.sleep(1)

        if image_temp.content != None:
            angle = int(image_temp.content.rotate.angle * (180 / math.pi) if image_temp.content.rotate else 0)
        else:
            angle = None


        list_forms = [
                object.content.rows[0].cells[1].content.content.value,
                object.content.rows[1].cells[1].content.content.value,
                object.content.rows[2].cells[1].content.content.value,
                object.content.rows[3].cells[1].content.content.value,
                object.content.rows[4].cells[1].content.content.value,
                object.content.rows[5].cells[1].content.content.value,
        ]


        add_point(page, list_profile, list_initial_coordinates, list_forms, image=image, angle=angle)
     
    new_number = sp.get_last_form_post()

    forms1 = forms.create_add_forms(ip=new_number, situ=None, tipo=None, pontos=None, bairro=".", logra=".")

    add_button = buttons.create_button(on_click=lambda e :send_point(forms1, image_temp.content),
                                            text="Adicionar",
                                            color=ft.colors.GREEN,
                                            col=6,
                                            padding=15,)
    back_home_button = buttons.create_button(on_click=lambda e: loading.new_loading_page(page=page, layout=create_page_home(page, list_profile, list_initial_coordinates)),
                                            text="Voltar",
                                            color=ft.colors.AMBER,
                                            col=6,
                                            padding=15,)
    





    image_temp = ft.Container(col=8,
                                  height=400,
                                  expand=True,
                                  clip_behavior=ft.ClipBehavior.HARD_EDGE,
                                  alignment=ft.alignment.center,
                                    border=ft.Border(
                                        left=ft.BorderSide(2, ft.colors.BLACK),
                                        top=ft.BorderSide(2, ft.colors.BLACK),
                                        right=ft.BorderSide(2, ft.colors.BLACK),
                                        bottom=ft.BorderSide(2, ft.colors.BLACK),
                                        ),
                                    content=None
                                  )




    def on_image_selected(e: ft.FilePickerResultEvent):

            if not e.files or len(e.files) == 0:
                return
            snack_bar = ft.SnackBar(
                content=ft.Text(value="Adicionando imagem...", color=ft.colors.BLACK),
                duration=2000,
                bgcolor=ft.colors.AMBER,
            )
            page.overlay.append(snack_bar)
            snack_bar.open = True

            selected_image = e.files[0]

            image_container = ft.Image(src=selected_image.path, col=8) 

            image_temp.content = image_container

            page.update()

    fp = ft.FilePicker(on_result=on_image_selected)
    if fp in page.overlay:
        page.overlay.remove(fp)
    page.overlay.append(fp)

    def open_gallery(e): 
        fp.pick_files(              
            allow_multiple=False,
            file_type=ft.FilePickerFileType.IMAGE
        )

    icon_camera = ft.IconButton(
        icon=ft.icons.CAMERA_ALT,
        icon_color=ft.colors.AMBER,
        expand=True,
        scale=2,
        on_click=open_gallery,  
        alignment=ft.alignment.center,
        padding=0,
    )

    def rotate(e):
        if hasattr(image_temp.content, 'rotate'):

            # Obtemos o ângulo atual em graus, assumindo 0 se não estiver definido
            current_angle_degrees = image_temp.content.rotate.angle * (180 / math.pi) if image_temp.content.rotate else 0
            # Adicionamos 90 graus ao ângulo atual
            new_angle_degrees = (current_angle_degrees + 90) % 360
            # Define a rotação com o novo ângulo em radianos
            image_temp.content.rotate = ft.transform.Rotate(math.radians(new_angle_degrees))

            angle = new_angle_degrees

            page.update()

    icon_rotate = ft.IconButton(
        icon=ft.icons.ROTATE_RIGHT_OUTLINED,
        icon_color=ft.colors.AMBER,
        expand=True,
        scale=1.5,
        on_click=rotate, 
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
            icon_rotate,
            add_button, 
            back_home_button   
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,

    )

def create_page_add_os_forms(page, list_profile, list_initial_coordinates, name):

    page.go("/")
    page.floating_action_button = None
    page.bottom_appbar = None
    page.appbar = None
    page.clean()
    page.controls.clear()
    page.overlay.clear()

    loading = LoadingPages(page)
    forms = Forms(page)
    buttons = Buttons(page)
    sp = SupaBase(page)
    
    def send_point(object):

        list_add_os = [
            object.content.rows[0].cells[1].content.content.value,
            object.content.rows[1].cells[1].content.content.value,
            object.content.rows[2].cells[1].content.content.value,
            object.content.rows[3].cells[1].content.content.value,
            object.content.rows[4].cells[1].content.content.value,
            object.content.rows[5].cells[1].content.content.value,
            object.content.rows[6].cells[1].content.content.value,
            object.content.rows[7].cells[1].content.content.value,
            object.content.rows[8].cells[1].content.content.value,
            object.content.rows[9].cells[1].content.content.value,
            object.content.rows[10].cells[1].content.content.value,
            object.content.rows[11].cells[1].content.content.value,
            object.content.rows[12].cells[1].content.content.value,
            object.content.rows[13].cells[1].content.content.value,
        ]
        
        add_os(page, list_profile, list_initial_coordinates, list_add_os, name)

    data_atual = datetime.now()
    data_formatada = data_atual.strftime("%d/%m/%Y")
    id = str(sp.get_os_id())
    new_order = id.zfill(4)





    list_os_forms = [data_formatada, name, list_profile[0], list_profile[1], list_profile[2], new_order, None, None, None, None, "Aberto", "Pendente", "Pendente", None]

    forms1 = forms.create_add_os_forms(list_os_forms)

    add_button = buttons.create_button(on_click=lambda e :send_point(forms1),
                                            text="Adicionar",
                                            color=ft.colors.GREEN,
                                            col=6,
                                            padding=15,)
    
    back_home_button = buttons.create_button(on_click=lambda e: loading.new_loading_page(page=page, layout=create_adm_page_order(page, list_profile, list_initial_coordinates, name)),
                                            text="Voltar",
                                            color=ft.colors.AMBER,
                                            col=6,
                                            padding=15,)
    
    return ft.ResponsiveRow(
        columns=12,
        controls=[
            forms1,
            add_button, 
            back_home_button   
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,

    )

def create_page_add_user_forms(page, list_profile, list_initial_coordinates):

    page.go("/")
    page.floating_action_button = None
    page.bottom_appbar = None
    page.appbar = None
    page.clean()
    page.controls.clear()
    page.overlay.clear()

    loading = LoadingPages(page)
    forms = Forms(page)
    buttons = Buttons(page)
    sp = SupaBase(page)

    
    def send_point(object, id):

        list_add_user = [
            object.content.rows[0].cells[1].content.content.value,
            object.content.rows[1].cells[1].content.content.value,
            object.content.rows[2].cells[1].content.content.value,
            object.content.rows[3].cells[1].content.content.value,
            object.content.rows[4].cells[1].content.content.value,
        ]
        
        add_user(page, list_profile, list_initial_coordinates, list_add_user, id)

    id = str(sp.get_user_id())

    list_os_forms = [None, None, None, None, None]

    forms1 = forms.create_add_user_forms(list_os_forms, new=True)

    add_button = buttons.create_button(on_click=lambda e :send_point(forms1, id),
                                            text="Adicionar",
                                            color=ft.colors.GREEN,
                                            col=6,
                                            padding=15,)
    
    back_home_button = buttons.create_button(on_click=lambda e: loading.new_loading_page(page=page, layout=create_view_users_form(page, list_profile, list_initial_coordinates, menu=None)),
                                            text="Voltar",
                                            color=ft.colors.AMBER,
                                            col=6,
                                            padding=15,)
    
    return ft.ResponsiveRow(
        columns=12,
        controls=[
            forms1,
            add_button, 
            back_home_button   
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,

    )



def create_page_edit_forms(page, list_profile, list_initial_coordinates, name, local=False):

    page.go("/")
    page.floating_action_button = None
    page.bottom_appbar = None
    page.appbar = None
    page.clean()
    page.controls.clear()
    page.overlay.clear()

    forms = Forms(page)
    loading = LoadingPages(page)
    sp = SupaBase(page)
    buttons = Buttons(page)

    def send_point(list_profile, object, image, list_initial_coordinates):

        list_forms = [
            object.content.rows[0].cells[1].content.content.value,
            object.content.rows[1].cells[1].content.content.value,
            object.content.rows[2].cells[1].content.content.value,
            object.content.rows[3].cells[1].content.content.value,
            object.content.rows[4].cells[1].content.content.value,
            object.content.rows[5].cells[1].content.content.value,
        ]

        edit_point(page, list_profile, list_initial_coordinates, list_forms, image, row)

    form = sp.get_form_post(name)
    data = form.json()
    row = data[0]
    numero = int(row["name"].split('-')[1])
    forms1 = forms.create_add_forms(numero, row["situation"], row["type"], row["point"], row["hood"], row["address"])

    def go_back(e=None):
        if local ==False:
            loading.new_loading_page(page=page, layout=create_page_forms(page, list_profile, list_initial_coordinates, name))
        else:
            loading.new_loading_page(page=page, layout=create_view_postes_form(page, list_profile, list_initial_coordinates, menu=None))

    add_button = buttons.create_button(on_click=lambda e :send_point(list_profile, forms1, image_temp.content, list_initial_coordinates),
                                            text="Salvar",
                                            color=ft.colors.GREEN,
                                            col=6,
                                            padding=5,)
    delete_button = buttons.create_button(on_click=lambda e :delete_point(page, list_profile, list_initial_coordinates, name),
                                            text="Excluir",
                                            color=ft.colors.RED,
                                            col=6,
                                            padding=5,)
    back_home_button = buttons.create_button(on_click=go_back,
                                            text="Voltar",
                                            color=ft.colors.AMBER,
                                            col=7,
                                            padding=5,)
    
    url_imagem1 = sp.get_storage_post(name)
    if url_imagem1 == "Nulo":
        initial_image = ft.Text(value="Sem Foto", color=ft.colors.BLACK, data= "semfoto")
    else:
        initial_image = ft.Image(src=url_imagem1, repeat=None, data="foto")
    image_temp = ft.Container(col=8,
                            height=400,
                            expand=True,
                            clip_behavior=ft.ClipBehavior.HARD_EDGE,
                            alignment=ft.alignment.center,
                            border=ft.Border(
                                left=ft.BorderSide(2, ft.colors.BLACK),
                                top=ft.BorderSide(2, ft.colors.BLACK),
                                right=ft.BorderSide(2, ft.colors.BLACK),
                                bottom=ft.BorderSide(2, ft.colors.BLACK),
                                ),
                            content=initial_image,
                            )  

    def on_image_selected(e: ft.FilePickerResultEvent):

            if not e.files or len(e.files) == 0:
                return
            snack_bar = ft.SnackBar(
                content=ft.Text(value="Adicionando imagem...", color=ft.colors.BLACK),
                duration=2000,
                bgcolor=ft.colors.AMBER,
            )
            page.overlay.append(snack_bar)
            snack_bar.open = True

            selected_image = e.files[0]

            image_container = ft.Image(src=selected_image.path, col=8, data="foto") 

            image_temp.content = image_container

            page.update()

    fp = ft.FilePicker(on_result=on_image_selected)
    if fp in page.overlay:
        page.overlay.remove(fp)
    page.overlay.append(fp)

    def open_gallery(e): 
        fp.pick_files(              
            allow_multiple=False,
            file_type=ft.FilePickerFileType.IMAGE
        )

    icon_camera = ft.IconButton(
        icon=ft.icons.CAMERA_ALT,
        icon_color=ft.colors.AMBER,
        expand=True,
        scale=2.3,
        on_click=open_gallery,  # Chama a função diretamente
        alignment=ft.alignment.center,
        padding=0,
    )

    def rotate(e):
        if hasattr(image_temp.content, 'rotate'):
            # Obtemos o ângulo atual em graus, assumindo 0 se não estiver definido
            current_angle_degrees = image_temp.content.rotate.angle * (180 / math.pi) if image_temp.content.rotate else 0
            # Adicionamos 90 graus ao ângulo atual
            new_angle_degrees = (current_angle_degrees + 90) % 360
            # Define a rotação com o novo ângulo em radianos
            image_temp.content.rotate = ft.transform.Rotate(math.radians(new_angle_degrees))
            page.update()


    icon_rotate = ft.IconButton(
        icon=ft.icons.ROTATE_RIGHT_OUTLINED,
        icon_color=ft.colors.AMBER,
        expand=True,
        scale=1.5,
        on_click=rotate, 
        alignment=ft.alignment.center,
        padding=0,
    )

    return ft.ResponsiveRow(
        columns=12,
        controls=[
            forms1,
            icon_camera,
            image_temp,
            icon_rotate,
            add_button,
            delete_button,
            back_home_button   
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
    )

def create_page_edit_os_forms(page, list_profile, list_initial_coordinates, name, order):

    page.go("/")
    page.floating_action_button = None
    page.bottom_appbar = None
    page.appbar = None
    page.clean()
    page.controls.clear()
    page.overlay.clear()

    loading = LoadingPages(page)
    forms = Forms(page)
    buttons = Buttons(page)
    sp = SupaBase(page)

    def send_point(list_profile, object, list_initial_coordinates):

        list_edited_os_forms = [
            object.content.rows[0].cells[1].content.content.value,
            object.content.rows[1].cells[1].content.content.value,
            object.content.rows[2].cells[1].content.content.value,
            object.content.rows[3].cells[1].content.content.value,
            object.content.rows[4].cells[1].content.content.value,
            object.content.rows[5].cells[1].content.content.value,
            object.content.rows[6].cells[1].content.content.value,
            object.content.rows[7].cells[1].content.content.value,
            object.content.rows[8].cells[1].content.content.value,
            object.content.rows[9].cells[1].content.content.value,
            object.content.rows[10].cells[1].content.content.value,
            object.content.rows[11].cells[1].content.content.value,
            object.content.rows[12].cells[1].content.content.value,
            object.content.rows[13].cells[1].content.content.value,
        ]

        edit_os(page, list_profile, list_initial_coordinates, list_edited_os_forms, order, name)
     

    os = sp.get_os(order)

    data = os.json()

    row = data[0]

    data_criacao = row["created_at"]
    ip = row["ip"]
    reclamante = row["reclamante"]
    function = row["function"]
    celular = row["celular"]
    order = row["order_id"]
    origem = row["origem"]
    obser = row["observacao"]
    materiais = row["materiais"]
    ponto = row["ponto"]
    status = row["status"]
    data_andamen = row["data_andamento"]
    data_conclu = row["data_conclusao"]
    equipe = row["equipe"]

    list_os_forms = [data_criacao, ip, reclamante, function, celular, order, origem, obser, materiais, ponto, status, data_andamen, data_conclu, equipe]

    forms1 = forms.create_add_os_forms(list_os_forms)


    add_button = buttons.create_button(on_click=lambda e :send_point(list_profile, forms1, list_initial_coordinates),
                                            text="Salvar",
                                            color=ft.colors.GREEN,
                                            col=6,
                                            padding=5,)
    delete_button = buttons.create_button(on_click=lambda e :delete_os(page, list_profile, list_initial_coordinates, name, order),
                                            text="Excluir",
                                            color=ft.colors.RED,
                                            col=6,
                                            padding=5,)
    back_home_button = buttons.create_button(on_click=lambda e :loading.new_loading_page(page=page, layout=create_page_os_forms(page, list_profile, list_initial_coordinates, name, order)),
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

def create_page_edit_user_forms(page, list_profile, list_initial_coordinates, user):

    page.go("/")
    page.floating_action_button = None
    page.bottom_appbar = None
    page.appbar = None
    page.clean()
    page.controls.clear()
    page.overlay.clear()

    loading = LoadingPages(page)
    forms = Forms(page)
    buttons = Buttons(page)
    sp = SupaBase(page)

    def send_point(list_profile, list_initial_coordinates, object, previus_user):

        list_edited_user_forms = [
            object.content.rows[0].cells[1].content.content.value,
            object.content.rows[1].cells[1].content.content.value,
            object.content.rows[2].cells[1].content.content.value,
            object.content.rows[3].cells[1].content.content.value,
            object.content.rows[4].cells[1].content.content.value,
        ]

        edit_user(page, list_profile, list_initial_coordinates, list_edited_user_forms, previus_user)
     

    user_data = sp.get_form_user(user)

    data = user_data.json()

    row = data[0]

    list_user_forms = [
        row["usuario"],
        row["email"],
        row["numero"],
        row["senha"],
        row["permission"],
    ]

    forms1 = forms.create_add_user_forms(list_user_forms)


    add_button = buttons.create_button(on_click=lambda e :send_point(list_profile, list_initial_coordinates, forms1, list_user_forms[0]),
                                            text="Salvar",
                                            color=ft.colors.GREEN,
                                            col=6,
                                            padding=5,)
    delete_button = buttons.create_button(on_click=lambda e :delete_user(page, list_profile, list_initial_coordinates, user),
                                            text="Excluir",
                                            color=ft.colors.RED,
                                            col=6,
                                            padding=5,)
    back_home_button = buttons.create_button(on_click=lambda e: loading.new_loading_page(page=page,layout=create_page_user_forms(page, list_profile, list_initial_coordinates, user)),
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
 


def create_invited_page_order(page, list_profile, list_initial_coordinates, name):

    page.go("/")
    page.floating_action_button = None
    page.bottom_appbar = None
    page.appbar = None
    page.clean()
    page.controls.clear()
    page.overlay.clear()

    loading = LoadingPages(page)
    calltexts = CallText(page)
    buttons = Buttons(page)
    checkboxes = CheckBox(page)
    sp = SupaBase(page)


    text1 = calltexts.create_container_calltext2(text=name)
    text2 = calltexts.create_calltext(
                      visible=True,
                      text="Qual o motivo da order de serviço",
                      color=ft.colors.BLACK,
                      size=30,
                      font=ft.FontWeight.W_900,
                      col=12,
                      padding=20)
    text3 = calltexts.create_calltext(
                        visible=True,
                        text="order enviada com sucesso",
                        color=ft.colors.GREEN,
                        size=30,
                        font=None,
                        col=12,
                        padding=None
                        )


    def checkbox_changed(e):
        for box in all_checkboxes:
            if box.controls[0].data != e.control.data:  
                box.controls[0].value = False
        page.update() 

    def send_order(e):
        for box in all_checkboxes:
            if box.controls[0].value == True:
                url = sp.get_url()
                key = sp.get_key()
                id = str(sp.get_os_id())
                new_order = id.zfill(4)
                data_atual = datetime.now()
                data_formatada = data_atual.strftime("%d/%m/%Y")
                numero = int(name.split('-')[1])

                headers = {
                    "apikey": key,
                    "Authorization": f"Bearer {key}",
                    "Content-Type": "application/json",
                }

                data={
                    "created_at": data_formatada,
                    "ip": name,
                    "numero": numero,
                    "reclamante": list_profile[0],
                    "function": "Convidado",
                    "celular": list_profile[2],
                    "order_id": new_order,
                    "origem": "Público",
                    "observacao": box.controls[0].data,
                    "materiais": ".",
                    "ponto": ".",
                    "status": "Aberto",
                    "data_andamento": ".",
                    "data_conclusao": ".",
                    "equipe": ".",
                }

                response = requests.post(
                    f"{url}/rest/v1/ordens_postes_capeladoalto",
                    headers=headers,
                    json=data,
                )


                if response.status_code == 201:
                    snack_bar = ft.SnackBar(
                        content=ft.Text("order enviada com sucesso"),
                        bgcolor=ft.colors.GREEN,
                        duration=2500,
                    )
                    loading.new_loading_page(page=page, layout=create_page_home(page, list_profile, list_initial_coordinates))
                else:
                    print(f"Resposta do erro: {response.text}")
                    snack_bar = ft.SnackBar(
                        content=ft.Text("Erro ao enviar ordem"),
                        bgcolor=ft.colors.RED,
                        duration=2500,
                    )

            elif all(box.controls[0].value == False for box in all_checkboxes):
                snack_bar = ft.SnackBar(
                    content=ft.Text("Nenhuma ordem selecionada"),
                    bgcolor=ft.colors.AMBER,
                    duration=2500,
                )
        page.overlay.append(snack_bar)
        snack_bar.open = True
        page.update()


    all_checkboxes = [
        checkboxes.create_checkbox(text="Ponto apagado", size=25, on_change=checkbox_changed, col=12, data="Ponto apagado"),
        checkboxes.create_checkbox(text="Ponto piscando", size=25, on_change=checkbox_changed, col=12, data="Ponto piscando"),
        checkboxes.create_checkbox(text="Ponto aceso durante o dia", size=25, on_change=checkbox_changed, col=12, data="Ponto aceso durante o dia"),
        checkboxes.create_checkbox(text="Rachadura", size=25, on_change=checkbox_changed, col=12, data="Rachadura"),
        checkboxes.create_checkbox(text="Queda", size=25, on_change=checkbox_changed, col=12, data="Queda"),
        checkboxes.create_checkbox(text="Incêndio elétrico", size=25, on_change=checkbox_changed, col=12, data="Incêndio elétrico"),
        checkboxes.create_checkbox(text="Adicionar ponto", size=25, on_change=checkbox_changed, col=12, data="Adicionar ponto"),
    ]


    send_button = buttons.create_button(on_click=send_order,
                                        text="Enviar",
                                        color=ft.colors.GREEN,
                                        col=6,
                                        padding=15,)
    back_forms_button = buttons.create_button(on_click=lambda e: loading.new_loading_page(page=page, layout=create_page_forms(page, list_profile, list_initial_coordinates, name)),
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
            *all_checkboxes,
            send_button,
            back_forms_button  
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
    )

def create_adm_page_order(page, list_profile, list_initial_coordinates, name):

    page.go("/")
    page.floating_action_button = None
    page.bottom_appbar = None
    page.appbar = None
    page.clean()
    page.controls.clear()
    page.overlay.clear()

    loading = LoadingPages(page)
    buttons = Buttons(page)
    textthemes = TextTheme()
    texttheme1 = textthemes.create_text_theme1()
    calltexts = CallText(page)
    sp = SupaBase(page)

    text1 = calltexts.create_container_calltext2(text=name)
  
    dicio = {}

    url = sp.get_url()
    key = sp.get_key()

    headers = {
        "apikey": key,
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json",
    }


    params = {
        "ip": f"eq.{name}",
        "select": "created_at, order_id, function",
        "order": "order_id.desc"
    }

    # Requisição à API
    response = requests.get(
        f"{url}/rest/v1/ordens_postes_capeladoalto",
        headers=headers,
        params=params,
    )

    data = response.json()

    for row in data:

            data = row["created_at"]
            order = row["order_id"]
            function = row["function"]

            def forms(order):
                return lambda e: loading.new_loading_page(
                    page=page,
                    layout=create_page_os_forms(page, list_profile, list_initial_coordinates, name, order)
                )
         

            linha = ft.DataRow(cells=[
                        ft.DataCell(ft.Text(value=data, theme_style=ft.TextThemeStyle.TITLE_LARGE, text_align=ft.TextAlign.CENTER)),
                        ft.DataCell(ft.Text(value=order, theme_style=ft.TextThemeStyle.TITLE_LARGE, text_align=ft.TextAlign.CENTER)),
                        ft.DataCell(ft.Text(value=function, theme_style=ft.TextThemeStyle.TITLE_LARGE, text_align=ft.TextAlign.CENTER)),
                        ft.DataCell(
                            ft.Container(content=
                                         buttons.create_icon_button(
                                                        icon=ft.icons.SEARCH,
                                                        on_click=forms(order),
                                                        color=ft.colors.BLUE,
                                                        col=2,
                                                        padding=0,
                                                        icon_color=ft.colors.WHITE,
                                                        ))
                        ),
                    ])

            dicio[order] = linha

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
                    ft.DataColumn(ft.Text(value="order", color=ft.colors.BLACK)),  
                    ft.DataColumn(ft.Text(value="Origem", color=ft.colors.BLACK)),  
                    ft.DataColumn(ft.Text(value="")),  
                ],
                rows=lista,
            ),
        )

    send_button = buttons.create_button(on_click=lambda e: loading.new_loading_page(page=page, layout=create_page_add_os_forms(page, list_profile, list_initial_coordinates, name)),
                                        text="Adicionar",
                                        color=ft.colors.GREEN,
                                        col=6,
                                        padding=15,)
    back_forms_button = buttons.create_button(on_click=lambda e: loading.new_loading_page(page=page, layout=create_page_forms(page, list_profile, list_initial_coordinates, name)),
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

    page.go("/")
    page.floating_action_button = None
    page.bottom_appbar = None
    page.appbar = None
    page.clean()
    page.controls.clear()
    page.overlay.clear()

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
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
    )

def create_page_register(page):

    page.go("/")
    page.floating_action_button = None
    page.bottom_appbar = None
    page.appbar = None
    page.clean()
    page.controls.clear()
    page.overlay.clear()

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



def create_view_postes_form(page, list_profile, list_initial_coordinates, menu):

    page.go("/")
    page.floating_action_button = None
    page.bottom_appbar = None
    page.appbar = None
    page.clean()
    page.controls.clear()
    page.overlay.clear()

    textthemes = TextTheme()
    texttheme1 = textthemes.create_text_theme1() 
    buttons = Buttons(page)
    loading = LoadingPages(page)
    sp = SupaBase(page)
    chk = CheckBox(page)

    dicio_filter = {
        "name_filter" : "like.*",
        "situation_filter" : "like.*",
        "type_filter" : "like.*"
    }
    dicio = {}

    def changesearch(e, filter, dicio, forms1):


        try:
            if e.control.value.strip() == "":
                dicio_filter["name_filter"] = "like.*"  
            else:
                dicio_filter["name_filter"] = f"ilike.%{e.control.value.strip().lower()}%"
        except:
            dicio_filter["name_filter"] = "like.*"

   
        params["name"] = dicio_filter["name_filter"]
        params["situation"] = dicio_filter["situation_filter"]
        params["type"] = dicio_filter["type_filter"]

        # Faz uma nova requisição com o filtro atualizado
        response = requests.get(
            f"{url}/rest/v1/form_post_capela",
            headers=headers,
            params=params,
        )

        if response.status_code == 200:
            data = response.json()

            # Reconstrói as linhas da tabela
            dicio.clear()
            for row in data:
                name = row["name"]
                number = int(name.split('-')[1])

                def forms(name=name):
                    return lambda e: loading.new_loading_page(
                        page=page,
                        layout=create_page_forms(page, list_profile, list_initial_coordinates, name, local=True)
                    )

                def edit(name=name):
                    return lambda e: loading.new_loading_page(
                        page=page,
                        layout=create_page_edit_forms(page, list_profile, list_initial_coordinates, name, local=True)
                    )

                def delete(name=name):
                    return lambda e: delete_point(page, list_profile, list_initial_coordinates, name)

                linha = ft.DataRow(cells=[
                    ft.DataCell(ft.Text(value=name, theme_style=ft.TextThemeStyle.TITLE_LARGE)),
                    ft.DataCell(
                        ft.Container(content=buttons.create_icon_button(
                            icon=ft.icons.SEARCH,
                            on_click=forms(),
                            color=ft.colors.BLUE,
                            col=2,
                            padding=0,
                            icon_color=ft.colors.WHITE,
                        ))
                    ),
                    ft.DataCell(
                        ft.Container(content=buttons.create_icon_button(
                            icon=ft.icons.EDIT_ROUNDED,
                            on_click=edit(),
                            color=ft.colors.BLUE,
                            col=2,
                            padding=0,
                            icon_color=ft.colors.WHITE,
                        ))
                    ),
                    ft.DataCell(
                        ft.Container(content=buttons.create_icon_button(
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

            # Atualiza as linhas no DataTable
            forms1.content.rows = list(dicio.values())
            page.update()
        else:
            print(f"Erro ao buscar dados: {response.text}")


    if menu:
        page.close(menu)

    url = sp.get_url()
    key = sp.get_key()

    headers = {
        "apikey": key,
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json",
    }


    params = {
        "select": "name, situation, type",
        "name": dicio_filter["name_filter"],
        "situation": dicio_filter["situation_filter"],
        "type": dicio_filter["type_filter"],
        "order": "name.asc",
    }

    response = requests.get(
        f"{url}/rest/v1/form_post_capela",
        headers=headers,
        params=params,
    )

    data = response.json()

    for row in data:

            name = row["name"]

            number = int(name.split('-')[1])
           
            def forms(name=name):
                return lambda e: loading.new_loading_page(
                    page=page,
                    layout=create_page_forms(page, list_profile, list_initial_coordinates, name, local=True)
                )

            def edit(name=name):
                return lambda e: loading.new_loading_page(
                    page=page,
                    layout=create_page_edit_forms(page, list_profile, list_initial_coordinates, name, local=True)
                )

            def delete(name=name):
                return lambda e :delete_point(page, list_profile, list_initial_coordinates, name)

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


    forms1 = ft.Container(
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
    
    def show_filter_container(e):
        filter_container.visible = not filter_container.visible
        page.update()

    def get_permission_filter(e):
        led_type = filter_container.content.controls[0].controls[0].value
        led_type_data = filter_container.content.controls[0].controls[0].data
        sodium_type = filter_container.content.controls[1].controls[0].value
        sodium_type_data = filter_container.content.controls[1].controls[0].data
        null_type = filter_container.content.controls[2].controls[0].value
        null_type_data = filter_container.content.controls[2].controls[0].data
        if led_type:
            dicio_filter["type_filter"] = f"eq.{led_type_data}"
        if sodium_type:
            dicio_filter["type_filter"] = f"eq.{sodium_type_data}"
        if led_type and sodium_type:
            dicio_filter["type_filter"] = f"neq.{null_type_data}"
        if null_type:
            dicio_filter["type_filter"] = f"eq.{null_type_data}"
        if null_type and led_type:
            dicio_filter["type_filter"] = f"neq.{sodium_type_data}"
        if null_type and sodium_type:
            dicio_filter["type_filter"] = f"neq.{led_type_data}"
        if led_type and sodium_type and null_type:
            dicio_filter["type_filter"] = f"like.*"
        filter_container.visible = not filter_container.visible
        page.update()
        changesearch(e, dicio_filter, dicio, forms1),



    filter_container = ft.Container(
            bgcolor=ft.colors.BLUE,
            padding=10,
            margin=10,
            height=250,
            border_radius=20,
            col=10,
            visible=False,
            content=ft.Column([
                chk.create_checkbox2("Lâmpada LED", 15, None, 8,"Lâmpada LED", True),
                chk.create_checkbox2("Lâmpada de vapor de sódio", 15, None, 8,"Lâmpada de vapor de sódio", True),
                chk.create_checkbox2("Sem iluminação", 15, None, 8,".", True),
                buttons.create_button(on_click=lambda e: get_permission_filter(e),
                                            text="Aplicar",
                                            color=ft.colors.AMBER,
                                            col=12,
                                            padding=5,)
                ])
            )

    back_home_button = buttons.create_button(on_click=lambda e: loading.new_loading_page(page=page, layout=create_page_home(page, list_profile, list_initial_coordinates)),
                                            text="Voltar",
                                            color=ft.colors.AMBER,
                                            col=12,
                                            padding=5,)

    searchfild = ft.TextField(label="Procurar",  # caixa de texto
                                col=8,
                                on_change=lambda e: changesearch(e, filter, dicio, forms1),
                                label_style= ft.TextStyle(color=ft.colors.BLACK),
                                text_style= ft.TextStyle(color=ft.colors.BLACK),
                                text_align=ft.TextAlign.CENTER,
                                border_radius=20,
                                border_color=ft.colors.BLACK,
                                bgcolor=ft.colors.WHITE

            )
    
    filter_button = buttons.create_icon_button(
                                                icon=ft.icons.FILTER_ALT_OUTLINED,
                                                on_click=show_filter_container,
                                                color=ft.colors.BLUE,
                                                col=2,
                                                padding=0,
                                                icon_color=ft.colors.WHITE,
                                                )

    return ft.ResponsiveRow(
        columns=12,
        controls=[
            ft.Container(height=50),
            searchfild,
            filter_button,
            filter_container,
            forms1,
            back_home_button
         
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
    )

def create_view_orders_form(page, list_profile, list_initial_coordinates, menu):

    page.go("/")
    page.floating_action_button = None
    page.bottom_appbar = None
    page.appbar = None
    page.clean()
    page.controls.clear()
    page.overlay.clear()

    textthemes = TextTheme()
    texttheme1 = textthemes.create_text_theme1() 
    buttons = Buttons(page)
    loading = LoadingPages(page)
    sp = SupaBase(page)
    chk = CheckBox(page)
    
    dicio_filter = {
        "order_filter" : "like.*",
        "permission_filter" : "like.*"
    }
    dicio = {}

    def changesearch(e, dicio_filter, dicio, forms1):

        try:
            if e.control.value.strip() == "":
                dicio_filter["order_filter"] = "like.*"  
            else:
                dicio_filter["order_filter"] = f"like.%{e.control.value}%"
        except:
            dicio_filter["order_filter"] = "like.*"

        # Atualiza o filtro nos parâmetros
        params["order_id"] = dicio_filter["order_filter"]
        params["function"] = dicio_filter["permission_filter"]

        # Faz uma nova requisição com o filtro atualizado
        response = requests.get(
            f"{url}/rest/v1/ordens_postes_capeladoalto",
            headers=headers,
            params=params,
        )

        if response.status_code == 200:
            data = response.json()

            # Reconstrói as linhas da tabela
            dicio.clear()
            for row in data:
                ip = row["ip"]
                order = row["order_id"]
                function = row["function"]

                def forms(order):
                    return lambda e: loading.new_loading_page(
                        page=page,
                        layout=create_page_os_forms(page, list_profile, list_initial_coordinates, name=None, order=order)
                    )

                linha = ft.DataRow(cells=[
                        ft.DataCell(ft.Text(value=ip, theme_style=ft.TextThemeStyle.TITLE_LARGE, text_align=ft.TextAlign.CENTER)),
                        ft.DataCell(ft.Text(value=order, theme_style=ft.TextThemeStyle.TITLE_LARGE, text_align=ft.TextAlign.CENTER)),
                        ft.DataCell(ft.Text(value=function, theme_style=ft.TextThemeStyle.TITLE_LARGE, text_align=ft.TextAlign.CENTER)),
                        ft.DataCell(
                            ft.Container(content=
                                         buttons.create_icon_button(
                                                        icon=ft.icons.SEARCH,
                                                        on_click=forms(order),
                                                        color=ft.colors.BLUE,
                                                        col=2,
                                                        padding=0,
                                                        icon_color=ft.colors.WHITE,
                                                        ))
                        ),
                    ])

                dicio[order] = linha

            # Atualiza as linhas no DataTable
            forms1.content.rows = list(dicio.values())
            page.update()
        else:
            print(f"Erro ao buscar dados: {response.text}")




    if menu != None:
        page.close(menu)

    url = sp.get_url()
    key = sp.get_key()

    headers = {
        "apikey": key,
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json",
    }


    params = {
        "select": "ip, order_id, function",
        "order_id": dicio_filter["order_filter"],
        "function": dicio_filter["permission_filter"],
        "order": "order_id.desc",
    }

    # Requisição à API
    response = requests.get(
        f"{url}/rest/v1/ordens_postes_capeladoalto",
        headers=headers,
        params=params,
    )

    data = response.json()

    for row in data:

            ip = row["ip"]
            order = row["order_id"]
            function = row["function"]

            def forms(order):

                return lambda e: loading.new_loading_page(
                    page=page,
                    layout=create_page_os_forms(page, list_profile, list_initial_coordinates, name=None, order=order)
                )
         

            linha = ft.DataRow(cells=[
                        ft.DataCell(ft.Text(value=ip, theme_style=ft.TextThemeStyle.TITLE_LARGE, text_align=ft.TextAlign.CENTER)),
                        ft.DataCell(ft.Text(value=order, theme_style=ft.TextThemeStyle.TITLE_LARGE, text_align=ft.TextAlign.CENTER)),
                        ft.DataCell(ft.Text(value=function, theme_style=ft.TextThemeStyle.TITLE_LARGE, text_align=ft.TextAlign.CENTER)),
                        ft.DataCell(
                            ft.Container(content=
                                         buttons.create_icon_button(
                                                        icon=ft.icons.SEARCH,
                                                        on_click=forms(order),
                                                        color=ft.colors.BLUE,
                                                        col=2,
                                                        padding=0,
                                                        icon_color=ft.colors.WHITE,
                                                        ))
                        ),
                    ])

            dicio[order] = linha

    lista = list(dicio.values())


    forms1 = ft.Container(
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
    
    def show_filter_container(e):
        filter_container.visible = not filter_container.visible
        page.update()

    def get_permission_filter(e):
        adm_permission = filter_container.content.controls[0].controls[0].value
        adm_permission_data = filter_container.content.controls[0].controls[0].data
        invited_permission = filter_container.content.controls[1].controls[0].value
        invited_permission_data = filter_container.content.controls[1].controls[0].data
        if adm_permission:
            dicio_filter["permission_filter"] = f"eq.{adm_permission_data}"
        if invited_permission:
            dicio_filter["permission_filter"] = f"eq.{invited_permission_data}"
        if invited_permission and adm_permission:
            dicio_filter["permission_filter"] = f"like.*"
        filter_container.visible = not filter_container.visible
        page.update()
        changesearch(e, dicio_filter, dicio, forms1),



    filter_container = ft.Container(
            bgcolor=ft.colors.BLUE,
            padding=10,
            margin=10,
            height=200,
            border_radius=20,
            col=10,
            visible=False,
            content=ft.Column([
                chk.create_checkbox2("Administrador", 15, None, 8,"ADM", True),
                chk.create_checkbox2("Convidado", 15, None, 8,"Convidado", True),
                buttons.create_button(on_click=lambda e: get_permission_filter(e),
                                            text="Aplicar",
                                            color=ft.colors.AMBER,
                                            col=12,
                                            padding=5,)
                ])
            )
    
    back_home_button = buttons.create_button(on_click=lambda e: loading.new_loading_page(page=page, layout=create_page_home(page, list_profile, list_initial_coordinates)),
                                            text="Voltar",
                                            color=ft.colors.AMBER,
                                            col=12,
                                            padding=5,)
    
    searchfild = ft.TextField(label="Procurar",  # caixa de texto
                                col=8,
                                on_change=lambda e: changesearch(e, dicio_filter, dicio, forms1),
                                label_style= ft.TextStyle(color=ft.colors.BLACK),
                                text_style= ft.TextStyle(color=ft.colors.BLACK),
                                text_align=ft.TextAlign.CENTER,
                                border_radius=20,
                                border_color=ft.colors.BLACK,
                                bgcolor=ft.colors.WHITE

            )
    
    filter_button = buttons.create_icon_button(
                                                icon=ft.icons.FILTER_ALT_OUTLINED,
                                                on_click=show_filter_container,
                                                color=ft.colors.BLUE,
                                                col=2,
                                                padding=0,
                                                icon_color=ft.colors.WHITE,
                                                )

    return ft.ResponsiveRow(
        columns=12,
        controls=[
            ft.Container(height=50),
            searchfild,
            filter_button,
            filter_container,
            forms1,
            back_home_button
         
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
    )

def create_view_users_form(page, list_profile, list_initial_coordinates, menu):

    page.go("/")
    page.floating_action_button = None
    page.bottom_appbar = None
    page.appbar = None
    page.clean()
    page.controls.clear()
    page.overlay.clear()

    textthemes = TextTheme()
    texttheme1 = textthemes.create_text_theme1() 
    buttons = Buttons(page)
    loading = LoadingPages(page)
    sp = SupaBase(page)
    chk = CheckBox(page)
    
    dicio_filter = {
        "user_filter" : "like.*",
        "permission_filter" : "like.*"
    }
    dicio = {}

    def changesearch(e, dicio_filter, dicio, forms1):

        try:
            if e.control.value.strip() == "":
                dicio_filter["user_filter"] = "like.*"  
            else:
                dicio_filter["user_filter"] = f"ilike.%{e.control.value.strip().lower()}%"
        except:
            dicio_filter["user_filter"] = "like.*"

        # Atualiza o filtro nos parâmetros
        params["usuario"] = dicio_filter["user_filter"]
        params["permission"] = dicio_filter["permission_filter"]

        # Faz uma nova requisição com o filtro atualizado
        response = requests.get(
            f"{url}/rest/v1/login_geopostes",
            headers=headers,
            params=params,
        )

        if response.status_code == 200:
            data = response.json()

            # Reconstrói as linhas da tabela
            dicio.clear()
            for row in data:

                user_id = row["user_id"]
                user_name = row["usuario"]
                user_permission = row["permission"]

                def forms(user_name):

                    return lambda e: loading.new_loading_page(
                        page=page,
                        layout=create_page_user_forms(page, list_profile, list_initial_coordinates, user=user_name)
                    )
            

                linha = ft.DataRow(cells=[
                            ft.DataCell(ft.Text(value=user_id, theme_style=ft.TextThemeStyle.TITLE_LARGE, text_align=ft.TextAlign.CENTER)),
                            ft.DataCell(ft.Text(value=user_name, theme_style=ft.TextThemeStyle.TITLE_LARGE, text_align=ft.TextAlign.CENTER)),
                            ft.DataCell(ft.Text(value=user_permission, theme_style=ft.TextThemeStyle.TITLE_LARGE, text_align=ft.TextAlign.CENTER)),
                            ft.DataCell(
                                ft.Container(content=
                                            buttons.create_icon_button(
                                                            icon=ft.icons.SEARCH,
                                                            on_click=forms(user_name),
                                                            color=ft.colors.BLUE,
                                                            col=2,
                                                            padding=0,
                                                            icon_color=ft.colors.WHITE,
                                                            ))
                            ),
                        ])

                dicio[user_id] = linha

            # Atualiza as linhas no DataTable
            forms1.content.rows = list(dicio.values())
            page.update()
        else:
            print(f"Erro ao buscar dados: {response.text}")

    if menu != None:
        page.close(menu)

    url = sp.get_url()
    key = sp.get_key()

    headers = {
        "apikey": key,
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json",
    }


    params = {
        "select": "user_id, usuario, permission",
        "usuario": dicio_filter["user_filter"],
        "permission": dicio_filter["permission_filter"],
        "order": "user_id.desc",
    }

    # Requisição à API
    response = requests.get(
        f"{url}/rest/v1/login_geopostes",
        headers=headers,
        params=params,
    )

    data = response.json()

    for row in data:

            user_id = row["user_id"]
            user_name = row["usuario"]
            user_permission = row["permission"]

            def forms(user_name):

                return lambda e: loading.new_loading_page(
                    page=page,
                    layout=create_page_user_forms(page, list_profile, list_initial_coordinates, user=user_name)
                )
         

            linha = ft.DataRow(cells=[
                        ft.DataCell(ft.Text(value=user_id, theme_style=ft.TextThemeStyle.TITLE_LARGE, text_align=ft.TextAlign.CENTER)),
                        ft.DataCell(ft.Text(value=user_name, theme_style=ft.TextThemeStyle.TITLE_LARGE, text_align=ft.TextAlign.CENTER)),
                        ft.DataCell(ft.Text(value=user_permission, theme_style=ft.TextThemeStyle.TITLE_LARGE, text_align=ft.TextAlign.CENTER)),
                        ft.DataCell(
                            ft.Container(content=
                                         buttons.create_icon_button(
                                                        icon=ft.icons.SEARCH,
                                                        on_click=forms(user_name),
                                                        color=ft.colors.BLUE,
                                                        col=2,
                                                        padding=0,
                                                        icon_color=ft.colors.WHITE,
                                                        ))
                        ),
                    ])

            dicio[user_id] = linha

    lista = list(dicio.values())


    forms1 = ft.Container(
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
    
    def show_filter_container(e):
        filter_container.visible = not filter_container.visible
        page.update()

    def get_permission_filter(e):
        adm_permission = filter_container.content.controls[0].controls[0].value
        adm_permission_data = filter_container.content.controls[0].controls[0].data
        invited_permission = filter_container.content.controls[1].controls[0].value
        invited_permission_data = filter_container.content.controls[1].controls[0].data
        if adm_permission:
            dicio_filter["permission_filter"] = f"eq.{adm_permission_data}"
        if invited_permission:
            dicio_filter["permission_filter"] = f"eq.{invited_permission_data}"
        if invited_permission and adm_permission:
            dicio_filter["permission_filter"] = f"like.*"
        filter_container.visible = not filter_container.visible
        page.update()
        changesearch(e, dicio_filter, dicio, forms1),



    filter_container = ft.Container(
            bgcolor=ft.colors.BLUE,
            padding=10,
            margin=10,
            height=200,
            border_radius=20,
            col=10,
            visible=False,
            content=ft.Column([
                chk.create_checkbox2("Administrador", 15, None, 8,"adm", True),
                chk.create_checkbox2("Convidado", 15, None, 8,"invited", True),
                buttons.create_button(on_click=lambda e: get_permission_filter(e),
                                            text="Aplicar",
                                            color=ft.colors.AMBER,
                                            col=12,
                                            padding=5,)
                ])
            )


    back_home_button = buttons.create_button(on_click=lambda e: loading.new_loading_page(page=page, layout=create_page_home(page, list_profile, list_initial_coordinates)),
                                            text="Voltar",
                                            color=ft.colors.AMBER,
                                            col=12,
                                            padding=5,)
    
    searchfild = ft.TextField(label="Procurar",  # caixa de texto
                                col=8,
                                on_change=lambda e: changesearch(e, dicio_filter, dicio, forms1),
                                label_style= ft.TextStyle(color=ft.colors.BLACK),
                                text_style= ft.TextStyle(color=ft.colors.BLACK),
                                text_align=ft.TextAlign.CENTER,
                                border_radius=20,
                                border_color=ft.colors.BLACK,
                                bgcolor=ft.colors.WHITE

            )
    
    filter_button = buttons.create_icon_button(
                                                icon=ft.icons.FILTER_ALT_OUTLINED,
                                                on_click=show_filter_container,
                                                color=ft.colors.BLUE,
                                                col=2,
                                                padding=0,
                                                icon_color=ft.colors.WHITE,
                                                )

    add_button = buttons.create_button(on_click=lambda e: loading.new_loading_page(page=page, layout=create_page_add_user_forms(page, list_profile, list_initial_coordinates)),
                                                text="Adicionar",
                                                color=ft.colors.GREEN,
                                                col=6,
                                                padding=5,)

    return ft.ResponsiveRow(
        columns=12,
        controls=[
            ft.Container(height=50),
            searchfild,
            filter_button,
            add_button,
            filter_container,
            forms1,
            back_home_button
         
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
    )







def verificar(username, password, page):

    loading = LoadingPages(page)
    sp = SupaBase(page)

    response = sp.check_login(username=username, password=password)

    if response.status_code == 200 and len(response.json()) > 0:

        data = response.json()
        row = data[0]
        name = row["usuario"]
        permission = row["permission"]
        number = row["numero"]
            
        snack_bar = ft.SnackBar(
        content=ft.Text("Login realizado"),
        bgcolor=ft.colors.GREEN,
        duration= 1000,
        )
        map_layer = "https://tile.openstreetmap.org/{z}/{x}/{y}.png"
        map_filter = ["Lâmpada LED", "Lâmpada de vapor de sódio", "." ]
        zoom = 18.4
        list_initial_coordinates = ["-23.3396", "-47.8238", map_layer, None, map_filter, zoom]
        list_profile = [name, permission, number]
        loading.new_loading_page(page=page, layout=create_page_home(page, list_profile, list_initial_coordinates))
        
    else:
        # Exibe mensagem de erro se as credenciais não forem encontradas
        snack_bar = ft.SnackBar(
            content=ft.Text("Login ou senha incorretos"),
            bgcolor=ft.colors.RED
        )

    page.overlay.append(snack_bar)
    snack_bar.open = True
    page.update()

def register(username, email, number, password1, password2, page):

    sp = SupaBase(page)

    # Verificar se todos os campos estão preenchidos
    if not username or not email or not number or not password1 or not password2:
        snack_bar = ft.SnackBar(
            content=ft.Text("Alguns campos não foram preenchidos"),
            bgcolor=ft.colors.RED
        )
        page.overlay.append(snack_bar)
        snack_bar.open = True
        page.update()
        return  # Interrompe a execução da função
    
    #Verificar se as senhas coincidem
    if password1 != password2:
        snack_bar = ft.SnackBar(
            content=ft.Text("As senhas não coincidem"),
            bgcolor=ft.colors.RED
        )
        page.overlay.append(snack_bar)
        snack_bar.open = True
        page.update()
        return  # Interrompe a execução da função 
    
    response = sp.register(username, email, number, password1, password2)

    # Verificar se a inserção foi bem-sucedida
    if response.status_code == 201:
        snack_bar = ft.SnackBar(
            content=ft.Text("Usuário registrado com sucesso"),
            bgcolor=ft.colors.GREEN
        )
    else:
        print(f"Erro ao inserir registro: {response.status_code}")
        print(f"Resposta do erro: {response.text}")
        snack_bar = ft.SnackBar(
            content=ft.Text(f"Erro ao registrar usuário: {response.text}"),
            bgcolor=ft.colors.RED
        )

    page.overlay.append(snack_bar)
    snack_bar.open = True
    page.update()



def add_point(page, list_profile, list_initial_coordinates, list_forms, image, angle):

    sp = SupaBase(page)
    loading = LoadingPages(page)

    # Verificar se todos os campos estão preenchidos
    if any(field == "" or field is None for field in list_forms):
        snack_bar = ft.SnackBar(
            content=ft.Text("Alguns campos não foram preenchidos"),
            bgcolor=ft.colors.RED
        )
        page.overlay.append(snack_bar)
        snack_bar.open = True
        page.update()
        return  # Interrompe a execução da função
    
    response = sp.add_point(list_profile, list_forms, list_initial_coordinates, image, angle)

    # Verificar se a inserção foi bem-sucedida
    if response.status_code == 201:

        snack_bar = ft.SnackBar(
            content=ft.Text("Ponto adicionado com sucesso"),
            bgcolor=ft.colors.GREEN,
            duration=3000,
        )
        loading.new_loading_page(page=page, layout=create_page_home(page, list_profile, list_initial_coordinates))

    elif  response.status_code == 199:
        return  

    else:
        snack_bar = ft.SnackBar(
            content=ft.Text(f"Erro ao inserir ponto: {response.text}"),
            bgcolor=ft.colors.RED,
            duration=4000,
        )
 
    page.overlay.append(snack_bar)
    snack_bar.open = True
    page.update()

def add_os(page, list_profile, list_initial_coordinates, list_add_os, name):

    sp = SupaBase(page)
    loading = LoadingPages(page)
   
    if any(field == "" or field is None for field in list_add_os):
        snack_bar = ft.SnackBar(
            content=ft.Text("Alguns campos não foram preenchidos"),
            bgcolor=ft.colors.RED
        )
        page.overlay.append(snack_bar)
        snack_bar.open = True
        page.update()
        return  # Interrompe a execução da função
    
    response = sp.add_os(list_add_os)

    # Verificar se a inserção foi bem-sucedida
    if response.status_code == 201:
        snack_bar = ft.SnackBar(
            content=ft.Text("ordem adicionada com sucesso"),
            bgcolor=ft.colors.GREEN,
            duration=2500,
        )

        loading.new_loading_page(page=page, layout=create_adm_page_order(page, list_profile, list_initial_coordinates, name))
      
    else:
        print(f"Erro ao adicionar ordem: {response.status_code}")
        print(f"Resposta do erro: {response.text}")
        snack_bar = ft.SnackBar(
            content=ft.Text(f"Erro ao adicionar ordem: {response.text}"),
            bgcolor=ft.colors.RED,
            duration=4000,
        )
 
    page.overlay.append(snack_bar)
    snack_bar.open = True
    page.update()

def add_user(page, list_profile, list_initial_coordinates, list_add_user, id):

    sp = SupaBase(page)
    loading = LoadingPages(page)
   
    if any(field == "" or field is None for field in list_add_user):
        snack_bar = ft.SnackBar(
            content=ft.Text("Alguns campos não foram preenchidos"),
            bgcolor=ft.colors.RED
        )
        page.overlay.append(snack_bar)
        snack_bar.open = True
        page.update()
        return  # Interrompe a execução da função
    
    response = sp.add_user(list_add_user, id)

    # Verificar se a inserção foi bem-sucedida
    if response.status_code == 201:
        snack_bar = ft.SnackBar(
            content=ft.Text("Usuario adicionado com sucesso"),
            bgcolor=ft.colors.GREEN,
            duration=2500,
        )

        loading.new_loading_page(page=page, layout=create_view_users_form(page, list_profile, list_initial_coordinates, menu=None))
      
    else:
        print(f"Erro ao adicionar usuário: {response.status_code}")
        print(f"Resposta do erro: {response.text}")
        snack_bar = ft.SnackBar(
            content=ft.Text(f"Erro ao adicionar usuario: {response.text}"),
            bgcolor=ft.colors.RED,
            duration=4000,
        )
 
    page.overlay.append(snack_bar)
    snack_bar.open = True
    page.update()



def edit_point(page, list_profile, list_initial_coordinates, list_forms, image, previous_data):

    sp = SupaBase(page)

    snack_bar = ft.SnackBar(
        content=ft.Text("Alterando..."),
        bgcolor=ft.colors.ORANGE,
        duration=1000,
    )
    page.overlay.append(snack_bar)
    snack_bar.open = True
    page.update()

    if any(field == "" or field is None for field in list_forms):
        snack_bar = ft.SnackBar(
            content=ft.Text("Alguns campos não foram preenchidos"),
            bgcolor=ft.colors.RED
        )
        page.overlay.append(snack_bar)
        snack_bar.open = True
        page.update()
        return  # Interrompe a execução da função

    response = sp.edit_point(image, list_forms, previous_data)
    
    if response.status_code in [200, 204]:  # 204 indica sucesso sem conteúdo
        snack_bar = ft.SnackBar(
            content=ft.Text("Alterações Salvas"),
            bgcolor=ft.colors.GREEN,
            duration=2000,
        )
        loading = LoadingPages(page)
        loading.new_loading_page(page=page, layout=create_page_home(page, list_profile, list_initial_coordinates))

    elif response.status_code == 199:
        return

    else:
        print(f"Erro ao editar ponto: {response.status_code}")
        print(f"Resposta do erro: {response.text}")
        snack_bar = ft.SnackBar(
            content=ft.Text(f"Erro ao editar ponto: {response.text}"),
            bgcolor=ft.colors.RED
        )


    page.overlay.append(snack_bar)
    snack_bar.open = True

def edit_os(page, list_profile, list_initial_coordinates, list_edited_os_forms, order, name):

    sp = SupaBase(page)
    loading = LoadingPages(page)

    snack_bar = ft.SnackBar(
        content=ft.Text("Alterando..."),
        bgcolor=ft.colors.ORANGE,
        duration=1000,
    )
    page.overlay.append(snack_bar)
    snack_bar.open = True
    page.update()


    if any(field == "" or field is None for field in list_edited_os_forms):
        snack_bar = ft.SnackBar(
            content=ft.Text("Alguns campos não foram preenchidos"),
            bgcolor=ft.colors.RED
        )
        page.overlay.append(snack_bar)
        snack_bar.open = True
        page.update()
        return  # Interrompe a execução da função

    response = sp.edit_os(list_edited_os_forms)
    
    if response.status_code in [200, 204]:  # 204 indica sucesso sem conteúdo
        snack_bar = ft.SnackBar(
            content=ft.Text("Alterações Salvas"),
            bgcolor=ft.colors.GREEN,
            duration=2000,
        )
        loading.new_loading_page(page=page, layout=create_page_os_forms(page, list_profile, list_initial_coordinates, name, order))

    else:
        print(f"Erro ao editar ponto: {response.status_code}")
        print(f"Resposta do erro: {response.text}")
        snack_bar = ft.SnackBar(
            content=ft.Text(f"Erro ao editar ponto: {response.text}"),
            bgcolor=ft.colors.RED
        )


    page.overlay.append(snack_bar)
    snack_bar.open = True
    page.update()

def edit_user(page, list_profile, list_initial_coordinates, list_edited_user_forms, previus_name):

    sp = SupaBase(page)
    loading = LoadingPages(page)

    snack_bar = ft.SnackBar(
        content=ft.Text("Alterando..."),
        bgcolor=ft.colors.ORANGE,
        duration=1000,
    )
    page.overlay.append(snack_bar)
    snack_bar.open = True
    page.update()


    if any(field == "" or field is None for field in list_edited_user_forms):
        snack_bar = ft.SnackBar(
            content=ft.Text("Alguns campos não foram preenchidos"),
            bgcolor=ft.colors.RED
        )
        page.overlay.append(snack_bar)
        snack_bar.open = True
        page.update()
        return  # Interrompe a execução da função

    response = sp.edit_user(list_edited_user_forms, previus_name)
    
    if response.status_code in [200, 204]:  # 204 indica sucesso sem conteúdo
        snack_bar = ft.SnackBar(
            content=ft.Text("Alterações Salvas"),
            bgcolor=ft.colors.GREEN,
            duration=2000,
        )
        loading.new_loading_page(page=page,
        layout=create_page_user_forms(page, list_profile, list_initial_coordinates, list_edited_user_forms[0]))

    else:
        print(f"Erro ao editar perfil: {response.status_code}")
        print(f"Resposta do erro: {response.text}")
        snack_bar = ft.SnackBar(
            content=ft.Text(f"Erro ao editar perfil: {response.text}"),
            bgcolor=ft.colors.RED
        )


    page.overlay.append(snack_bar)
    snack_bar.open = True
    page.update()



def delete_point(page, list_profile, list_initial_coordinates, name):

    sp = SupaBase(page)
    loading = LoadingPages(page)

    snack_bar = ft.SnackBar(
        content=ft.Text("Excluindo..."),
        bgcolor=ft.colors.ORANGE,
        duration=1000,
    )
    page.overlay.append(snack_bar)
    snack_bar.open = True
    page.update()

    list_response = sp.delete_point_post(name)


    if list_response[0].status_code == 204 and list_response[1].status_code == 204:
        snack_bar = ft.SnackBar(
                content=ft.Text("Ponto excluido"),
                bgcolor=ft.colors.GREEN,
                duration=2500,
            )
        loading.new_loading_page(page=page, layout=create_page_home(page, list_profile, list_initial_coordinates))

    else:
        snack_bar = ft.SnackBar(
            content=ft.Text(f"Erro ao excluir ponto: {list_response[0].text}, {list_response[1].text}, {list_response[2].text}"),
            bgcolor=ft.colors.RED
        )
        loading.new_loading_page(page=page, layout=create_page_home(page, list_profile, list_initial_coordinates))

    page.overlay.append(snack_bar)
    snack_bar.open = True
    page.update()

def delete_os(page, list_profile, list_initial_coordinates, name, order):

    loading = LoadingPages(page)

    snack_bar = ft.SnackBar(
        content=ft.Text("Excluindo..."),
        bgcolor=ft.colors.ORANGE,
        duration=1000,
    )
    page.overlay.append(snack_bar)
    snack_bar.open = True
    page.update()

    sp = SupaBase(page)

    response = sp.delete_os(order)

    if response.status_code == 204:

        if name != None:
            snack_bar = ft.SnackBar(
                    content=ft.Text("ordem excluida"),
                    bgcolor=ft.colors.GREEN,
                    duration=2500,
                )

            loading.new_loading_page(page=page, layout=create_adm_page_order(page, list_profile, list_initial_coordinates, name))

        else:
            snack_bar = ft.SnackBar(
                    content=ft.Text("ordem excluida"),
                    bgcolor=ft.colors.GREEN,
                    duration=2500,
                )

            loading.new_loading_page(page=page, layout=create_page_home(page, list_profile, list_initial_coordinates))


    else:
        print(f"Erro ao excluir order: {response.status_code}")
        print(f"Resposta do erro: {response.text}")
        snack_bar = ft.SnackBar(
            content=ft.Text(f"Erro ao excluir order: {response.text}"),
            bgcolor=ft.colors.RED
        )

    # Exibir a mensagem e atualizar a página
    page.overlay.append(snack_bar)
    snack_bar.open = True
    page.update()

def delete_user(page, list_profile, list_initial_coordinates, user):

    loading = LoadingPages(page)

    snack_bar = ft.SnackBar(
        content=ft.Text("Excluindo..."),
        bgcolor=ft.colors.ORANGE,
        duration=1000,
    )
    page.overlay.append(snack_bar)
    snack_bar.open = True
    page.update()

    sp = SupaBase(page)

    response = sp.delete_user(user)

    if response.status_code == 204:

        snack_bar = ft.SnackBar(
                content=ft.Text("Usuario excluido"),
                bgcolor=ft.colors.GREEN,
                duration=2500,
            )

        loading.new_loading_page(page=page, layout=create_view_users_form(page, list_profile, list_initial_coordinates, menu=None))

    else:
        snack_bar = ft.SnackBar(
            content=ft.Text(f"Erro ao excluir usuario: {response.text}"),
            bgcolor=ft.colors.RED
        )

    # Exibir a mensagem e atualizar a página
    page.overlay.append(snack_bar)
    snack_bar.open = True
    page.update()





class Map:

    def __init__(self, page, list_profile, point_location, list_initial_coordinates, list_center_map_coordinates):
        self.page = page
        self.name = list_profile
        self.point_location = point_location
        self.initial_coordinates = list_initial_coordinates
        self.center_map_coordinates = list_center_map_coordinates 
        self.markers = Marker(self.page, self.initial_coordinates)
        self.mappoints = self.markers.create_points(self.name, 20, True)
        self.current_zoom = None
        self.zoom_zone = "above_17"


        self.google = None

        self.MarkerLayer = []

    def create_map(self):

        self.MarkerLayer.append(self.mappoints)

        def handle_event(e: map.MapEvent):
            self.center_map_coordinates[0] = f"{e.center.latitude:.6f}"
            self.center_map_coordinates[1] = f"{e.center.longitude:.6f}"
            self.center_map_coordinates[5] = e.zoom
            self.current_zoom = e.zoom

            self.page.update()

        def tap_event(e: map.MapEvent):
            try:
                self.page.overlay[1].visible = False
                self.page.overlay.pop(1)
                self.page.update()
            except:
                None

        max_zoom = 20.9
        initial_zoom = self.initial_coordinates[5]
        if self.initial_coordinates[2] == "https://services.arcgisonline.com/arcgis/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}":
            max_zoom = 18.44
            if self.initial_coordinates[5] > 18.44:
                initial_zoom = 18.44

        self.google = map.Map(
                    expand=True,
                    initial_zoom=initial_zoom,
                    min_zoom=15.5,
                    max_zoom=max_zoom,
                    on_event=handle_event,
                    on_tap=tap_event,
                    initial_center=map.MapLatitudeLongitude(self.initial_coordinates[0], self.initial_coordinates[1]),    
                    layers=[
                        map.TileLayer(
                            url_template=self.initial_coordinates[2],
                        ),
                        map.MarkerLayer(*self.MarkerLayer),
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
                            width=430,
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

        try:
            if self.current_zoom is not None:
                if self.current_zoom > 17:
                    new_zoom_zone = "above_17"
                if self.current_zoom < 17:
                    new_zoom_zone = "below_17"
                if self.current_zoom < 16:
                    new_zoom_zone = "below_16"

                if new_zoom_zone != self.zoom_zone:
                    self.zoom_zone = new_zoom_zone
                    if new_zoom_zone == "above_17":
                        self.update_size_point(20, True)
                    if new_zoom_zone == "below_17":
                        self.update_size_point(10, True)
                    if new_zoom_zone == "below_16":
                        self.update_size_point(5, False)
        except:
            None

        try:

            if self.point_location.coordinates is not None:
                if self.point_location in self.MarkerLayer[0]:
                    self.MarkerLayer[0].remove(self.point_location)
                    self.page.update()

                # Adicionar o marcador atualizado
                else:      
                    self.MarkerLayer[0].append(self.point_location)
                    self.page.update()

            self.page.update()

        except:
            None
        
  

    def update_size_point(self, size, visible):

        try:
            self.MarkerLayer[0].clear()
            self.page.update()
            if self.MarkerLayer[0] == []:
                new_mappoints = self.markers.create_points(self.name, size, visible)
                self.MarkerLayer[0].extend(new_mappoints)
            self.page.update()
        except:
            None


class Marker:

    def __init__(self, page, list_initial_coordinates):
        self.page = page
        self.list_initial_coordinates = list_initial_coordinates


    def create_points(self, list_profile, size, visible):
        
        sp = SupaBase(self.page)

        response = sp.get_point_post()

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
            name = row["name"]
            x = row["x"]
            y = row["y"]
            data_color = row["color"]

            point = sp.get_form_post(name)
            data = point.json()
            row = data[0]
            list_post_form= [
                row["name"],
                row["situation"],
                row["type"],
                row["point"],
                row["hood"],
                row["address"]
            ]

            if data_color == "yellow":
                point_color = ft.colors.AMBER
            if data_color == "white":
                point_color = ft.colors.PINK_200
            if data_color == "blue":
                point_color = ft.colors.BLUE
                

            list_initial_coordinates = [x, y, self.list_initial_coordinates[2], self.list_initial_coordinates[3], self.list_initial_coordinates[4], self.list_initial_coordinates[5]]

            loading = LoadingPages(self.page)
      
            def create_on_click(name=name, list_initial_coordinates=list_initial_coordinates):
                return lambda e: loading.new_loading_page(
                    page=self.page,
                    layout=create_page_forms(self.page, list_profile, list_initial_coordinates, name)
                )

            number = int(name.split('-')[1])

            if list_post_form[2] in list_initial_coordinates[4]:

                InitialButtons[number] = {
                    "element": buttons.create_point_button(
                        on_click=create_on_click(),  # Usa a função auxiliar
                        text=str(number),
                        color=point_color,
                        size=size,
                        visible=visible,
                    ),
                    "x": x,
                    "y": y,
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


class Search:

    def __init__(self, page, list_profile, list_initial_coordinates):
        self.page = page
        self.list_initial_coordinates = list_initial_coordinates
        self.sp = SupaBase(self.page)

        self.resultdata = ft.ListView()

        self.resultcon = ft.Container(
            bgcolor=ft.colors.BLUE,
            padding=10,
            margin=10,
            height=300,
            border_radius=20,
            offset=ft.transform.Offset(-2,0),
            animate_offset = ft.animation.Animation(600,curve="easeIn"),
            content=ft.Column([
                self.resultdata

                ])
            )

        url = self.sp.get_url()
        key = self.sp.get_key()

        headers = {
            "apikey": key,
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json",
        }

        # Parâmetros da requisição GET
        params = {"select": "name, x, y"}

        # Requisição à API
        response = requests.get(
            f"{url}/rest/v1/point_post_capela",
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
            name = row["name"]
            Latitude = row["x"]
            Longitude = row["y"]

            loading = LoadingPages(self.page)

            # Função para criar o evento de clique com coordenadas fixas
            def create_on_click(lat=Latitude, long=Longitude):
                return lambda e: loading.new_loading_page(
                    page=self.page,
                    layout=create_page_home(self.page, list_profile, list_initial_coordinates=[lat, long, self.list_initial_coordinates[2],self.list_initial_coordinates[3], self.list_initial_coordinates[4], 18.4]),
                )

            # Adiciona o botão à lista de itens
            itens.append(
                ft.ListTile(
                    title=ft.Text(value=name, color=ft.colors.WHITE),
                    on_click=create_on_click(),
                    bgcolor_activated=ft.colors.AMBER
                )
            )

        def searchnow(e):
            mysearch = e.control.value
            result = []  # cria outra lista

            if mysearch.strip():  # Se houver texto digitado
                try:
                    self.page.overlay.pop(1)
                except:
                    None
                if self.resultcon not in self.page.overlay:
                    self.resultcon.visible = True
                    self.page.overlay.insert(1, self.resultcon)  # Adiciona ao overlay
                for item in itens:
                    # Verifica se o texto da pesquisa está no título do ListTile
                    if mysearch.lower() in item.title.value.lower():  # Usa `.lower()` para ignorar maiúsculas/minúsculas
                        result.append(item)  # Adiciona à lista apenas os itens pesquisados
                self.page.update()

            if result:  # Se houver resultados
                self.resultdata.controls.clear()
                for x in result:
                    self.resultdata.controls.append(x)  # Adiciona o próprio ListTile ao resultado
                self.page.update()
            else:  # Se não houver resultados ou a busca estiver vazia
                if self.resultcon in self.page.overlay:
                    self.page.overlay.remove(self.resultcon)  # Remove do overlay
                self.resultdata.controls.clear()
                self.page.update()

        self.txtsearch = ft.TextField(label="Procurar",  # caixa de texto
                                        on_change=searchnow,
                                        label_style= ft.TextStyle(color=ft.colors.BLACK),
                                        text_style= ft.TextStyle(color=ft.colors.BLACK),
                                        border_radius=20,
                                        border_color=ft.colors.WHITE,
                                        bgcolor=ft.colors.WHITE

            )


    def create_search_text(self):

        return self.txtsearch

    def create_search_container(self):
        self.resultcon.offset = ft.transform.Offset(0, 0)  # Centralizado
        self.resultcon.animate_offset = ft.animation.Animation(600, curve="easeIn")
        return self.resultcon


class Container:

    def __init__(self, page, list_profile, list_initial_coordinates):
        self.page = page
        self.sp = SupaBase(page)
        loading = LoadingPages(page)
        web_images = Web_Image(page)
        chk =CheckBox(page)
        buttons = Buttons(page)

        url_imagem1 = web_images.get_image_url(name="map_aerial")
        map_aerial = web_images.create_web_image(src=url_imagem1) 
        url_imagem2 = web_images.get_image_url(name="map_road")
        map_road = web_images.create_web_image(src=url_imagem2)

        def create_map_aerial(e):
            layer_aerial = "https://services.arcgisonline.com/arcgis/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}"
            list_initial_coordinates[2]=layer_aerial
            loading.new_loading_page(page=page, layout=create_page_home(page, list_profile, list_initial_coordinates))

        def create_map_road(e):
            layer_aerial = "https://tile.openstreetmap.org/{z}/{x}/{y}.png"
            list_initial_coordinates[2]=layer_aerial
            loading.new_loading_page(page=page, layout=create_page_home(page, list_profile, list_initial_coordinates))

        def get_permission_filter(e):

            led_type = self.filter_container.content.controls[0].controls[0].value
            sodium_type = self.filter_container.content.controls[1].controls[0].value
            null_type = self.filter_container.content.controls[2].controls[0].value
            list_map_filter = []

            if led_type:
                list_map_filter.append("Lâmpada LED")
            if sodium_type:
                list_map_filter.append("Lâmpada de vapor de sódio")
            if null_type:
                list_map_filter.append(".")

            list_initial_coordinates[4] = list_map_filter
            loading.new_loading_page(page=page, layout=create_page_home(page, list_profile, list_initial_coordinates))

        self.map_container = ft.Row([
                                ft.Container(
                                    bgcolor=ft.colors.BLUE,
                                    padding=10,
                                    margin=10,
                                    height=120,
                                    width=250,
                                    border_radius=20,
                                    alignment=ft.alignment.center,
                                    content=ft.Column([
                                            ft.Row([
                                                ft.Container(
                                                    bgcolor=ft.colors.WHITE,
                                                    width=100,
                                                    height=100,
                                                    content=(map_road),
                                                    on_click=create_map_road,
                                                    border_radius=10,   
                                                ),
                                                ft.Container(
                                                    bgcolor=ft.colors.WHITE,
                                                    width=100,
                                                    height=100,
                                                    content=(map_aerial),
                                                    on_click=create_map_aerial,
                                                    border_radius=10,   
                                                ),
                                            ],
                                            spacing=25)
                                        ])
                                    )
                                ],
                                vertical_alignment=ft.CrossAxisAlignment.END,
                                alignment=ft.MainAxisAlignment.CENTER,
                                )

        self.filter_container = ft.Container(
            bgcolor=ft.colors.BLUE,
            padding=10,
            margin=10,
            height=250,
            border_radius=20,
            col=10,
            content=ft.Column([
                chk.create_checkbox2("Lâmpada LED", 15, None, 8,"Lâmpada LED", True),
                chk.create_checkbox2("Lâmpada de vapor de sódio", 15, None, 8,"Lâmpada de vapor de sódio", True),
                chk.create_checkbox2("Sem iluminação", 15, None, 8,".", True),
                buttons.create_button(on_click=lambda e: get_permission_filter(e),
                                            text="Aplicar",
                                            color=ft.colors.AMBER,
                                            col=12,
                                            padding=5,)
                ])
            )


    def create_maps_container(self):
        self.map_container.offset = ft.transform.Offset(0, 0)  # Centralizado
        self.map_container.animate_offset = ft.animation.Animation(600, curve="easeIn")
        return self.map_container

    def create_filter_container(self):
        self.filter_container.offset = ft.transform.Offset(0, 0)  # Centralizado
        self.filter_container.animate_offset = ft.animation.Animation(600, curve="easeIn")
        return self.filter_container




                



