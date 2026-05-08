import tkinter as tk
from tkinter import ttk, messagebox
import json
import os

# Имя файла для хранения данных
DB_FILE = 'movies.json'

class MovieLibraryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Movie Library (Личная кинотека)")

        # Данные
        self.movies = self.load_data()

        # Интерфейс (Форма ввода)
        frame = tk.Frame(root, padx=10, pady=10)
        frame.pack(side=tk.TOP, fill=tk.X)

        tk.Label(frame, text="Название:").grid(row=0, column=0)
        self.ent_title = tk.Entry(frame)
        self.ent_title.grid(row=0, column=1)

        tk.Label(frame, text="Жанр:").grid(row=1, column=0)
        self.ent_genre = tk.Entry(frame)
        self.ent_genre.grid(row=1, column=1)

        tk.Label(frame, text="Год:").grid(row=2, column=0)
        self.ent_year = tk.Entry(frame)
        self.ent_year.grid(row=2, column=1)

        tk.Label(frame, text="Рейтинг (0-10):").grid(row=3, column=0)
        self.ent_rating = tk.Entry(frame)
        self.ent_rating.grid(row=3, column=1)

        btn_add = tk.Button(frame, text="Добавить фильм", command=self.add_movie)
        btn_add.grid(row=4, columnspan=2, pady=5)

        # Фильтрация
        filter_frame = tk.Frame(root, padx=10)
        filter_frame.pack(side=tk.TOP, fill=tk.X)
        
        tk.Label(filter_frame, text="Фильтр по жанру:").pack(side=tk.LEFT)
        self.ent_f_genre = tk.Entry(filter_frame, width=10)
        self.ent_f_genre.pack(side=tk.LEFT, padx=5)
        
        tk.Button(filter_frame, text="Применить", command=self.update_table).pack(side=tk.LEFT)
        tk.Button(filter_frame, text="Сброс", command=self.reset_filter).pack(side=tk.LEFT, padx=5)

        # Таблица
        self.tree = ttk.Treeview(root, columns=("Title", "Genre", "Year", "Rating"), show='headings')
        self.tree.heading("Title", text="Название")
        self.tree.heading("Genre", text="Жанр")
        self.tree.heading("Year", text="Год")
        self.tree.heading("Rating", text="Рейтинг")
        self.tree.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        self.update_table()

    def load_data(self):
        if os.path.exists(DB_FILE):
            with open(DB_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []

    def save_data(self):
        with open(DB_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.movies, f, ensure_ascii=False, indent=4)

    def add_movie(self):
        title = self.ent_title.get()
        genre = self.ent_genre.get()
        year = self.ent_year.get()
        rating = self.ent_rating.get()

        # Валидация
        try:
            if not title or not genre: raise ValueError("Заполните все поля")
            year = int(year)
            rating = float(rating)
            if not (0 <= rating <= 10): raise ValueError("Рейтинг от 0 до 10")
        except ValueError as e:
            messagebox.showerror("Ошибка", f"Некорректный ввод: {e}")
            return

        self.movies.append({"title": title, "genre": genre, "year": year, "rating": rating})
        self.save_data()
        self.update_table()
        
        # Очистка полей
        for entry in [self.ent_title, self.ent_genre, self.ent_year, self.ent_rating]:
            entry.delete(0, tk.END)

    def update_table(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        
        genre_filter = self.ent_f_genre.get().lower()
        
        for m in self.movies:
            if genre_filter in m['genre'].lower():
                self.tree.insert("", tk.END, values=(m['title'], m['genre'], m['year'], m['rating']))

    def reset_filter(self):
        self.ent_f_genre.delete(0, tk.END)
        self.update_table()

if __name__ == "__main__":
    root = tk.Tk()
    app = MovieLibraryApp(root)
    root.mainloop()
