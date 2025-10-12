import tkinter as tk
from PIL import ImageTk, Image

class Login:
    def __init__(self):
        self.ventana_login = tk.Tk()
        self.ventana_login.title("Login")
        self.ventana_login.geometry("900x800")


        fondo = 'white'

        self.left_frame = tk.Frame(self.ventana_login)
        self.left_frame.configure(bg=fondo)
        self.left_frame.pack(expand=True, fill="both", side='left')

        self.right_frame = tk.Frame(self.ventana_login)
        self.right_frame.configure(bg='black')
        self.right_frame.pack(expand=True, fill="both", side='right')

        self.label_usr = tk.Label(self.left_frame, text="Usuario", font=("Arial", 20), fg="black", bg=fondo)
        self.label_usr.pack(pady=10)

        self.input_user = tk.Entry(self.left_frame, width=40, bd=1)
        self.input_user.pack(pady=10)

        self.label_password = tk.Label(self.left_frame, text="Contraseña", font=("Arial", 20), fg="black", bg=fondo)
        self.label_password.pack(pady=10)

        self.input_password = tk.Entry(self.left_frame, width=40, show='*', bd=1)
        self.input_password.pack(pady=10)

        self.ventana_login.mainloop()


Login()