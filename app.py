import tkinter as tk
from tkinter import scrolledtext
import os

from poetry_data import load_poetry_data
from search_engine import recommend_top_k


folder_path = 'poetry'
file_list, word_list, word_to_index, doc_to_index, U_k, S_k, reduced_docs = load_poetry_data(folder_path)

#GUI
root = tk.Tk()
root.title("Poetry Search System")

#검색 창(상단)
search_frame = tk.Frame(root)
search_frame.pack(pady=10)

search_entry = tk.Entry(search_frame, width=40)
search_entry.pack(side=tk.LEFT, padx=5)

def on_search():
    query = search_entry.get()
    results = recommend_top_k(query, word_list, word_to_index, U_k, S_k, reduced_docs, file_list, k=10)

    result_listbox.delete(0, tk.END)
    for filename, _ in results:
        result_listbox.insert(tk.END, filename)

search_button = tk.Button(search_frame, text="검색", command=on_search)
search_button.pack(side=tk.LEFT)

#결과 리스트박스
result_listbox = tk.Listbox(root, width=50)
result_listbox.pack(pady=10)

# 본문이랑 추천시스템 적용하기
poem_text = scrolledtext.ScrolledText(root, width=60, height=20)
poem_text.pack(pady=10)

recommend_frame = tk.Frame(root)
recommend_frame.pack(pady=5)

recommend_buttons = []

def show_poem(filename):
    file_path = os.path.join(folder_path, filename)
    with open(file_path, 'r', encoding='utf-8') as f:
        poem = f.read()

    poem_text.delete(1.0, tk.END)
    poem_text.insert(tk.END, filename.split(".txt")[0] + "\n\n")
    poem_text.insert(tk.END, poem)

    update_recommendations(filename)

def update_recommendations(current_filename):
    for btn in recommend_buttons:
        btn.destroy()
    recommend_buttons.clear()

    file_path = os.path.join(folder_path, current_filename)
    with open(file_path, 'r', encoding='utf-8') as f:
        text = f.read()

    recommendations = recommend_top_k(text, word_list, word_to_index, U_k, S_k, reduced_docs, file_list, k=4)
    recommendations = [r for r in recommendations if r[0] != current_filename][:3]

    for filename, _ in recommendations:
        btn = tk.Button(recommend_frame, text=filename, command=lambda f=filename: show_poem(f))
        btn.pack(side=tk.LEFT, padx=5)
        recommend_buttons.append(btn)

def on_select(event):
    if not result_listbox.curselection():
        return
    index = result_listbox.curselection()[0]
    filename = result_listbox.get(index)
    show_poem(filename)

result_listbox.bind('<<ListboxSelect>>', on_select)

root.mainloop()
