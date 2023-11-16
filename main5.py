import flet as ft
from flet import TextField,Checkbox,ElevatedButton,Text,Row,Column
from flet_core.control_event import ControlEvent

def main(page:ft.Page)->None:
    page.title="VaultShare"
    page.vertical_alignment=ft.MainAxisAlignment.CENTER
    page.horizontal_alignment=ft.MainAxisAlignment.CENTER
    page.theme_mode=ft.ThemeMode.LIGHT
    
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
        print("Username",text_username.value)
        print("Password:",text_password.value)
        
        page.clean()
        page.add(
            Row(
                controls=[Text(value=f"Welcome: {text_username.value}",size=20)],
                alignment=ft.MainAxisAlignment.CENTER
            )
        )
        
    text_username.on_change=validate
    text_password.on_change=validate
    button_submit.on_click=submit
    
    page.add(
        Row(
            controls=[
                Column(
                    [
                        text_username,text_password,button_submit
                    ]
                )
            ],
            alignment=ft.MainAxisAlignment.CENTER
        )
    )
    
if __name__=="__main__":
    ft.app(target=main)