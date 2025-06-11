import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3
import datetime

# --- DATABASE SETUP ---
conn = sqlite3.connect('seilinshop.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT, password TEXT)''')
c.execute('''CREATE TABLE IF NOT EXISTS products (id INTEGER PRIMARY KEY, name TEXT, price INTEGER, stock INTEGER)''')
c.execute('''CREATE TABLE IF NOT EXISTS transactions (id INTEGER PRIMARY KEY, username TEXT, product_name TEXT, quantity INTEGER, total INTEGER, date TEXT)''')
conn.commit()

# --- COLORS AND STYLES ---
BG_COLOR = "#e6d6f2"  # ungu pastel
SECOND_BG = "#f2f2f2"  # abu muda
FONT = ("Verdana", 10)
TITLE_FONT = ("Verdana", 16, "bold")
BUTTON_STYLE = {'bg': SECOND_BG, 'font': FONT, 'padx': 10, 'pady': 5}
ENTRY_STYLE = {'font': FONT, 'bd': 2, 'relief': tk.GROOVE}

# --- MAIN APP CLASS ---
class SeilinShopApp:
    def __init__(self, master):
        self.master = master
        self.master.title("SeilinShop - Toko Laptop")
        self.master.configure(bg=BG_COLOR)
        self.style = ttk.Style()
        self.style.configure('Treeview', font=FONT, rowheight=25)
        self.style.configure('Treeview.Heading', font=('Verdana', 10, 'bold'))
        self.login_screen()

    def set_style(self):
        self.master.configure(bg=BG_COLOR)

    def create_frame(self, title=None):
        frame = tk.Frame(self.master, bg=BG_COLOR, padx=20, pady=20)
        frame.pack(expand=True, fill=tk.BOTH)
        
        if title:
            title_label = tk.Label(frame, text=title, font=TITLE_FONT, bg=BG_COLOR, fg="black")
            title_label.pack(pady=(0, 20))
            
        return frame

    def login_screen(self):
        self.clear()
        self.set_style()
        frame = self.create_frame("Login")
        
        # Username Section
        user_frame = tk.Frame(frame, bg=BG_COLOR)
        user_frame.pack(pady=5)
        tk.Label(user_frame, text="Username", font=FONT, bg=BG_COLOR, fg="black", width=10).pack(side=tk.LEFT)
        self.username_entry = tk.Entry(user_frame, **ENTRY_STYLE)
        self.username_entry.pack(side=tk.LEFT, padx=5)
        
        # Password Section
        pass_frame = tk.Frame(frame, bg=BG_COLOR)
        pass_frame.pack(pady=5)
        tk.Label(pass_frame, text="Password", font=FONT, bg=BG_COLOR, fg="black", width=10).pack(side=tk.LEFT)
        self.password_entry = tk.Entry(pass_frame, show="*", **ENTRY_STYLE)
        self.password_entry.pack(side=tk.LEFT, padx=5)
        
        # Button Section
        button_frame = tk.Frame(frame, bg=BG_COLOR)
        button_frame.pack(pady=20)
        tk.Button(button_frame, text="Login", command=self.login, **BUTTON_STYLE).pack(side=tk.LEFT, padx=10)
        tk.Button(button_frame, text="Register", command=self.register_screen, **BUTTON_STYLE).pack(side=tk.LEFT, padx=10)

    def register_screen(self):
        self.clear()
        self.set_style()
        frame = self.create_frame("Register")
        
        # Username Section
        user_frame = tk.Frame(frame, bg=BG_COLOR)
        user_frame.pack(pady=10)
        tk.Label(user_frame, text="Username", font=FONT, bg=BG_COLOR, fg="black", width=15).pack(side=tk.LEFT)
        self.reg_username = tk.Entry(user_frame, **ENTRY_STYLE)
        self.reg_username.pack(side=tk.LEFT, padx=5)
        
        # Password Section
        pass_frame = tk.Frame(frame, bg=BG_COLOR)
        pass_frame.pack(pady=10)
        tk.Label(pass_frame, text="Password", font=FONT, bg=BG_COLOR, fg="black", width=15).pack(side=tk.LEFT)
        self.reg_password = tk.Entry(pass_frame, show="*", **ENTRY_STYLE)
        self.reg_password.pack(side=tk.LEFT, padx=5)
        
        # Button Section
        button_frame = tk.Frame(frame, bg=BG_COLOR)
        button_frame.pack(pady=20)
        tk.Button(button_frame, text="Submit", command=self.register, **BUTTON_STYLE).pack(side=tk.LEFT, padx=10)
        tk.Button(button_frame, text="Back to Login", command=self.login_screen, **BUTTON_STYLE).pack(side=tk.LEFT, padx=10)

    def main_menu(self):
        self.clear()
        self.set_style()
        frame = self.create_frame(f"Welcome {self.current_user}")
        
        # Menu Buttons
        buttons = [
            ("Kelola Produk", self.manage_products),
            ("Transaksi", self.transaction_screen),
            ("Logout", self.login_screen)
        ]
        
        for text, command in buttons:
            tk.Button(frame, text=text, width=25, command=command, **BUTTON_STYLE).pack(pady=10)

    def manage_products(self):
        self.clear()
        self.set_style()
        frame = self.create_frame("Kelola Produk Laptop")
        
        # Treeview for products
        tree_frame = tk.Frame(frame, bg=BG_COLOR)
        tree_frame.pack(pady=10)
        
        scroll_y = tk.Scrollbar(tree_frame, orient=tk.VERTICAL)
        scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.prod_tree = ttk.Treeview(tree_frame, columns=("Nama", "Harga", "Stok"), 
                                     show='headings', height=8, yscrollcommand=scroll_y.set)
        self.prod_tree.heading("Nama", text="Nama Produk")
        self.prod_tree.heading("Harga", text="Harga (Rp)")
        self.prod_tree.heading("Stok", text="Stok")
        self.prod_tree.column("Nama", width=200)
        self.prod_tree.column("Harga", width=150, anchor=tk.CENTER)
        self.prod_tree.column("Stok", width=100, anchor=tk.CENTER)
        self.prod_tree.pack()
        scroll_y.config(command=self.prod_tree.yview)
        
        self.load_products()
        
        # Form Frame
        form_frame = tk.Frame(frame, bg=BG_COLOR)
        form_frame.pack(pady=10)
        
        labels = ["Nama Produk:", "Harga (Rp):", "Stok:"]
        entries = []
        
        for i, label in enumerate(labels):
            tk.Label(form_frame, text=label, font=FONT, bg=BG_COLOR, fg="black").grid(row=i, column=0, sticky=tk.E, padx=5, pady=5)
            entry = tk.Entry(form_frame, **ENTRY_STYLE)
            entry.grid(row=i, column=1, padx=5, pady=5)
            entries.append(entry)
            
        self.name_entry, self.price_entry, self.stock_entry = entries
        
        # Button Frame
        button_frame = tk.Frame(frame, bg=BG_COLOR)
        button_frame.pack(pady=10)
        
        buttons = [
            ("Tambah", self.add_product),
            ("Ubah", self.update_product),
            ("Hapus", self.delete_product),
            ("Cari Produk", self.search_product),
            ("Kembali", self.main_menu)
        ]
        
        for i, (text, command) in enumerate(buttons):
            tk.Button(button_frame, text=text, command=command, **BUTTON_STYLE).grid(row=0, column=i, padx=5)

    def transaction_screen(self):
        self.clear()
        self.set_style()
        frame = self.create_frame("Transaksi Pembelian")
        
        # Product Info
        product_frame = tk.Frame(frame, bg=BG_COLOR)
        product_frame.pack(pady=10)
        
        tk.Label(product_frame, text="Nama Produk", font=FONT, bg=BG_COLOR, fg="black", width=15).pack(side=tk.LEFT)
        self.trans_product = tk.Entry(product_frame, **ENTRY_STYLE)
        self.trans_product.pack(side=tk.LEFT, padx=5)
        
        # Quantity Info
        qty_frame = tk.Frame(frame, bg=BG_COLOR)
        qty_frame.pack(pady=10)
        
        tk.Label(qty_frame, text="Jumlah", font=FONT, bg=BG_COLOR, fg="black", width=15).pack(side=tk.LEFT)
        self.trans_qty = tk.Entry(qty_frame, **ENTRY_STYLE)
        self.trans_qty.pack(side=tk.LEFT, padx=5)
        
        # Button Frame
        button_frame = tk.Frame(frame, bg=BG_COLOR)
        button_frame.pack(pady=20)
        
        tk.Button(button_frame, text="Beli", command=self.buy_product, **BUTTON_STYLE).pack(side=tk.LEFT, padx=10)
        tk.Button(button_frame, text="Kembali", command=self.main_menu, **BUTTON_STYLE).pack(side=tk.LEFT, padx=10)

    def buy_product(self):
        name = self.trans_product.get()
        qty = self.trans_qty.get()
        
        if not name or not qty:
            messagebox.showerror("Error", "Harap isi semua field!")
            return
            
        try:
            qty = int(qty)
            if qty <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Jumlah harus angka positif!")
            return
            
        c.execute("SELECT price, stock FROM products WHERE name=?", (name,))
        result = c.fetchone()
        
        if result:
            price, stock = result
            if qty <= stock:
                total = price * qty
                date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                c.execute("INSERT INTO transactions (username, product_name, quantity, total, date) VALUES (?, ?, ?, ?, ?)",
                          (self.current_user, name, qty, total, date))
                c.execute("UPDATE products SET stock=stock-? WHERE name=?", (qty, name))
                conn.commit()
                
                receipt = f"=== STRUK PEMBELIAN ===\n"
                receipt += f"Produk: {name}\n"
                receipt += f"Jumlah: {qty}\n"
                receipt += f"Harga Satuan: Rp{price:,}\n"
                receipt += f"Total: Rp{total:,}\n"
                receipt += f"Tanggal: {date}\n"
                receipt += f"Kasir: {self.current_user}\n"
                receipt += "===================="
                
                messagebox.showinfo("Berhasil", receipt)
            else:
                messagebox.showerror("Gagal", f"Stok tidak mencukupi. Stok tersedia: {stock}")
        else:
            messagebox.showerror("Gagal", "Produk tidak ditemukan")

    def load_products(self):
        for i in self.prod_tree.get_children():
            self.prod_tree.delete(i)
        for row in c.execute("SELECT name, price, stock FROM products"):
            self.prod_tree.insert("", "end", values=row)

    def add_product(self):
        try:
            name = self.name_entry.get()
            price = int(self.price_entry.get())
            stock = int(self.stock_entry.get())
            
            if not name or price <= 0 or stock < 0:
                raise ValueError
                
            c.execute("INSERT INTO products (name, price, stock) VALUES (?, ?, ?)", (name, price, stock))
            conn.commit()
            self.load_products()
            self.name_entry.delete(0, tk.END)
            self.price_entry.delete(0, tk.END)
            self.stock_entry.delete(0, tk.END)
        except ValueError:
            messagebox.showerror("Error", "Harap isi data dengan benar!\nHarga harus > 0\nStok tidak boleh negatif")

    def update_product(self):
        selected = self.prod_tree.focus()
        if not selected:
            messagebox.showerror("Error", "Pilih produk terlebih dahulu!")
            return
            
        try:
            values = self.prod_tree.item(selected, 'values')
            new_name = self.name_entry.get()
            new_price = int(self.price_entry.get())
            new_stock = int(self.stock_entry.get())
            
            if not new_name or new_price <= 0 or new_stock < 0:
                raise ValueError
                
            c.execute("UPDATE products SET name=?, price=?, stock=? WHERE name=?", 
                      (new_name, new_price, new_stock, values[0]))
            conn.commit()
            self.load_products()
        except ValueError:
            messagebox.showerror("Error", "Harap isi data dengan benar!\nHarga harus > 0\nStok tidak boleh negatif")

    def delete_product(self):
        selected = self.prod_tree.focus()
        if not selected:
            messagebox.showerror("Error", "Pilih produk terlebih dahulu!")
            return
            
        if messagebox.askyesno("Konfirmasi", "Apakah Anda yakin ingin menghapus produk ini?"):
            values = self.prod_tree.item(selected, 'values')
            c.execute("DELETE FROM products WHERE name=?", (values[0],))
            conn.commit()
            self.load_products()

    def search_product(self):
        keyword = self.name_entry.get()
        for i in self.prod_tree.get_children():
            self.prod_tree.delete(i)
        for row in c.execute("SELECT name, price, stock FROM products WHERE name LIKE ?", (f"%{keyword}%",)):
            self.prod_tree.insert("", "end", values=row)

    def login(self):
        user = self.username_entry.get()
        pwd = self.password_entry.get()
        
        if not user or not pwd:
            messagebox.showerror("Error", "Harap isi username dan password!")
            return
            
        c.execute("SELECT * FROM users WHERE username=? AND password=?", (user, pwd))
        if c.fetchone():
            self.current_user = user
            self.main_menu()
        else:
            messagebox.showerror("Gagal", "Username atau password salah")

    def register(self):
        user = self.reg_username.get()
        pwd = self.reg_password.get()
        
        if not user or not pwd:
            messagebox.showerror("Error", "Harap isi username dan password!")
            return
            
        c.execute("SELECT * FROM users WHERE username=?", (user,))
        if c.fetchone():
            messagebox.showerror("Error", "Username sudah terdaftar!")
        else:
            c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (user, pwd))
            conn.commit()
            messagebox.showinfo("Sukses", "Registrasi berhasil")
            self.login_screen()

    def clear(self):
        for widget in self.master.winfo_children():
            widget.destroy()

# --- MAIN LOOP ---
if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("800x600")
    app = SeilinShopApp(root)
    root.mainloop()