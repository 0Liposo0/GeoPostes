import flet as ft
from models import *
import requests
import flet.map as map
from datetime import datetime
import math
import time
import asyncio
from reportlab.lib.pagesizes import landscape, letter
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
import pandas as pd

def create_page_home(page):
    
    page.go("/")
    loading = LoadingPages(page)
    buttons = Buttons(page)
    menus = SettingsMenu(page)
    profile = CurrentProfile()
    dict_profile = profile.return_current_profile()

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

        snack_bar = ft.SnackBar(
                        content=ft.Text("Atualizado"),
                        bgcolor=ft.Colors.GREEN,
                        duration=2000,
                    )
        page.overlay.append(snack_bar)
        snack_bar.open = True
        page.update()
        time.sleep(2)
        loading = LoadingPages(page)
        loading.back_home(page=page)


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
    button_location.controls[0].content.icon_color = ft.Colors.GREEN
#..............................................................................................

    task_ref = [None, 1]  # Variável global para rastrear a tarefa

    async def to_check_size(page, maps, point_location, button_location, mapa1):
        
        while True:
            if len(page.overlay) == 1:
                lat_center = maps.get_lat_center_coordinates()
                long_center = maps.get_long_center_coordinates()
                current_points = current_map_points.return_current_points()
                new_points = points_radius(current_points, [lat_center, long_center])
                map_height = (int(page.height)) * 0.83

                maps.reload_map(new_points)
                maps.to_check_update_size()
                maps.update_position()
                maps.update_map_height(map_height)

                if page.route == "/home":
                    mapa1.update()

            await asyncio.sleep(0.75)
        
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

#..............................................................................................

    action1 = lambda e: go_back()

    action2 = lambda e: reload_map()

    action3 = lambda e: loading.new_loading_overlay_page(page=page,
    call_layout=lambda:create_view_form(page, maps, object="post"))

    action4 = lambda e: loading.new_loading_overlay_page(page=page,
    call_layout=lambda:create_view_orders(page, maps, object="post"))

    action5 = lambda e: loading.new_loading_overlay_page(page=page,
    call_layout=lambda:create_view_users_form(page))

    action6 = lambda e: loading.new_loading_overlay_page(page=page,
    call_layout=lambda:create_page_add_forms(page,
    maps = maps,
    object= "post"
    ))

    action7 = lambda e: loading.new_loading_overlay_page(page=page,
    call_layout=lambda:create_page_add_forms(page,
    maps = maps,
    object= "tree"
    ))

    action8 = lambda e: loading.new_loading_overlay_page(page=page,
    call_layout=lambda:create_view_form(page, maps, object="tree"))

    action9 = lambda e: loading.new_loading_overlay_page(page=page,
    call_layout=lambda:create_view_orders(page, maps, object="tree"))

    name_points = markers.return_name_points()
    searchs = Search(page, maps, name_points)
    search_text_fild = searchs.create_search_text()
    search_container = searchs.create_search_container()
    list_maps_acess_controls.insert(0, search_text_fild)
    search_container.visible = False


    containers = Container(page, maps, action1, action2, action3, action4, action5, action6, action7, action8, action9)
    map_layer_container = containers.create_maps_container()
    map_filter_container = containers.create_filter_container()
    menu_container = containers.create_menu_container()
    add_container = containers.create_add_container()

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

    def show_add_container(e):
        if add_container in page.overlay:
            page.overlay.remove(add_container)
        else:
            overlay_copy = list(page.overlay)
            for item in overlay_copy:
                if item == gl:
                    pass
                else:
                    page.overlay.remove(item)
            page.overlay.append(add_container)
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


    if dict_profile["permission"] == "adm":
        page.floating_action_button = ft.FloatingActionButton(
                            content=ft.Icon(name=ft.Icons.ADD_LOCATION_ROUNDED, color=ft.Colors.BLUE, scale=2),
                            bgcolor=ft.Colors.WHITE,
                            shape=ft.RoundedRectangleBorder(radius=50),
                            on_click= show_add_container 
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



def create_page_forms(page, name, maps, object, local=False):

    loading = LoadingPages(page)
    forms = Forms(page)
    sp = SupaBase(page)
    buttons = Buttons(page)
 
    point = sp.get_forms(name, object)
    data = point.json()
    row = data[0]

    default_value = "N/A"

    method_map = {
        "post": [
            row.get("name", default_value), 
            row.get("situation", default_value), 
            row.get("type", default_value), 
            row.get("point", default_value), 
            row.get("hood", default_value), 
            row.get("address", default_value)
        ],
        "tree": [
            row.get("name", default_value), 
            row.get("type", default_value), 
            row.get("height", default_value), 
            row.get("diameter", default_value), 
            row.get("hood", default_value), 
            row.get("address", default_value)
        ]
    }
    
    post_forms = {
       "IP": ft.Text(value=method_map[object][0], theme_style=ft.TextThemeStyle.TITLE_MEDIUM),
       "Situação": ft.Text(value=method_map[object][1], theme_style=ft.TextThemeStyle.TITLE_MEDIUM),
       "Tipo de Lâmpada": ft.Text(value=method_map[object][2], theme_style=ft.TextThemeStyle.TITLE_MEDIUM),
       "Pontos": ft.Text(value=method_map[object][3], theme_style=ft.TextThemeStyle.TITLE_MEDIUM),
       "Bairro": ft.Text(value=method_map[object][4], theme_style=ft.TextThemeStyle.TITLE_MEDIUM),
       "Logradouro": ft.Text(value=method_map[object][5], theme_style=ft.TextThemeStyle.TITLE_MEDIUM)
    }
    tree_forms = {
       "IA": ft.Text(value=method_map[object][0], theme_style=ft.TextThemeStyle.TITLE_MEDIUM),
       "Tipo": ft.Text(value=method_map[object][1], theme_style=ft.TextThemeStyle.TITLE_MEDIUM),
       "Altura aproximada": ft.Text(value=method_map[object][2], theme_style=ft.TextThemeStyle.TITLE_MEDIUM),
       "Diâmetro do tronco": ft.Text(value=method_map[object][3], theme_style=ft.TextThemeStyle.TITLE_MEDIUM),
       "Bairro": ft.Text(value=method_map[object][4], theme_style=ft.TextThemeStyle.TITLE_MEDIUM),
       "Logradouro": ft.Text(value=method_map[object][5], theme_style=ft.TextThemeStyle.TITLE_MEDIUM)
    }

    method_map2 = {
        "post" : post_forms,
        "tree": tree_forms,
    }

    form = forms.create_forms_post(method_map2[object])

    url_imagem1 = sp.get_storage(name, object)

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
            call_layout=lambda:create_view_form(page, maps, object),
            current_container=page.overlay[1])       

    order_layout = lambda e: loading.add_loading_overlay_page(page=page,
    call_layout=lambda:create_invited_page_order(page, name, maps, object),
    current_container=page.overlay[1])

    profile = CurrentProfile()
    dict_profile = profile.return_current_profile()

    if dict_profile["permission"] == "adm":
        order_layout = lambda e: loading.add_loading_overlay_page(page=page,
        call_layout=lambda:create_adm_page_order(page, name, maps, object),
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
                                                    call_layout=lambda:create_page_edit_forms(page, name, maps, object),
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
                               
def create_page_os_forms(page, name, order, maps, object):

    loading = LoadingPages(page)
    forms = Forms(page)
    sp = SupaBase(page)

    os = sp.get_os(order, object)

    data = os.json()

    row = data[0]

    default_value = "N/A"

    method_map = {
        "post": [
            row.get("created_at", default_value), 
            row.get("ip", default_value), 
            row.get("reclamante", default_value), 
            row.get("function", default_value), 
            row.get("celular", default_value), 
            row.get("order_id", default_value),
            row.get("origem", default_value),
            row.get("observacao", default_value),
            row.get("materiais", default_value),
            row.get("ponto", default_value),
            row.get("status", default_value),
            row.get("data_andamento", default_value),
            row.get("data_conclusao", default_value),
            row.get("equipe", default_value),
        ],
        "tree": [
            row.get("created_at", default_value), 
            row.get("ip", default_value), 
            row.get("reclamante", default_value), 
            row.get("function", default_value), 
            row.get("celular", default_value), 
            row.get("order_id", default_value),
            row.get("origem", default_value),
            row.get("observacao", default_value),
            row.get("materiais", default_value),
            row.get("altura", default_value),
            row.get("status", default_value),
            row.get("data_andamento", default_value),
            row.get("data_conclusao", default_value),
            row.get("equipe", default_value),
        ]
    }

    post_forms = {
       "Criação": ft.Text(value=method_map[object][0], theme_style=ft.TextThemeStyle.TITLE_MEDIUM),
       "IP": ft.Text(value=method_map[object][1], theme_style=ft.TextThemeStyle.TITLE_MEDIUM),
       "Reclamante": ft.Text(value=method_map[object][2], theme_style=ft.TextThemeStyle.TITLE_MEDIUM),
       "Usuário": ft.Text(value=method_map[object][3], theme_style=ft.TextThemeStyle.TITLE_MEDIUM),
       "Celular": ft.Text(value=method_map[object][4], theme_style=ft.TextThemeStyle.TITLE_MEDIUM),
       "Ordem": ft.Text(value=method_map[object][5], theme_style=ft.TextThemeStyle.TITLE_MEDIUM),
       "Origem": ft.Text(value=method_map[object][6], theme_style=ft.TextThemeStyle.TITLE_MEDIUM),
       "Observação": ft.Text(value=method_map[object][7], theme_style=ft.TextThemeStyle.TITLE_MEDIUM),
       "Materiais": ft.Text(value=method_map[object][8], theme_style=ft.TextThemeStyle.TITLE_MEDIUM),
       "Ponto": ft.Text(value=method_map[object][9], theme_style=ft.TextThemeStyle.TITLE_MEDIUM),
       "Status": ft.Text(value=method_map[object][10], theme_style=ft.TextThemeStyle.TITLE_MEDIUM),
       "Data do andamento": ft.Text(value=method_map[object][11], theme_style=ft.TextThemeStyle.TITLE_MEDIUM),
       "Data da conclusão": ft.Text(value=method_map[object][12], theme_style=ft.TextThemeStyle.TITLE_MEDIUM),
       "Equipe": ft.Text(value=method_map[object][13], theme_style=ft.TextThemeStyle.TITLE_MEDIUM),
    }
    tree_forms = {
       "Criação": ft.Text(value=method_map[object][0], theme_style=ft.TextThemeStyle.TITLE_MEDIUM),
       "IP": ft.Text(value=method_map[object][1], theme_style=ft.TextThemeStyle.TITLE_MEDIUM),
       "Reclamante": ft.Text(value=method_map[object][2], theme_style=ft.TextThemeStyle.TITLE_MEDIUM),
       "Usuário": ft.Text(value=method_map[object][3], theme_style=ft.TextThemeStyle.TITLE_MEDIUM),
       "Celular": ft.Text(value=method_map[object][4], theme_style=ft.TextThemeStyle.TITLE_MEDIUM),
       "Ordem": ft.Text(value=method_map[object][5], theme_style=ft.TextThemeStyle.TITLE_MEDIUM),
       "Origem": ft.Text(value=method_map[object][6], theme_style=ft.TextThemeStyle.TITLE_MEDIUM),
       "Observação": ft.Text(value=method_map[object][7], theme_style=ft.TextThemeStyle.TITLE_MEDIUM),
       "Materiais": ft.Text(value=method_map[object][8], theme_style=ft.TextThemeStyle.TITLE_MEDIUM),
       "Altura": ft.Text(value=method_map[object][9], theme_style=ft.TextThemeStyle.TITLE_MEDIUM),
       "Status": ft.Text(value=method_map[object][10], theme_style=ft.TextThemeStyle.TITLE_MEDIUM),
       "Data do andamento": ft.Text(value=method_map[object][11], theme_style=ft.TextThemeStyle.TITLE_MEDIUM),
       "Data da conclusão": ft.Text(value=method_map[object][12], theme_style=ft.TextThemeStyle.TITLE_MEDIUM),
       "Equipe": ft.Text(value=method_map[object][13], theme_style=ft.TextThemeStyle.TITLE_MEDIUM),
    }

    method_map2 = {
        "post" : post_forms,
        "tree": tree_forms,
    }

    os_forms = forms.create_os_forms(method_map2[object], object)

    def go_back(e=None):
        if name == None:
            loading.add_loading_overlay_page(page=page,
            call_layout=lambda:create_view_orders(page, maps, object=object),
            current_container=page.overlay[1])
        else:
            loading.add_loading_overlay_page(page=page,
            call_layout=lambda:create_adm_page_order(page, name, maps, object),
            current_container=page.overlay[1])


    buttons = Buttons(page)
    back_home_button = buttons.create_button(on_click=go_back,
                                            text="Voltar",
                                            color=ft.Colors.AMBER,
                                            col=12,
                                            padding=5,)
    
    edit_button = buttons.create_button(on_click=lambda e: loading.add_loading_overlay_page(page=page,
    call_layout=lambda:create_page_edit_os_forms(page, name, order, maps, object),
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



def create_page_add_forms(page, maps, object):

    forms = Forms(page)
    buttons = Buttons(page)
    sp = SupaBase(page)
    textfields = TextField(page)

    lat = maps.get_lat_center_coordinates()
    lon = maps.get_long_center_coordinates()
    coordinates = [lat, lon]

    def send_point(forms, image, rows_forms):

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

        list_forms = []

        for n in range(rows_forms):
            list_forms.append(forms.controls[0].content.rows[n].cells[1].content.content.value)

        add_point(page, coordinates, list_forms, image=image, angle=angle, maps=maps, object=object)
     
    new_number = sp.get_last_form(object)


    def drop_down_menu(value=None, opt1=None, opt2=None, opt3=None, opt4=None, opt5=None, opt6=None):

            list = [opt1, opt2, opt3, opt4, opt5, opt6]
            list_option = []
            for opt in list:
                if opt != None:
                    list_option.append(ft.dropdown.Option(opt))

            menu = ft.Dropdown(
                options=list_option,
                value=value,
                label_style=ft.TextStyle(color=ft.Colors.BLACK, size=12),
                bgcolor=ft.Colors.WHITE,
                options_fill_horizontally=True,
                text_style= ft.TextStyle(size=12, color=ft.Colors.BLACK)
            )
            return menu

    post_forms = {
        "IP": textfields.create_textfield(value=new_number, text=None, password=False, read=None, input_filter=ft.NumbersOnlyInputFilter(), keyboard_type=ft.KeyboardType.NUMBER),
        "Situação": drop_down_menu(None, "Com iluminação", "Sem iluminação"),
        "Tipo de Lâmpada": drop_down_menu(None, ".", "Lâmpada LED", "Lâmpada de vapor de sódio"),
        "Pontos": drop_down_menu(None, "0","1", "2", "3", "4", "5"),
        "Bairro": textfields.create_textfield(value=None, text=None, password=False),
        "Logradouro": textfields.create_textfield(value=None, text=None, password=False)
    }
    tree_forms = {
        "IA": textfields.create_textfield(value=new_number, text=None, password=False, read=None, input_filter=ft.NumbersOnlyInputFilter(), keyboard_type=ft.KeyboardType.NUMBER),
        "Tipo": drop_down_menu(None, "Frutífera", "Infrutífera"),
        "Altura aproximada": textfields.create_textfield(value=None, text=None, password=False),
        "Diâmetro do tronco": textfields.create_textfield(value=None, text=None, password=False),
        "Bairro": textfields.create_textfield(value=None, text=None, password=False),
        "Logradouro": textfields.create_textfield(value=None, text=None, password=False)
    }

    method_map = {
                "post": forms.create_add_forms(post_forms),
                "tree": forms.create_add_forms(tree_forms)
            }

    forms1 = method_map[object]

    rows_forms = len(forms1.controls[0].content.rows)

    def go_back(e=None):

        overlay_copy = list(page.overlay)
        for item in overlay_copy:
            if item.data == "geolocator":
                    pass
            else:
                page.overlay.remove(item)
        page.update() # Necessario


    add_button = buttons.create_button(on_click=lambda e :send_point(forms1, image_temp.controls[0].content, rows_forms),
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

def create_page_add_os_forms(page, name, maps, object):

    loading = LoadingPages(page)
    forms = Forms(page)
    buttons = Buttons(page)
    sp = SupaBase(page)
    textfields = TextField(page)
    
    def send_point(forms, rows_forms):

        list_add_os = []

        for n in range(rows_forms):
            list_add_os.append(forms.controls[0].content.rows[n].cells[1].content.content.value)
        
        add_os(page, list_add_os, name, maps, object)

    data_atual = datetime.now()
    data_formatada = data_atual.strftime("%d/%m/%Y")
    id = str(sp.get_os_id(object))
    new_order = id.zfill(4)

    profile = CurrentProfile()
    dict_profile = profile.return_current_profile()

    def drop_down_menu(value=None, opt1=None, opt2=None, opt3=None, opt4=None, opt5=None, opt6=None):

            list = [opt1, opt2, opt3, opt4, opt5, opt6]
            list_option = []
            for opt in list:
                if opt != None:
                    list_option.append(ft.dropdown.Option(opt))

            menu = ft.Dropdown(
                options=list_option,
                value=value,
                label_style=ft.TextStyle(color=ft.Colors.BLACK, size=12),
                bgcolor=ft.Colors.WHITE,
                options_fill_horizontally=True,
                text_style= ft.TextStyle(size=12, color=ft.Colors.BLACK)
            )
            return menu

    post_forms = {
        "Data de Criação": textfields.create_textfield(value=data_formatada, text=None, password=False, read=True),
        "IP": textfields.create_textfield(value=name, text=None, password=False, read=True),
        "Reclamante": textfields.create_textfield(value=dict_profile["user"], text=None, password=False, read=True),
        "Usuário": textfields.create_textfield(value=dict_profile["permission"], text=None, password=False, read=True),
        "Celular": textfields.create_textfield(value=dict_profile["number"], text=None, password=False, read=True),
        "Ordem": textfields.create_textfield(value=new_order, text=None, password=False, read=True),
        "Origem": textfields.create_textfield(value=None, text=None, password=False),
        "Observação": textfields.create_textfield(value=None, text=None, password=False),
        "Material": textfields.create_textfield(value=None, text=None, password=False),
        "Ponto Queimado": drop_down_menu(None, "1", "2", "3", "4", "5"),
        "Status": drop_down_menu("Aberto", "Aberto", "Andamento", "Concluido"),
        "Data de Andamento": textfields.create_textfield(value="Pendente", text=None, password=False),
        "Data de Conclusão": textfields.create_textfield(value="Pendente", text=None, password=False),
        "Equipe": textfields.create_textfield(value=None, text=None, password=False), 
    }
    tree_forms = {
        "Data de Criação": textfields.create_textfield(value=data_formatada, text=None, password=False, read=True),
        "IP": textfields.create_textfield(value=name, text=None, password=False, read=True),
        "Reclamante": textfields.create_textfield(value=dict_profile["user"], text=None, password=False, read=True),
        "Usuário": textfields.create_textfield(value=dict_profile["permission"], text=None, password=False, read=True),
        "Celular": textfields.create_textfield(value=dict_profile["number"], text=None, password=False, read=True),
        "Ordem": textfields.create_textfield(value=new_order, text=None, password=False, read=True),
        "Origem": textfields.create_textfield(value=None, text=None, password=False),
        "Observação": textfields.create_textfield(value=None, text=None, password=False),
        "Material": textfields.create_textfield(value=None, text=None, password=False),
        "Altura": drop_down_menu(None, "1", "2", "3", "4", "5"),
        "Status": drop_down_menu("Aberto", "Aberto", "Andamento", "Concluido"),
        "Data de Andamento": textfields.create_textfield(value="Pendente", text=None, password=False),
        "Data de Conclusão": textfields.create_textfield(value="Pendente", text=None, password=False),
        "Equipe": textfields.create_textfield(value=None, text=None, password=False), 
    }

    method_map = {
                "post": forms.create_add_os_forms(post_forms),
                "tree": forms.create_add_os_forms(tree_forms)
            }
    
    forms1 = method_map[object]

    rows_forms = len(forms1.controls[0].content.rows)

    add_button = buttons.create_button(on_click=lambda e :send_point(forms1, rows_forms),
                                            text="Adicionar",
                                            color=ft.Colors.GREEN,
                                            col=12,
                                            padding=5,)
    
    back_home_button = buttons.create_button(on_click=lambda e: loading.add_loading_overlay_page(page=page,
    call_layout=lambda:create_adm_page_order(page, name, maps, object),
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



def create_page_edit_forms(page, name, maps, object, local=False):
  
    forms = Forms(page)
    loading = LoadingPages(page)
    sp = SupaBase(page)
    buttons = Buttons(page)
    texts = CallText(page)
    textfields = TextField(page)

    def send_point(forms, image, rows_forms):

        snack_bar = ft.SnackBar(
        content=ft.Text("Alterando..."),
        bgcolor=ft.Colors.ORANGE,
        duration=1000,
        )
        page.overlay.append(snack_bar)
        snack_bar.open = True
        page.update()

        list_forms = []

        for n in range(rows_forms):
            list_forms.append(forms.controls[0].content.rows[n].cells[1].content.content.value)

        edit_point(page, list_forms, image, row, maps, object)

    form = sp.get_forms(name, object)
    data = form.json()
    row = data[0]
    numero = int(row["name"].split('-')[1])
    default_value = "N/A"

    def drop_down_menu(value=None, opt1=None, opt2=None, opt3=None, opt4=None, opt5=None, opt6=None):

            list = [opt1, opt2, opt3, opt4, opt5, opt6]
            list_option = []
            for opt in list:
                if opt != None:
                    list_option.append(ft.dropdown.Option(opt))

            menu = ft.Dropdown(
                options=list_option,
                value=value,
                label_style=ft.TextStyle(color=ft.Colors.BLACK, size=12),
                bgcolor=ft.Colors.WHITE,
                options_fill_horizontally=True,
                text_style= ft.TextStyle(size=12, color=ft.Colors.BLACK)
            )
            return menu

    post_forms = {
        "IP": textfields.create_textfield(value=numero, text=None, password=False, read=None, input_filter=ft.NumbersOnlyInputFilter(), keyboard_type=ft.KeyboardType.NUMBER),
        "Situação": drop_down_menu(row.get("situation", default_value), "Com iluminação", "Sem iluminação"),
        "Tipo de Lâmpada": drop_down_menu(row.get("type", default_value), ".", "Lâmpada LED", "Lâmpada de vapor de sódio"),
        "Pontos": drop_down_menu(row.get("point", default_value), "0","1", "2", "3", "4", "5"),
        "Bairro": textfields.create_textfield(value=row.get("hood", default_value), text=None, password=False),
        "Logradouro": textfields.create_textfield(value=row.get("address", default_value), text=None, password=False)
    }
    tree_forms = {
        "IA": textfields.create_textfield(value=numero, text=None, password=False, read=None, input_filter=ft.NumbersOnlyInputFilter(), keyboard_type=ft.KeyboardType.NUMBER),
        "Tipo": drop_down_menu(row.get("type", default_value), "Frutífera", "Infrutífera"),
        "Altura aproximada": textfields.create_textfield(value=row.get("height", default_value), text=None, password=False),
        "Diâmetro do tronco": textfields.create_textfield(value=row.get("diameter", default_value), text=None, password=False),
        "Bairro": textfields.create_textfield(value=row.get("hood", default_value), text=None, password=False),
        "Logradouro": textfields.create_textfield(value=row.get("address", default_value), text=None, password=False)
    }

    method_map = {
                "post": forms.create_add_forms(post_forms),
                "tree": forms.create_add_forms(tree_forms)
            }

    forms1 = method_map[object]

    rows_forms = len(forms1.controls[0].content.rows)

    def go_back(e=None):
        if local ==False:
            loading.add_loading_overlay_page(page=page,
                                            call_layout=lambda:create_page_forms(page, name, maps, object),
                                            current_container=page.overlay[1]
                                            )
        else:
            loading.add_loading_overlay_page(page=page,
            call_layout=lambda:create_view_form(page, maps, object),
            current_container=page.overlay[1])

    add_button = buttons.create_button(on_click=lambda e :send_point(forms1, image_temp.controls[0].content, rows_forms),
                                            text="Salvar",
                                            color=ft.Colors.GREEN,
                                            col=6,
                                            padding=5,)
    delete_button = buttons.create_button(on_click=lambda e :delete_point(page, name, maps, object),
                                            text="Excluir",
                                            color=ft.Colors.RED,
                                            col=6,
                                            padding=5,)
    back_home_button = buttons.create_button(on_click=go_back,
                                            text="Voltar",
                                            color=ft.Colors.AMBER,
                                            col=7,
                                            padding=5,)
    
    url_imagem1 = sp.get_storage(name, object)
    
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

def create_page_edit_os_forms(page, name, order, maps, object):
  
    loading = LoadingPages(page)
    forms = Forms(page)
    buttons = Buttons(page)
    sp = SupaBase(page)
    textfields = TextField(page)

    def send_point(forms, rows_forms):

        list_edited_os_forms = []

        for n in range(rows_forms):
            list_edited_os_forms.append(forms.controls[0].content.rows[n].cells[1].content.content.value)

        edit_os(page, list_edited_os_forms, order, name, maps, object)
     
    os = sp.get_os(order, object)
    data = os.json()
    row = data[0]
    default_value = "N/A"

    def drop_down_menu(value=None, opt1=None, opt2=None, opt3=None, opt4=None, opt5=None, opt6=None):

            list = [opt1, opt2, opt3, opt4, opt5, opt6]
            list_option = []
            for opt in list:
                if opt != None:
                    list_option.append(ft.dropdown.Option(opt))

            menu = ft.Dropdown(
                options=list_option,
                value=value,
                label_style=ft.TextStyle(color=ft.Colors.BLACK, size=12),
                bgcolor=ft.Colors.WHITE,
                options_fill_horizontally=True,
                text_style= ft.TextStyle(size=12, color=ft.Colors.BLACK)
            )
            return menu

    post_forms = {
        "Data de Criação": textfields.create_textfield(value=row.get("created_at", default_value), text=None, password=False, read=True),
        "IP": textfields.create_textfield(value=row.get("ip", default_value), text=None, password=False, read=True),
        "Reclamante": textfields.create_textfield(value=row.get("reclamante", default_value), text=None, password=False, read=True),
        "Usuário": textfields.create_textfield(value=row.get("function", default_value), text=None, password=False, read=True),
        "Celular": textfields.create_textfield(value=row.get("celular", default_value), text=None, password=False, read=True),
        "Ordem": textfields.create_textfield(value=row.get("order_id", default_value), text=None, password=False, read=True),
        "Origem": textfields.create_textfield(value=row.get("origem", default_value), text=None, password=False),
        "Observação": textfields.create_textfield(value=row.get("observacao", default_value), text=None, password=False),
        "Material": textfields.create_textfield(value=row.get("materiais", default_value), text=None, password=False),
        "Ponto Queimado": drop_down_menu(row.get("ponto", default_value), "1", "2", "3", "4", "5"),
        "Status": drop_down_menu(row.get("status", default_value), "Aberto", "Andamento", "Concluido"),
        "Data de Andamento": textfields.create_textfield(value=row.get("data_andamento", default_value), text=None, password=False),
        "Data de Conclusão": textfields.create_textfield(value=row.get("data_conclusao", default_value), text=None, password=False),
        "Equipe": textfields.create_textfield(value=row.get("equipe", default_value), text=None, password=False), 
    }
    tree_forms = {
        "Data de Criação": textfields.create_textfield(value=row.get("created_at", default_value), text=None, password=False, read=True),
        "IP": textfields.create_textfield(value=row.get("ip", default_value), text=None, password=False, read=True),
        "Reclamante": textfields.create_textfield(value=row.get("reclamante", default_value), text=None, password=False, read=True),
        "Usuário": textfields.create_textfield(value=row.get("function", default_value), text=None, password=False, read=True),
        "Celular": textfields.create_textfield(value=row.get("celular", default_value), text=None, password=False, read=True),
        "Ordem": textfields.create_textfield(value=row.get("order_id", default_value), text=None, password=False, read=True),
        "Origem": textfields.create_textfield(value=row.get("origem", default_value), text=None, password=False),
        "Observação": textfields.create_textfield(value=row.get("observacao", default_value), text=None, password=False),
        "Material": textfields.create_textfield(value=row.get("materiais", default_value), text=None, password=False),
        "Altura": drop_down_menu(row.get("altura", default_value), "1", "2", "3", "4", "5"),
        "Status": drop_down_menu(row.get("status", default_value), "Aberto", "Andamento", "Concluido"),
        "Data de Andamento": textfields.create_textfield(value=row.get("data_andamento", default_value), text=None, password=False),
        "Data de Conclusão": textfields.create_textfield(value=row.get("data_conclusao", default_value), text=None, password=False),
        "Equipe": textfields.create_textfield(value=row.get("equipe", default_value), text=None, password=False), 
    }

    method_map = {
                "post": forms.create_add_os_forms(post_forms),
                "tree": forms.create_add_os_forms(tree_forms)
            }
    
    forms1 = method_map[object]
    rows_forms = len(forms1.controls[0].content.rows)

    add_button = buttons.create_button(on_click=lambda e :send_point(forms1, rows_forms),
                                            text="Salvar",
                                            color=ft.Colors.GREEN,
                                            col=12,
                                            padding=5,)
    delete_button = buttons.create_button(on_click=lambda e :delete_os(page, name, order, maps, object),
                                            text="Excluir",
                                            color=ft.Colors.RED,
                                            col=12,
                                            padding=5,)
    back_home_button = buttons.create_button(on_click=lambda e :loading.add_loading_overlay_page(page=page,
    call_layout=lambda:create_page_os_forms(page, name, order, maps, object),
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
 


def create_invited_page_order(page, name, maps, object):

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
                id = str(sp.get_os_id(object))
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

                method_map = {
                "post": {
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
                    "equipe": "Attam",
                    },
                "tree": {
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
                    "altura": ".",
                    "status": "Aberto",
                    "data_andamento": ".",
                    "data_conclusao": ".",
                    "equipe": "Attam",
                    },
                
                }

                data = method_map[object]

                profile = CurrentProfile()
                current_profile = profile.return_current_profile()

                response = requests.post(
                    f'{url}/rest/v1/order_{object}_{current_profile["city_call_name"]}',
                    headers=headers,
                    json=data,
                )

                if response.status_code == 201:
                    snack_bar = ft.SnackBar(
                        content=ft.Text("ordem enviada com sucesso"),
                        bgcolor=ft.Colors.GREEN,
                        duration=2000,
                    )
                    page.overlay.append(snack_bar)
                    snack_bar.open = True
                    page.update()
                    time.sleep(2)
                    loading = LoadingPages(page)
                    loading.back_home(page=page)
                    
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

    method_map2 = {
                "post": [
                        checkboxes.create_checkbox(text="Ponto apagado", size=25, on_change=checkbox_changed, col=12, data="Ponto apagado"),
                        checkboxes.create_checkbox(text="Ponto piscando", size=25, on_change=checkbox_changed, col=12, data="Ponto piscando"),
                        checkboxes.create_checkbox(text="Ponto aceso durante o dia", size=25, on_change=checkbox_changed, col=12, data="Ponto aceso durante o dia"),
                        checkboxes.create_checkbox(text="Rachadura", size=25, on_change=checkbox_changed, col=12, data="Rachadura"),
                        checkboxes.create_checkbox(text="Queda", size=25, on_change=checkbox_changed, col=12, data="Queda"),
                        checkboxes.create_checkbox(text="Incêndio elétrico", size=25, on_change=checkbox_changed, col=12, data="Incêndio elétrico"),
                        checkboxes.create_checkbox(text="Adicionar ponto", size=25, on_change=checkbox_changed, col=12, data="Adicionar ponto"),
                    ],
                "tree": [
                        checkboxes.create_checkbox(text="Queda", size=25, on_change=checkbox_changed, col=12, data="Queda"),
                        checkboxes.create_checkbox(text="Obstrução de fiação", size=25, on_change=checkbox_changed, col=12, data="Obstrução de fiação"),
                        checkboxes.create_checkbox(text="Rachadura", size=25, on_change=checkbox_changed, col=12, data="Rachadura"),
                        checkboxes.create_checkbox(text="Invasão de terreno", size=25, on_change=checkbox_changed, col=12, data="Rachadura"),
                        checkboxes.create_checkbox(text="Adicionar ponto", size=25, on_change=checkbox_changed, col=12, data="Adicionar ponto"),
                    ],    
                }

    all_checkboxes = method_map2[object]


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

def create_adm_page_order(page, name, maps, object):

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
        "select": "created_at, order_id, status",
        "order": "order_id.desc"
    }

    profile = CurrentProfile()
    current_profile = profile.return_current_profile()

    response = requests.get(
        f'{url}/rest/v1/order_{object}_{current_profile["city_call_name"]}',
        headers=headers,
        params=params,
    )

    data = response.json()

    for row in data:

            data = row["created_at"]
            order = row["order_id"]
            status = row["status"]

            def forms(order):
                return lambda e: loading.add_loading_overlay_page(
                    page=page,
                    call_layout=lambda:create_page_os_forms(page, name, order, maps, object),
                    current_container=page.overlay[1]
                )
         

            linha = ft.DataRow(cells=[
                        ft.DataCell(ft.Text(value=data, theme_style=ft.TextThemeStyle.TITLE_LARGE, text_align=ft.TextAlign.CENTER)),
                        ft.DataCell(ft.Text(value=order, theme_style=ft.TextThemeStyle.TITLE_MEDIUM, text_align=ft.TextAlign.CENTER)),
                        ft.DataCell(ft.Text(value=status, theme_style=ft.TextThemeStyle.TITLE_MEDIUM, text_align=ft.TextAlign.CENTER)),
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
                        ft.DataColumn(ft.Text(value="Status", theme_style=ft.TextThemeStyle.TITLE_LARGE)),  
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
    call_layout=lambda:create_page_add_os_forms(page, name, maps, object),
    current_container=page.overlay[1]),
    text="Adicionar",
    color=ft.Colors.GREEN,
    col=6,
    padding=15,)
    
    back_forms_button = buttons.create_button(on_click=lambda e: loading.add_loading_overlay_page(page=page,
    call_layout=lambda:create_page_forms(page, name, maps, object),
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
        objects = row["objects"]

        list_objects = []
        if "post" in objects:
            list_objects.append("post")
        if "tree" in objects:
            list_objects.append("tree")

        def add_city(name, call_name, lat, lon, acronym, list_objects):
            def callback(e):
                anchor.controls[0].close_view()
                page.update()
                time.sleep(0.5)
                profile.add_city_name(name)
                profile.add_city_call_name(call_name)
                profile.add_city_lat(lat)
                profile.add_city_lon(lon)
                profile.add_city_acronym(acronym)
                profile.add_city_objects(list_objects)
                loading.new_loading_page(page=page, call_layout=lambda: create_page_login(page))
            return callback


        list_tile = ft.ListTile(title=ft.Text(name), on_click=add_city(name=name, call_name=call_name, lat=lat, lon=lon, acronym=acronym, list_objects=list_objects))

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



def create_view_form(page, maps, object):

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

    def changesearch(e, dicio_filter, dicio, forms1, count_itens, text_count_itens, all_data_dicio):

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

            method_map[object]["name"] = dicio_filter["name_filter"]
            method_map[object]["type"] = dicio_filter["type_filter"]
            method_map[object]["offset"] = offset
            method_map[object]["limit"] = limit

            response = requests.get(
                f'{url}/rest/v1/form_{object}_{current_profile["city_call_name"]}',
                headers=headers,
                params=method_map[object],
            )

            data = response.json()
            new_response_data.extend(data)

            if len(data) < limit:
                break
        
            offset += limit

        count_itens = len(new_response_data)
        text_count_itens.value = f"Resultado: {count_itens}"
        dicio.clear()
        all_data_dicio.clear()

        if new_response_data[0] == "code" or len(new_response_data) == 0:
            count_itens = 0
            text_count_itens.value = f"Resultado: {count_itens}"
            dicio.values() == None
        else:

            for row in new_response_data:

                default_value = "N/A"

                method_map4 = {
                    "post": [
                        row.get("name", default_value), 
                        row.get("situation", default_value), 
                        row.get("type", default_value), 
                        row.get("point", default_value), 
                        row.get("hood", default_value), 
                        row.get("address", default_value)
                    ],
                    "tree": [
                        row.get("name", default_value), 
                        row.get("type", default_value), 
                        row.get("height", default_value), 
                        row.get("diameter", default_value), 
                        row.get("hood", default_value), 
                        row.get("address", default_value)
                    ]
                }

                all_data_dicio.append(method_map4[object])

            for row in new_response_data[:50]:

                name = row["name"]
                number = (str(name.split('-')[1])).zfill(4)

                def forms(name=name):
                    return lambda e: loading.add_loading_overlay_page(
                        page=page,
                        call_layout=lambda:create_page_forms(page, name, maps, object, local=True),
                        current_container=page.overlay[1]
                    )

                def edit(name=name):
                    return lambda e: loading.add_loading_overlay_page(
                        page=page,
                        call_layout=lambda:create_page_edit_forms(page, name, maps=maps, object=object, local=True),
                        current_container=page.overlay[1]
                    )

                def delete(name=name):
                    return lambda e: delete_point(page, name, maps=maps, object=object)

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

        method_map = {
                "post": {
                    "select": "name, situation, type, point, hood, address",
                    "name": dicio_filter["name_filter"],
                    "type": dicio_filter["type_filter"],
                    "order": "name.asc",
                    "offset": offset,  
                    "limit": limit,
                },
                "tree": {
                    "select": "name, type, height, diameter, hood, address",
                    "name": dicio_filter["name_filter"],
                    "type": dicio_filter["type_filter"],
                    "order": "name.asc",
                    "offset": offset,  
                    "limit": limit,
                },
            }

        response = requests.get(
            f'{url}/rest/v1/form_{object}_{current_profile["city_call_name"]}',
            headers=headers,
            params=method_map[object],
        )
        
        data = response.json()
        response_data.extend(data)

        if len(data) < limit:
                break
        
        offset += limit

    count_itens = len(response_data)
    text_count_itens.value = f"Resultado: {count_itens}"

    all_data_dicio = []

    for row in response_data:

        default_value = "N/A"

        method_map4 = {
            "post": [
                row.get("name", default_value), 
                row.get("situation", default_value), 
                row.get("type", default_value), 
                row.get("point", default_value), 
                row.get("hood", default_value), 
                row.get("address", default_value)
            ],
            "tree": [
                row.get("name", default_value), 
                row.get("type", default_value), 
                row.get("height", default_value), 
                row.get("diameter", default_value), 
                row.get("hood", default_value), 
                row.get("address", default_value)
            ]
        }

        all_data_dicio.append(method_map4[object])

    for row in response_data[:50]:

            name = row["name"]

            number = (str(name.split('-')[1])).zfill(4)
           
            def forms(name=name):
                return lambda e: loading.add_loading_overlay_page(
                    page=page,
                    call_layout=lambda:create_page_forms(page, name, maps, object, local=True),
                    current_container=page.overlay[1]
                )

            def edit(name=name):
                return lambda e: loading.add_loading_overlay_page(
                    page=page,
                    call_layout=lambda:create_page_edit_forms(page, name, maps=maps, object=object, local=True),
                    current_container=page.overlay[1]
                )

            def delete(name=name):
                return lambda e :delete_point(page, name, maps=maps, object=object)

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

    def show_print_container(e):
        print_container.controls[0].visible = not print_container.controls[0].visible
        print_container.update()

    def get_permission_filter(e):
        if object == "post":
            led_type = filter_container.controls[0].content.controls[0].controls[0].value
            led_type_data = filter_container.controls[0].content.controls[0].controls[0].data
            sodium_type = filter_container.controls[0].content.controls[1].controls[0].value
            sodium_type_data = filter_container.controls[0].content.controls[1].controls[0].data
            null_type = filter_container.controls[0].content.controls[2].controls[0].value
            null_type_data = filter_container.controls[0].content.controls[2].controls[0].data

            filter_button.controls[0].bgcolor = ft.Colors.RED

            type_filter_map = {
                (True, False, False): f"eq.{led_type_data}",
                (False, True, False): f"eq.{sodium_type_data}",
                (True, True, False): f"neq.{null_type_data}",
                (False, False, True): f"eq.{null_type_data}",
                (True, False, True): f"neq.{sodium_type_data}",
                (False, True, True): f"neq.{led_type_data}",
                (True, True, True): f"like.*",
            }

            key = (bool(led_type), bool(sodium_type), bool(null_type))
            dicio_filter["type_filter"] = type_filter_map.get(key, "")
        
            if key == (True, True, True):
                filter_button.controls[0].bgcolor = ft.Colors.BLUE
        else:
            fruit_type = filter_container.controls[0].content.controls[0].controls[0].value
            fruit_data = filter_container.controls[0].content.controls[0].controls[0].data
            no_fruit_type = filter_container.controls[0].content.controls[1].controls[0].value
            no_fruit_data = filter_container.controls[0].content.controls[1].controls[0].data

            filter_button.controls[0].bgcolor = ft.Colors.RED

            type_filter_map = {
                (True, False): f"eq.{fruit_data}",
                (False, True): f"eq.{no_fruit_data}",
                (True, True): f"like.*",
            }

            key = (bool(fruit_type), bool(no_fruit_type))
            dicio_filter["type_filter"] = type_filter_map.get(key, "")

            if key == (True, True):
                filter_button.controls[0].bgcolor = ft.Colors.BLUE

        filter_container.controls[0].visible = not filter_container.controls[0].visible
        searchfild.value = ""
        page.update()
        changesearch(e, dicio_filter, dicio, forms1, count_itens, text_count_itens, all_data_dicio),


    method_map3 = {
                "post": [
                        chk.create_checkbox2("Lâmpada LED", 15, None, 8,"Lâmpada LED", True),
                        chk.create_checkbox2("Lâmpada de vapor de sódio", 15, None, 8,"Lâmpada de vapor de sódio", True),
                        chk.create_checkbox2("Sem iluminação", 15, None, 8,".", True),
                        buttons.create_button(on_click=lambda e: get_permission_filter(e),
                                                    text="Aplicar",
                                                    color=ft.Colors.AMBER,
                                                    col=12,
                                                    padding=5,)
                        ],
                "tree": [
                        chk.create_checkbox2("Frutífera", 15, None, 8,"Frutífera", True),
                        chk.create_checkbox2("Infrutífera", 15, None, 8,"Infrutífera", True),
                        buttons.create_button(on_click=lambda e: get_permission_filter(e),
                                                    text="Aplicar",
                                                    color=ft.Colors.AMBER,
                                                    col=12,
                                                    padding=5,)
                        ],
            }

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
                            content=ft.Column(method_map3[object])
                            )
                            ],
                            vertical_alignment=ft.CrossAxisAlignment.END,
                            alignment=ft.MainAxisAlignment.CENTER,
                            )

#....................................................................................................

    def save_as_pdf(list_itens, object, path):

        snack_bar = ft.SnackBar(
            content=ft.Text(value="Gerando documento...", color=ft.Colors.BLACK),
            duration=2000,
            bgcolor=ft.Colors.AMBER,
        )
        page.overlay.append(snack_bar)
        snack_bar.open = True
        page.update()

        # Filepath for the generated PDF
        pdf_filepath = f"{path}/Relatorio.pdf"

        # Create a PDF document
        doc = SimpleDocTemplate(pdf_filepath, pagesize=landscape(letter))
        elements = []

        # Header based on the object type
        method_map4 = {
            "post": ["Nome", "Situação", "Tipo", "Pontos", "Bairro", "Rua"],
            "tree": ["Nome", "Situação", "Tipo", "Altura", "Bairro", "Rua"],
        }

        # Add header row to the table data
        table_data = [method_map4[object]]

        # Add rows to the table from list_itens
        for item in list_itens:
            table_data.append(item)

        # Create a Table object
        table = Table(table_data)

        # Style the table
        style = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), ft.Colors.WHITE),  # Header background color
            ('TEXTCOLOR', (0, 0), (-1, 0), ft.Colors.BLACK),  # Header text color
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  # Center align all cells
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),  # Bold font for the header
            ('FONTSIZE', (0, 0), (-1, -1), 7),  # Font size
            ('BOTTOMPADDING', (0, 0), (-1, 0), 1),  # Padding for header
            ('BACKGROUND', (0, 1), (-1, -1), ft.Colors.WHITE),  # Row background color
            ('GRID', (0, 0), (-1, -1), 0.5, ft.Colors.BLACK),  # Grid lines
        ])
        table.setStyle(style)

        # Add table to the document elements
        elements.append(table)

        # Build the PDF
        doc.build(elements)

        # Show a success message in the app
        snack_bar = ft.SnackBar(
            content=ft.Text(value="Download concluído", color=ft.Colors.BLACK),
            duration=2000,
            bgcolor=ft.Colors.GREEN,
        )
        page.overlay.append(snack_bar)
        snack_bar.open = True
        page.update()

    def save_as_excel(list_itens, object, path):

        snack_bar = ft.SnackBar(
                content=ft.Text(value="Gerando documento...", color=ft.Colors.BLACK),
                duration=2000,
                bgcolor=ft.Colors.AMBER,
            )
        page.overlay.append(snack_bar)
        snack_bar.open = True
        page.update()

        # Filepath for the generated Excel file
        excel_filepath = f"{path}/Relatorio.xlsx"

        # Header mapping for different object types
        method_map4 = {
            "post": ["Nome", "Situação", "Tipo", "Pontos", "Bairro", "Rua"],
            "tree": ["Nome", "Tipo", "Altura", "Diâmetro", "Bairro", "Rua"]
        }

        # Create a DataFrame using the header and data
        if object in method_map4:
            headers = method_map4[object]
            df = pd.DataFrame(list_itens, columns=headers)
        else:
            print("Tipo de objeto inválido!")
            return

        # Save the DataFrame to an Excel file
        try:
            df.to_excel(excel_filepath, index=False)
            print(f"Planilha salva com sucesso em: {excel_filepath}")

            # Show a success SnackBar
            snack_bar = ft.SnackBar(
                content=ft.Text(value="Download concluído", color=ft.Colors.BLACK),
                duration=2000,
                bgcolor=ft.Colors.GREEN,
            )
            page.overlay.append(snack_bar)
            snack_bar.open = True
            page.update()

        except Exception as e:
            print(f"Erro ao salvar a planilha: {e}")

            # Show an error SnackBar
            snack_bar = ft.SnackBar(
                content=ft.Text(value="Erro ao gerar planilha!", color=ft.Colors.WHITE),
                duration=2000,
                bgcolor=ft.Colors.RED,
            )
            page.overlay.append(snack_bar)
            snack_bar.open = True
            page.update()

    document = ["Nulo"]

    def on_directory_selected(e: ft.FilePickerResultEvent):

        method_map5 = {
        "pdf": save_as_pdf,
        "excel": save_as_excel,
        "Nulo": lambda *args: print("Nenhum selecionado")
        }

        method_map5[document[0]](all_data_dicio, object, e.path)

    def open_explorer(object): 
        document.clear()
        document.append(object)
        fp.get_directory_path()
    

    fp = ft.FilePicker(on_result=on_directory_selected)
    if fp in page.overlay:
        page.overlay.remove(fp)
    page.overlay.insert(2, fp)

    print_itens = [
                    ft.Text(value=f"Gerar Relátório dos itens, filtrados",
                               color=ft.Colors.WHITE,
                               text_align=ft.TextAlign.CENTER,
                               size=15,
                               weight=ft.FontWeight.W_900,
                               ),
                    buttons.create_button(on_click=lambda e: open_explorer(object="pdf"),
                                                text="Gerar PFD",
                                                color=ft.Colors.AMBER,
                                                col=12,
                                                padding=5,),
                    buttons.create_button(on_click=lambda e: open_explorer(object="excel"),
                                                text="Gerar Planilha",
                                                color=ft.Colors.AMBER,
                                                col=12,
                                                padding=5,),
                    buttons.create_button(on_click=show_print_container,
                                                text="Fechar",
                                                color=ft.Colors.RED,
                                                col=12,
                                                padding=5,)
                    ]

    print_container = ft.Row([ 
                        ft.Container(
                            bgcolor=ft.Colors.BLUE,
                            padding=10,
                            margin=10,
                            height=270,
                            width=300,
                            border_radius=20,
                            col=12,
                            visible=False,
                            content=ft.Column(print_itens)
                            )
                            ],
                            vertical_alignment=ft.CrossAxisAlignment.END,
                            alignment=ft.MainAxisAlignment.CENTER,
                            )

#....................................................................................................


    back_home_button = buttons.create_button(on_click=lambda e: loading.back_home(page=page),
    text="Voltar",
    color=ft.Colors.AMBER,
    col=12,
    padding=5,)

    searchfild = ft.TextField(label="Pesquisar",  # caixa de texto
                                col=10,
                                on_change=lambda e: changesearch(e, dicio_filter, dicio, forms1, count_itens, text_count_itens, all_data_dicio),
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
                                                col=2,
                                                padding=0,
                                                icon_color=ft.Colors.WHITE,
                                                )

    print_button = buttons.create_icon_button(
                                                icon=ft.Icons.SIM_CARD_DOWNLOAD,
                                                on_click=show_print_container,
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
            print_container,
            text_count_itens,
            print_button,
            forms1,
            ft.Container(padding=5),
            ft.Container(padding=5),
            back_home_button,
         
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
    )

def create_view_orders(page, maps, object):

    textthemes = TextTheme()
    texttheme1 = textthemes.create_text_theme1() 
    buttons = Buttons(page)
    loading = LoadingPages(page)
    sp = SupaBase(page)
    chk = CheckBox(page)
    
    dicio_filter = {
        "order_filter" : "like.*",
        "permission_filter" : "like.*",
        "status_filter" : "like.*",
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

            method_map[object]["order_id"] = dicio_filter["order_filter"]
            method_map[object]["function"] = dicio_filter["permission_filter"]
            method_map[object]["status"] = dicio_filter["status_filter"]
            method_map[object]["offset"] = offset
            method_map[object]["limit"] = limit

            response = requests.get(
                f'{url}/rest/v1/order_{object}_{current_profile["city_call_name"]}',
                headers=headers,
                params=method_map[object],
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
        all_data_dicio.clear()

        try:
            if new_response_data[0] == "code" or len(new_response_data) == 0:
                count_itens = 0
                text_count_itens.value = f"Resultado: {count_itens}"
                dicio.values() == None
        except:
            pass

        else:

            for row in new_response_data:

                default_value = "N/A"

                method_map4 = {
                    "post": [
                        row.get("created_at", default_value), 
                        row.get("ip", default_value), 
                        row.get("reclamante", default_value), 
                        row.get("function", default_value), 
                        row.get("celular", default_value),
                        row.get("order_id", default_value),
                        row.get("origem", default_value),
                        row.get("observacao", default_value),
                        row.get("materiais", default_value),
                        row.get("ponto", default_value),
                        row.get("status", default_value),
                        row.get("data_andamento", default_value),
                        row.get("data_conclusao", default_value),
                        row.get("equipe", default_value),
                    ],
                    "tree": [
                        row.get("created_at", default_value), 
                        row.get("ip", default_value), 
                        row.get("reclamante", default_value), 
                        row.get("function", default_value), 
                        row.get("celular", default_value),
                        row.get("order_id", default_value),
                        row.get("origem", default_value),
                        row.get("observacao", default_value),
                        row.get("materiais", default_value),
                        row.get("altura", default_value),
                        row.get("status", default_value),
                        row.get("data_andamento", default_value),
                        row.get("data_conclusao", default_value),
                        row.get("equipe", default_value),
                    ]
                }

                all_data_dicio.append(method_map4[object])

            for row in new_response_data[:50]:
                
                data = row["created_at"]
                order = row["order_id"]
                status = row["status"]

                def forms(order):
                    return lambda e: loading.add_loading_overlay_page(
                        page=page,
                        call_layout=lambda:create_page_os_forms(page, name=None, order=order, maps=maps, object=object),
                        current_container=page.overlay[1]
                    )

                linha = ft.DataRow(cells=[
                        ft.DataCell(ft.Text(value=data, theme_style=ft.TextThemeStyle.TITLE_LARGE, text_align=ft.TextAlign.CENTER)),
                        ft.DataCell(ft.Text(value=order, theme_style=ft.TextThemeStyle.TITLE_MEDIUM, text_align=ft.TextAlign.CENTER)),
                        ft.DataCell(ft.Text(value=status, theme_style=ft.TextThemeStyle.TITLE_MEDIUM, text_align=ft.TextAlign.CENTER)),
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

        method_map = {
                "post": {
                    "select": "created_at, ip, reclamante, function, celular, order_id, origem, observacao, materiais, ponto, status, data_andamento, data_conclusao, equipe",
                    "order_id": dicio_filter["order_filter"],
                    "function": dicio_filter["permission_filter"],
                    "status": dicio_filter["status_filter"],
                    "order": "order_id.desc",
                    "offset": offset,  
                    "limit": limit,
                },
                "tree": {
                    "select": "created_at, ip, reclamante, function, celular, order_id, origem, observacao, materiais, altura, status, data_andamento, data_conclusao, equipe",
                    "order_id": dicio_filter["order_filter"],
                    "function": dicio_filter["permission_filter"],
                    "status": dicio_filter["status_filter"],
                    "order": "order_id.desc",
                    "offset": offset,  
                    "limit": limit,
                },
            }

        response = requests.get(
            f'{url}/rest/v1/order_{object}_{current_profile["city_call_name"]}',
            headers=headers,
            params=method_map[object],
        )

        data = response.json()
        response_data.extend(data)

        if len(data) < limit:
                break
        
        offset += limit

    count_itens = len(response_data)
    text_count_itens.value = f"Resultado: {count_itens}"

    all_data_dicio = []

    for row in response_data:

        default_value = "N/A"

        method_map4 = {
            "post": [
                row.get("created_at", default_value), 
                row.get("ip", default_value), 
                row.get("reclamante", default_value), 
                row.get("function", default_value), 
                row.get("celular", default_value),
                row.get("order_id", default_value),
                row.get("origem", default_value),
                row.get("observacao", default_value),
                row.get("materiais", default_value),
                row.get("ponto", default_value),
                row.get("status", default_value),
                row.get("data_andamento", default_value),
                row.get("data_conclusao", default_value),
                row.get("equipe", default_value),
            ],
            "tree": [
                row.get("created_at", default_value), 
                row.get("ip", default_value), 
                row.get("reclamante", default_value), 
                row.get("function", default_value), 
                row.get("celular", default_value),
                row.get("order_id", default_value),
                row.get("origem", default_value),
                row.get("observacao", default_value),
                row.get("materiais", default_value),
                row.get("altura", default_value),
                row.get("status", default_value),
                row.get("data_andamento", default_value),
                row.get("data_conclusao", default_value),
                row.get("equipe", default_value),
            ]
        }

        all_data_dicio.append(method_map4[object])

    for row in response_data[:50]:
            
            data = row["created_at"]
            order = row["order_id"]
            status = row["status"]

            def forms(order):

                return lambda e: loading.add_loading_overlay_page(
                    page=page,
                    call_layout=lambda:create_page_os_forms(page, name=None, order=order, maps=maps, object=object),
                    current_container=page.overlay[1]
                )
         

            linha = ft.DataRow(cells=[
                        ft.DataCell(ft.Text(value=data, theme_style=ft.TextThemeStyle.TITLE_LARGE, text_align=ft.TextAlign.CENTER)),
                        ft.DataCell(ft.Text(value=order, theme_style=ft.TextThemeStyle.TITLE_MEDIUM, text_align=ft.TextAlign.CENTER)),
                        ft.DataCell(ft.Text(value=status, theme_style=ft.TextThemeStyle.TITLE_MEDIUM, text_align=ft.TextAlign.CENTER)),
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

    def show_print_container(e):
        print_container.controls[0].visible = not print_container.controls[0].visible
        print_container.update()

    def get_permission_filter(e):
        # Valores e dados para "permission_filter"
        adm_permission = filter_container.controls[0].content.controls[0].controls[0].value
        adm_permission_data = filter_container.controls[0].content.controls[0].controls[0].data
        invited_permission = filter_container.controls[0].content.controls[1].controls[0].value
        invited_permission_data = filter_container.controls[0].content.controls[1].controls[0].data

        # Valores e dados para "status_filter"
        open_status = filter_container.controls[0].content.controls[2].controls[0].value
        open_status_data = filter_container.controls[0].content.controls[2].controls[0].data
        close_status = filter_container.controls[0].content.controls[3].controls[0].value
        close_status_data = filter_container.controls[0].content.controls[3].controls[0].data

        # Inicializa cores
        filter_button.controls[0].bgcolor = ft.Colors.RED

        # Mapeamento para "permission_filter"
        permission_filter_map = {
            (True, False): f"eq.{adm_permission_data}",
            (False, True): f"eq.{invited_permission_data}",
            (True, True): f"like.*",
        }

        # Gera chave para "permission_filter"
        permission_key = (bool(adm_permission), bool(invited_permission))
        dicio_filter["permission_filter"] = permission_filter_map.get(permission_key, "")

        # Mapeamento para "status_filter"
        status_filter_map = {
            (True, False): f"eq.{open_status_data}",
            (False, True): f"eq.{close_status_data}",
            (True, True): f"like.*",
        }

        # Gera chave para "status_filter"
        status_key = (bool(open_status), bool(close_status))
        dicio_filter["status_filter"] = status_filter_map.get(status_key, "")

        # Atualiza cor do botão em casos específicos
        if permission_key == (True, True) and status_key == (True, True):
            filter_button.controls[0].bgcolor = ft.Colors.BLUE

        # Atualiza visibilidade e campos
        filter_container.controls[0].visible = not filter_container.controls[0].visible
        searchfild.value = ""
        page.update()
        changesearch(e, dicio_filter, dicio, forms1, count_itens, text_count_itens)

    filter_container = ft.Row([
                        ft.Container(
                            bgcolor=ft.Colors.BLUE,
                            padding=10,
                            margin=10,
                            height=220,
                            width=300,
                            border_radius=20,
                            col=10,
                            visible=False,
                            content=ft.Column([
                                chk.create_checkbox2("Administrador", 15, None, 8,"adm", True),
                                chk.create_checkbox2("Convidado", 15, None, 8,"convidado", True),
                                chk.create_checkbox2("Aberto", 15, None, 8,"Aberto", True),
                                chk.create_checkbox2("Concluído", 15, None, 8,"Concluido", True),
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
    
    #....................................................................................................

    def save_as_pdf(list_itens, object, path):
        # Filepath for the generated PDF
        pdf_filepath = f"{path}/Relatorio.pdf"

        # Create a PDF document
        doc = SimpleDocTemplate(pdf_filepath, pagesize=landscape(letter))
        elements = []

        # Header based on the object type
        method_map4 = {
            "post": ["Criação", "Nome", "Reclamante", "Usuário", "Celular", "Ordem", "Origem", "Observação", "Materiais", "Pontos", "Status", "Data do andamento", "Data da conclusão", "Equipe"],
            "tree": ["Criação", "Nome", "Reclamante", "Usuário", "Celular", "Ordem", "Origem", "Observação", "Materiais", "Altura", "Status", "Data do andamento", "Data da conclusão", "Equipe"],
        }

        # Add header row to the table data
        table_data = [method_map4[object]]

        # Add rows to the table from list_itens
        for item in list_itens:
            table_data.append(item)

        # Create a Table object
        table = Table(table_data)

        # Style the table
        style = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), ft.Colors.WHITE),  # Header background color
            ('TEXTCOLOR', (0, 0), (-1, 0), ft.Colors.BLACK),  # Header text color
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  # Center align all cells
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),  # Bold font for the header
            ('FONTSIZE', (0, 0), (-1, -1), 7),  # Font size
            ('BOTTOMPADDING', (0, 0), (-1, 0), 1),  # Padding for header
            ('BACKGROUND', (0, 1), (-1, -1), ft.Colors.WHITE),  # Row background color
            ('GRID', (0, 0), (-1, -1), 0.5, ft.Colors.BLACK),  # Grid lines
        ])
        table.setStyle(style)

        # Add table to the document elements
        elements.append(table)

        # Build the PDF
        doc.build(elements)

        # Show a success message in the app
        snack_bar = ft.SnackBar(
            content=ft.Text(value="Download concluído", color=ft.Colors.BLACK),
            duration=2000,
            bgcolor=ft.Colors.GREEN,
        )
        page.overlay.append(snack_bar)
        snack_bar.open = True
        page.update()

    def save_as_excel(list_itens, object, path):

        snack_bar = ft.SnackBar(
                content=ft.Text(value="Gerando relatório", color=ft.Colors.BLACK),
                duration=2000,
                bgcolor=ft.Colors.AMBER,
            )
        page.overlay.append(snack_bar)
        snack_bar.open = True
        page.update()

        # Filepath for the generated Excel file
        excel_filepath = f"{path}/Relatorio.xlsx"

        # Header mapping for different object types
        method_map4 = {
            "post": ["Criação", "Nome", "Reclamante", "Usuário", "Celular",
                        "Ordem", "Origem", "Observação", "Materiais",
                        "Pontos", "Status", "Data do andamento", "Data da conclusão", "Equipe"],

            "tree": ["Criação", "Nome", "Reclamante", "Usuário", "Celular",
                        "Ordem", "Origem", "Observação", "Materiais",
                        "Altura", "Status", "Data do andamento", "Data da conclusão", "Equipe"]
        }

        # Create a DataFrame using the header and data
        if object in method_map4:
            headers = method_map4[object]
            df = pd.DataFrame(list_itens, columns=headers)
        else:
            print("Tipo de objeto inválido!")
            return

        # Save the DataFrame to an Excel file
        try:
            df.to_excel(excel_filepath, index=False)
            print(f"Planilha salva com sucesso em: {excel_filepath}")

            # Show a success SnackBar
            snack_bar = ft.SnackBar(
                content=ft.Text(value="Download concluído", color=ft.Colors.BLACK),
                duration=2000,
                bgcolor=ft.Colors.GREEN,
            )
            page.overlay.append(snack_bar)
            snack_bar.open = True
            page.update()

        except Exception as e:
            print(f"Erro ao salvar a planilha: {e}")

            # Show an error SnackBar
            snack_bar = ft.SnackBar(
                content=ft.Text(value="Erro ao gerar planilha!", color=ft.Colors.WHITE),
                duration=2000,
                bgcolor=ft.Colors.RED,
            )
            page.overlay.append(snack_bar)
            snack_bar.open = True
            page.update()

    document = ["Nulo"]

    def on_directory_selected(e: ft.FilePickerResultEvent):

        method_map5 = {
        "pdf": save_as_pdf,
        "excel": save_as_excel,
        "Nulo": lambda *args: print("Nenhum selecionado")
        }

        method_map5[document[0]](all_data_dicio, object, e.path)

    def open_explorer(object): 
        document.clear()
        document.append(object)
        fp.get_directory_path()
    

    fp = ft.FilePicker(on_result=on_directory_selected)
    if fp in page.overlay:
        page.overlay.remove(fp)
    page.overlay.insert(2, fp)

    print_itens = [
                    ft.Text(value=f"Gerar Relátório dos itens, filtrados",
                               color=ft.Colors.WHITE,
                               text_align=ft.TextAlign.CENTER,
                               size=15,
                               weight=ft.FontWeight.W_900,
                               ),
                    buttons.create_button(on_click=lambda e: open_explorer(object="pdf"),
                                                text="Gerar PFD",
                                                color=ft.Colors.AMBER,
                                                col=12,
                                                padding=5,),
                    buttons.create_button(on_click=lambda e: open_explorer(object="excel"),
                                                text="Gerar Planilha",
                                                color=ft.Colors.AMBER,
                                                col=12,
                                                padding=5,),
                    buttons.create_button(on_click=show_print_container,
                                                text="Fechar",
                                                color=ft.Colors.RED,
                                                col=12,
                                                padding=5,)
                    ]

    print_container = ft.Row([ 
                        ft.Container(
                            bgcolor=ft.Colors.BLUE,
                            padding=10,
                            margin=10,
                            height=270,
                            width=300,
                            border_radius=20,
                            col=12,
                            visible=False,
                            content=ft.Column(print_itens)
                            )
                            ],
                            vertical_alignment=ft.CrossAxisAlignment.END,
                            alignment=ft.MainAxisAlignment.CENTER,
                            )

#....................................................................................................

    back_home_button = buttons.create_button(on_click=lambda e: loading.back_home(page=page),
    text="Voltar",
    color=ft.Colors.AMBER,
    col=12,
    padding=5,)
    
    searchfild = ft.TextField(label="Procurar",  # caixa de texto
                                col=10,
                                on_change=lambda e: changesearch(e, dicio_filter, dicio, forms1, count_itens, text_count_itens, all_data_dicio),
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
                                                col=2,
                                                padding=0,
                                                icon_color=ft.Colors.WHITE,
                                                )

    print_button = buttons.create_icon_button(
                                                icon=ft.Icons.SIM_CARD_DOWNLOAD,
                                                on_click=show_print_container,
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
            print_container,
            text_count_itens,
            print_button,
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
                f'{url}/rest/v1/users_{current_profile["city_call_name"]}',
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
            f'{url}/rest/v1/users_{current_profile["city_call_name"]}',
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



def add_point(page, coordinates, list_forms, image, angle, maps, object):

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
    
    response = sp.add_point(list_forms, coordinates, image, angle, object)

    # Verificar se a inserção foi bem-sucedida
    if response.status_code == 201:

        profile = CurrentProfile()
        current_profile = profile.return_current_profile()

        new_number = list_forms[0].zfill(4)

        method_map = {
                "post": f'IP {current_profile["city_acronym"]}-{new_number}',
                "tree": f'IA {current_profile["city_acronym"]}-{new_number}'
            }

        point_data = sp.get_one_point(method_map[object], object)
        data = point_data.json()
        row = data[0]
        color_mapping = {
            "yellow": ft.Colors.AMBER,
            "white": ft.Colors.PINK_200,
            "blue": ft.Colors.BLUE,
            "green": ft.Colors.GREEN,
        }

        name = row["name"]
        x = row["x"]
        y = row["y"]
        data_color = row["color"]
        type_point = row["type"]
        object = row["object"]

        point_color = color_mapping.get(data_color, ft.Colors.GREY)

        loading = LoadingPages(page)
    
        def create_on_click(name=name, object=object):  
            return lambda e: loading.new_loading_overlay_page(
                page=page,
                call_layout=lambda: create_page_forms(
                    page, name, maps, object
                )
            )

        number = int(name.split('-')[1])

        method_map = {
                "post": buttons.create_point_button_post,
                "tree": buttons.create_point_button_tree,
            }

        point_button = method_map[object](
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
            duration=2000,
        )
        page.overlay.append(snack_bar)
        snack_bar.open = True
        page.update()
        time.sleep(2)
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
 
def add_os(page, list_add_os, name, maps, object):

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
    
    response = sp.add_os(list_add_os, object)

    # Verificar se a inserção foi bem-sucedida
    if response.status_code == 201:
        snack_bar = ft.SnackBar(
            content=ft.Text("ordem adicionada com sucesso"),
            bgcolor=ft.Colors.GREEN,
            duration=2500,
        )

        loading.add_loading_overlay_page(page=page, call_layout=lambda:create_adm_page_order(page, name, maps, object),
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



def edit_point(page, list_edited_forms, image, previous_data, maps, object):

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

    response = sp.edit_point(image, list_edited_forms, previous_data, object)
    
    if response.status_code in [200, 204]:  # 204 indica sucesso sem conteúdo

        profile = CurrentProfile()
        current_profile = profile.return_current_profile()

        new_number = (str(list_edited_forms[0])).zfill(4)

        method_map = {
                "post": f'IP {current_profile["city_acronym"]}-{new_number}',
                "tree": f'IA {current_profile["city_acronym"]}-{new_number}'
            }

        point_data = sp.get_one_point(method_map[object], object)
        data = point_data.json()
        row = data[0]
        color_mapping = {
            "yellow": ft.Colors.AMBER,
            "white": ft.Colors.PINK_200,
            "blue": ft.Colors.BLUE,
            "green": ft.Colors.GREEN,
        }

        name = row["name"]
        x = row["x"]
        y = row["y"]
        data_color = row["color"]
        type_point = row["type"]
        object = row["object"]

        point_color = color_mapping.get(data_color, ft.Colors.GREY)

        loading = LoadingPages(page)
    
        def create_on_click(name=name, object=object):  
            return lambda e: loading.new_loading_overlay_page(
                page=page,
                call_layout=lambda: create_page_forms(
                    page, name, maps, object
                )
            )

        number = int(name.split('-')[1])

        method_map = {
                "post": buttons.create_point_button_post,
                "tree": buttons.create_point_button_tree,
            }

        point_button = method_map[object](
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
        current_map_points.remove_point(previous_data["name"])
        maps.remove_marker(previous_data["name"])
        current_map_points.add_point(point_marker)
        maps.add_marker(point_marker)

        snack_bar = ft.SnackBar(
            content=ft.Text("Alterações Salvas"),
            bgcolor=ft.Colors.GREEN,
            duration=2000,
        )
        page.overlay.append(snack_bar)
        snack_bar.open = True
        page.update()
        time.sleep(2)
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

def edit_os(page, list_edited_os_forms, order, name, maps, object):

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

    response = sp.edit_os(list_edited_os_forms, object)
    
    if response.status_code in [200, 204]:  # 204 indica sucesso sem conteúdo
        snack_bar = ft.SnackBar(
            content=ft.Text("Alterações Salvas"),
            bgcolor=ft.Colors.GREEN,
            duration=2000,
        )
        loading.add_loading_overlay_page(page=page,
        call_layout=lambda:create_page_os_forms(page, name, order, maps, object),
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



def delete_point(page, name, maps, object):

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

    list_response = sp.delete_point(name, object)


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
                duration=2000,
            )
        page.overlay.append(snack_bar)
        snack_bar.open = True
        page.update()
        time.sleep(2)
        loading.back_home(page=page)

    else:
        snack_bar = ft.SnackBar(
            content=ft.Text(f"Erro ao excluir ponto: {list_response[0].text}, {list_response[1].text}, {list_response[2].text}"),
            bgcolor=ft.Colors.RED
        )
        page.overlay.append(snack_bar)
        snack_bar.open = True
        page.update()
        loading.add_loading_overlay_page(page=page,
        call_layout=lambda:create_page_home(page),
        current_container=page.overlay[1])

def delete_os(page, name, order, maps, object):

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

    response = sp.delete_os(order, object)

    if response.status_code == 204:

        if name != None:
            snack_bar = ft.SnackBar(
                    content=ft.Text("ordem excluida"),
                    bgcolor=ft.Colors.GREEN,
                    duration=2500,
                )

            loading.add_loading_overlay_page(page=page,
            call_layout=lambda:create_adm_page_order(page, name, maps, object),
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
        
        map_height = (int(page.height)) * 0.83

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
                            height=map_height, 
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
                try:
                    item.content.width = size
                    item.content.height = size
                    item.content.size = size
                    item.content.content.size = size + 5
                except:
                    pass
            
    def move_map(self, x, y, zoom):
        self.google.move_to(
            destination=map.MapLatitudeLongitude(x, y),
            zoom=zoom
        )
        overlay_copy = list(self.page.overlay)
        for item in overlay_copy:
            if item.data == "geolocator":
                pass
            else:
                self.page.overlay.remove(item)
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
        
    def filter_map(self, new_filter, new_order_filter):

        self.list_filter = new_filter

        overlay_copy = list(self.page.overlay)
        for item in overlay_copy:
            if item.data == "geolocator":
                pass
            else:
                self.page.overlay.remove(item)
        self.page.update()         

        self.list_maps_acess_controls[0].value = ""
        self.list_maps_acess_controls[0].update()

        current_points = CurrentMapPoints()
        current_points.filter_points(new_filter, new_order_filter)

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

    def update_map_height(self, new_map_height):
        self.complete_map.controls[0].height = new_map_height

class Marker:

    def __init__(self, page):
        self.page = page
        self.NamePoints = {}

    def create_points(self, size, visible, maps):
        
        sp = SupaBase(self.page)
        profile = CurrentProfile()
        current_profile = profile.return_current_profile()
        list_objects = current_profile["city_objects"]
        response_data = []
        response_data_orders = []
        dicio_data_orders = {}
        offset = 0
        limit = 1000

        if "post" in list_objects:
            while True:
                response = sp.get_all_points(object="post", offset=offset, limit=limit)

                if response.status_code != 200:
                    print("Erro ao buscar dados:", response.text)
                    break

                data = response.json()
                response_data.extend(data)

                # Se o número de registros retornados for menor que o limite, terminamos
                if len(data) < limit:
                    break

                offset += limit

            offset = 0
            limit = 1000

            while True:
                response = sp.get_all_orders(object="post", offset=offset, limit=limit)

                if response.status_code != 200:
                    print("Erro ao buscar dados:", response.text)
                    break

                data = response.json()
                response_data_orders.extend(data)

                # Se o número de registros retornados for menor que o limite, terminamos
                if len(data) < limit:
                    break

                offset += limit

        offset = 0
        limit = 1000

        if "tree" in list_objects:
            while True:
                response = sp.get_all_points(object="tree", offset=offset, limit=limit)

                if response.status_code != 200:
                    print("Erro ao buscar dados:", response.text)
                    break

                data = response.json()
                response_data.extend(data)

                # Se o número de registros retornados for menor que o limite, terminamos
                if len(data) < limit:
                    break

                offset += limit

            offset = 0
            limit = 1000

            while True:
                response = sp.get_all_orders(object="tree", offset=offset, limit=limit)

                if response.status_code != 200:
                    print("Erro ao buscar dados:", response.text)
                    break

                data = response.json()
                response_data_orders.extend(data)

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

        for row in response_data_orders:
            name_order = row["ip"]
            status_order = row["status"]

            dicio_data_orders[name_order] = status_order


        # Loop para criar os botões com base nas linhas da tabela
        for row in response_data:
            name = row["name"]
            x = row["x"]
            y = row["y"]
            data_color = row["color"]
            type_point = row["type"]
            object = row["object"]

            count += 1

            point_color = color_mapping.get(data_color, ft.Colors.GREY)

            if object == "tree":
                point_color = ft.Colors.GREEN

            loading = LoadingPages(self.page)
      
            def create_on_click(name=name, object=object):  
                return lambda e: loading.new_loading_overlay_page(
                    page=self.page,
                    call_layout=lambda: create_page_forms(
                        self.page, name, maps, object
                    )
                )

            number = int(name.split('-')[1])


            method_map = {
                "post": buttons.create_point_button_post,
                "tree": buttons.create_point_button_tree,
            }

            InitialButtons[name] = {
                "element": method_map[object](
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
                "order": "Nulo", 
            }

            self.NamePoints[name] = {
                "name": name,
                "x": x,
                "y": y,
            }

            if name in dicio_data_orders:
                InitialButtons[name]["order"] = dicio_data_orders[name]

        # Cria marcadores com base nos botões criados
        for name, button_data in InitialButtons.items():
            marker = buttons.create_point_marker(
                content=button_data["element"],
                x=button_data["x"],
                y=button_data["y"],
                data=[(button_data["name"]), (button_data["type"]), (button_data["x"]), (button_data["y"]), (button_data["order"])],
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
            result = []  

            if mysearch.strip():  

                overlay_copy = list(self.page.overlay)
                for item in overlay_copy:
                    if item.data == "geolocator":
                        pass
                    else:
                        self.page.overlay.remove(item)
                page.update()

                if self.resultcon not in self.page.overlay:
                    self.resultcon.visible = True
                    self.page.overlay.insert(1, self.resultcon)  
                for item in self.itens:
                    if mysearch in item.title.value:  
                        result.append(item)
                    if len(result) >= 5:
                        break

            if result: 
                self.resultdata.controls.clear()
                for x in result:
                    self.resultdata.controls.append(x)  
                self.page.update()
            else:  
                if self.resultcon in self.page.overlay:
                    self.page.overlay.remove(self.resultcon)  
                self.resultdata.controls.clear()
                self.page.update()

        self.txtsearch = ft.TextField(label="Procurar",  
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

    def __init__(self, page, maps, action1, action2, action3, action4, action5, action6, action7, action8, action9):
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

            led_type = self.filter_container.controls[0].content.controls[1].controls[0].value
            sodium_type = self.filter_container.controls[0].content.controls[2].controls[0].value
            null_type = self.filter_container.controls[0].content.controls[3].controls[0].value
            tree_type = self.filter_container.controls[0].content.controls[4].controls[0].value
            order_open = self.filter_container.controls[0].content.controls[6].controls[0].value
            order_close = self.filter_container.controls[0].content.controls[7].controls[0].value
            order_null = self.filter_container.controls[0].content.controls[8].controls[0].value
            list_map_filter = []
            list_map_order_filter = []

            if led_type:
                list_map_filter.append("Lâmpada LED")
            if sodium_type:
                list_map_filter.append("Lâmpada de vapor de sódio")
            if null_type:
                list_map_filter.append(".")
            if tree_type:
                list_map_filter.append("tree")
            if order_open:
                list_map_order_filter.append("Aberto")
            if order_close:
                list_map_order_filter.append("Concluido")
            if order_null:
                list_map_order_filter.append("Nulo")
            

            self.maps.filter_map(list_map_filter, list_map_order_filter)

       
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
                                    height=450,
                                    width=300,
                                    border_radius=20,
                                    col=12,
                                    content=ft.Column([
                                        ft.Row(alignment=ft.MainAxisAlignment.CENTER,
                                                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                                                controls=[ft.Text(value="Tipos de Pontos", color=ft.Colors.WHITE, text_align=ft.TextAlign.CENTER, weight=ft.FontWeight.W_900)]),
                                        chk.create_checkbox2("Lâmpada LED", 15, None, 8,"Lâmpada LED", True),
                                        chk.create_checkbox2("Lâmpada de vapor de sódio", 15, None, 8,"Lâmpada de vapor de sódio", True),
                                        chk.create_checkbox2("Sem iluminação", 15, None, 8,".", True),
                                        chk.create_checkbox2("Árvore", 15, None, 8,"tree", True),
                                        ft.Row(alignment=ft.MainAxisAlignment.CENTER,
                                                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                                                controls=[ft.Text(value="Ordens de Serviço", color=ft.Colors.WHITE, text_align=ft.TextAlign.CENTER, weight=ft.FontWeight.W_900)]),
                                        chk.create_checkbox2("Aberto", 15, None, 8,"open", True),
                                        chk.create_checkbox2("Concluído", 15, None, 8,"close", True),
                                        chk.create_checkbox2("Ausente", 15, None, 8,"null", True),
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
                        title=ft.Text(f"Lista de árvores", color=ft.Colors.BLACK),
                        on_click=action8,
                        bgcolor=ft.Colors.WHITE,
                        shape=ft.RoundedRectangleBorder(radius=10),
                    )
            )
            listtiles.append(
                ft.ListTile(
                        title=ft.Text(f"Lista de ordens de poste", color=ft.Colors.BLACK),
                        on_click=action4,
                        bgcolor=ft.Colors.WHITE,
                        shape=ft.RoundedRectangleBorder(radius=10),
                    )
            )
            listtiles.append(
                ft.ListTile(
                        title=ft.Text(f"Lista de ordens de árvore", color=ft.Colors.BLACK),
                        on_click=action9,
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
                                    height=500,
                                    width=370,
                                    border_radius=20,
                                    col=12,
                                    content=ft.Column(listtiles)
                                )
                                ],
                                vertical_alignment=ft.CrossAxisAlignment.END,
                                alignment=ft.MainAxisAlignment.CENTER,
                                )

        listtiles2 = [

            ft.ListTile(
                title=ft.Text(f"Adicionar Poste", color=ft.Colors.BLACK),
                on_click=action6,
                bgcolor=ft.Colors.WHITE,
                shape=ft.RoundedRectangleBorder(radius=10),
            ),
            ft.ListTile(
                title=ft.Text(f"Adicionar Árvore", color=ft.Colors.BLACK),
                on_click=action7,
                bgcolor=ft.Colors.WHITE,
                shape=ft.RoundedRectangleBorder(radius=10),
            ),
        ]

        self.add_container = ft.Row([
                                ft.Container(
                                    bgcolor=ft.Colors.BLACK,
                                    padding=10,
                                    margin=10,
                                    height=150,
                                    width=370,
                                    border_radius=20,
                                    col=12,
                                    content=ft.Column(listtiles2)
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

    def create_add_container(self):
        self.menu_container.offset = ft.transform.Offset(0, 0)  # Centralizado
        self.menu_container.animate_offset = ft.animation.Animation(600, curve="easeIn")
        return self.add_container




                



