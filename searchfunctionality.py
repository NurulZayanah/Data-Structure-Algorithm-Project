import tkinter as tk 
from tkinter import simpledialog
def search_book(self):
    # input book
    title = simpledialog.askstring("Search Book","Enter Title or Author:")
    if not title:
        return
    title = title.strip().lower
    results = []
    # Find matches
    for book in self.book_list.to_list():
        if title in book["Title"].lower() or title in book["Author"].lower():
            results.append(book)
            print(
                book["Book_ID"], "|", book["Title"], "|", book["Author"], "|",
                book["Year"], "|", book["Genre"], "|", "Available:", book["Available"]
            )
            found = True

    if not found:
        print("No matching books found.")

