# app.py
import tkinter as tk
from tkinter import messagebox
from db import adicionar_livro, listar_livros

class BibliotecaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Biblioteca")

        self.titulo_label = tk.Label(root, text="Título")
        self.titulo_label.grid(row=0, column=0)
        self.titulo_entry = tk.Entry(root)
        self.titulo_entry.grid(row=0, column=1)

        self.autor_label = tk.Label(root, text="Autor")
        self.autor_label.grid(row=1, column=0)
        self.autor_entry = tk.Entry(root)
        self.autor_entry.grid(row=1, column=1)

        self.codigo_label = tk.Label(root, text="Código de Barras")
        self.codigo_label.grid(row=2, column=0)
        self.codigo_entry = tk.Entry(root)
        self.codigo_entry.grid(row=2, column=1)

        self.adicionar_button = tk.Button(root, text="Adicionar Livro", command=self.adicionar_livro)
        self.adicionar_button.grid(row=3, column=0, columnspan=2)

        self.listar_button = tk.Button(root, text="Listar Livros", command=self.listar_livros)
        self.listar_button.grid(row=4, column=0, columnspan=2)

        self.resultado_text = tk.Text(root, height=10, width=40)
        self.resultado_text.grid(row=5, column=0, columnspan=2)

    def adicionar_livro(self):
        titulo = self.titulo_entry.get()
        autor = self.autor_entry.get()
        codigo_barras = self.codigo_entry.get()
        if titulo and autor and codigo_barras:
            adicionar_livro(titulo, autor, codigo_barras)
            self.titulo_entry.delete(0, tk.END)
            self.autor_entry.delete(0, tk.END)
            self.codigo_entry.delete(0, tk.END)
        else:
            messagebox.showerror("Erro", "Todos os campos devem ser preenchidos")

    def listar_livros(self):
        livros = listar_livros()
        self.resultado_text.delete(1.0, tk.END)
        for livro in livros:
            self.resultado_text.insert(tk.END, f"ID: {livro[0]}, Título: {livro[1]}, Autor: {livro[2]}, Código de Barras: {livro[3]}\n")

if __name__ == "__main__":
    root = tk.Tk()
    app = BibliotecaApp(root)
    root.mainloop()
