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


    loading = LoadingPages(page)
    loading.new_loading_page(page=page, layout=create_page_home(page))



# Executa a aplicação
if __name__ == "__main__":
    ft.app(target=main)
