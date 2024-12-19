import flet as ft
from models import *
import requests
import flet.map as map
from datetime import datetime
import math
import time
import asyncio


def create_page_home(page):
    
    page.go("/")
    loading = LoadingPages(page)
    buttons = Buttons(page)
    menus = SettingsMenu(page)

    point_location = map.Marker(
                content=ft.Column(
                            spacing=0,
                            controls=[ 
                                ft.Stack(
                                    expand=True,
                                    alignment=ft.alignment.center,
                                    controls=[
                                        ft.Container(
                                            width=20,
                                            height=20,
                                            bgcolor=ft.Colors.BLUE,
                                            border_radius=10,
                                            ),
                                        ft.Container(
                                            width=10,
                                            height=10,
                                            bgcolor=ft.Colors.WHITE,
                                            border_radius=5,
                                            ),
                                    ]
                                 ),    
                            ]
                        ),
                coordinates=None,
                rotate=True,
                data="point_location" 
                )

    list_maps_acess_controls = []
    markers = Marker(page)
    maps = Map(page, point_location, list_maps_acess_controls)
    requests_points = markers.create_points(15, True, maps)
    current_map_points = CurrentMapPoints()
    current_map_points.add_list_point(requests_points)
    map_points = current_map_points.return_current_points()

    def points_radius(lista_pontos, ponto_central, raio=500):
       
        list_points_radius = []
        lat_central = float(ponto_central[0])
        lon_central = float(ponto_central[1])
        r_terra = 6371000  # Raio da Terra em metros

        for item in lista_pontos:
            
            lat = float(item.coordinates.latitude)
            lon = float(item.coordinates.longitude)

            lat1 = math.radians(lat_central)
            lon1 = math.radians(lon_central)
            lat2 = math.radians(lat)
            lon2 = math.radians(lon)
            
            # Diferenças
            delta_lat = lat2 - lat1
            delta_lon = lon2 - lon1

            # Fórmula de haversine
            a = math.sin(delta_lat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(delta_lon / 2)**2
            c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
            distancia = r_terra * c

            # Verificar se o ponto está dentro do raio
            if distancia <= raio:
                list_points_radius.append(item)

        return list_points_radius

    radius_map_points = points_radius(map_points, ["-23.481570", "-47.740459"])
    maps.add_points_map(radius_map_points)
    mapa1 = maps.create_map()

    def reload_map():

        snack_bar = ft.SnackBar(
                        content=ft.Text(f"Atualziando..."),
                        bgcolor=ft.Colors.AMBER,
                        duration=2000,
                    )
        page.overlay.append(snack_bar)
        snack_bar.open = True
        page.update()

        new_requests_points = markers.create_points(15, True, maps)
        current_map_points = CurrentMapPoints()
        current_map_points.add_list_point(new_requests_points)
        acess_search = Search(page=page, maps=maps, name_points=None)
        list_tiles = []

        for item in new_requests_points:
            name = item.data[0]
            Latitude = item.data[2]
            Longitude = item.data[3]

            def move_and_reset(lat, long):
                maps.move_map(lat, long, 18.4)
                maps.reset_home_text_field()

            list_tiles.append(
                ft.ListTile(
                    title=ft.Text(value=name, color=ft.Colors.WHITE),
                    on_click=lambda e, lat=Latitude, long=Longitude: move_and_reset(lat, long),
                    bgcolor=ft.Colors.BLUE,
                    data=name
                )
            )

        acess_search.reload_itens(list_tiles)

        overlay_copy = list(page.overlay)
        for item in overlay_copy:
            if item.data == "geolocator":
                pass
            else:
                page.overlay.remove(item)

        snack_bar = ft.SnackBar(
                        content=ft.Text(f"Atualizado"),
                        bgcolor=ft.Colors.GREEN,
                        duration=1500,
                    )
        page.overlay.append(snack_bar)
        snack_bar.open = True
        page.update()

        

    def handle_position_change(e):
        point_location.coordinates = map.MapLatitudeLongitude(e.latitude, e.longitude)

    gl = ft.Geolocator(
                    location_settings=ft.GeolocatorSettings(
                        accuracy=ft.GeolocatorPositionAccuracy.BEST,
                        distance_filter=1,
                    ),
                    on_position_change=handle_position_change,
                    data = "geolocator",
                    )
    page.overlay.insert(0, gl)
    list_maps_acess_controls.insert(0, gl)

    def go_to_location(e=None):
        if point_location.coordinates is not None:
            lat = str(point_location.coordinates.latitude)
            long = str(point_location.coordinates.longitude)
            maps.move_map(lat, long, 18.4)

    async def location(e=None):

        snack_bar = ft.SnackBar(
                content=ft.Text(value="Buscando...", color=ft.Colors.BLACK),
                duration=1000,
                bgcolor=ft.Colors.AMBER,
            )
        page.overlay.append(snack_bar)
        snack_bar.open = True

        status = await gl.get_permission_status_async()

        if str(status) == "GeolocatorPermissionStatus.DENIED":

            await gl.request_permission_async(wait_timeout=60)
            page.update()
            try:
               go_to_location()
            except:
                pass
        else:
            go_to_location()

    button_location = buttons.create_call_location_button(
                                                        icon=ft.Icons.MY_LOCATION,
                                                        on_click=location,
                                                        color=ft.Colors.WHITE,
                                                        col=2,
                                                        padding=0,
                                                        )


    task_ref = [None, 1]  # Variável global para rastrear a tarefa

    async def to_check_size(page, maps, point_location, button_location, mapa1):
        
        while True:
            current_points = current_map_points.return_current_points()
            new_points = points_radius(current_points, [maps.get_lat_center_coordinates(), maps.get_long_center_coordinates()])
            maps.reload_map(new_points)
            maps.to_check_update_size()
            maps.update_position()
            if page.route == "/home":
                button_location.controls[0].content.icon_color = (
                    ft.Colors.GREEN if point_location.coordinates else ft.Colors.RED
                )
                mapa1.update()
                button_location.update()
            await asyncio.sleep(1)
        
    def start_task(page, maps, point_location, button_location, mapa1, task_ref):
        if task_ref[0] is None or task_ref[0].done():  # Evita iniciar múltiplas instâncias
            task_ref[0] = page.run_task(
                to_check_size,  
                page, maps, point_location, button_location, mapa1  
            )
    start_task(page, maps, point_location, button_location, mapa1, task_ref)

    def cancel_task():
        task_ref[0].cancel()  



    def go_back():
        cancel_task()
        loading.new_loading_page(page=page, call_layout=lambda:create_page_login(page))

    action1 = lambda e: go_back()

    action2 = lambda e: reload_map()

    action3 = lambda e: loading.new_loading_overlay_page(page=page,
    call_layout=lambda:create_view_postes_form(page, maps))

    action4 = lambda e: loading.new_loading_overlay_page(page=page,
    call_layout=lambda:create_view_orders_form(page, maps))

    action5 = lambda e: loading.new_loading_overlay_page(page=page,
    call_layout=lambda:create_view_users_form(page))


    name_points = markers.return_name_points()
    searchs = Search(page, maps, name_points)
    search_text_fild = searchs.create_search_text()
    search_container = searchs.create_search_container()
    list_maps_acess_controls.insert(0, search_text_fild)
    search_container.visible = False


    containers = Container(page, maps, action1, action2, action3, action4, action5)
    map_layer_container = containers.create_maps_container()
    map_filter_container = containers.create_filter_container()
    menu_container = containers.create_menu_container()

    def show_map_layer_container(e):
        if map_layer_container in page.overlay:
            page.overlay.remove(map_layer_container)
        else:
            overlay_copy = list(page.overlay)
            for item in overlay_copy:
                if item == gl:
                    pass
                else:
                    page.overlay.remove(item)
            page.overlay.append(map_layer_container)
        page.update()

    def show_filter_container(e):
        if map_filter_container in page.overlay:
            page.overlay.remove(map_filter_container)
        else:
            overlay_copy = list(page.overlay)
            for item in overlay_copy:
                if item == gl:
                    pass
                else:
                    page.overlay.remove(item)
            page.overlay.append(map_filter_container)
        page.update()

    def show_menu_container(e):
        if menu_container in page.overlay:
            page.overlay.remove(menu_container)
        else:
            overlay_copy = list(page.overlay)
            for item in overlay_copy:
                if item == gl:
                    pass
                else:
                    page.overlay.remove(item)
            page.overlay.append(menu_container)
        page.update()

    menu = menus.create_settings_menu(color=ft.Colors.WHITE, col=10, action=show_menu_container)

    button_map_layer = buttons.create_call_location_button(
                                                        icon=ft.Icons.LAYERS,
                                                        on_click=show_map_layer_container,
                                                        color=ft.Colors.WHITE,
                                                        col=2,
                                                        padding=0,
                                                        icon_color=ft.Colors.BLUE
                                                        )
    
    button_map_filter = buttons.create_call_location_button(
                                                        icon=ft.Icons.FILTER_ALT_OUTLINED,
                                                        on_click=show_filter_container,
                                                        color=ft.Colors.WHITE,
                                                        col=2,
                                                        padding=0,
                                                        icon_color=ft.Colors.BLUE
                                                        )

    button_map_rotate = buttons.create_call_location_button(
                                                        icon=ft.Icons.ROTATE_RIGHT_OUTLINED,
                                                        on_click=lambda e: maps.reset_map_rotation(),
                                                        color=ft.Colors.WHITE,
                                                        col=2,
                                                        padding=0,
                                                        icon_color=ft.Colors.BLUE
                                                        )


    page.appbar = ft.AppBar(
        bgcolor=ft.Colors.BLUE,
        toolbar_height=80,
        center_title=True,
        actions=[
                search_text_fild,
                ft.Container(width=20),  
                menu,
                ft.Container(width=25),
            ],
    )

    profile = CurrentProfile()
    dict_profile = profile.return_current_profile()

    if dict_profile["permission"] == "adm":
        page.floating_action_button = ft.FloatingActionButton(
                            content=ft.Icon(name=ft.Icons.ADD_LOCATION_ROUNDED, color=ft.Colors.BLUE, scale=2),
                            bgcolor=ft.Colors.WHITE,
                            shape=ft.RoundedRectangleBorder(radius=50),
                            on_click= lambda e: loading.new_loading_overlay_page(page=page,
                            call_layout=lambda:create_page_add_forms(page,
                            maps = maps,
                            )) 
                        )
    
    page.floating_action_button_location = ft.FloatingActionButtonLocation.MINI_CENTER_DOCKED
    page.bottom_appbar = ft.BottomAppBar(
        bgcolor=ft.Colors.BLUE,
        shape=ft.NotchShape.CIRCULAR,
        height=80,
        content=ft.Row(
            spacing=40,
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[
                button_location,
                button_map_rotate,
                ft.Container(width=10),
                button_map_filter,
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



def create_page_forms(page, name, maps, local=False):

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

    texts = CallText(page)
    foto = texts.create_calltext(
                                visible=True,
                                text="Sem foto",
                                color=ft.Colors.BLACK,
                                size=15,
                                font=ft.FontWeight.W_400,
                                col=12,
                                padding=0,
                                )

    if url_imagem1 != "Nulo":
        foto = ft.Image(src=url_imagem1, repeat=None)

    foto_poste = ft.Column(
        [
            ft.Container(
                clip_behavior=ft.ClipBehavior.HARD_EDGE,
                alignment=ft.alignment.center,
                height=400,  
                width=301,
                col=12,  
                border=ft.Border(
                    left=ft.BorderSide(2, ft.Colors.BLACK),
                    top=ft.BorderSide(2, ft.Colors.BLACK),
                    right=ft.BorderSide(2, ft.Colors.BLACK),
                    bottom=ft.BorderSide(2, ft.Colors.BLACK),
                ),
                content=foto  
            )
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=10,  
    )

    def go_back(e=None):
        if local ==False:
            overlay_copy = list(page.overlay)
            for item in overlay_copy:
                if item.data == "geolocator":
                    pass
                else:
                    page.overlay.remove(item)
            page.update()
        else:
            loading.add_loading_overlay_page(page=page,
            call_layout=lambda:create_view_postes_form(page, maps),
            current_container=page.overlay[1])       

    order_layout = lambda e: loading.add_loading_overlay_page(page=page,
    call_layout=lambda:create_invited_page_order(page, name, maps),
    current_container=page.overlay[1])

    profile = CurrentProfile()
    dict_profile = profile.return_current_profile()

    if dict_profile["permission"] == "adm":
        order_layout = lambda e: loading.add_loading_overlay_page(page=page,
        call_layout=lambda:create_adm_page_order(page, name, maps),
        current_container=page.overlay[1])

    order_button = buttons.create_button(on_click=order_layout,
                                            text="Ordens",
                                            color=ft.Colors.RED,
                                            col=None,
                                            padding=5,)
        
    back_home_button = buttons.create_button(on_click=go_back,
                                            text="Voltar",
                                            color=ft.Colors.AMBER,
                                            col=12,
                                            padding=5,)
    
    edit_button = ft.Container(height=2)
    if dict_profile["permission"] == "adm":
        edit_button = buttons.create_button(on_click=lambda e: loading.add_loading_overlay_page(
                                                    page=page,
                                                    call_layout=lambda:create_page_edit_forms(page, name, maps),
                                                    current_container=page.overlay[1],
                                                    ),
                                                text="Editar",
                                                color=ft.Colors.GREEN,
                                                col=None,
                                                padding=5,)    
        

    return  ft.ResponsiveRow(
                columns=12,
                controls=[
                    form,
                    foto_poste,  
                    order_button,
                    edit_button,
                    back_home_button,
                    ft.Container(height=10),   
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            )
                               
def create_page_os_forms(page, name, order, maps):

    loading = LoadingPages(page)
    forms = Forms(page)
    sp = SupaBase(page)


    os = sp.get_os(order)

    data = os.json()

    row = data[0]

    list_os_form =[
        row["created_at"],
        row["ip"],
        row["reclamante"],
        row["function"],
        row["celular"],
        row["order_id"],
        row["origem"],
        row["observacao"],
        row["materiais"],
        row["ponto"],
        row["status"],
        row["data_andamento"],
        row["data_conclusao"],
        row["equipe"]
    ]

    os_forms = forms.create_os_forms(list_os_form)


    def go_back(e=None):
        if name == None:
            loading.add_loading_overlay_page(page=page,
            call_layout=lambda:create_view_orders_form(page, maps),
            current_container=page.overlay[1])
        else:
            loading.add_loading_overlay_page(page=page,
            call_layout=lambda:create_adm_page_order(page, name, maps),
            current_container=page.overlay[1])


    buttons = Buttons(page)
    back_home_button = buttons.create_button(on_click=go_back,
                                            text="Voltar",
                                            color=ft.Colors.AMBER,
                                            col=12,
                                            padding=5,)
    
    edit_button = buttons.create_button(on_click=lambda e: loading.add_loading_overlay_page(page=page,
    call_layout=lambda:create_page_edit_os_forms(page, name, order, maps),
    current_container=page.overlay[1]),
    text="Editar",
    color=ft.Colors.GREEN,
    col=6,
    padding=5,)
          

    return ft.ResponsiveRow(
        columns=12,
        controls=[
            os_forms,
            edit_button,
            back_home_button,
            ft.Container(height=10),   
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
    )

def create_page_user_forms(page, user):

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


    back_home_button = buttons.create_button(on_click= lambda e: loading.add_loading_overlay_page(page=page,
    call_layout=lambda:create_view_users_form(page),
    current_container=page.overlay[1]),
    text="Voltar",
    color=ft.Colors.AMBER,
    col=12,
    padding=5,)
    

    edit_button = buttons.create_button(on_click=lambda e: loading.add_loading_overlay_page(page=page,
    call_layout=lambda:create_page_edit_user_forms(page, user),
    current_container=page.overlay[1]),
    text="Editar",
    color=ft.Colors.GREEN,
    col=12,
    padding=5,)    
        

    return ft.ResponsiveRow(
        columns=12,
        controls=[
            form,
            edit_button,
            back_home_button,
            ft.Container(height=10),   
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
    )



def create_page_add_forms(page, maps):

    forms = Forms(page)
    buttons = Buttons(page)
    sp = SupaBase(page)

    lat = maps.get_lat_center_coordinates()
    lon = maps.get_long_center_coordinates()
    coordinates = [lat, lon]

    def send_point(object, image):

        snack_bar = ft.SnackBar(
                        content=ft.Text(f"Adicionando..."),
                        bgcolor=ft.Colors.AMBER,
                        duration=1000,
                    )
        page.overlay.append(snack_bar)
        snack_bar.open = True
        page.update()  #Necessario

        time.sleep(1)

        if image_temp.controls[0].content != None:
            angle = int(image_temp.controls[0].content.rotate.angle * (180 / math.pi) if image_temp.controls[0].content.rotate else 0)
        else:
            angle = None

        list_forms = [
                object.controls[0].content.rows[0].cells[1].content.content.value,
                object.controls[0].content.rows[1].cells[1].content.content.value,
                object.controls[0].content.rows[2].cells[1].content.content.value,
                object.controls[0].content.rows[3].cells[1].content.content.value,
                object.controls[0].content.rows[4].cells[1].content.content.value,
                object.controls[0].content.rows[5].cells[1].content.content.value,
        ]


        add_point(page, coordinates, list_forms, image=image, angle=angle, maps=maps)
     
    new_number = sp.get_last_form_post()

    forms1 = forms.create_add_forms(ip=new_number, situ=None, tipo=None, pontos=None, bairro=".", logra=".")

    def go_back(e=None):

        overlay_copy = list(page.overlay)
        for item in overlay_copy:
            if item.data == "geolocator":
                    pass
            else:
                page.overlay.remove(item)
        page.update() # Necessario


    add_button = buttons.create_button(on_click=lambda e :send_point(forms1, image_temp.controls[0].content),
                                            text="Adicionar",
                                            color=ft.Colors.GREEN,
                                            col=12,
                                            padding=5,)
    back_home_button = buttons.create_button(on_click=go_back,
                                            text="Voltar",
                                            color=ft.Colors.AMBER,
                                            col=12,
                                            padding=5,)
    

    image_temp = ft.Column(
        [
            ft.Container(
                clip_behavior=ft.ClipBehavior.HARD_EDGE,
                alignment=ft.alignment.center,
                height=400,  
                width=301,
                col=12,  
                border=ft.Border(
                    left=ft.BorderSide(2, ft.Colors.BLACK),
                    top=ft.BorderSide(2, ft.Colors.BLACK),
                    right=ft.BorderSide(2, ft.Colors.BLACK),
                    bottom=ft.BorderSide(2, ft.Colors.BLACK),
                ),
                content=None  
            )
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=10,  
    )




    def on_image_selected(e: ft.FilePickerResultEvent):

            if not e.files or len(e.files) == 0:
                return
            snack_bar = ft.SnackBar(
                content=ft.Text(value="Adicionando imagem...", color=ft.Colors.BLACK),
                duration=2000,
                bgcolor=ft.Colors.AMBER,
            )
            page.overlay.append(snack_bar)
            snack_bar.open = True

            selected_image = e.files[0]

            image_container = ft.Image(src=selected_image.path, col=8) 

            image_temp.controls[0].content = image_container

            page.update()

    fp = ft.FilePicker(on_result=on_image_selected)
    if fp in page.overlay:
        page.overlay.remove(fp)
    page.overlay.insert(2, fp)

    def open_gallery(e): 
        fp.pick_files(              
            allow_multiple=False,
            file_type=ft.FilePickerFileType.IMAGE
        )

    icon_camera = ft.IconButton(
        icon=ft.Icons.CAMERA_ALT,
        icon_color=ft.Colors.AMBER,
        expand=True,
        scale=2,
        on_click=open_gallery,  
        alignment=ft.alignment.center,
        padding=0,
    )

    def rotate(e):
        if hasattr(image_temp.controls[0].content, 'rotate'):

            # Obtemos o ângulo atual em graus, assumindo 0 se não estiver definido
            current_angle_degrees = image_temp.controls[0].content.rotate.angle * (180 / math.pi) if image_temp.controls[0].content.rotate else 0
            # Adicionamos 90 graus ao ângulo atual
            new_angle_degrees = (current_angle_degrees + 90) % 360
            # Define a rotação com o novo ângulo em radianos
            image_temp.controls[0].content.rotate = ft.transform.Rotate(math.radians(new_angle_degrees))

            angle = new_angle_degrees

            page.update()

    icon_rotate = ft.IconButton(
        icon=ft.Icons.ROTATE_RIGHT_OUTLINED,
        icon_color=ft.Colors.AMBER,
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
            back_home_button,
            ft.Container(height=10)   
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,

    )

def create_page_add_os_forms(page, name, maps):

    loading = LoadingPages(page)
    forms = Forms(page)
    buttons = Buttons(page)
    sp = SupaBase(page)
    
    def send_point(object):

        list_add_os = [
            object.controls[0].content.rows[0].cells[1].content.content.value,
            object.controls[0].content.rows[1].cells[1].content.content.value,
            object.controls[0].content.rows[2].cells[1].content.content.value,
            object.controls[0].content.rows[3].cells[1].content.content.value,
            object.controls[0].content.rows[4].cells[1].content.content.value,
            object.controls[0].content.rows[5].cells[1].content.content.value,
            object.controls[0].content.rows[6].cells[1].content.content.value,
            object.controls[0].content.rows[7].cells[1].content.content.value,
            object.controls[0].content.rows[8].cells[1].content.content.value,
            object.controls[0].content.rows[9].cells[1].content.content.value,
            object.controls[0].content.rows[10].cells[1].content.content.value,
            object.controls[0].content.rows[11].cells[1].content.content.value,
            object.controls[0].content.rows[12].cells[1].content.content.value,
            object.controls[0].content.rows[13].cells[1].content.content.value,
        ]
        
        add_os(page, list_add_os, name, maps)

    data_atual = datetime.now()
    data_formatada = data_atual.strftime("%d/%m/%Y")
    id = str(sp.get_os_id())
    new_order = id.zfill(4)

    profile = CurrentProfile()
    dict_profile = profile.return_current_profile()

    profile = CurrentProfile()
    dict_profile = profile.return_current_profile()

    list_os_forms = [data_formatada, name, dict_profile["user"], dict_profile["permission"], dict_profile["number"], new_order, None, None, None, None, "Aberto", "Pendente", "Pendente", None]

    forms1 = forms.create_add_os_forms(list_os_forms)

    add_button = buttons.create_button(on_click=lambda e :send_point(forms1),
                                            text="Adicionar",
                                            color=ft.Colors.GREEN,
                                            col=12,
                                            padding=5,)
    
    back_home_button = buttons.create_button(on_click=lambda e: loading.add_loading_overlay_page(page=page,
    call_layout=lambda:create_adm_page_order(page, name, maps),
    current_container=page.overlay[1]),
    text="Voltar",
    color=ft.Colors.AMBER,
    col=12,
    padding=5,)
    
    return ft.ResponsiveRow(
        columns=12,
        controls=[
            forms1,
            add_button, 
            back_home_button,
            ft.Container(height=10),   
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,

    )

def create_page_add_user_forms(page):
 
    loading = LoadingPages(page)
    forms = Forms(page)
    buttons = Buttons(page)
    sp = SupaBase(page)

    
    def send_point(object, id):

        list_add_user = [
            object.controls[0].content.rows[0].cells[1].content.content.value,
            object.controls[0].content.rows[1].cells[1].content.content.value,
            object.controls[0].content.rows[2].cells[1].content.content.value,
            object.controls[0].content.rows[3].cells[1].content.content.value,
            object.controls[0].content.rows[4].cells[1].content.content.value,
        ]
        
        add_user(page, list_add_user, id)

    id = str(sp.get_user_id())

    list_os_forms = [None, None, None, None, None]

    forms1 = forms.create_add_user_forms(list_os_forms, new=True)

    add_button = buttons.create_button(on_click=lambda e :send_point(forms1, id),
                                            text="Adicionar",
                                            color=ft.Colors.GREEN,
                                            col=12,
                                            padding=15,)
    
    back_home_button = buttons.create_button(on_click=lambda e: loading.add_loading_overlay_page(page=page,
    call_layout=lambda:create_view_users_form(page),
    current_container=page.overlay[1]),
    text="Voltar",
    color=ft.Colors.AMBER,
    col=12,
    padding=15,)
    
    return ft.ResponsiveRow(
        columns=12,
        controls=[
            forms1,
            add_button, 
            back_home_button,
            ft.Container(height=10),   
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,

    )



def create_page_edit_forms(page, name, maps, local=False):
  
    forms = Forms(page)
    loading = LoadingPages(page)
    sp = SupaBase(page)
    buttons = Buttons(page)
    texts = CallText(page)

    def send_point(object, image):

        snack_bar = ft.SnackBar(
        content=ft.Text("Alterando..."),
        bgcolor=ft.Colors.ORANGE,
        duration=1000,
        )
        page.overlay.append(snack_bar)
        snack_bar.open = True
        page.update()

        list_forms = [
            object.controls[0].content.rows[0].cells[1].content.content.value,
            object.controls[0].content.rows[1].cells[1].content.content.value,
            object.controls[0].content.rows[2].cells[1].content.content.value,
            object.controls[0].content.rows[3].cells[1].content.content.value,
            object.controls[0].content.rows[4].cells[1].content.content.value,
            object.controls[0].content.rows[5].cells[1].content.content.value,
        ]

        edit_point(page, list_forms, image, row, maps)

    form = sp.get_form_post(name)
    data = form.json()
    row = data[0]
    numero = int(row["name"].split('-')[1])
    forms1 = forms.create_add_forms(numero, row["situation"], row["type"], row["point"], row["hood"], row["address"])

    def go_back(e=None):
        if local ==False:
            loading.add_loading_overlay_page(page=page,
                                            call_layout=lambda:create_page_forms(page, name, maps),
                                            current_container=page.overlay[1]
                                            )
        else:
            loading.add_loading_overlay_page(page=page,
            call_layout=lambda:create_view_postes_form(page, maps),
            current_container=page.overlay[1])

    add_button = buttons.create_button(on_click=lambda e :send_point(forms1, image_temp.controls[0].content),
                                            text="Salvar",
                                            color=ft.Colors.GREEN,
                                            col=6,
                                            padding=5,)
    delete_button = buttons.create_button(on_click=lambda e :delete_point(page, name, maps),
                                            text="Excluir",
                                            color=ft.Colors.RED,
                                            col=6,
                                            padding=5,)
    back_home_button = buttons.create_button(on_click=go_back,
                                            text="Voltar",
                                            color=ft.Colors.AMBER,
                                            col=7,
                                            padding=5,)
    
    url_imagem1 = sp.get_storage_post(name)
    
    initial_image = texts.create_calltext(
                                visible=True,
                                text="Sem foto",
                                color=ft.Colors.BLACK,
                                size=15,
                                font=ft.FontWeight.W_400,
                                col=12,
                                padding=0,
                                )

    if url_imagem1 != "Nulo":
        initial_image = ft.Image(src=url_imagem1, repeat=None)

    image_temp = ft.Column(
        [
            ft.Container(
                clip_behavior=ft.ClipBehavior.HARD_EDGE,
                alignment=ft.alignment.center,
                height=400,  
                width=301,
                col=12,  
                border=ft.Border(
                    left=ft.BorderSide(2, ft.Colors.BLACK),
                    top=ft.BorderSide(2, ft.Colors.BLACK),
                    right=ft.BorderSide(2, ft.Colors.BLACK),
                    bottom=ft.BorderSide(2, ft.Colors.BLACK),
                ),
                content=initial_image  
            )
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=10,  
    )  

    def on_image_selected(e: ft.FilePickerResultEvent):

            if not e.files or len(e.files) == 0:
                return
            snack_bar = ft.SnackBar(
                content=ft.Text(value="Adicionando imagem...", color=ft.Colors.BLACK),
                duration=2000,
                bgcolor=ft.Colors.AMBER,
            )
            page.overlay.append(snack_bar)
            snack_bar.open = True

            selected_image = e.files[0]

            image_container = ft.Image(src=selected_image.path, col=8, data="foto") 

            image_temp.controls[0].content = image_container

            page.update()

    fp = ft.FilePicker(on_result=on_image_selected)
    if fp in page.overlay:
        page.overlay.remove(fp)
    page.overlay.insert(2, fp)

    def open_gallery(e): 
        fp.pick_files(              
            allow_multiple=False,
            file_type=ft.FilePickerFileType.IMAGE
        )

    icon_camera = ft.IconButton(
        icon=ft.Icons.CAMERA_ALT,
        icon_color=ft.Colors.AMBER,
        expand=True,
        scale=2.3,
        on_click=open_gallery,  # Chama a função diretamente
        alignment=ft.alignment.center,
        padding=0,
    )

    def rotate(e):
        if hasattr(image_temp.controls[0].content, 'rotate'):
            # Obtemos o ângulo atual em graus, assumindo 0 se não estiver definido
            current_angle_degrees = image_temp.controls[0].content.rotate.angle * (180 / math.pi) if image_temp.controls[0].content.rotate else 0
            # Adicionamos 90 graus ao ângulo atual
            new_angle_degrees = (current_angle_degrees + 90) % 360
            # Define a rotação com o novo ângulo em radianos
            image_temp.controls[0].content.rotate = ft.transform.Rotate(math.radians(new_angle_degrees))
            page.update()


    icon_rotate = ft.IconButton(
        icon=ft.Icons.ROTATE_RIGHT_OUTLINED,
        icon_color=ft.Colors.AMBER,
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

def create_page_edit_os_forms(page, name, order, maps):
  
    loading = LoadingPages(page)
    forms = Forms(page)
    buttons = Buttons(page)
    sp = SupaBase(page)

    def send_point(object):

        list_edited_os_forms = [
            object.controls[0].content.rows[0].cells[1].content.content.value,
            object.controls[0].content.rows[1].cells[1].content.content.value,
            object.controls[0].content.rows[2].cells[1].content.content.value,
            object.controls[0].content.rows[3].cells[1].content.content.value,
            object.controls[0].content.rows[4].cells[1].content.content.value,
            object.controls[0].content.rows[5].cells[1].content.content.value,
            object.controls[0].content.rows[6].cells[1].content.content.value,
            object.controls[0].content.rows[7].cells[1].content.content.value,
            object.controls[0].content.rows[8].cells[1].content.content.value,
            object.controls[0].content.rows[9].cells[1].content.content.value,
            object.controls[0].content.rows[10].cells[1].content.content.value,
            object.controls[0].content.rows[11].cells[1].content.content.value,
            object.controls[0].content.rows[12].cells[1].content.content.value,
            object.controls[0].content.rows[13].cells[1].content.content.value,
        ]

        edit_os(page, list_edited_os_forms, order, name, maps)
     

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


    add_button = buttons.create_button(on_click=lambda e :send_point(forms1),
                                            text="Salvar",
                                            color=ft.Colors.GREEN,
                                            col=12,
                                            padding=5,)
    delete_button = buttons.create_button(on_click=lambda e :delete_os(page, name, order, maps),
                                            text="Excluir",
                                            color=ft.Colors.RED,
                                            col=12,
                                            padding=5,)
    back_home_button = buttons.create_button(on_click=lambda e :loading.add_loading_overlay_page(page=page,
    call_layout=lambda:create_page_os_forms(page, name, order, maps),
    current_container=page.overlay[1]),
    text="Voltar",
    color=ft.Colors.AMBER,
    col=12,
    padding=5,)
    


    return ft.ResponsiveRow(
        columns=12,
        controls=[
            forms1,
            add_button,
            delete_button,
            back_home_button,
            ft.Container(height=10),   
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
    )

def create_page_edit_user_forms(page, user):

    loading = LoadingPages(page)
    forms = Forms(page)
    buttons = Buttons(page)
    sp = SupaBase(page)

    def send_point(object, previus_user):

        list_edited_user_forms = [
            object.controls[0].content.rows[0].cells[1].content.content.value,
            object.controls[0].content.rows[1].cells[1].content.content.value,
            object.controls[0].content.rows[2].cells[1].content.content.value,
            object.controls[0].content.rows[3].cells[1].content.content.value,
            object.controls[0].content.rows[4].cells[1].content.content.value,
        ]

        edit_user(page, list_edited_user_forms, previus_user)
     

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


    add_button = buttons.create_button(on_click=lambda e :send_point(forms1, list_user_forms[0]),
                                            text="Salvar",
                                            color=ft.Colors.GREEN,
                                            col=6,
                                            padding=5,)
    delete_button = buttons.create_button(on_click=lambda e :delete_user(page, user),
                                            text="Excluir",
                                            color=ft.Colors.RED,
                                            col=6,
                                            padding=5,)
    back_home_button = buttons.create_button(on_click=lambda e: loading.add_loading_overlay_page(page=page,
    call_layout=lambda:create_page_user_forms(page, user),
    current_container=page.overlay[1]),
    text="Voltar",
    color=ft.Colors.AMBER,
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
 


def create_invited_page_order(page, name, maps):

    loading = LoadingPages(page)
    calltexts = CallText(page)
    buttons = Buttons(page)
    checkboxes = CheckBox(page)
    sp = SupaBase(page)


    text1 = calltexts.create_container_calltext2(text=name)
    text2 = calltexts.create_calltext(
                      visible=True,
                      text="Qual o motivo da ordem de serviço",
                      color=ft.Colors.BLACK,
                      size=30,
                      font=ft.FontWeight.W_900,
                      col=12,
                      padding=20)
    text3 = calltexts.create_calltext(
                        visible=True,
                        text="order enviada com sucesso",
                        color=ft.Colors.GREEN,
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

                profile = CurrentProfile()
                dict_profile = profile.return_current_profile()

                data={
                    "created_at": data_formatada,
                    "ip": name,
                    "numero": numero,
                    "reclamante": dict_profile["user"],
                    "function": "convidado",
                    "celular": dict_profile["number"],
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

                profile = CurrentProfile()
                current_profile = profile.return_current_profile()

                response = requests.post(
                    f'{url}/rest/v1/order_post_{current_profile["city_call_name"]}',
                    headers=headers,
                    json=data,
                )

                if response.status_code == 201:
                    snack_bar = ft.SnackBar(
                        content=ft.Text("ordem enviada com sucesso"),
                        bgcolor=ft.Colors.GREEN,
                        duration=2500,
                    )
                    overlay_copy = list(page.overlay)
                    for item in overlay_copy:
                        if item.data == "geolocator":
                            pass
                        else:
                            page.overlay.remove(item)
                    page.update()
                else:
                    print(f"Resposta do erro: {response.text}")
                    snack_bar = ft.SnackBar(
                        content=ft.Text("Erro ao enviar ordem"),
                        bgcolor=ft.Colors.RED,
                        duration=2500,
                    )

            elif all(box.controls[0].value == False for box in all_checkboxes):
                snack_bar = ft.SnackBar(
                    content=ft.Text("Nenhuma ordem selecionada"),
                    bgcolor=ft.Colors.AMBER,
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
                                        color=ft.Colors.GREEN,
                                        col=6,
                                        padding=15,)
    back_forms_button = buttons.create_button(on_click=lambda e: loading.add_loading_overlay_page(page=page,
    call_layout=lambda:create_page_forms(page, name, maps),
    current_container=page.overlay[1]),
    text="Voltar",
    color=ft.Colors.AMBER,
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

def create_adm_page_order(page, name, maps):

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

    profile = CurrentProfile()
    current_profile = profile.return_current_profile()

    response = requests.get(
        f"{url}/rest/v1/order_post_{current_profile["city_call_name"]}",
        headers=headers,
        params=params,
    )

    data = response.json()

    for row in data:

            data = row["created_at"]
            order = row["order_id"]
            function = row["function"]

            def forms(order):
                return lambda e: loading.add_loading_overlay_page(
                    page=page,
                    call_layout=lambda:create_page_os_forms(page, name, order, maps),
                    current_container=page.overlay[1]
                )
         

            linha = ft.DataRow(cells=[
                        ft.DataCell(ft.Text(value=data, theme_style=ft.TextThemeStyle.TITLE_LARGE, text_align=ft.TextAlign.CENTER)),
                        ft.DataCell(ft.Text(value=order, theme_style=ft.TextThemeStyle.TITLE_MEDIUM, text_align=ft.TextAlign.CENTER)),
                        ft.DataCell(ft.Text(value=function, theme_style=ft.TextThemeStyle.TITLE_MEDIUM, text_align=ft.TextAlign.CENTER)),
                        ft.DataCell(
                            ft.Container(content=
                                         buttons.create_icon_button(
                                                        icon=ft.Icons.SEARCH,
                                                        on_click=forms(order),
                                                        color=ft.Colors.BLUE,
                                                        col=2,
                                                        padding=0,
                                                        icon_color=ft.Colors.WHITE,
                                                        ))
                        ),
                    ])

            dicio[order] = linha

    lista = list(dicio.values())


    
    forms2 =ft.Column(
        controls=[
            ft.Container(
                padding=0,
                theme=texttheme1,  
                content=ft.DataTable(
                    data_row_max_height=50,
                    column_spacing=10,
                    expand=True, 
                    columns=[
                        ft.DataColumn(ft.Text(value="Data", theme_style=ft.TextThemeStyle.TITLE_LARGE)),  
                        ft.DataColumn(ft.Text(value="N°", theme_style=ft.TextThemeStyle.TITLE_LARGE)),  
                        ft.DataColumn(ft.Text(value="", theme_style=ft.TextThemeStyle.TITLE_LARGE)),  
                        ft.DataColumn(ft.Text(value="")),  
                    ],
                    rows=lista,
                ),
            )
        ],
        scroll=ft.ScrollMode.AUTO,  
        alignment=ft.MainAxisAlignment.CENTER,  
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        height=300,
        width=440,  
        expand=True, 
        )

    send_button = buttons.create_button(on_click=lambda e: loading.add_loading_overlay_page(page=page,
    call_layout=lambda:create_page_add_os_forms(page, name, maps),
    current_container=page.overlay[1]),
    text="Adicionar",
    color=ft.Colors.GREEN,
    col=6,
    padding=15,)
    
    back_forms_button = buttons.create_button(on_click=lambda e: loading.add_loading_overlay_page(page=page,
    call_layout=lambda:create_page_forms(page, name, maps),
    current_container=page.overlay[1]),
    text="Voltar",
    color=ft.Colors.AMBER,
    col=6,
    padding=15,
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


def create_page_cities(page):

    sp = SupaBase(page)
    loading = LoadingPages(page)

    web_images = Web_Image(page)
    url_imagem1 = web_images.get_image_url(name="titulo_geopostes")
    login_title = web_images.create_web_image(src=url_imagem1)
    login_title.height = 120 
    url_imagem2 = web_images.get_image_url(name="globo")
    globo_img = web_images.create_web_image(src=url_imagem2)
    globo_img.height = 250

    response = sp.get_cities()
    data = response.json()
    list_cities = []

    profile = CurrentProfile()

    for row in data:
        name = row["name"]
        call_name = row["call_name"]
        lat = row["lat"]
        lon = row["lon"]
        acronym = row["acronym"]

        def add_city(name, call_name, lat, lon, acronym):
            def callback(e):
                anchor.controls[0].close_view()
                page.update()
                time.sleep(0.5)
                profile.add_city_name(name)
                profile.add_city_call_name(call_name)
                profile.add_city_lat(lat)
                profile.add_city_lon(lon)
                profile.add_city_acronym(acronym)
                loading.new_loading_page(page=page, call_layout=lambda: create_page_login(page))
            return callback


        list_tile = ft.ListTile(title=ft.Text(name), on_click=add_city(name=name, call_name=call_name, lat=lat, lon=lon, acronym=acronym))

        list_cities.append(list_tile)

    def handle_tap(e):
        anchor.controls[0].open_view()

    anchor = ft.Column(
        [
            ft.SearchBar(
                view_elevation=4,
                divider_color=ft.Colors.AMBER,
                bar_hint_text="Escolha uma cidade",
                on_tap=handle_tap,
                controls=list_cities,
                width=300,
                bar_bgcolor=ft.Colors.BLUE_700,
                bar_text_style=ft.TextStyle(color=ft.Colors.WHITE)
            ) 
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        width=300,  
    )

    container1 = ft.Container(padding=10)

    return ft.ResponsiveRow(
        columns=12,
        controls=[
            container1,
            login_title,
            container1,
            globo_img,
            container1,
            anchor            
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
    )

def create_page_login(page):

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

    textfields = TextField(page)
    username_field = textfields.create_textfield2(value=None, text="Usuário ou E-mail", password=False)
    password_field = textfields.create_textfield2(value=None, text="Senha", password=True, reveal_password=True)

    loading = LoadingPages(page)

    buttons = Buttons(page)

    btn_login = buttons.create_button(on_click=lambda e: verificar(username_field.controls[0].value, password_field.controls[0].value, page),
                                      text="Entrar",
                                      color=ft.Colors.GREEN,
                                      col=7,
                                      padding=5,)
    btn_register = buttons.create_button(on_click=lambda e: loading.new_loading_page(page=page, call_layout=lambda:create_page_register(page)),
                                         text="Cadastrar",
                                         color=ft.Colors.BLUE_700,
                                         col=7,
                                         padding=5,)
    btn_back = buttons.create_button(on_click=lambda e: loading.new_loading_page(page=page, call_layout=lambda:create_page_cities(page)),
                                         text="Voltar",
                                         color=ft.Colors.AMBER,
                                         col=7,
                                         padding=5,)

    calltexts = CallText(page)
    profile = CurrentProfile()
    current_profile = profile.return_current_profile()
    text1 = calltexts.create_container_calltext2(text=current_profile["city_name"])

    container1 = ft.Container(padding=10)
    container2 = ft.Container(padding=5)


    return ft.ResponsiveRow(
        columns=12,
        controls=[
            container1,
            login_title,
            container2,
            text1,
            container2,  
            username_field,  
            password_field,
            container2,
            btn_login,
            btn_register,
            btn_back, 
            container2,             
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
    )

def create_page_register(page):

    web_images = Web_Image(page)
    url_imagem1 = web_images.get_image_url(name="titulo_geopostes")
    register_title = web_images.create_web_image(src=url_imagem1)

    register_title.col = 12 
    register_title.height = 120

    textfields = TextField(page)
    username_field = textfields.create_textfield2(value=None, text="Primeiro Nome", password=False)
    email_field = textfields.create_textfield2(value=None, text="Email", password=False)
    number_field = textfields.create_textfield2(value=None, text="Celular  Ex: 15912345678", password=False)
    password_field1 = textfields.create_textfield2(value=None, text="Senha", password=True)
    password_field2 = textfields.create_textfield2(value=None, text="Confirmar senha", password=False)

    container1 = ft.Container(padding=5)
    container2 = ft.Container(padding=5)
    loading = LoadingPages(page)
    buttons = Buttons(page)

    btn_register = buttons.create_button(on_click=lambda e: register(username_field.controls[0].value.strip(), email_field.controls[0].value.strip(), number_field.controls[0].value.strip(), password_field1.controls[0].value.strip(), password_field2.controls[0].value.strip(), page),
                                         text="Registrar",
                                         color=ft.Colors.BLUE_700,
                                         col=7,
                                         padding=10,)
    btn_back = buttons.create_button(on_click=lambda e: loading.new_loading_page(page=page, call_layout=lambda:create_page_login(page)),
                                     text="Voltar",
                                     color=ft.Colors.AMBER,
                                     col=7,
                                     padding=10)

    calltexts = CallText(page)
    profile = CurrentProfile()
    current_profile = profile.return_current_profile()
    text1 = calltexts.create_container_calltext2(text=current_profile["city_name"])

    return ft.ResponsiveRow(
        columns=12,
        controls=[
            container1,
            register_title,
            container2,
            text1,
            container2, 
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



def create_view_postes_form(page, maps):

    textthemes = TextTheme()
    texttheme1 = textthemes.create_text_theme1() 
    buttons = Buttons(page)
    loading = LoadingPages(page)
    sp = SupaBase(page)
    chk = CheckBox(page)

    dicio_filter = {
        "name_filter" : "like.*",
        "type_filter" : "like.*"
    }
    dicio = {}

    count_itens = 0

    text_count_itens = ft.Text(value=f"Resultado: {count_itens}",
                               color=ft.Colors.BLACK,
                               text_align=ft.TextAlign.CENTER,
                               size=20,
                               weight=ft.FontWeight.W_900,
                               )

    def changesearch(e, dicio_filter, dicio, forms1, count_itens, text_count_itens):

        time.sleep(0.5)

        try:
            if e.control.value.strip() == "":
                dicio_filter["name_filter"] = "like.*"  
            else:
                dicio_filter["name_filter"] = f"ilike.%{e.control.value.strip().lower()}%"
        except:
            dicio_filter["name_filter"] = "like.*"

        profile = CurrentProfile()
        current_profile = profile.return_current_profile()
        count_itens = 0
        offset = 0
        limit = 1000
        new_response_data = []

        while True:

            params["name"] = dicio_filter["name_filter"]
            params["type"] = dicio_filter["type_filter"]
            params["offset"] = offset
            params["limit"] = limit

            response = requests.get(
                f"{url}/rest/v1/form_post_{current_profile["city_call_name"]}",
                headers=headers,
                params=params,
            )

            data = response.json()
            new_response_data.extend(data)

            if len(data) < limit:
                break
        
            offset += limit

        count_itens = len(new_response_data)
        text_count_itens.value = f"Resultado: {count_itens}"

        dicio.clear()
        for row in new_response_data[:50]:

            name = row["name"]
            number = (str(name.split('-')[1])).zfill(4)

            def forms(name=name):
                return lambda e: loading.add_loading_overlay_page(
                    page=page,
                    call_layout=lambda:create_page_forms(page, name, maps, local=True),
                    current_container=page.overlay[1]
                )

            def edit(name=name):
                return lambda e: loading.add_loading_overlay_page(
                    page=page,
                    call_layout=lambda:create_page_edit_forms(page, name, maps=maps, local=True),
                    current_container=page.overlay[1]
                )

            def delete(name=name):
                return lambda e: delete_point(page, name, maps=maps)

            linha = ft.DataRow(cells=[
                ft.DataCell(ft.Text(value=number, theme_style=ft.TextThemeStyle.TITLE_LARGE)),
                ft.DataCell(
                    ft.Container(content=buttons.create_icon_button(
                        icon=ft.Icons.SEARCH,
                        on_click=forms(),
                        color=ft.Colors.BLUE,
                        col=2,
                        padding=0,
                        icon_color=ft.Colors.WHITE,
                    ))
                ),
                ft.DataCell(
                    ft.Container(content=buttons.create_icon_button(
                        icon=ft.Icons.EDIT_ROUNDED,
                        on_click=edit(),
                        color=ft.Colors.BLUE,
                        col=2,
                        padding=0,
                        icon_color=ft.Colors.WHITE,
                    ))
                ),
                ft.DataCell(
                    ft.Container(content=buttons.create_icon_button(
                        icon=ft.Icons.DELETE,
                        on_click=delete(),
                        color=ft.Colors.BLUE,
                        col=2,
                        padding=0,
                        icon_color=ft.Colors.WHITE,
                    ))
                ),
            ])

            dicio[number] = linha

        forms1.controls[0].content.rows = list(dicio.values())
        page.update()
       

    url = sp.get_url()
    key = sp.get_key()
    offset = 0
    limit = 1000
    response_data = []
    profile = CurrentProfile()
    current_profile = profile.return_current_profile()

    while True:

        headers = {
            "apikey": key,
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json",
        }


        params = {
            "select": "name, situation, type",
            "name": dicio_filter["name_filter"],
            "type": dicio_filter["type_filter"],
            "order": "name.asc",
            "offset": offset,  
            "limit": limit,
        }

        response = requests.get(
            f"{url}/rest/v1/form_post_{current_profile["city_call_name"]}",
            headers=headers,
            params=params,
        )
        
        data = response.json()
        response_data.extend(data)

        if len(data) < limit:
                break
        
        offset += limit

    count_itens = len(response_data)
    text_count_itens.value = f"Resultado: {count_itens}"

    for row in response_data[:50]:

            name = row["name"]

            number = (str(name.split('-')[1])).zfill(4)
           
            def forms(name=name):
                return lambda e: loading.add_loading_overlay_page(
                    page=page,
                    call_layout=lambda:create_page_forms(page, name, maps, local=True),
                    current_container=page.overlay[1]
                )

            def edit(name=name):
                return lambda e: loading.add_loading_overlay_page(
                    page=page,
                    call_layout=lambda:create_page_edit_forms(page, name, maps=maps, local=True),
                    current_container=page.overlay[1]
                )

            def delete(name=name):
                return lambda e :delete_point(page, name, maps=maps)

            linha = ft.DataRow(cells=[
                        ft.DataCell(ft.Text(value=number, theme_style=ft.TextThemeStyle.TITLE_LARGE)),
                        ft.DataCell(
                            ft.Container(content=
                                         buttons.create_icon_button(
                                                        icon=ft.Icons.SEARCH,
                                                        on_click=forms(),
                                                        color=ft.Colors.BLUE,
                                                        col=2,
                                                        padding=0,
                                                        icon_color=ft.Colors.WHITE,
                                                        ))
                        ),
                        ft.DataCell(
                            ft.Container(content=
                                         buttons.create_icon_button(
                                                        icon=ft.Icons.EDIT_ROUNDED,
                                                        on_click=edit(),
                                                        color=ft.Colors.BLUE,
                                                        col=2,
                                                        padding=0,
                                                        icon_color=ft.Colors.WHITE,
                                                        ))
                        ),
                        ft.DataCell(
                            ft.Container(content=
                                         buttons.create_icon_button(
                                                        icon=ft.Icons.DELETE,
                                                        on_click=delete(),
                                                        color=ft.Colors.BLUE,
                                                        col=2,
                                                        padding=0,
                                                        icon_color=ft.Colors.WHITE,
                                                        ))
                        ),
                    ])

            dicio[number] = linha

    lista = list(dicio.values())


    forms1 = ft.Column(
        controls=[
            ft.Container(
                padding=0,  
                expand=True,  
                theme=texttheme1,
                content=ft.DataTable(
                    data_row_max_height=50,
                    column_spacing=40,  
                    expand=True,  
                    columns=[
                        ft.DataColumn(ft.Text(value="", text_align=ft.TextAlign.CENTER)),  
                        ft.DataColumn(ft.Text(value="Ficha", text_align=ft.TextAlign.CENTER)),  
                        ft.DataColumn(ft.Text(value="Editar", text_align=ft.TextAlign.CENTER)),  
                        ft.DataColumn(ft.Text(value="Excluir", text_align=ft.TextAlign.CENTER)),  
                    ],
                    rows=lista,  
                ),
            )
        ],
        scroll=ft.ScrollMode.AUTO,  
        alignment=ft.MainAxisAlignment.CENTER,  
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        height=300,
        width=440,  
        expand=True,  
    )
    
    def show_filter_container(e):
        filter_container.controls[0].visible = not filter_container.controls[0].visible
        filter_container.update()

    def get_permission_filter(e):
        led_type = filter_container.controls[0].content.controls[0].controls[0].value
        led_type_data = filter_container.controls[0].content.controls[0].controls[0].data
        sodium_type = filter_container.controls[0].content.controls[1].controls[0].value
        sodium_type_data = filter_container.controls[0].content.controls[1].controls[0].data
        null_type = filter_container.controls[0].content.controls[2].controls[0].value
        null_type_data = filter_container.controls[0].content.controls[2].controls[0].data
        filter_button.controls[0].bgcolor = ft.Colors.RED
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
            filter_button.controls[0].bgcolor = ft.Colors.BLUE
        filter_container.controls[0].visible = not filter_container.controls[0].visible
        searchfild.value = ""
        page.update()
        changesearch(e, dicio_filter, dicio, forms1, count_itens, text_count_itens),



    filter_container = ft.Row([ 
                        ft.Container(
                            bgcolor=ft.Colors.BLUE,
                            padding=10,
                            margin=10,
                            height=250,
                            width=300,
                            border_radius=20,
                            col=12,
                            visible=False,
                            content=ft.Column([
                                chk.create_checkbox2("Lâmpada LED", 15, None, 8,"Lâmpada LED", True),
                                chk.create_checkbox2("Lâmpada de vapor de sódio", 15, None, 8,"Lâmpada de vapor de sódio", True),
                                chk.create_checkbox2("Sem iluminação", 15, None, 8,".", True),
                                buttons.create_button(on_click=lambda e: get_permission_filter(e),
                                                            text="Aplicar",
                                                            color=ft.Colors.AMBER,
                                                            col=12,
                                                            padding=5,)
                                ])
                            )
                            ],
                            vertical_alignment=ft.CrossAxisAlignment.END,
                            alignment=ft.MainAxisAlignment.CENTER,
                            )

    back_home_button = buttons.create_button(on_click=lambda e: loading.back_home(page=page),
    text="Voltar",
    color=ft.Colors.AMBER,
    col=12,
    padding=5,)

    searchfild = ft.TextField(label="Pesquisar",  # caixa de texto
                                col=8,
                                on_change=lambda e: changesearch(e, dicio_filter, dicio, forms1, count_itens, text_count_itens),
                                label_style= ft.TextStyle(color=ft.Colors.BLACK),
                                text_style= ft.TextStyle(color=ft.Colors.BLACK),
                                text_align=ft.TextAlign.CENTER,
                                border_radius=20,
                                border_color=ft.Colors.BLACK,
                                bgcolor=ft.Colors.WHITE

            )
    
    filter_button = buttons.create_icon_button(
                                                icon=ft.Icons.FILTER_ALT_OUTLINED,
                                                on_click=show_filter_container,
                                                color=ft.Colors.BLUE,
                                                col=6,
                                                padding=0,
                                                icon_color=ft.Colors.WHITE,
                                                )

    return ft.ResponsiveRow(
        columns=12,
        controls=[
            searchfild,
            filter_button,
            filter_container,
            text_count_itens,
            forms1,
            back_home_button,
         
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
    )

def create_view_orders_form(page, maps):

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

    count_itens = 0
    text_count_itens = ft.Text(value=f"Resultado: {count_itens}",
                               color=ft.Colors.BLACK,
                               text_align=ft.TextAlign.CENTER,
                               size=20,
                               weight=ft.FontWeight.W_900,
                               )

    def changesearch(e, dicio_filter, dicio, forms1, count_itens, text_count_itens):

        time.sleep(0.5)

        try:
            if e.control.value.strip() == "":
                dicio_filter["order_filter"] = "like.*"  
            else:
                dicio_filter["order_filter"] = f"like.%{e.control.value}%"
        except:
            dicio_filter["order_filter"] = "like.*"

        profile = CurrentProfile()
        current_profile = profile.return_current_profile()
        count_itens = 0
        offset = 0
        limit = 1000
        new_response_data = []

        while True:

            params["order_id"] = dicio_filter["order_filter"]
            params["function"] = dicio_filter["permission_filter"]
            params["offset"] = offset
            params["limit"] = limit

            response = requests.get(
                f"{url}/rest/v1/order_post_{current_profile["city_call_name"]}",
                headers=headers,
                params=params,
            )

            data = response.json()
            new_response_data.extend(data)

            if len(data) < limit:
                break
        
            offset += limit

        count_itens = len(new_response_data)
        text_count_itens.value = f"Resultado: {count_itens}"

        # Reconstrói as linhas da tabela
        dicio.clear()
        for row in new_response_data[:50]:

            data = row["created_at"]
            order = row["order_id"]
            function = row["function"]

            def forms(order):
                return lambda e: loading.add_loading_overlay_page(
                    page=page,
                    call_layout=lambda:create_page_os_forms(page, name=None, order=order, maps=maps),
                    current_container=page.overlay[1]
                )

            linha = ft.DataRow(cells=[
                    ft.DataCell(ft.Text(value=data, theme_style=ft.TextThemeStyle.TITLE_LARGE, text_align=ft.TextAlign.CENTER)),
                    ft.DataCell(ft.Text(value=order, theme_style=ft.TextThemeStyle.TITLE_MEDIUM, text_align=ft.TextAlign.CENTER)),
                    ft.DataCell(ft.Text(value=function, theme_style=ft.TextThemeStyle.TITLE_MEDIUM, text_align=ft.TextAlign.CENTER)),
                    ft.DataCell(
                        ft.Container(content=
                                        buttons.create_icon_button(
                                                    icon=ft.Icons.SEARCH,
                                                    on_click=forms(order),
                                                    color=ft.Colors.BLUE,
                                                    col=2,
                                                    padding=0,
                                                    icon_color=ft.Colors.WHITE,
                                                    ))
                    ),
                ])

            dicio[order] = linha

        # Atualiza as linhas no DataTable
        forms1.controls[0].content.rows = list(dicio.values())
        page.update()

    url = sp.get_url()
    key = sp.get_key()
    offset = 0
    limit = 1000
    response_data = []
    profile = CurrentProfile()
    current_profile = profile.return_current_profile()

    while True:

        headers = {
            "apikey": key,
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json",
        }

        params = {
            "select": "created_at, order_id, function",
            "order_id": dicio_filter["order_filter"],
            "function": dicio_filter["permission_filter"],
            "order": "order_id.desc",
            "offset": offset,  
            "limit": limit,
        }

        response = requests.get(
            f"{url}/rest/v1/order_post_{current_profile["city_call_name"]}",
            headers=headers,
            params=params,
        )

        data = response.json()
        response_data.extend(data)

        if len(data) < limit:
                break
        
        offset += limit

    count_itens = len(response_data)
    text_count_itens.value = f"Resultado: {count_itens}"

    for row in response_data[:50]:
            
            data = row["created_at"]
            order = row["order_id"]
            function = row["function"]

            def forms(order):

                return lambda e: loading.add_loading_overlay_page(
                    page=page,
                    call_layout=lambda:create_page_os_forms(page, name=None, order=order, maps=maps),
                    current_container=page.overlay[1]
                )
         

            linha = ft.DataRow(cells=[
                        ft.DataCell(ft.Text(value=data, theme_style=ft.TextThemeStyle.TITLE_LARGE, text_align=ft.TextAlign.CENTER)),
                        ft.DataCell(ft.Text(value=order, theme_style=ft.TextThemeStyle.TITLE_MEDIUM, text_align=ft.TextAlign.CENTER)),
                        ft.DataCell(ft.Text(value=function, theme_style=ft.TextThemeStyle.TITLE_MEDIUM, text_align=ft.TextAlign.CENTER)),
                        ft.DataCell(
                            ft.Container(content=
                                         buttons.create_icon_button(
                                                        icon=ft.Icons.SEARCH,
                                                        on_click=forms(order),
                                                        color=ft.Colors.BLUE,
                                                        col=2,
                                                        padding=0,
                                                        icon_color=ft.Colors.WHITE,
                                                        ))
                        ),
                    ])

            dicio[order] = linha

    lista = list(dicio.values())


    forms1 = ft.Column(
        controls=[
            ft.Container(
                padding=0,  
                expand=True,  
                theme=texttheme1,
                content=ft.DataTable(
                    data_row_max_height=50,
                    column_spacing=10,  
                    expand=True,  
                    columns=[
                        ft.DataColumn(ft.Text(value="Data", text_align=ft.TextAlign.CENTER)),  
                        ft.DataColumn(ft.Text(value="Nº", text_align=ft.TextAlign.CENTER)),  
                        ft.DataColumn(ft.Text(value="", text_align=ft.TextAlign.CENTER)),  
                        ft.DataColumn(ft.Text(value="", text_align=ft.TextAlign.CENTER)),  
                    ],
                    rows=lista,  
                ),
            )
        ],
        scroll=ft.ScrollMode.AUTO,  
        alignment=ft.MainAxisAlignment.CENTER,  
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        height=300,
        width=440,  
        expand=True,  
    )
    
    def show_filter_container(e):
        filter_container.controls[0].visible = not filter_container.controls[0].visible
        page.update()

    def get_permission_filter(e):
        adm_permission = filter_container.controls[0].content.controls[0].controls[0].value
        adm_permission_data = filter_container.controls[0].content.controls[0].controls[0].data
        invited_permission = filter_container.controls[0].content.controls[1].controls[0].value
        invited_permission_data = filter_container.controls[0].content.controls[1].controls[0].data
        filter_button.controls[0].bgcolor = ft.Colors.RED
        if adm_permission:
            dicio_filter["permission_filter"] = f"eq.{adm_permission_data}"
        if invited_permission:
            dicio_filter["permission_filter"] = f"eq.{invited_permission_data}"
        if invited_permission and adm_permission:
            dicio_filter["permission_filter"] = f"like.*"
            filter_button.controls[0].bgcolor = ft.Colors.BLUE
        filter_container.controls[0].visible = not filter_container.controls[0].visible
        searchfild.value = ""
        page.update()
        changesearch(e, dicio_filter, dicio, forms1, count_itens, text_count_itens),

    filter_container = ft.Row([
                        ft.Container(
                            bgcolor=ft.Colors.BLUE,
                            padding=10,
                            margin=10,
                            height=200,
                            width=300,
                            border_radius=20,
                            col=10,
                            visible=False,
                            content=ft.Column([
                                chk.create_checkbox2("Administrador", 15, None, 8,"adm", True),
                                chk.create_checkbox2("Convidado", 15, None, 8,"convidado", True),
                                buttons.create_button(on_click=lambda e: get_permission_filter(e),
                                                            text="Aplicar",
                                                            color=ft.Colors.AMBER,
                                                            col=12,
                                                            padding=5,)
                                ])
                            )
                            ],
                            vertical_alignment=ft.CrossAxisAlignment.END,
                            alignment=ft.MainAxisAlignment.CENTER,
                            )
    
    back_home_button = buttons.create_button(on_click=lambda e: loading.back_home(page=page),
    text="Voltar",
    color=ft.Colors.AMBER,
    col=12,
    padding=5,)
    
    searchfild = ft.TextField(label="Procurar",  # caixa de texto
                                col=8,
                                on_change=lambda e: changesearch(e, dicio_filter, dicio, forms1, count_itens, text_count_itens),
                                label_style= ft.TextStyle(color=ft.Colors.BLACK),
                                text_style= ft.TextStyle(color=ft.Colors.BLACK),
                                text_align=ft.TextAlign.CENTER,
                                border_radius=20,
                                border_color=ft.Colors.BLACK,
                                bgcolor=ft.Colors.WHITE

            )
    
    filter_button = buttons.create_icon_button(
                                                icon=ft.Icons.FILTER_ALT_OUTLINED,
                                                on_click=show_filter_container,
                                                color=ft.Colors.BLUE,
                                                col=6,
                                                padding=0,
                                                icon_color=ft.Colors.WHITE,
                                                )

    return ft.ResponsiveRow(
        columns=12,
        controls=[
            searchfild,
            filter_button,
            filter_container,
            text_count_itens,
            forms1,
            back_home_button,   
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
    )

def create_view_users_form(page):
 
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

    count_itens = 0

    text_count_itens = ft.Text(value=f"Resultado: {count_itens}",
                               color=ft.Colors.BLACK,
                               text_align=ft.TextAlign.CENTER,
                               size=20,
                               weight=ft.FontWeight.W_900,
                               )

    def changesearch(e, dicio_filter, dicio, forms1, count_itens, text_count_itens):

        time.sleep(0.5)

        try:
            if e.control.value.strip() == "":
                dicio_filter["user_filter"] = "like.*"  
            else:
                dicio_filter["user_filter"] = f"ilike.%{e.control.value.strip().lower()}%"
        except:
            dicio_filter["user_filter"] = "like.*"

        profile = CurrentProfile()
        current_profile = profile.return_current_profile()
        count_itens = 0
        offset = 0
        limit = 1000
        new_response_data = []

        while True:

            params["usuario"] = dicio_filter["user_filter"]
            params["permission"] = dicio_filter["permission_filter"]
            params["offset"] = offset
            params["limit"] = limit

            response = requests.get(
                f"{url}/rest/v1/users_{current_profile["city_call_name"]}",
                headers=headers,
                params=params,
            )

            data = response.json()
            new_response_data.extend(data)

            if len(data) < limit:
                break
        
            offset += limit

        count_itens = len(new_response_data)
        text_count_itens.value = f"Resultado: {count_itens}"

        dicio.clear()
        for row in new_response_data[:50]:

            user_id = row["user_id"]
            user_name = row["usuario"]
            user_permission = row["permission"]

            def forms(user_name):

                return lambda e: loading.add_loading_overlay_page(
                    page=page,
                    call_layout=lambda:create_page_user_forms(page, user=user_name),
                    current_container=page.overlay[1]
                )
        

            linha = ft.DataRow(cells=[
                        ft.DataCell(ft.Text(value=user_name, theme_style=ft.TextThemeStyle.TITLE_LARGE, text_align=ft.TextAlign.CENTER)),
                        ft.DataCell(ft.Text(value=user_permission, theme_style=ft.TextThemeStyle.TITLE_MEDIUM, text_align=ft.TextAlign.CENTER)),
                        ft.DataCell(
                            ft.Container(content=
                                        buttons.create_icon_button(
                                                        icon=ft.Icons.SEARCH,
                                                        on_click=forms(user_name),
                                                        color=ft.Colors.BLUE,
                                                        col=2,
                                                        padding=0,
                                                        icon_color=ft.Colors.WHITE,
                                                        ))
                        ),
                    ])

            dicio[user_id] = linha

        # Atualiza as linhas no DataTable
        forms1.controls[0].content.rows = list(dicio.values())
        page.update()


    url = sp.get_url()
    key = sp.get_key()
    offset = 0
    limit = 1000
    response_data = []
    profile = CurrentProfile()
    current_profile = profile.return_current_profile()

    while True:

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
            "offset": offset,  
            "limit": limit,
        }

        response = requests.get(
            f"{url}/rest/v1/users_{current_profile["city_call_name"]}",
            headers=headers,
            params=params,
        )

        data = response.json()
        response_data.extend(data)

        if len(data) < limit:
                break
        
        offset += limit
        
    count_itens = len(response_data)
    text_count_itens.value = f"Resultado: {count_itens}"

    for row in response_data[:50]:
            
            user_id = row["user_id"]
            user_name = row["usuario"]
            user_permission = row["permission"]

            def forms(user_name):

                return lambda e: loading.add_loading_overlay_page(
                    page=page,
                    call_layout=lambda:create_page_user_forms(page, user=user_name),
                    current_container=page.overlay[1]
                )
         

            linha = ft.DataRow(cells=[
                        ft.DataCell(ft.Text(value=user_name, theme_style=ft.TextThemeStyle.TITLE_LARGE, text_align=ft.TextAlign.CENTER)),
                        ft.DataCell(ft.Text(value=user_permission, theme_style=ft.TextThemeStyle.TITLE_MEDIUM, text_align=ft.TextAlign.CENTER)),
                        ft.DataCell(
                            ft.Container(content=
                                         buttons.create_icon_button(
                                                        icon=ft.Icons.SEARCH,
                                                        on_click=forms(user_name),
                                                        color=ft.Colors.BLUE,
                                                        col=2,
                                                        padding=0,
                                                        icon_color=ft.Colors.WHITE,
                                                        ))
                        ),
                    ])

            dicio[user_id] = linha

    lista = list(dicio.values())


    forms1 = ft.Column(
        controls=[
            ft.Container(
                padding=0,  
                expand=True,  
                theme=texttheme1,
                content=ft.DataTable(
                    data_row_max_height=50,
                    column_spacing=10,  
                    expand=True,  
                    columns=[
                        ft.DataColumn(ft.Text(value="Usuario", text_align=ft.TextAlign.CENTER)),  
                        ft.DataColumn(ft.Text(value="", text_align=ft.TextAlign.CENTER)),  
                        ft.DataColumn(ft.Text(value="", text_align=ft.TextAlign.CENTER)),  
                    ],
                    rows=lista,  
                ),
            )
        ],
        scroll=ft.ScrollMode.AUTO,  
        alignment=ft.MainAxisAlignment.CENTER,  
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        height=300,
        width=440,  
        expand=True,  
    )
    
    def show_filter_container(e):
        filter_container.controls[0].visible = not filter_container.controls[0].visible
        page.update()

    def get_permission_filter(e):
        adm_permission = filter_container.controls[0].content.controls[0].controls[0].value
        adm_permission_data = filter_container.controls[0].content.controls[0].controls[0].data
        invited_permission = filter_container.controls[0].content.controls[1].controls[0].value
        invited_permission_data = filter_container.controls[0].content.controls[1].controls[0].data
        filter_button.controls[0].bgcolor = ft.Colors.RED
        if adm_permission:
            dicio_filter["permission_filter"] = f"eq.{adm_permission_data}"
        if invited_permission:
            dicio_filter["permission_filter"] = f"eq.{invited_permission_data}"
        if invited_permission and adm_permission:
            dicio_filter["permission_filter"] = f"like.*"
            filter_button.controls[0].bgcolor = ft.Colors.BLUE
        filter_container.controls[0].visible = not filter_container.controls[0].visible
        searchfild.value = ""
        page.update()
        changesearch(e, dicio_filter, dicio, forms1, count_itens, text_count_itens),


    filter_container = ft.Row([
                        ft.Container(
                            bgcolor=ft.Colors.BLUE,
                            padding=10,
                            margin=10,
                            height=200,
                            width=300,
                            border_radius=20,
                            col=10,
                            visible=False,
                            content=ft.Column([
                                chk.create_checkbox2("Administrador", 15, None, 8,"adm", True),
                                chk.create_checkbox2("Convidado", 15, None, 8,"convidado", True),
                                buttons.create_button(on_click=lambda e: get_permission_filter(e),
                                                            text="Aplicar",
                                                            color=ft.Colors.AMBER,
                                                            col=12,
                                                            padding=5,)
                                ])
                            )
                            ],
                            vertical_alignment=ft.CrossAxisAlignment.END,
                            alignment=ft.MainAxisAlignment.CENTER,
                            )


    back_home_button = buttons.create_button(on_click=lambda e: loading.back_home(page=page),
    text="Voltar",
    color=ft.Colors.AMBER,
    col=12,
    padding=5,)
    
    searchfild = ft.TextField(label="Procurar",  # caixa de texto
                                col=8,
                                on_change=lambda e: changesearch(e, dicio_filter, dicio, forms1, count_itens, text_count_itens),
                                label_style= ft.TextStyle(color=ft.Colors.BLACK),
                                text_style= ft.TextStyle(color=ft.Colors.BLACK),
                                text_align=ft.TextAlign.CENTER,
                                border_radius=20,
                                border_color=ft.Colors.BLACK,
                                bgcolor=ft.Colors.WHITE

            )
    
    filter_button = buttons.create_icon_button(
                                                icon=ft.Icons.FILTER_ALT_OUTLINED,
                                                on_click=show_filter_container,
                                                color=ft.Colors.BLUE,
                                                col=6,
                                                padding=0,
                                                icon_color=ft.Colors.WHITE,
                                                )

    add_button = buttons.create_button(on_click=lambda e: loading.add_loading_overlay_page(page=page,
    call_layout=lambda:create_page_add_user_forms(page),
    current_container=page.overlay[1]),
    text="Adicionar",
    color=ft.Colors.GREEN,
    col=6,
    padding=5,)


    return ft.ResponsiveRow(
        columns=12,
        controls=[
            searchfild,
            filter_button,
            filter_container,
            text_count_itens,
            forms1,
            add_button,
            back_home_button,
         
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

        profile = CurrentProfile()
        profile.add_user(name)
        profile.add_permission(permission)
        profile.add_number(number)

        snack_bar = ft.SnackBar(
        content=ft.Text("Login realizado"),
        bgcolor=ft.Colors.GREEN,
        duration= 1000,
        )

        loading.new_loading_page(page=page, call_layout=lambda:create_page_home(page), text="Gerando Mapa", route="/home")
        
    else:
        # Exibe mensagem de erro se as credenciais não forem encontradas
        snack_bar = ft.SnackBar(
            content=ft.Text("Login ou senha incorretos"),
            bgcolor=ft.Colors.RED
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
            bgcolor=ft.Colors.RED
        )
        page.overlay.append(snack_bar)
        snack_bar.open = True
        page.update()
        return  # Interrompe a execução da função
    
    #Verificar se as senhas coincidem
    if password1 != password2:
        snack_bar = ft.SnackBar(
            content=ft.Text("As senhas não coincidem"),
            bgcolor=ft.Colors.RED
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
            bgcolor=ft.Colors.GREEN
        )
    else:
        print(f"Erro ao inserir registro: {response.status_code}")
        print(f"Resposta do erro: {response.text}")
        snack_bar = ft.SnackBar(
            content=ft.Text(f"Erro ao registrar usuário: {response.text}"),
            bgcolor=ft.Colors.RED
        )

    page.overlay.append(snack_bar)
    snack_bar.open = True
    page.update()



def add_point(page, coordinates, list_forms, image, angle, maps):

    sp = SupaBase(page)
    loading = LoadingPages(page)
    buttons = Buttons(page)

    if any(field == "" or field is None for field in list_forms):
        snack_bar = ft.SnackBar(
            content=ft.Text("Alguns campos não foram preenchidos"),
            bgcolor=ft.Colors.RED
        )
        page.overlay.append(snack_bar)
        snack_bar.open = True
        page.update() # Necessario
        return  
    
    response = sp.add_point(list_forms, coordinates, image, angle)

    # Verificar se a inserção foi bem-sucedida
    if response.status_code == 201:

        profile = CurrentProfile()
        current_profile = profile.return_current_profile()

        new_number = list_forms[0].zfill(4)
        ip = f"IP {current_profile["city_acronym"]}-{new_number}"
        point_data = sp.get_one_point_post(ip)
        data = point_data.json()
        row = data[0]
        color_mapping = {
            "yellow": ft.Colors.AMBER,
            "white": ft.Colors.PINK_200,
            "blue": ft.Colors.BLUE
        }

        name = row["name"]
        x = row["x"]
        y = row["y"]
        data_color = row["color"]
        type_point = row["type"]

        point_color = color_mapping.get(data_color, ft.Colors.GREY)

        loading = LoadingPages(page)
    
        def create_on_click(name=name, lat=x, long=y):  
            return lambda e: loading.new_loading_overlay_page(
                page=page,
                call_layout=lambda: create_page_forms(
                    page, name, maps,
                )
            )

        number = int(name.split('-')[1])

        point_button = buttons.create_point_button(
        on_click=create_on_click(),  
        text=str(number),
        color=point_color,
        size=15,
        visible=True,
        )
           
        point_marker = buttons.create_point_marker(
            content=point_button,
            x=x,
            y=y,
            data=[name, type_point, x, y]
        )

        current_map_points = CurrentMapPoints()
        current_map_points.add_point(point_marker)
        maps.add_marker(point_marker)

        def move_and_reset(lat, long):
            maps.move_map(lat, long, 18.4)
            maps.reset_home_text_field()

        item = ft.ListTile(
                    title=ft.Text(value=name, color=ft.Colors.WHITE),
                    on_click=lambda e, lat=x, long=y: move_and_reset(lat, long),
                    bgcolor=ft.Colors.BLUE,
                    data=name,
                )
        
        acess_search = Search(page=page, maps=maps, name_points=None)
        acess_search.add_item(item)
      
        snack_bar = ft.SnackBar(
            content=ft.Text("Ponto adicionado com sucesso"),
            bgcolor=ft.Colors.GREEN,
            duration=3000,
        )

        loading.back_home(page=page)

    elif  response.status_code == 199:
        return  

    else:
        snack_bar = ft.SnackBar(
            content=ft.Text(f"Erro ao inserir ponto: {response.text}"),
            bgcolor=ft.Colors.RED,
            duration=4000,
        )
 
    page.overlay.append(snack_bar)
    snack_bar.open = True
    page.update()

def add_os(page, list_add_os, name, maps):

    sp = SupaBase(page)
    loading = LoadingPages(page)
   
    if any(field == "" or field is None for field in list_add_os):
        snack_bar = ft.SnackBar(
            content=ft.Text("Alguns campos não foram preenchidos"),
            bgcolor=ft.Colors.RED
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
            bgcolor=ft.Colors.GREEN,
            duration=2500,
        )

        loading.add_loading_overlay_page(page=page, call_layout=lambda:create_adm_page_order(page, name, maps),
        current_container=page.overlay[1])
      
    else:
        print(f"Erro ao adicionar ordem: {response.status_code}")
        print(f"Resposta do erro: {response.text}")
        snack_bar = ft.SnackBar(
            content=ft.Text(f"Erro ao adicionar ordem: {response.text}"),
            bgcolor=ft.Colors.RED,
            duration=4000,
        )
 
    page.overlay.append(snack_bar)
    snack_bar.open = True
    page.update()

def add_user(page, list_add_user, id):

    sp = SupaBase(page)
    loading = LoadingPages(page)
   
    if any(field == "" or field is None for field in list_add_user):
        snack_bar = ft.SnackBar(
            content=ft.Text("Alguns campos não foram preenchidos"),
            bgcolor=ft.Colors.RED
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
            bgcolor=ft.Colors.GREEN,
            duration=2500,
        )

        loading.add_loading_overlay_page(page=page,
        call_layout=lambda:create_view_users_form(page),
        current_container=page.overlay[1])
      
    else:
        print(f"Erro ao adicionar usuário: {response.status_code}")
        print(f"Resposta do erro: {response.text}")
        snack_bar = ft.SnackBar(
            content=ft.Text(f"Erro ao adicionar usuario: {response.text}"),
            bgcolor=ft.Colors.RED,
            duration=4000,
        )
 
    page.overlay.append(snack_bar)
    snack_bar.open = True
    page.update()



def edit_point(page, list_edited_forms, image, previous_data, maps):

    sp = SupaBase(page)
    buttons = Buttons(page)

    if any(field == "" or field is None for field in list_edited_forms):
        snack_bar = ft.SnackBar(
            content=ft.Text("Alguns campos não foram preenchidos"),
            bgcolor=ft.Colors.RED
        )
        page.overlay.append(snack_bar)
        snack_bar.open = True
        page.update()
        return  # Interrompe a execução da função

    response = sp.edit_point(image, list_edited_forms, previous_data)
    
    if response.status_code in [200, 204]:  # 204 indica sucesso sem conteúdo

        profile = CurrentProfile()
        current_profile = profile.return_current_profile()

        new_number = (str(list_edited_forms[0])).zfill(4)
        ip = f"IP {current_profile["city_acronym"]}-{new_number}"
        point_data = sp.get_one_point_post(ip)
        data = point_data.json()
        row = data[0]
        color_mapping = {
            "yellow": ft.Colors.AMBER,
            "white": ft.Colors.PINK_200,
            "blue": ft.Colors.BLUE
        }

        name = row["name"]
        x = row["x"]
        y = row["y"]
        data_color = row["color"]
        type_point = row["type"]

        point_color = color_mapping.get(data_color, ft.Colors.GREY)

        loading = LoadingPages(page)
    
        def create_on_click(name=name, lat=x, long=y):  
            return lambda e: loading.new_loading_overlay_page(
                page=page,
                call_layout=lambda: create_page_forms(
                    page, name, maps,
                )
            )

        number = int(name.split('-')[1])

        point_button = buttons.create_point_button(
        on_click=create_on_click(),  
        text=str(number),
        color=point_color,
        size=15,
        visible=True,
        )
           
        point_marker = buttons.create_point_marker(
            content=point_button,
            x=x,
            y=y,
            data=[name, type_point]
        )

        current_map_points = CurrentMapPoints()
        current_map_points.remove_point(previous_data["name"])
        maps.remove_marker(previous_data["name"])
        current_map_points.add_point(point_marker)
        maps.add_marker(point_marker)

        snack_bar = ft.SnackBar(
            content=ft.Text("Alterações Salvas"),
            bgcolor=ft.Colors.GREEN,
            duration=2000,
        )
        loading = LoadingPages(page)
        loading.back_home(page=page)

    elif response.status_code == 199:
        return

    else:
        print(f"Erro ao editar ponto: {response.status_code}")
        print(f"Resposta do erro: {response.text}")
        snack_bar = ft.SnackBar(
            content=ft.Text(f"Erro ao editar ponto: {response.text}"),
            bgcolor=ft.Colors.RED
        )


    page.overlay.append(snack_bar)
    snack_bar.open = True
    page.update()

def edit_os(page, list_edited_os_forms, order, name, maps):

    sp = SupaBase(page)
    loading = LoadingPages(page)

    snack_bar = ft.SnackBar(
        content=ft.Text("Alterando..."),
        bgcolor=ft.Colors.ORANGE,
        duration=1000,
    )
    page.overlay.append(snack_bar)
    snack_bar.open = True
    page.update()


    if any(field == "" or field is None for field in list_edited_os_forms):
        snack_bar = ft.SnackBar(
            content=ft.Text("Alguns campos não foram preenchidos"),
            bgcolor=ft.Colors.RED
        )
        page.overlay.append(snack_bar)
        snack_bar.open = True
        page.update()
        return  # Interrompe a execução da função

    response = sp.edit_os(list_edited_os_forms)
    
    if response.status_code in [200, 204]:  # 204 indica sucesso sem conteúdo
        snack_bar = ft.SnackBar(
            content=ft.Text("Alterações Salvas"),
            bgcolor=ft.Colors.GREEN,
            duration=2000,
        )
        loading.add_loading_overlay_page(page=page,
        call_layout=lambda:create_page_os_forms(page, name, order, maps),
        current_container=page.overlay[1])

    else:
        print(f"Erro ao editar ponto: {response.status_code}")
        print(f"Resposta do erro: {response.text}")
        snack_bar = ft.SnackBar(
            content=ft.Text(f"Erro ao editar ponto: {response.text}"),
            bgcolor=ft.Colors.RED
        )


    page.overlay.append(snack_bar)
    snack_bar.open = True
    page.update()

def edit_user(page, list_edited_user_forms, previus_name):

    sp = SupaBase(page)
    loading = LoadingPages(page)

    snack_bar = ft.SnackBar(
        content=ft.Text("Alterando..."),
        bgcolor=ft.Colors.ORANGE,
        duration=1000,
    )
    page.overlay.append(snack_bar)
    snack_bar.open = True
    page.update()


    if any(field == "" or field is None for field in list_edited_user_forms):
        snack_bar = ft.SnackBar(
            content=ft.Text("Alguns campos não foram preenchidos"),
            bgcolor=ft.Colors.RED
        )
        page.overlay.append(snack_bar)
        snack_bar.open = True
        page.update()
        return  # Interrompe a execução da função

    response = sp.edit_user(list_edited_user_forms, previus_name)
    
    if response.status_code in [200, 204]:  # 204 indica sucesso sem conteúdo
        snack_bar = ft.SnackBar(
            content=ft.Text("Alterações Salvas"),
            bgcolor=ft.Colors.GREEN,
            duration=2000,
        )
        loading.add_loading_overlay_page(page=page,
        call_layout=lambda:create_page_user_forms(page, list_edited_user_forms[0]),
        current_container=page.overlay[1])

    else:
        print(f"Erro ao editar perfil: {response.status_code}")
        print(f"Resposta do erro: {response.text}")
        snack_bar = ft.SnackBar(
            content=ft.Text(f"Erro ao editar perfil: {response.text}"),
            bgcolor=ft.Colors.RED
        )


    page.overlay.append(snack_bar)
    snack_bar.open = True
    page.update()



def delete_point(page, name, maps):

    sp = SupaBase(page)
    loading = LoadingPages(page)

    snack_bar = ft.SnackBar(
        content=ft.Text("Excluindo..."),
        bgcolor=ft.Colors.ORANGE,
        duration=1000,
    )
    page.overlay.append(snack_bar)
    snack_bar.open = True
    page.update()

    list_response = sp.delete_point_post(name)


    if list_response[0].status_code == 204 and list_response[1].status_code == 204:

        current_map_points = CurrentMapPoints()
        current_map_points.remove_point(name)
        maps.remove_marker(name)

        acess_search = Search(page=page, maps=maps, name_points=None)
        acess_search.remove_item(name)

        maps.update_map()

        snack_bar = ft.SnackBar(
                content=ft.Text("Ponto excluido"),
                bgcolor=ft.Colors.GREEN,
                duration=2500,
            )
        loading.back_home(page=page)

    else:
        snack_bar = ft.SnackBar(
            content=ft.Text(f"Erro ao excluir ponto: {list_response[0].text}, {list_response[1].text}, {list_response[2].text}"),
            bgcolor=ft.Colors.RED
        )
        loading.add_loading_overlay_page(page=page,
        call_layout=lambda:create_page_home(page),
        current_container=page.overlay[1])

    page.overlay.append(snack_bar)
    snack_bar.open = True
    page.update()

def delete_os(page, name, order, maps):

    loading = LoadingPages(page)

    snack_bar = ft.SnackBar(
        content=ft.Text("Excluindo..."),
        bgcolor=ft.Colors.ORANGE,
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
                    bgcolor=ft.Colors.GREEN,
                    duration=2500,
                )

            loading.add_loading_overlay_page(page=page,
            call_layout=lambda:create_adm_page_order(page, name, maps),
            current_container=page.overlay[1])

        else:
            snack_bar = ft.SnackBar(
                    content=ft.Text("ordem excluida"),
                    bgcolor=ft.Colors.GREEN,
                    duration=2500,
                )

            loading.back_home(page=page)


    else:
        print(f"Erro ao excluir order: {response.status_code}")
        print(f"Resposta do erro: {response.text}")
        snack_bar = ft.SnackBar(
            content=ft.Text(f"Erro ao excluir order: {response.text}"),
            bgcolor=ft.Colors.RED
        )

    # Exibir a mensagem e atualizar a página
    page.overlay.append(snack_bar)
    snack_bar.open = True
    page.update()

def delete_user(page, user):

    loading = LoadingPages(page)

    snack_bar = ft.SnackBar(
        content=ft.Text("Excluindo..."),
        bgcolor=ft.Colors.ORANGE,
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
                bgcolor=ft.Colors.GREEN,
                duration=2500,
            )

        loading.add_loading_overlay_page(page=page,
        call_layout=lambda:create_view_users_form(page),
        current_container=page.overlay[1])

    else:
        snack_bar = ft.SnackBar(
            content=ft.Text(f"Erro ao excluir usuario: {response.text}"),
            bgcolor=ft.Colors.RED
        )

    # Exibir a mensagem e atualizar a página
    page.overlay.append(snack_bar)
    snack_bar.open = True
    page.update()



class Map:

    def __init__(self, page, point_location, list_maps_acess_controls):
        self.page = page
        self.point_location = point_location

        profile = CurrentProfile()
        current_profile = profile.return_current_profile()
        self.center_map_coordinates = [current_profile["city_lat"], current_profile["city_lon"], None] 

        self.current_zoom = 18.44
        self.zoom_zone = "above_17"
        self.list_filter = ["Lâmpada LED", "Lâmpada de vapor de sódio", "."]
        self.list_maps_acess_controls = list_maps_acess_controls

        self.google = None  #Verificar

        initial_marker =  map.Marker(
                content=ft.Text(""),
                coordinates=map.MapLatitudeLongitude(self.center_map_coordinates, self.center_map_coordinates),
                )
    
        self.MarkerLayer = [[initial_marker]]

        def handle_event(e: map.MapEvent):
            self.center_map_coordinates[0] = f"{e.center.latitude:.6f}"
            self.center_map_coordinates[1] = f"{e.center.longitude:.6f}"
            self.center_map_coordinates[2] = e.zoom
            self.current_zoom = e.zoom

        def tap_event(e: map.MapEvent):

            overlay_copy = list(self.page.overlay)
            for item in overlay_copy:
                if item.data == "geolocator":
                    pass
                else:
                    self.page.overlay.remove(item)
            self.list_maps_acess_controls[0].value = ""
            self.page.update()



        self.google = map.Map(
                    initial_center=map.MapLatitudeLongitude(self.center_map_coordinates[0], self.center_map_coordinates[1]),
                    expand=True,
                    initial_zoom=18.44,
                    min_zoom=16.5,
                    max_zoom=20.9,
                    on_event=handle_event,
                    on_tap=tap_event,
                    interaction_configuration=map.MapInteractionConfiguration(),  
                    layers=[
                        map.TileLayer(
                            url_template="https://tile.openstreetmap.org/{z}/{x}/{y}.png",
                        ),
                        map.MarkerLayer(*self.MarkerLayer),
                        map.RichAttribution(
                            attributions=[map.TextSourceAttribution(text="Teste")]
                        )
                    ],
                )
        conteiner_height = 900

        self.complete_map = ft.Column(
                    visible=True,
                    spacing=0,
                    col=12,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        ft.Container(
                            alignment=ft.alignment.center,
                            bgcolor=ft.Colors.GREY,
                            padding=0,
                            expand=True,
                            height=conteiner_height, 
                            content=ft.Stack(
                                expand=True,  
                                controls=[
                                    self.google,  
                                    ft.TransparentPointer(
                                        content=ft.Container(
                                            alignment=ft.alignment.center,
                                            content=ft.Icon(
                                                name=ft.Icons.CONTROL_POINT,
                                                size=40,
                                                color=ft.Colors.BLACK,
                                            ),
                                        ),
                                    ),
                                ],
                            ),
                        ),
                    ],
                )


    def update_map(self):
        self.google.update()

    def add_points_map(self, points):

        for item in points:
            self.MarkerLayer[0].append(item)
        self.MarkerLayer[0].pop(0)

    def create_map (self):
        return  self.complete_map
         
    def update_position(self):
        if self.point_location.coordinates:
            marker_layer = self.MarkerLayer[0]
            action = marker_layer.remove if self.point_location in marker_layer else marker_layer.append
            action(self.point_location)

    def to_check_update_size(self):

        zoom_mapping = {
        "above_17": {"size": 15},
        "below_17": {"size": 7},
        }

        new_zoom_zone = "above_17" if self.current_zoom > 17.5 else "below_17"

        if new_zoom_zone != self.zoom_zone:
            self.zoom_zone = new_zoom_zone
            zoom_data = zoom_mapping[new_zoom_zone]
            self.current_point_size = zoom_data["size"]
            self.update_size_point(self.current_point_size)

    def update_size_point(self, size):

        for item in self.MarkerLayer[0]:
            if item == self.point_location:
                pass
            else:
                item.content.width = size
                item.content.height = size
                item.content.size = size
            
    def move_map(self, x, y, zoom):
        self.google.move_to(
            destination=map.MapLatitudeLongitude(x, y),
            zoom=zoom
        )
        self.page.overlay[1].visible = False  #Verificar
        self.page.overlay.pop(1)  
        self.page.update()
        
    def change_layer(self, url, max_zoom, zoom_to=False):

        self.google.layers[0].url_template = url
        self.google.max_zoom = max_zoom
        if zoom_to:
            if self.current_zoom > 18.44:
                self.google.zoom_to(zoom=zoom_to)

        overlay_copy = list(self.page.overlay)
        for item in overlay_copy:
            if item.data == "geolocator":
                pass
            else:
                self.page.overlay.remove(item)
        self.page.update()
    
    def filter_map(self, new_filter):

        self.list_filter = new_filter

        overlay_copy = list(self.page.overlay)
        for item in overlay_copy:
            if item.data == "geolocator":
                pass
            else:
                self.page.overlay.remove(item)
        self.list_maps_acess_controls[0].value = ""
        self.page.update()


        current_points = CurrentMapPoints()
        current_points.filter_points(new_filter)

        self.google.update()

    def reset_map_rotation(self):
        self.google.reset_rotation()

    def reset_home_text_field(self):
        self.list_maps_acess_controls[0].value = ""
        self.list_maps_acess_controls[0].update()

    def get_zoom(self):
        return self.google.zoom

    def get_lat_center_coordinates(self):
        return self.center_map_coordinates[0]
    
    def get_long_center_coordinates(self):
        return self.center_map_coordinates[1]

    def add_marker(self, point):
        self.MarkerLayer[0].append(point)
  
    def remove_marker(self, point):
        for item in list(self.MarkerLayer[0]): 
            if item.data[0] == point:  
                self.MarkerLayer[0].remove(item)
                first_item = self.MarkerLayer[0][0]
                self.MarkerLayer[0].remove(first_item)
                self.MarkerLayer[0].append(first_item)
                break  

    def reload_map(self, list_points):
        marker_layer = self.MarkerLayer[0]  # Referência local para otimização
        
        # Remover itens não desejados em uma única operação
        marker_layer[:] = [item for item in marker_layer 
                        if item in list_points or item == self.point_location]

        # Definir o tamanho baseado na zona de zoom
        size = 15 if self.zoom_zone == "above_17" else 7

        # Adicionar novos itens que não estão no marcador
        existing_items = set(marker_layer)  # Conjunto para busca mais rápida
        for item in list_points:
            if item not in existing_items:
                item.content.width = size
                item.content.height = size
                marker_layer.append(item)     
        
class Marker:

    def __init__(self, page):
        self.page = page
        self.NamePoints = {}


    def create_points(self, size, visible, maps):
        
        sp = SupaBase(self.page)
        response_data = []
        offset = 0
        limit = 1000

        while True:
            response = sp.get_point_post(offset=offset, limit=limit)

            if response.status_code != 200:
                print("Erro ao buscar dados:", response.text)
                break

            data = response.json()
            response_data.extend(data)

            # Se o número de registros retornados for menor que o limite, terminamos
            if len(data) < limit:
                break

            offset += limit


        # Inicializa o dicionário de botões e a lista de marcadores
        InitialButtons = {}
        FinalPoints = []

        # Classe Buttons usada para criar botões e marcadores
        buttons = Buttons(self.page)

        color_mapping = {
            "yellow": ft.Colors.AMBER,
            "white": ft.Colors.PINK_200,
            "blue": ft.Colors.BLUE
        }

        count = 0

        # Loop para criar os botões com base nas linhas da tabela
        for row in response_data:
            name = row["name"]
            x = row["x"]
            y = row["y"]
            data_color = row["color"]
            type_point = row["type"]

            count += 1

            point_color = color_mapping.get(data_color, ft.Colors.GREY)

            loading = LoadingPages(self.page)
      
            def create_on_click(name=name, lat=x, long=y):  
                return lambda e: loading.new_loading_overlay_page(
                    page=self.page,
                    call_layout=lambda: create_page_forms(
                        self.page, name, maps,
                    )
                )

            number = int(name.split('-')[1])

            InitialButtons[number] = {
                "element": buttons.create_point_button(
                   on_click=create_on_click(),  
                    text=str(number),
                    color=point_color,
                    size=size,
                    visible=visible,
                ),
                "x": x,
                "y": y,
                "type": type_point,
                "name": name, 
            }

            self.NamePoints[number] = {
                "name": name,
                "x": x,
                "y": y,
            }

        # Cria marcadores com base nos botões criados
        for number, button_data in InitialButtons.items():
            marker = buttons.create_point_marker(
                content=button_data["element"],
                x=button_data["x"],
                y=button_data["y"],
                data=[(button_data["name"]), (button_data["type"]), (button_data["x"]), (button_data["y"])],
            )
            FinalPoints.append(marker)

        # Retorna a lista de marcadores
        return FinalPoints
    
    def return_name_points(self):
        return self.NamePoints

class Search:

    itens = []

    def __init__(self, page, maps, name_points):
        self.page = page
        self.maps = maps
        self.name_points = name_points
        self.sp = SupaBase(self.page)

        if name_points == None:
            return

        self.resultdata = ft.ListView()

        self.resultcon = ft.Row([
                            ft.Container(
                                bgcolor=ft.Colors.BLUE,
                                padding=10,
                                margin=10,
                                height=300,
                                width=300,
                                border_radius=20,
                                col=12,
                                content=ft.Column([
                                    self.resultdata
                                    ])
                                )
                                ],
                        vertical_alignment=ft.CrossAxisAlignment.END,
                        alignment=ft.MainAxisAlignment.CENTER,
                        )

        self.itens.clear()

        for item_data in self.name_points.values():
            name = item_data["name"]
            Latitude = item_data["x"]
            Longitude = item_data["y"]

            loading = LoadingPages(self.page)

            def move_and_reset(lat, long):
                self.maps.move_map(lat, long, 18.4)
                self.maps.reset_home_text_field()

            # Adiciona o botão à lista de itens
            self.itens.append(
                ft.ListTile(
                    title=ft.Text(value=name, color=ft.Colors.WHITE),
                    on_click=lambda e, lat=Latitude, long=Longitude: move_and_reset(lat, long),
                    bgcolor=ft.Colors.BLUE,
                    data=name
                )
            )

        def searchnow(e):
            mysearch = str(e.control.value)
            result = []  # cria outra lista

            if mysearch.strip():  # Se houver texto digitado

                overlay_copy = list(self.page.overlay)
                for item in overlay_copy:
                    if item.data == "geolocator":
                        pass
                    else:
                        self.page.overlay.remove(item)
                page.update()

                if self.resultcon not in self.page.overlay:
                    self.resultcon.visible = True
                    self.page.overlay.insert(1, self.resultcon)  # Adiciona ao overlay
                for item in self.itens:
                    # Verifica se o texto da pesquisa está no título do ListTile
                    if mysearch in item.title.value:  # Usa `.lower()` para ignorar maiúsculas/minúsculas
                        result.append(item)  # Adiciona à lista apenas os itens pesquisados
                    if len(result) >= 5:
                        break

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
                                        label_style= ft.TextStyle(color=ft.Colors.BLACK),
                                        text_style= ft.TextStyle(color=ft.Colors.BLACK),
                                        border_radius=20,
                                        border_color=ft.Colors.WHITE,
                                        bgcolor=ft.Colors.WHITE,
                                        keyboard_type=ft.KeyboardType.NUMBER,
                                        width=300,

            )


    def create_search_text(self):

        return self.txtsearch

    def create_search_container(self):

        return self.resultcon
    
    def reset_serach(self):
        self.txtsearch.value = ""
        self.page.update()

    def add_item(self, item):
        self.itens.append(item)

    def remove_item(self, item_name):
        for item in self.itens:
            if item.data == item_name:
                self.itens.remove(item)
                break
            else:
                pass

    def reload_itens(self, list_itens):
        self.itens.clear()
        for item in list_itens:
            self.itens.append(item)

class Container:

    def __init__(self, page, maps, action1, action2, action3, action4, action5):
        self.page = page
        self.maps = maps
        self.layer_aerial = "https://services.arcgisonline.com/arcgis/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}"
        self.layer_road = "https://tile.openstreetmap.org/{z}/{x}/{y}.png"
        self.sp = SupaBase(page)
        loading = LoadingPages(page)
        web_images = Web_Image(page)
        chk =CheckBox(page)
        buttons = Buttons(page)
        profile = CurrentProfile()
        dict_profile = profile.return_current_profile()

        url_imagem1 = web_images.get_image_url(name="map_aerial")
        map_aerial = web_images.create_web_image(src=url_imagem1) 
        url_imagem2 = web_images.get_image_url(name="map_road")
        map_road = web_images.create_web_image(src=url_imagem2)

        def get_permission_filter(e):

            led_type = self.filter_container.controls[0].content.controls[0].controls[0].value
            sodium_type = self.filter_container.controls[0].content.controls[1].controls[0].value
            null_type = self.filter_container.controls[0].content.controls[2].controls[0].value
            list_map_filter = []

            if led_type:
                list_map_filter.append("Lâmpada LED")
            if sodium_type:
                list_map_filter.append("Lâmpada de vapor de sódio")
            if null_type:
                list_map_filter.append(".")

            self.maps.filter_map(list_map_filter)

        self.map_container = ft.Row([
                                ft.Container(
                                    bgcolor=ft.Colors.BLUE,
                                    padding=10,
                                    margin=10,
                                    height=120,
                                    width=250,
                                    border_radius=20,
                                    alignment=ft.alignment.center,
                                    content=ft.Column([
                                            ft.Row([
                                                ft.Container(
                                                    bgcolor=ft.Colors.WHITE,
                                                    width=100,
                                                    height=100,
                                                    content=(map_road),
                                                    on_click=lambda e, layer=self.layer_road: self.maps.change_layer(layer, 20.9),
                                                    border_radius=10,   
                                                ),
                                                ft.Container(
                                                    bgcolor=ft.Colors.WHITE,
                                                    width=100,
                                                    height=100,
                                                    content=(map_aerial),
                                                    on_click=lambda e, layer=self.layer_aerial: self.maps.change_layer(layer, 18.44, 18.44),
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

        self.filter_container = ft.Row([
                                ft.Container(
                                    bgcolor=ft.Colors.BLUE,
                                    padding=10,
                                    margin=10,
                                    height=250,
                                    width=300,
                                    border_radius=20,
                                    col=12,
                                    content=ft.Column([
                                        chk.create_checkbox2("Lâmpada LED", 15, None, 8,"Lâmpada LED", True),
                                        chk.create_checkbox2("Lâmpada de vapor de sódio", 15, None, 8,"Lâmpada de vapor de sódio", True),
                                        chk.create_checkbox2("Sem iluminação", 15, None, 8,".", True),
                                        buttons.create_button(on_click=lambda e: get_permission_filter(e),
                                                                    text="Aplicar",
                                                                    color=ft.Colors.AMBER,
                                                                    col=12,
                                                                    padding=5,)
                                        ])
                                )
                                ],
                                vertical_alignment=ft.CrossAxisAlignment.END,
                                alignment=ft.MainAxisAlignment.CENTER,
                                )


        listtiles = [

            ft.ListTile(
                title=ft.Text(f"Deslogar", color=ft.Colors.BLACK),
                on_click=action1,
                bgcolor=ft.Colors.WHITE,
                shape=ft.RoundedRectangleBorder(radius=10),
            ),
            ft.ListTile(
                title=ft.Text(f"Atualizar", color=ft.Colors.BLACK),
                on_click=action2,
                bgcolor=ft.Colors.WHITE,
                shape=ft.RoundedRectangleBorder(radius=10),
            ),
        ]

        if dict_profile["permission"] == "adm":

            listtiles.append(
                ft.ListTile(
                        title=ft.Text(f"Lista de postes", color=ft.Colors.BLACK),
                        on_click=action3,
                        bgcolor=ft.Colors.WHITE,
                        shape=ft.RoundedRectangleBorder(radius=10),
                    )
            )
            listtiles.append(
                ft.ListTile(
                        title=ft.Text(f"Lista de ordens de serviço", color=ft.Colors.BLACK),
                        on_click=action4,
                        bgcolor=ft.Colors.WHITE,
                        shape=ft.RoundedRectangleBorder(radius=10),
                    )
            )
            listtiles.append(
                ft.ListTile(
                        title=ft.Text(f"Gestão de usuários", color=ft.Colors.BLACK),
                        on_click=action5,
                        bgcolor=ft.Colors.WHITE,
                        shape=ft.RoundedRectangleBorder(radius=10),
                    )
            )

        self.menu_container = ft.Row([
                                ft.Container(
                                    bgcolor=ft.Colors.BLACK,
                                    padding=10,
                                    margin=10,
                                    height=340,
                                    width=370,
                                    border_radius=20,
                                    col=12,
                                    content=ft.Column(listtiles)
                                )
                                ],
                                vertical_alignment=ft.CrossAxisAlignment.END,
                                alignment=ft.MainAxisAlignment.CENTER,
                                )

    def create_maps_container(self):
        self.map_container.offset = ft.transform.Offset(0, 0)  # Centralizado
        self.map_container.animate_offset = ft.animation.Animation(600, curve="easeIn")
        return self.map_container

    def create_filter_container(self):
        self.filter_container.offset = ft.transform.Offset(0, 0)  # Centralizado
        self.filter_container.animate_offset = ft.animation.Animation(600, curve="easeIn")
        return self.filter_container
    
    def create_menu_container(self):
        self.menu_container.offset = ft.transform.Offset(0, 0)  # Centralizado
        self.menu_container.animate_offset = ft.animation.Animation(600, curve="easeIn")
        return self.menu_container




                



