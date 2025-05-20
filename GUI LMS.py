import datetime
from collections import deque
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, scrolledtext
from tkinter.font import Font
from PIL import Image, ImageTk
import os

# Book Class
class Book:
    def __init__(self, isbn, title, author, quantity):
        self.isbn = isbn
        self.title = title
        self.author = author
        self.quantity = quantity
        self.available = quantity
        self.borrowers = {}  # user_id: due_date
        
    def __str__(self):
        return f"ISBN: {self.isbn}, Title: {self.title}, Author: {self.author}, Available: {self.available}/{self.quantity}"

# Node for Doubly Linked List
class BookNode:
    def __init__(self, book):
        self.book = book
        self.prev = None
        self.next = None

# Doubly Linked List for Book Inventory
class BookInventory:
    def __init__(self):
        self.head = None
        self.tail = None
        self.size = 0
    
    def add_book(self, book):
        new_node = BookNode(book)
        if not self.head:
            self.head = new_node
            self.tail = new_node
        else:
            new_node.prev = self.tail
            self.tail.next = new_node
            self.tail = new_node
        self.size += 1
    
    def delete_book(self, isbn):
        current = self.head
        while current:
            if current.book.isbn == isbn:
                if current.prev:
                    current.prev.next = current.next
                else:
                    self.head = current.next
                
                if current.next:
                    current.next.prev = current.prev
                else:
                    self.tail = current.prev
                
                self.size -= 1
                return True
            current = current.next
        return False
    
    def find_book(self, isbn):
        current = self.head
        while current:
            if current.book.isbn == isbn:
                return current.book
            current = current.next
        return None
    
    def get_all_books(self):
        books = []
        current = self.head
        while current:
            books.append(current.book)
            current = current.next
        return books

# Node for Binary Search Tree
class BSTNode:
    def __init__(self, key, book):
        self.key = key
        self.book = book
        self.left = None
        self.right = None

# Binary Search Tree for Book Search
class BookSearchTree:
    def __init__(self, key_type='isbn'):
        self.root = None
        self.key_type = key_type  # 'isbn', 'title', or 'author'
    
    def insert(self, book):
        key = self.get_key(book)
        self.root = self._insert(self.root, key, book)
    
    def get_key(self, book):
        if self.key_type == 'isbn':
            return book.isbn
        elif self.key_type == 'title':
            return book.title.lower()
        else:  # author
            return book.author.lower()
    
    def _insert(self, node, key, book):
        if not node:
            return BSTNode(key, book)
        
        if key < node.key:
            node.left = self._insert(node.left, key, book)
        elif key > node.key:
            node.right = self._insert(node.right, key, book)
        
        return node
    
    def search(self, key):
        key = key.lower() if self.key_type != 'isbn' else key
        return self._search(self.root, key)
    
    def _search(self, node, key):
        if not node:
            return None
        
        if key == node.key:
            return node.book
        elif key < node.key:
            return self._search(node.left, key)
        else:
            return self._search(node.right, key)
    
    def search_by_prefix(self, prefix):
        prefix = prefix.lower()
        results = []
        self._search_by_prefix(self.root, prefix, results)
        return results
    
    def _search_by_prefix(self, node, prefix, results):
        if not node:
            return
        
        if node.key.startswith(prefix):
            results.append(node.book)
            self._search_by_prefix(node.left, prefix, results)
            self._search_by_prefix(node.right, prefix, results)
        elif prefix < node.key:
            self._search_by_prefix(node.left, prefix, results)
        else:
            self._search_by_prefix(node.right, prefix, results)

# User Class
class User:
    def __init__(self, user_id, name, email):
        self.user_id = user_id
        self.name = name
        self.email = email
        self.borrowed_books = {}  # isbn: due_date
    
    def __str__(self):
        return f"ID: {self.user_id}, Name: {self.name}, Email: {self.email}, Borrowed Books: {len(self.borrowed_books)}"

# User Management
class UserManager:
    def __init__(self):
        self.users = {}  # user_id: User object
    
    def add_user(self, user):
        if user.user_id in self.users:
            return False
        self.users[user.user_id] = user
        return True
    
    def get_user(self, user_id):
        return self.users.get(user_id)
    
    def get_all_users(self):
        return list(self.users.values())

# Action Class for Undo/Redo
class Action:
    def __init__(self, action_type, user_id, isbn, due_date=None):
        self.action_type = action_type  # 'borrow' or 'return'
        self.user_id = user_id
        self.isbn = isbn
        self.due_date = due_date

# Library Management System
class LibraryManagementSystem:
    def __init__(self):
        self.inventory = BookInventory()
        self.isbn_search_tree = BookSearchTree('isbn')
        self.title_search_tree = BookSearchTree('title')
        self.author_search_tree = BookSearchTree('author')
        self.user_manager = UserManager()
        self.undo_stack = deque()
        self.redo_stack = deque()
    
    # Book Management
    def add_book(self, isbn, title, author, quantity):
        if self.inventory.find_book(isbn):
            return False, "Book with this ISBN already exists."
        
        book = Book(isbn, title, author, quantity)
        self.inventory.add_book(book)
        self.isbn_search_tree.insert(book)
        self.title_search_tree.insert(book)
        self.author_search_tree.insert(book)
        return True, "Book added successfully."
    
    def delete_book(self, isbn):
        book = self.inventory.find_book(isbn)
        if not book:
            return False, "Book not found."
        
        if book.available != book.quantity:
            return False, "Cannot delete book as some copies are still borrowed."
        
        success = self.inventory.delete_book(isbn)
        if success:
            return True, "Book deleted successfully."
        else:
            return False, "Failed to delete book."
    
    def update_book(self, isbn, title=None, author=None, quantity=None):
        book = self.inventory.find_book(isbn)
        if not book:
            return False, "Book not found."
        
        borrowed_count = book.quantity - book.available
        
        if quantity is not None:
            if quantity < borrowed_count:
                return False, f"Cannot reduce quantity below {borrowed_count} as these copies are borrowed."
            book.available += (quantity - book.quantity)
            book.quantity = quantity
        
        if title:
            book.title = title
        if author:
            book.author = author
        
        return True, "Book updated successfully."
    
    def get_all_books(self):
        return self.inventory.get_all_books()
    
    # Search Functions
    def search_book_by_isbn(self, isbn):
        return self.isbn_search_tree.search(isbn)
    
    def search_books_by_title(self, title):
        return self.title_search_tree.search_by_prefix(title)
    
    def search_books_by_author(self, author):
        return self.author_search_tree.search_by_prefix(author)
    
    # User Management
    def register_user(self, user_id, name, email):
        user = User(user_id, name, email)
        if self.user_manager.add_user(user):
            return True, "User registered successfully."
        else:
            return False, "User ID already exists."
    
    def get_all_users(self):
        return self.user_manager.get_all_users()
    
    # Borrow/Return Functions
    def borrow_book(self, user_id, isbn, days=14):
        user = self.user_manager.get_user(user_id)
        if not user:
            return False, "User not found."
        
        book = self.inventory.find_book(isbn)
        if not book:
            return False, "Book not found."
        
        if book.available <= 0:
            return False, "No copies of this book available."
        
        if isbn in user.borrowed_books:
            return False, "User has already borrowed this book."
        
        due_date = datetime.date.today() + datetime.timedelta(days=days)
        book.available -= 1
        book.borrowers[user_id] = due_date
        user.borrowed_books[isbn] = due_date
        
        self.undo_stack.append(Action('borrow', user_id, isbn, due_date))
        self.redo_stack.clear()
        
        return True, f"Book borrowed successfully. Due date: {due_date}"
    
    def return_book(self, user_id, isbn):
        user = self.user_manager.get_user(user_id)
        if not user:
            return False, "User not found."
        
        book = self.inventory.find_book(isbn)
        if not book:
            return False, "Book not found."
        
        if isbn not in user.borrowed_books:
            return False, "User hasn't borrowed this book."
        
        due_date = user.borrowed_books[isbn]
        book.available += 1
        if user_id in book.borrowers:
            del book.borrowers[user_id]
        del user.borrowed_books[isbn]
        
        self.undo_stack.append(Action('return', user_id, isbn, due_date))
        self.redo_stack.clear()
        
        return True, "Book returned successfully."
    
    def get_user_borrowed_books(self, user_id):
        user = self.user_manager.get_user(user_id)
        if not user:
            return None, "User not found."
        
        if not user.borrowed_books:
            return [], "User has no borrowed books."
        
        today = datetime.date.today()
        borrowed_books = []
        for isbn, due_date in user.borrowed_books.items():
            book = self.inventory.find_book(isbn)
            status = "OVERDUE" if due_date < today else "On Time"
            borrowed_books.append((book, due_date, status))
        
        return borrowed_books, None
    
    # Undo/Redo Functions
    def undo(self):
        if not self.undo_stack:
            return False, "Nothing to undo."
        
        action = self.undo_stack.pop()
        self.redo_stack.append(action)
        
        user = self.user_manager.get_user(action.user_id)
        book = self.inventory.find_book(action.isbn)
        
        if not user or not book:
            return False, "Undo failed: User or Book not found."
        
        if action.action_type == 'borrow':
            book.available += 1
            book.borrowers.pop(action.user_id, None)
            user.borrowed_books.pop(action.isbn, None)
            return True, f"Undo: Book '{book.title}' returned by {user.name}"
        else:
            if book.available <= 0:
                return False, "Undo failed: No available copies to borrow again."
            book.available -= 1
            book.borrowers[action.user_id] = action.due_date
            user.borrowed_books[action.isbn] = action.due_date
            return True, f"Undo: Book '{book.title}' borrowed again by {user.name}"
    
    def redo(self):
        if not self.redo_stack:
            return False, "Nothing to redo."
        
        action = self.redo_stack.pop()
        self.undo_stack.append(action)
        
        user = self.user_manager.get_user(action.user_id)
        book = self.inventory.find_book(action.isbn)
        
        if not user or not book:
            return False, "Redo failed: User or Book not found."
        
        if action.action_type == 'borrow':
            if book.available <= 0:
                return False, "Redo failed: No copies available to borrow."
            book.available -= 1
            book.borrowers[action.user_id] = action.due_date
            user.borrowed_books[action.isbn] = action.due_date
            return True, f"Redo: Book '{book.title}' borrowed by {user.name}"
        else:
            book.available += 1
            book.borrowers.pop(action.user_id, None)
            user.borrowed_books.pop(action.isbn, None)
            return True, f"Redo: Book '{book.title}' returned by {user.name}"
    
    # Reports
    def get_overdue_books(self):
        today = datetime.date.today()
        overdue_books = []
        
        current = self.inventory.head
        while current:
            for user_id, due_date in current.book.borrowers.items():
                if due_date < today:
                    user = self.user_manager.get_user(user_id)
                    if user:
                        overdue_days = (today - due_date).days
                        overdue_books.append((current.book, user, due_date, overdue_days))
            current = current.next
        
        return overdue_books
    
    def get_most_borrowed_books(self, top_n=5):
        book_borrow_counts = []
        
        current = self.inventory.head
        while current:
            borrow_count = current.book.quantity - current.book.available
            book_borrow_counts.append((current.book, borrow_count))
            current = current.next
        
        book_borrow_counts.sort(key=lambda x: x[1], reverse=True)
        return book_borrow_counts[:top_n]

# GUI Application
class LibraryApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.lms = LibraryManagementSystem()
        self.title("Library Management System")
        self.geometry("1000x700")
        self.configure(bg="#f0f0f0")
        
        # Add sample data
        self._add_sample_data()
        
        # Create custom fonts
        self.title_font = Font(family="Helvetica", size=16, weight="bold")
        self.button_font = Font(family="Helvetica", size=12)
        self.text_font = Font(family="Courier", size=10)
        
        # Create main container
        self.container = tk.Frame(self, bg="#f0f0f0")
        self.container.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Create header
        self.header = tk.Frame(self.container, bg="#f0f0f0")
        self.header.pack(fill="x", pady=(0, 20))
        
        # Add logo (placeholder - replace with actual image path)
        try:
            self.logo_img = Image.open("library_logo.png").resize((50, 50))
            self.logo = ImageTk.PhotoImage(self.logo_img)
            self.logo_label = tk.Label(self.header, image=self.logo, bg="#f0f0f0")
            self.logo_label.pack(side="left", padx=(0, 10))
        except:
            pass
        
        self.title_label = tk.Label(
            self.header, 
            text="Library Management System", 
            font=self.title_font, 
            bg="#f0f0f0"
        )
        self.title_label.pack(side="left")
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(self.container)
        self.notebook.pack(fill="both", expand=True)
        
        # Create tabs
        self._create_book_tab()
        self._create_user_tab()
        self._create_borrow_tab()
        self._create_search_tab()
        self._create_reports_tab()
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_bar = tk.Label(
            self.container, 
            textvariable=self.status_var, 
            relief="sunken", 
            anchor="w",
            bg="#e0e0e0",
            font=self.text_font
        )
        self.status_bar.pack(fill="x", pady=(10, 0))
        
        # Set initial status
        self.update_status("Ready")
    
    def _add_sample_data(self):
        # Add sample books
        self.lms.add_book("978-3-16-148410-0", "Introduction to Algorithms", "Thomas Cormen", 5)
        self.lms.add_book("978-0-262-03293-3", "Clean Code", "Robert Martin", 3)
        self.lms.add_book("978-0-13-235088-4", "Design Patterns", "Erich Gamma", 4)
        self.lms.add_book("978-0-201-63361-0", "The Art of Computer Programming", "Donald Knuth", 2)
        
        # Register sample users
        self.lms.register_user("U001", "Alice Johnson", "alice@example.com")
        self.lms.register_user("U002", "Bob Smith", "bob@example.com")
    
    def update_status(self, message):
        self.status_var.set(message)
    
    def _create_book_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Book Management")
        
        # Book management frame
        book_frame = ttk.LabelFrame(tab, text="Book Operations", padding=10)
        book_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Add book form
        add_frame = ttk.Frame(book_frame)
        add_frame.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        
        ttk.Label(add_frame, text="ISBN:").grid(row=0, column=0, sticky="e", padx=5, pady=2)
        self.isbn_entry = ttk.Entry(add_frame)
        self.isbn_entry.grid(row=0, column=1, padx=5, pady=2)
        
        ttk.Label(add_frame, text="Title:").grid(row=1, column=0, sticky="e", padx=5, pady=2)
        self.title_entry = ttk.Entry(add_frame)
        self.title_entry.grid(row=1, column=1, padx=5, pady=2)
        
        ttk.Label(add_frame, text="Author:").grid(row=2, column=0, sticky="e", padx=5, pady=2)
        self.author_entry = ttk.Entry(add_frame)
        self.author_entry.grid(row=2, column=1, padx=5, pady=2)
        
        ttk.Label(add_frame, text="Quantity:").grid(row=3, column=0, sticky="e", padx=5, pady=2)
        self.quantity_entry = ttk.Entry(add_frame)
        self.quantity_entry.grid(row=3, column=1, padx=5, pady=2)
        
        add_btn = ttk.Button(add_frame, text="Add Book", command=self.add_book)
        add_btn.grid(row=4, column=0, columnspan=2, pady=5)
        
        # Update/Delete book form
        ud_frame = ttk.Frame(book_frame)
        ud_frame.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")
        
        ttk.Label(ud_frame, text="ISBN to Update/Delete:").grid(row=0, column=0, sticky="e", padx=5, pady=2)
        self.ud_isbn_entry = ttk.Entry(ud_frame)
        self.ud_isbn_entry.grid(row=0, column=1, padx=5, pady=2)
        
        update_btn = ttk.Button(ud_frame, text="Update Book", command=self.update_book_dialog)
        update_btn.grid(row=1, column=0, columnspan=2, pady=5)
        
        delete_btn = ttk.Button(ud_frame, text="Delete Book", command=self.delete_book)
        delete_btn.grid(row=2, column=0, columnspan=2, pady=5)
        
        # Book list
        list_frame = ttk.LabelFrame(book_frame, text="Book Inventory", padding=10)
        list_frame.grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")
        
        columns = ("isbn", "title", "author", "quantity", "available")
        self.book_tree = ttk.Treeview(
            list_frame, 
            columns=columns, 
            show="headings",
            selectmode="browse"
        )
        
        self.book_tree.heading("isbn", text="ISBN")
        self.book_tree.heading("title", text="Title")
        self.book_tree.heading("author", text="Author")
        self.book_tree.heading("quantity", text="Total")
        self.book_tree.heading("available", text="Available")
        
        self.book_tree.column("isbn", width=150)
        self.book_tree.column("title", width=200)
        self.book_tree.column("author", width=150)
        self.book_tree.column("quantity", width=60, anchor="center")
        self.book_tree.column("available", width=80, anchor="center")
        
        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.book_tree.yview)
        self.book_tree.configure(yscrollcommand=scrollbar.set)
        
        self.book_tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Load books into treeview
        self.refresh_book_list()
        
        # Configure grid weights
        book_frame.columnconfigure(0, weight=1)
        book_frame.columnconfigure(1, weight=1)
        book_frame.rowconfigure(1, weight=1)
    
    def _create_user_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="User Management")
        
        # User management frame
        user_frame = ttk.LabelFrame(tab, text="User Operations", padding=10)
        user_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Add user form
        add_frame = ttk.Frame(user_frame)
        add_frame.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        
        ttk.Label(add_frame, text="User ID:").grid(row=0, column=0, sticky="e", padx=5, pady=2)
        self.user_id_entry = ttk.Entry(add_frame)
        self.user_id_entry.grid(row=0, column=1, padx=5, pady=2)
        
        ttk.Label(add_frame, text="Name:").grid(row=1, column=0, sticky="e", padx=5, pady=2)
        self.name_entry = ttk.Entry(add_frame)
        self.name_entry.grid(row=1, column=1, padx=5, pady=2)
        
        ttk.Label(add_frame, text="Email:").grid(row=2, column=0, sticky="e", padx=5, pady=2)
        self.email_entry = ttk.Entry(add_frame)
        self.email_entry.grid(row=2, column=1, padx=5, pady=2)
        
        add_btn = ttk.Button(add_frame, text="Register User", command=self.register_user)
        add_btn.grid(row=3, column=0, columnspan=2, pady=5)
        
        # User list
        list_frame = ttk.LabelFrame(user_frame, text="Registered Users", padding=10)
        list_frame.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")
        
        columns = ("user_id", "name", "email", "borrowed")
        self.user_tree = ttk.Treeview(
            list_frame, 
            columns=columns, 
            show="headings",
            selectmode="browse"
        )
        
        self.user_tree.heading("user_id", text="User ID")
        self.user_tree.heading("name", text="Name")
        self.user_tree.heading("email", text="Email")
        self.user_tree.heading("borrowed", text="Books Borrowed")
        
        self.user_tree.column("user_id", width=100)
        self.user_tree.column("name", width=150)
        self.user_tree.column("email", width=200)
        self.user_tree.column("borrowed", width=100, anchor="center")
        
        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.user_tree.yview)
        self.user_tree.configure(yscrollcommand=scrollbar.set)
        
        self.user_tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Load users into treeview
        self.refresh_user_list()
        
        # Configure grid weights
        user_frame.columnconfigure(0, weight=1)
        user_frame.rowconfigure(1, weight=1)
    
    def _create_borrow_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Borrow/Return")
        
        # Borrow/Return frame
        br_frame = ttk.LabelFrame(tab, text="Book Transactions", padding=10)
        br_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Borrow form
        borrow_frame = ttk.Frame(br_frame)
        borrow_frame.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        
        ttk.Label(borrow_frame, text="User ID:").grid(row=0, column=0, sticky="e", padx=5, pady=2)
        self.borrow_user_entry = ttk.Entry(borrow_frame)
        self.borrow_user_entry.grid(row=0, column=1, padx=5, pady=2)
        
        ttk.Label(borrow_frame, text="ISBN:").grid(row=1, column=0, sticky="e", padx=5, pady=2)
        self.borrow_isbn_entry = ttk.Entry(borrow_frame)
        self.borrow_isbn_entry.grid(row=1, column=1, padx=5, pady=2)
        
        ttk.Label(borrow_frame, text="Days (default 14):").grid(row=2, column=0, sticky="e", padx=5, pady=2)
        self.days_entry = ttk.Entry(borrow_frame)
        self.days_entry.grid(row=2, column=1, padx=5, pady=2)
        
        borrow_btn = ttk.Button(borrow_frame, text="Borrow Book", command=self.borrow_book)
        borrow_btn.grid(row=3, column=0, columnspan=2, pady=5)
        
        # Return form
        return_frame = ttk.Frame(br_frame)
        return_frame.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")
        
        ttk.Label(return_frame, text="User ID:").grid(row=0, column=0, sticky="e", padx=5, pady=2)
        self.return_user_entry = ttk.Entry(return_frame)
        self.return_user_entry.grid(row=0, column=1, padx=5, pady=2)
        
        ttk.Label(return_frame, text="ISBN:").grid(row=1, column=0, sticky="e", padx=5, pady=2)
        self.return_isbn_entry = ttk.Entry(return_frame)
        self.return_isbn_entry.grid(row=1, column=1, padx=5, pady=2)
        
        return_btn = ttk.Button(return_frame, text="Return Book", command=self.return_book)
        return_btn.grid(row=2, column=0, columnspan=2, pady=5)
        
        # Undo/Redo buttons
        undo_redo_frame = ttk.Frame(br_frame)
        undo_redo_frame.grid(row=0, column=2, padx=5, pady=5, sticky="nsew")
        
        undo_btn = ttk.Button(undo_redo_frame, text="Undo", command=self.undo_action)
        undo_btn.pack(pady=5, fill="x")
        
        redo_btn = ttk.Button(undo_redo_frame, text="Redo", command=self.redo_action)
        redo_btn.pack(pady=5, fill="x")
        
        # Borrowed books list
        list_frame = ttk.LabelFrame(br_frame, text="Borrowed Books", padding=10)
        list_frame.grid(row=1, column=0, columnspan=3, padx=5, pady=5, sticky="nsew")
        
        self.borrowed_text = scrolledtext.ScrolledText(
            list_frame, 
            wrap=tk.WORD, 
            font=self.text_font,
            height=10
        )
        self.borrowed_text.pack(fill="both", expand=True)
        
        # Configure grid weights
        br_frame.columnconfigure(0, weight=1)
        br_frame.columnconfigure(1, weight=1)
        br_frame.columnconfigure(2, weight=1)
        br_frame.rowconfigure(1, weight=1)
    
    def _create_search_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Search Books")
        
        # Search frame
        search_frame = ttk.LabelFrame(tab, text="Search Options", padding=10)
        search_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Search type
        ttk.Label(search_frame, text="Search by:").grid(row=0, column=0, sticky="w", padx=5, pady=2)
        self.search_type = tk.StringVar(value="isbn")
        
        ttk.Radiobutton(
            search_frame, 
            text="ISBN", 
            variable=self.search_type, 
            value="isbn"
        ).grid(row=1, column=0, sticky="w", padx=5, pady=2)
        
        ttk.Radiobutton(
            search_frame, 
            text="Title", 
            variable=self.search_type, 
            value="title"
        ).grid(row=2, column=0, sticky="w", padx=5, pady=2)
        
        ttk.Radiobutton(
            search_frame, 
            text="Author", 
            variable=self.search_type, 
            value="author"
        ).grid(row=3, column=0, sticky="w", padx=5, pady=2)
        
        # Search entry
        ttk.Label(search_frame, text="Search term:").grid(row=0, column=1, sticky="w", padx=5, pady=2)
        self.search_entry = ttk.Entry(search_frame)
        self.search_entry.grid(row=1, column=1, rowspan=3, padx=5, pady=2, sticky="we")
        
        search_btn = ttk.Button(search_frame, text="Search", command=self.search_books)
        search_btn.grid(row=4, column=0, columnspan=2, pady=5)
        
        # Results frame
        results_frame = ttk.LabelFrame(search_frame, text="Search Results", padding=10)
        results_frame.grid(row=5, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")
        
        columns = ("isbn", "title", "author", "available")
        self.search_tree = ttk.Treeview(
            results_frame, 
            columns=columns, 
            show="headings",
            selectmode="browse"
        )
        
        self.search_tree.heading("isbn", text="ISBN")
        self.search_tree.heading("title", text="Title")
        self.search_tree.heading("author", text="Author")
        self.search_tree.heading("available", text="Available")
        
        self.search_tree.column("isbn", width=150)
        self.search_tree.column("title", width=250)
        self.search_tree.column("author", width=150)
        self.search_tree.column("available", width=80, anchor="center")
        
        scrollbar = ttk.Scrollbar(results_frame, orient="vertical", command=self.search_tree.yview)
        self.search_tree.configure(yscrollcommand=scrollbar.set)
        
        self.search_tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Configure grid weights
        search_frame.columnconfigure(1, weight=1)
        search_frame.rowconfigure(5, weight=1)
    
    def _create_reports_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Reports")
        
        # Reports frame
        reports_frame = ttk.LabelFrame(tab, text="Library Reports", padding=10)
        reports_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Report buttons
        ttk.Button(
            reports_frame, 
            text="Show Overdue Books", 
            command=self.show_overdue_books
        ).pack(pady=5, fill="x")
        
        ttk.Button(
            reports_frame, 
            text="Show Most Borrowed Books", 
            command=self.show_most_borrowed
        ).pack(pady=5, fill="x")
        
        # Report display
        self.report_text = scrolledtext.ScrolledText(
            reports_frame, 
            wrap=tk.WORD, 
            font=self.text_font,
            height=15
        )
        self.report_text.pack(fill="both", expand=True, pady=10)
    
    # Book management methods
    def add_book(self):
        isbn = self.isbn_entry.get().strip()
        title = self.title_entry.get().strip()
        author = self.author_entry.get().strip()
        quantity = self.quantity_entry.get().strip()
        
        if not all([isbn, title, author, quantity]):
            messagebox.showerror("Error", "All fields are required!")
            return
        
        if not quantity.isdigit() or int(quantity) <= 0:
            messagebox.showerror("Error", "Quantity must be a positive integer!")
            return
        
        success, message = self.lms.add_book(isbn, title, author, int(quantity))
        if success:
            self.refresh_book_list()
            self.isbn_entry.delete(0, tk.END)
            self.title_entry.delete(0, tk.END)
            self.author_entry.delete(0, tk.END)
            self.quantity_entry.delete(0, tk.END)
            self.update_status(message)
        else:
            messagebox.showerror("Error", message)
    
    def update_book_dialog(self):
        isbn = self.ud_isbn_entry.get().strip()
        if not isbn:
            messagebox.showerror("Error", "Please enter an ISBN!")
            return
        
        book = self.lms.search_book_by_isbn(isbn)
        if not book:
            messagebox.showerror("Error", "Book not found!")
            return
        
        # Create update dialog
        dialog = tk.Toplevel(self)
        dialog.title("Update Book")
        dialog.transient(self)
        dialog.grab_set()
        
        ttk.Label(dialog, text=f"Updating: {book.title}").pack(pady=5)
        
        # Title
        ttk.Label(dialog, text="Title:").pack()
        title_entry = ttk.Entry(dialog)
        title_entry.insert(0, book.title)
        title_entry.pack(fill="x", padx=20, pady=2)
        
        # Author
        ttk.Label(dialog, text="Author:").pack()
        author_entry = ttk.Entry(dialog)
        author_entry.insert(0, book.author)
        author_entry.pack(fill="x", padx=20, pady=2)
        
        # Quantity
        ttk.Label(dialog, text="Quantity:").pack()
        quantity_entry = ttk.Entry(dialog)
        quantity_entry.insert(0, str(book.quantity))
        quantity_entry.pack(fill="x", padx=20, pady=2)
        
        def update():
            title = title_entry.get().strip()
            author = author_entry.get().strip()
            quantity = quantity_entry.get().strip()
            
            qty = None
            if quantity:
                if not quantity.isdigit() or int(quantity) < 0:
                    messagebox.showerror("Error", "Quantity must be a non-negative integer!")
                    return
                qty = int(quantity)
            
            success, message = self.lms.update_book(
                isbn,
                title if title else None,
                author if author else None,
                qty
            )
            
            if success:
                self.refresh_book_list()
                dialog.destroy()
                self.update_status(message)
            else:
                messagebox.showerror("Error", message)
        
        ttk.Button(dialog, text="Update", command=update).pack(pady=10)
    
    def delete_book(self):
        isbn = self.ud_isbn_entry.get().strip()
        if not isbn:
            messagebox.showerror("Error", "Please enter an ISBN!")
            return
        
        if not messagebox.askyesno("Confirm", "Are you sure you want to delete this book?"):
            return
        
        success, message = self.lms.delete_book(isbn)
        if success:
            self.refresh_book_list()
            self.ud_isbn_entry.delete(0, tk.END)
            self.update_status(message)
        else:
            messagebox.showerror("Error", message)
    
    def refresh_book_list(self):
        self.book_tree.delete(*self.book_tree.get_children())
        for book in self.lms.get_all_books():
            self.book_tree.insert("", "end", values=(
                book.isbn,
                book.title,
                book.author,
                book.quantity,
                book.available
            ))
    
    # User management methods
    def register_user(self):
        user_id = self.user_id_entry.get().strip()
        name = self.name_entry.get().strip()
        email = self.email_entry.get().strip()
        
        if not all([user_id, name, email]):
            messagebox.showerror("Error", "All fields are required!")
            return
        
        success, message = self.lms.register_user(user_id, name, email)
        if success:
            self.refresh_user_list()
            self.user_id_entry.delete(0, tk.END)
            self.name_entry.delete(0, tk.END)
            self.email_entry.delete(0, tk.END)
            self.update_status(message)
        else:
            messagebox.showerror("Error", message)
    
    def refresh_user_list(self):
        self.user_tree.delete(*self.user_tree.get_children())
        for user in self.lms.get_all_users():
            self.user_tree.insert("", "end", values=(
                user.user_id,
                user.name,
                user.email,
                len(user.borrowed_books)
            ))
    
    # Borrow/Return methods
    def borrow_book(self):
        user_id = self.borrow_user_entry.get().strip()
        isbn = self.borrow_isbn_entry.get().strip()
        days = self.days_entry.get().strip()
        
        if not all([user_id, isbn]):
            messagebox.showerror("Error", "User ID and ISBN are required!")
            return
        
        days_int = 14
        if days:
            if not days.isdigit() or int(days) <= 0:
                messagebox.showerror("Error", "Days must be a positive integer!")
                return
            days_int = int(days)
        
        success, message = self.lms.borrow_book(user_id, isbn, days_int)
        if success:
            self.refresh_book_list()
            self.refresh_user_list()
            self.update_borrowed_books(user_id)
            self.borrow_user_entry.delete(0, tk.END)
            self.borrow_isbn_entry.delete(0, tk.END)
            self.days_entry.delete(0, tk.END)
            self.update_status(message)
        else:
            messagebox.showerror("Error", message)
    
    def return_book(self):
        user_id = self.return_user_entry.get().strip()
        isbn = self.return_isbn_entry.get().strip()
        
        if not all([user_id, isbn]):
            messagebox.showerror("Error", "User ID and ISBN are required!")
            return
        
        success, message = self.lms.return_book(user_id, isbn)
        if success:
            self.refresh_book_list()
            self.refresh_user_list()
            self.update_borrowed_books(user_id)
            self.return_user_entry.delete(0, tk.END)
            self.return_isbn_entry.delete(0, tk.END)
            self.update_status(message)
        else:
            messagebox.showerror("Error", message)
    
    def update_borrowed_books(self, user_id=None):
        self.borrowed_text.delete(1.0, tk.END)
        
        if not user_id:
            user_id = self.borrow_user_entry.get().strip()
            if not user_id:
                user_id = self.return_user_entry.get().strip()
        
        if user_id:
            borrowed_books, error = self.lms.get_user_borrowed_books(user_id)
            if error:
                self.borrowed_text.insert(tk.END, error)
            else:
                today = datetime.date.today()
                self.borrowed_text.insert(tk.END, f"Books borrowed by user {user_id}:\n\n")
                for book, due_date, status in borrowed_books:
                    self.borrowed_text.insert(tk.END, 
                        f"- {book.title} (Due: {due_date}, Status: {status})\n")
    
    def undo_action(self):
        success, message = self.lms.undo()
        if success:
            self.refresh_book_list()
            self.refresh_user_list()
            self.update_status(message)
        else:
            messagebox.showerror("Error", message)
    
    def redo_action(self):
        success, message = self.lms.redo()
        if success:
            self.refresh_book_list()
            self.refresh_user_list()
            self.update_status(message)
        else:
            messagebox.showerror("Error", message)
    
    # Search methods
    def search_books(self):
        search_type = self.search_type.get()
        term = self.search_entry.get().strip()
        
        if not term:
            messagebox.showerror("Error", "Please enter a search term!")
            return
        
        self.search_tree.delete(*self.search_tree.get_children())
        
        if search_type == "isbn":
            book = self.lms.search_book_by_isbn(term)
            if book:
                self.search_tree.insert("", "end", values=(
                    book.isbn,
                    book.title,
                    book.author,
                    book.available
                ))
            else:
                messagebox.showinfo("Not Found", "No book found with this ISBN.")
        elif search_type == "title":
            books = self.lms.search_books_by_title(term)
            if books:
                for book in books:
                    self.search_tree.insert("", "end", values=(
                        book.isbn,
                        book.title,
                        book.author,
                        book.available
                    ))
            else:
                messagebox.showinfo("Not Found", "No books found with this title prefix.")
        elif search_type == "author":
            books = self.lms.search_books_by_author(term)
            if books:
                for book in books:
                    self.search_tree.insert("", "end", values=(
                        book.isbn,
                        book.title,
                        book.author,
                        book.available
                    ))
            else:
                messagebox.showinfo("Not Found", "No books found by this author prefix.")
    
    # Report methods
    def show_overdue_books(self):
        overdue_books = self.lms.get_overdue_books()
        self.report_text.delete(1.0, tk.END)
        
        if not overdue_books:
            self.report_text.insert(tk.END, "No overdue books.")
            return
        
        today = datetime.date.today()
        self.report_text.insert(tk.END, "=== Overdue Books ===\n\n")
        
        for book, user, due_date, overdue_days in overdue_books:
            self.report_text.insert(tk.END, 
                f"Book: {book.title}\n"
                f"Borrower: {user.name} (ID: {user.user_id})\n"
                f"Due Date: {due_date} (Overdue by {overdue_days} day(s))\n"
                f"ISBN: {book.isbn}\n\n")
    
    def show_most_borrowed(self):
        top_n = simpledialog.askinteger(
            "Top N Books",
            "Enter number of books to display:",
            parent=self,
            minvalue=1,
            initialvalue=5
        )
        
        if not top_n:
            return
        
        most_borrowed = self.lms.get_most_borrowed_books(top_n)
        self.report_text.delete(1.0, tk.END)
        
        self.report_text.insert(tk.END, f"=== Top {top_n} Most Borrowed Books ===\n\n")
        
        for i, (book, count) in enumerate(most_borrowed, 1):
            self.report_text.insert(tk.END, 
                f"{i}. {book.title} by {book.author}\n"
                f"   ISBN: {book.isbn}\n"
                f"   Borrowed {count} time(s)\n"
                f"   Available: {book.available}/{book.quantity}\n\n")

if __name__ == "__main__":
    app = LibraryApp()
    app.mainloop()
    