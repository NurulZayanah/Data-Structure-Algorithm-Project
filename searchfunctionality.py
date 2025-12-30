def search_book(self , title , book_list):
    title = title.strip().lower()
    found = False 
    # Traverse linked list to find matches
    for book in self.book_list.to_list():
        if title in book["Title"].lower() or title in book["Author"].lower():
            print(
                book["Book_ID"], "|", book["Title"], "|", book["Author"], "|",
                book["Year"], "|", book["Genre"], "|", "Available:", book["Available"]
            )
            found = True

    if not found:
        print("No matching books found.")
