import tkinter as tk
from PIL import ImageTk, Image

class Login:
    def __init__(self):
        self.ventana_login = tk.Tk()
        self.ventana_login.title("Login")
        self.ventana_login.geometry("900x800")

        self.imagen = Image.open("fondo.jpg")

        fondo = 'white'

        self.frame_superior = tk.Frame(self.ventana_login)
        self.frame_superior.configure(bg=fondo)
        self.frame_superior.pack(expand=True, fill="both")

        self.frame_inferior = tk.Frame(self.ventana_login)
        self.frame_inferior.configure(bg=fondo)
        self.frame_inferior.pack(expand=True, fill="both")

        self.label_usr = tk.Label(self.frame_superior, text="Usuario", font=("Arial", 20), fg="black", bg=fondo)
        self.label_usr.pack(pady=10)

        self.input_user = tk.Entry(self.frame_superior, width=40, bd=1)
        self.input_user.pack(pady=10)

        self.label_password = tk.Label(self.frame_superior, text="Contraseña", font=("Arial", 20), fg="black", bg=fondo)
        self.label_password.pack(pady=10)

        self.input_password = tk.Entry(self.frame_superior, width=40, show='*', bd=1)
        self.input_password.pack(pady=10)

        self.ventana_login.mainloop()


Login()