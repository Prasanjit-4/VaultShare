import flet as ft
from flet import *
import os
from dotenv import load_dotenv
from supabase import create_client,Client
import socket
import time
from os import listdir
from os.path import isfile, join
import threading
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
    
    text_id:TextField=TextField(label="User ID",text_align=ft.TextAlign.LEFT)
    text_username:TextField=TextField(label="Username",text_align=ft.TextAlign.LEFT)
    text_password:TextField=TextField(label="Password",text_align=ft.TextAlign.LEFT,password=True)
    button_submit: ElevatedButton=ElevatedButton(text="Login",disabled=True)
    send_to:TextField= TextField(label="Send to: (Enter User ID)",text_align=ft.TextAlign.LEFT)
    
    def send_file(e:FilePickerResultEvent):
        send_ip=supabase.table("users").select("addr").eq("id",send_to.value).execute().data[0]['addr']
        print(send_ip)
        file_info=e.files
        print(len(file_info))
        for i in file_info:
            time.sleep(1)
            client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            client.connect((send_ip,8888))
            with open(i.path,"rb") as file:
                client.send(i.name.encode())
                data = file.read(1024)
                while data:
                    client.send(data)
                    data=file.read(1024)
            client.send(b"<END>")
            client.close()
            
    def validate(e:ControlEvent)->None:
        if all([text_username.value,text_password.value]):
            button_submit.disabled=False
        else:
            button_submit.disabled =True
        page.update()
    
    def submit(e:ControlEvent)->None:
        data=supabase.table('users').select("id,username,password").eq("id",text_id.value).execute()
        if(len(data.data)):
            if(text_password.value==data.data[0]['password']):
                supabase.table('users').update({"addr":str(local_ip())}).eq("id",text_id.value).execute()
                page.go('/home')
            else:
                print("Invalid Credentials")
        
    
    file_choosen=FilePicker(on_result=send_file)   
    page.overlay.append(file_choosen)  
    text_username.on_change=validate
    text_password.on_change=validate
    text_id.on_change=validate
    button_submit.on_click=submit
    lv=ft.ListView(expand=True,spacing=10)
    page.theme_mode=ft.ThemeMode.LIGHT
    
    def load_files():
        onlyfiles = [f for f in listdir("recv") if isfile(join("recv", f))]
        for i in onlyfiles:
            lv.controls.append(ft.Text(f"{i}"))
        page.update()

            
    def recv_file():
        server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        server.bind((str(local_ip()),8888))
        while True:
            server.listen()
            print("Listening....")
            client,addr=server.accept()

            file_name=client.recv(1024).decode()
            print(file_name)

            file=open(f"recv/{file_name}","wb")
            file_bytes=b""
            done = False

            while not done:
                data = client.recv(1024)
                if file_bytes[-5:]==b"<END>":
                    done = True
                else:
                    file_bytes+=data

            file.write(file_bytes[:-5])
            lv.controls.append(ft.Text(f"{file_name}"))
            page.update()
            file.close()

    def route_change(route):
        page.views.clear()
        page.views.append(
            ft.View(
                "/",   
                [
                    ft.AppBar(title=ft.Text("Vault Share"), bgcolor="blue"),
                    text_id,
                    text_username,
                    text_password,
                    button_submit
                ]
            )
        )
        if page.route == "/home":
            update_file=threading.Thread(target=recv_file,daemon=True)
            update_file.start()
            load_files()
            page.views.append(
                ft.View(
                    "/home",
                    [
                       ft.AppBar(title=ft.Text("Home"), bgcolor="blue",automatically_imply_leading=False),  
                      send_to,
            ElevatedButton("Send File",on_click=lambda _:file_choosen.pick_files(allow_multiple=True)),
            lv],
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