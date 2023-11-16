import flet as ft
from flet import *
import os
from dotenv import load_dotenv
from supabase import create_client,Client
import socket
load_dotenv()

load_dotenv()
url:str=os.environ.get("SUPABASE_URL")
key:str=os.environ.get("SUPABASE_KEY")

supabase: Client=create_client(url,key)


def local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = s.getsockname()[0]
    s.close()
    return ip

def main(page: ft.Page):
    page.title = "Routes Example"
    
    text_username:TextField=TextField(label="Username",text_align=ft.TextAlign.LEFT)
    text_password:TextField=TextField(label="Password",text_align=ft.TextAlign.LEFT,password=True)
    button_submit: ElevatedButton=ElevatedButton(text="Login",disabled=True)
    
    def validate(e:ControlEvent)->None:
        if all([text_username.value,text_password.value]):
            button_submit.disabled=False
        else:
            button_submit.disabled =True
        page.update()
    
    def submit(e:ControlEvent)->None:
        data=supabase.table('users').select("*").execute()
        print(len(data.data))
        for i in data.data:
            if(i['username']==text_username.value and i['password']==text_password.value):
                page.go("/home")
                break
    
                        
    text_username.on_change=validate
    text_password.on_change=validate
    button_submit.on_click=submit

    def route_change(route):
        page.views.clear()
        page.views.append(
            ft.View(
                "/",
                [
                    ft.AppBar(title=ft.Text("Vault Share"), bgcolor="blue"),
                    text_username,
                    text_password,
                    button_submit
                ]
            )
        )
        if page.route == "/home":
            page.views.append(
                ft.View(
                    "/home",
                    [
                       ft.AppBar(title=ft.Text("Home"), bgcolor="blue",automatically_imply_leading=False),                   ],
                )
            )
        page.update()

    def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go(page.route)


ft.app(target=main)