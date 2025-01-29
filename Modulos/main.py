import flet as ft
from views import *
from models import *

def main(page: ft.Page):
    page.title = 'GeoPostes'
    page.expand = True  
    page.bgcolor = ft.Colors.WHITE 
    page.scroll = "auto"
    page.padding=0 
 
    loading = LoadingPages(page)
    loading.new_loading_page(page=page, call_layout=lambda:create_page_cities(page))


if __name__ == "__main__":
    ft.app(target=main, upload_dir="uploads")




