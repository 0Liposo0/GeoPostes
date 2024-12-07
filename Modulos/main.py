import flet as ft
from views import *
from models import *

def main(page: ft.Page):
    page.title = 'GeoPostes'
    page.window.always_on_top = True
    page.window.height = 960
    page.window.width = 440
    page.expand = True 
    page.window.resizable = False  
    page.bgcolor = ft.Colors.WHITE 
    page.scroll = "auto"
    page.padding=0  

    map_layer = "https://tile.openstreetmap.org/{z}/{x}/{y}.png"
    map_filter = ["Lâmpada LED", "Lâmpada de vapor de sódio", "." ]
    zoom = 18.4
    list_initial_coordinates = ["-23.3396", "-47.8238", map_layer, None, map_filter, zoom]
    list_profile =["Carlos", "adm", "11982245028"]
 

    loading = LoadingPages(page)
    loading.new_loading_page(page=page, call_layout=lambda:create_page_login(page))
#    loading.new_loading_page(page=page, call_layout=lambda:create_page_home(page, list_profile, list_initial_coordinates), text="Gerando Mapa")

if __name__ == "__main__":
    ft.app(target=main, upload_dir="uploads")


 