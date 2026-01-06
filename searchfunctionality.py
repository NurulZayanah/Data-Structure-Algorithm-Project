import tkinter as tk 
from tkinter import simpledialog,Toplevel,ttk,Scrollbar,VERTICAL,Text,RIGHT,END
def search_book(self):
    # input book
    title = simpledialog.askstring("Search Book","Enter Title or Author:")
    if not title:
        return
    title = title.strip().lower()
    results = []
    # Find matches
    for book in self.book_list.to_list():
        if title in book["Title"].lower() or title in book["Author"].lower():
            results.append(book)
    window = Toplevel(self.root)
        window.title("search Results")
        window.attributes("-fullscreen", False)
        columns = ("Book_ID", "Title", "Author", "Year", "Genre","Available")
        tree = ttk.Treeview(window, columns=columns, show="headings")
        tree.pack(expand=True, fill="both", padx=20)
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, anchor="center", width=150)

        if results:
            for book in results:
                tree.insert("", "end", values=(
                    book["Book_ID"],
                    book["Title"],
                    book["Author"],
                    book["Year"],
                    book["Genre"],
                    book["Available"]
                ))

        else:
            display ="No matching books found."


        scrollbar = Scrollbar(window, orient=VERTICAL)
        text = Text(window, yscrollcommand=scrollbar.set)
        scrollbar.config(command=text.yview)

        scrollbar.pack(side=RIGHT, fill=Y)
        text.pack(expand=True, fill="both")

        text.insert(END, display)
        text.config(state="disabled")

        tk.Button(window, text="Back", command=window.destroy).pack(pady=10)
        window.bind("<Escape>", lambda e: window.destroy())



