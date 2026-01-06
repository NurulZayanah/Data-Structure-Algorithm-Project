import csv
import os
import tkinter as tk
from struct import pack
from tkinter import messagebox, simpledialog, Toplevel, Text, Scrollbar, VERTICAL, RIGHT, Y, END , ttk
from datetime import datetime, timedelta

BOOK_FILE = "Books.csv"

if not os.path.exists(BOOK_FILE):
    with open(BOOK_FILE, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            "Book_ID", "Title", "Author", "Year",
            "Genre", "Available", "Borrower", "Return_Date"
        ])

class BookNode:
    def __init__(self, book):
        self.book = book
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None

    def insert(self, book):
        node = BookNode(book)
        node.next = self.head
        self.head = node

    def delete(self, book_id):
        current = self.head
        prev = None
        while current:
            if current.book["Book_ID"] == book_id:
                if prev:
                    prev.next = current.next
                else:
                    self.head = current.next
                return True
            prev = current
            current = current.next
        return False

    def to_list(self):
        books = []
        current = self.head
        while current:
            books.append(current.book)
            current = current.next
        return books

class LibrarySystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Library Book Inventory System")
        self.root.attributes("-fullscreen", False)


        self.book_list = LinkedList()
        self.book_table = {}

        self.load_books()
        self.main_menu()

    def load_books(self):
        with open(BOOK_FILE, newline="") as f:
            reader = csv.DictReader(f)
            for row in reader:
                row["Book_ID"] = row["Book_ID"].strip().upper()

                self.book_list.insert(row)
                self.book_table[row["Book_ID"]] = row

    def save_books(self):
        with open(BOOK_FILE, "w", newline="") as f:
            fieldnames = [
                "Book_ID", "Title", "Author", "Year",
                "Genre", "Available", "Borrower", "Return_Date"
            ]
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for book in self.book_list.to_list():
                writer.writerow(book)

    def main_menu(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        #hias
        self.root.configure(bg="#f0f4f7")
        tk.Label(
       self.root ,
            text="Library Book Inventory System",
            font=("Cooper Black", 38, "bold"),
            bg="#f0f4f7",
            fg="#773841"
        ).pack(pady=30)

        button_style = {
            "width": 30,
            "height": 3,
            "bg": "#EFC3CA",
            "fg": "black",
            "font": ("Cooper Black", 15)
        }

        tk.Button(self.root, text="View Available Books", command=self.view_books, **button_style).pack(pady=10)
        tk.Button(self.root, text="Search Book", command=self.search_book ,**button_style).pack(pady=10)
        tk.Button(self.root, text="Borrow Book", command=self.borrow_book, **button_style).pack(pady=10)
        tk.Button(self.root, text="Return Book", command=self.return_book , **button_style).pack(pady=10)
        tk.Button(self.root, text="Exit",  command=self.exit_system ,**button_style).pack(pady=10)

    from tkinter import ttk  # Tambah di atas kalau belum ada

    def view_books(self):
        window = Toplevel(self.root)
        window.geometry("1000x600")
        window.configure(bg="#f0f4f7")

        tk.Label(window, text="Available Books", font=("Helvetica", 24, "bold"), bg="#f0f4f7").pack(pady=20)

        columns = ("Book_ID", "Title", "Author", "Year", "Genre")
        tree = ttk.Treeview(window, columns=columns, show="headings")
        tree.pack(expand=True, fill="both", padx=20)

        # Define column headings
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, anchor="center", width=180)

        # Insert data
        for book in self.book_list.to_list():
            if book["Available"].lower() == "yes":
                tree.insert("", "end", values=(
                    book["Book_ID"],
                    book["Title"],
                    book["Author"],
                    book["Year"],
                    book["Genre"]
                ))

        # Scrollbar
        scrollbar = ttk.Scrollbar(window, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        tk.Button(window, text="Back", command=window.destroy, font=("Arial", 12), bg="#3498db", fg="white").pack(
            pady=10)
        window.bind("<Escape>", lambda e: window.destroy())

    def search_book(self):
        # input book
        title = simpledialog.askstring("Search Book", "Enter Title or Author:")
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
        columns = ("Book_ID", "Title", "Author", "Year", "Genre", "Available")
        tree = ttk.Treeview(window, columns=columns, show="headings")
        tree.pack(expand=True, fill="both", padx=20)
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, anchor="center", width=180)

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
            display = "No matching books found."

        scrollbar = ttk.Scrollbar(window, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        tk.Button(window, text="Back", command=window.destroy, font=("Arial", 12), bg="#3498db", fg="white").pack(
            pady=10)
        window.bind("<Escape>", lambda e: window.destroy())
    def borrow_book(self):
        book_id = simpledialog.askstring("Borrow Book", "Enter Book ID:")
        if not book_id:
            return

        book_id = book_id.strip().upper()

        if book_id not in self.book_table:
            messagebox.showerror("Error", "Invalid Book ID.")
            return

        book = self.book_table[book_id]

        if book["Available"] == "No":
            messagebox.showerror("Error", "Book is not available.")
            return

        borrower = simpledialog.askstring("Borrower", "Enter borrower name:")
        if not borrower:
            return

        book["Available"] = "No"
        book["Borrower"] = borrower
        book["Return_Date"] = (datetime.now() + timedelta(days=21)).strftime("%Y-%m-%d")

        self.save_books()
        messagebox.showinfo("Success", "Book borrowed successfully.")

    def return_book(self):
        book_id = simpledialog.askstring("Return Book", "Enter Book ID:")
        if not book_id:
            return

        book_id = book_id.strip().upper()

        if book_id not in self.book_table:
            messagebox.showerror("Error", "Invalid Book ID.")
            return

        book = self.book_table[book_id]

        if book["Available"] == "Yes":
            messagebox.showinfo("Info", "This book is not currently borrowed.")
            return

        due_date = datetime.strptime(book["Return_Date"], "%Y-%m-%d")
        overdue_days = (datetime.now() - due_date).days
        fine = max(0, overdue_days * 0.2)

        book["Available"] = "Yes"
        book["Borrower"] = ""
        book["Return_Date"] = ""

        self.save_books()

        if fine > 0:
            messagebox.showinfo("Returned", f"Book returned.\nFine: RM {fine:.2f}")
        else:
            messagebox.showinfo("Returned", "Book returned successfully. No fine.")

    def exit_system(self):
        self.save_books()
        self.root.quit()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    LibrarySystem(root)
    root.mainloop()