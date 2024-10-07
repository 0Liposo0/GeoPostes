import flet as ft

# Classe para representar um poste
class Poste:
    def __init__(self, ip, situacao, tipo, pontos, bairro, logradouro):
        self.ip = ip
        self.situacao = situacao
        self.tipo = tipo
        self.pontos = pontos
        self.bairro = bairro
        self.logradouro = logradouro


# Componentes Visuais



theme1 = ft.Theme(
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


btn_null = ft.Column(
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        controls=[
            ft.ElevatedButton(
                width=20,
                height=20,
                bgcolor=ft.colors.AMBER,
                text=" ",
                style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10),)
                )
        ]
    )


texto_chamada = ft.Column(
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


chamda_ordem = ft.Container(
    visible=True,
    col=12,
    padding=20,
    content=ft.Text(
        value="Qual o motivo da Ordem de Serviço ?",
        text_align=ft.TextAlign.CENTER,
        size=30,
        color=ft.colors.BLACK,
        weight=ft.FontWeight.W_900,
    ),
    theme=theme1,
)


box_1 = ft.Checkbox(
    label="Ponto apagado",
    label_style=ft.TextStyle(
        color=ft.colors.BLACK,
        size=30,    
    )
)


box_2 = ft.Checkbox(
    label="Ponto piscando",
    label_style=ft.TextStyle(
        color=ft.colors.BLACK,
        size=30,    
    )
)


box_3 = ft.Checkbox(
    label="Rachadura",
    label_style=ft.TextStyle(
        color=ft.colors.BLACK,
        size=30,    
    )
)


box_4 = ft.Checkbox(
    label="Queda",
    label_style=ft.TextStyle(
        color=ft.colors.BLACK,
        size=30,    
    )
)


box_5 = ft.Checkbox(
    label="Incêndio elétrico",
    label_style=ft.TextStyle(
        color=ft.colors.BLACK,
        size=30,    
    )
)


box_6 = ft.Checkbox(
    label="Adicionar ponto",
    label_style=ft.TextStyle(
        color=ft.colors.BLACK,
        size=30,    
    )
)


text_field_order = ft.Column(
                    controls=[
                        ft.Container(
                            col=12,
                            alignment=ft.alignment.center,
                            content=ft.TextField(
                                value="",
                                label="Adicionar descrição",
                                text_align=ft.TextAlign.CENTER,
                                multiline=True,
                                min_lines=3,
                                label_style=ft.TextStyle(size=20),
                                text_style=ft.TextStyle(color=ft.colors.BLACK),
                            )
                        )
                    ]
)



