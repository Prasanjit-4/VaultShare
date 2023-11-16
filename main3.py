import flet as ft
from flet import *
from flet import RouteChangeEvent,ViewPopEvent,CrossAxisAlignment,MainAxisAlignment


def main(page:Page)->None:
    page.title="VaultShare"
    
    text_username:TextField=TextField(label="Username",text_align=ft.TextAlign.LEFT)
    text_password:TextField=TextField(label="Password",text_align=ft.TextAlign.LEFT,password=True)
    button_submit: ElevatedButton=ElevatedButton(text="Login",disabled=True,width=300)
    
    def validate(e:ControlEvent)->None:
        if all([text_username.value,text_password.value]):
            button_submit.disabled=False
        else:
            button_submit.disabled =True
        page.update()
    
    def submit(e:ControlEvent)->None:
        for i in data:
            print(i)
        page.go("/share")
        
    text_username.on_change=validate
    text_password.on_change=validate
    button_submit.on_click=submit
    
    def route_change(e:RouteChangeEvent)->None:
        page.views.clear()  
        page.views.append(
            View(
                route='/',
                controls=[
                    AppBar(title="Login Screen",bgcolor="blue"),
                    text_username,
                    text_password,
                    button_submit
                ],
                vertical_alignment=MainAxisAlignment.CENTER,
                horizontal_alignment=CrossAxisAlignment.CENTER,
                spacing=26
            )
        )
        
        if page.route == '/share':
            page.views.append(
                View(
                    route="/share",
                    controls=[
                        Text(value=f"{text_username.value}")
                    ]
                )
            )
        page.update()
        
        page.on_route_change=route_change
        
        page.go("/")

if __name__=="__main__":
    ft.app(target=main)
        