import tkinter as tk
from PIL import ImageTk, Image

class Login:
    def __init__(self):
        self.ventana_login = tk.Tk()
        self.ventana_login.title("Login")
        self.ventana_login.state("zoomed")
        self.ventana_login.geometry('900x800')


        fondo = 'white'

        self.left_frame = tk.Frame(self.ventana_login)
        self.left_frame.configure(bg=fondo)
        self.left_frame.pack(expand=True, fill="both", side='left')

        self.right_frame = tk.Frame(self.ventana_login)
        self.right_frame.configure(bg='black')
        self.right_frame.pack(expand=True, fill="both", side='right')

        self.left_frame.grid_rowconfigure(0, weight=1)
        self.left_frame.grid_rowconfigure(2, weight=1)
        self.left_frame.grid_columnconfigure(0, weight=1)

        content = tk.Frame(self.left_frame, bg=fondo)
        content.grid(row=1, column=0)

        tk.Label(content, text="Usuario", font=("Arial", 20), fg="black", bg=fondo).pack(pady=10)
        tk.Entry(content, width=40, bd=1).pack(pady=10)

        tk.Label(content, text="Contraseña", font=("Arial", 20), fg="black", bg=fondo).pack(pady=10)
        tk.Entry(content, width=40, show='*', bd=1).pack(pady=10)

        tk.Button(content, text="Iniciar sesión", font=("Arial", 16), bg="white", fg="black").pack(pady=20)

        self.ventana_login.mainloop()

Login()