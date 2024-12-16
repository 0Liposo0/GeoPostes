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

#    profile = CurrentProfile()
#    profile.add_user("Carlos")
#    profile.add_permission("adm")
#    profile.add_number("11982245028")
#    profile.add_city_name("Tatuí")
#    profile.add_city_call_name("tatui")
#   profile.add_city_lat("-23.3396")
#   profile.add_city_lon("-47.8238")
#    profile.add_city_acronym("CAP")
 
    loading = LoadingPages(page)
    loading.new_loading_page(page=page, call_layout=lambda:create_page_cities(page))
#    loading.new_loading_page(page=page, call_layout=lambda:create_page_login(page))
#    loading.new_loading_page(page=page, call_layout=lambda:create_page_home(page), text="Gerando Mapa")

if __name__ == "__main__":
    ft.app(target=main, upload_dir="uploads")


 