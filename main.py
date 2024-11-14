import flet as ft
from views import *
from models import *

def main(page: ft.Page):
    page.title = 'GeoPostes'
    page.window.always_on_top = True
    page.window.height = 960
    page.window.width = 440 
    page.window.resizable = False  
    page.bgcolor = ft.colors.WHITE  
    page.scroll = "auto"
    page.padding=0  

    list_initial_coordinates = ["-23.3396", "-47.8238"]
    list_profile =["Carlos"]

    loading = LoadingPages(page)
    loading.first_loading_page(page=page, layout=create_page_login(page))
#    loading.new_loading_page(page=page, layout=create_page_home(page, list_profile, list_initial_coordinates), home=True)

if __name__ == "__main__":
    ft.app(target=main, upload_dir="uploads")


 