from flet import *
import flet as ft
from flet_core.control_event import ControlEvent
from flet.auth.providers import GoogleOAuthProvider
import os
from flet.security import encrypt,decrypt


# secret_key=os.getenv("MY_APP_SECRET_KEY")

clientID="1013629291002-nugsftrhab1otkcmtes45ji13clhg7bm.apps.googleusercontent.com"
clientSecret="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"

def main(page:Page):
    
    provider=GoogleOAuthProvider(
        client_id=clientID,
        client_secret=clientSecret,
        redirect_url="http://127.0.0.1:6969/api/oauth/redirect"
    )
    
    result_txt=Column()
    
    # AUTH_TOKEN_KEY="myapp.auth_token"
    
    # def perform_login(e):
    #     saved_token=None
    #     ejt=page.client_storage.get(AUTH_TOKEN_KEY)
    #     if ejt:
    #         saved_token=decrypt(ejt,secret_key)
    #     if e is not None or saved_token is not None:
    #         page.login(provider,saved_token=saved_token)
        
    
    def google_login(e):
        page.login(provider)
    
    def on_login(e):
        print(page.auth.user)
        result_txt.controls.append(
            Column([
                Text(f"name: {page.auth.user['name']}")
            ])
        )
        # jt=page.auth.token.to_json()
        # ejt=encrypt(jt,secret_key)
        # page.client_storage.set(AUTH_TOKEN_KEY,ejt)
        page.update()
        
    page.on_login=on_login
    page.add(
        Column([
            Text("Google Login",size=30),
            ElevatedButton("SignIn",
                           bgcolor="blue",
                           color="white",
                           on_click=google_login),
            result_txt
        ])
    )

ft.app(target=main,port=6969,view=WEB_BROWSER)