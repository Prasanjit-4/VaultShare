import flet as ft
from flet import *
import time
import socket 
import threading
from os import listdir
from os.path import isfile, join


def main(page: Page):
    
    file_path = Text("")
    lv=ft.ListView(expand=True,spacing=10)
    page.theme_mode=ft.ThemeMode.LIGHT
    
    def load_files():
        onlyfiles = [f for f in listdir("recv") if isfile(join("recv", f))]
        for i in onlyfiles:
            lv.controls.append(ft.Text(f"{i}"))
        page.update()

            
    def recv_file():
        server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        server.bind(("192.168.11.127",8888))
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
    
    
    def send_file(e:FilePickerResultEvent):
        
        file_info=e.files
        print(len(file_info))
        for i in file_info:
            time.sleep(1)
            client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            client.connect(("192.168.11.140",8888))
            with open(i.path,"rb") as file:
                client.send(i.name.encode())
                data = file.read(1024)
                while data:
                    client.send(data)
                    data=file.read(1024)
            client.send(b"<END>")
            client.close()
            
        
        
    update_file=threading.Thread(target=recv_file,daemon=True)
    update_file.start()
    
    file_choosen=FilePicker(on_result= send_file)
    page.overlay.append(file_choosen)
    page.add(
        
            Column([
                TextField(label="Send to:"),
            ElevatedButton("Send File",on_click=lambda _:file_choosen.pick_files(allow_multiple=True)),
            lv])
                   
        )
    load_files()
    
ft.app(target=main)