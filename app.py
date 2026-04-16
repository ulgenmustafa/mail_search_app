import tkinter as tk
from search import search
import indexer

def do_search():
    query = entry.get()
    results = search(query)

    text.delete(1.0, tk.END)

    if not results:
        text.insert(tk.END, "Sonuç bulunamadı\n")
        return

    for r in results:
        text.insert(tk.END, f"Dosya: {r[0]}\n")
        text.insert(tk.END, f"Gönderen: {r[1]}\n")
        text.insert(tk.END, f"Tarih: {r[2]}\n")
        text.insert(tk.END, f"Konu: {r[3]}\n")
        text.insert(tk.END, "-"*40 + "\n")


def update_database():
    text.delete(1.0, tk.END)
    text.insert(tk.END, "Veritabanı güncelleniyor...\n")

    indexer.index_folder("data")

    text.insert(tk.END, "Bitti!\n")


root = tk.Tk()
root.title("Mail Arama Sistemi")

entry = tk.Entry(root, width=50)
entry.pack(pady=10)

search_btn = tk.Button(root, text="Ara", command=do_search)
search_btn.pack()

update_btn = tk.Button(root, text="Veritabanını Güncelle", command=update_database)
update_btn.pack(pady=5)

text = tk.Text(root, width=80, height=25)
text.pack()

root.mainloop()