import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from datetime import datetime
import math

class FarmersMarketplace:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🌾 Farmers Marketplace - Uganda")
        self.root.geometry("1000x700")
        self.root.configure(bg="#f0f8f0")
        self.root.resizable(True, True)
        
        # Shopping cart
        self.cart = {}
        
        # Sample farmers products database
        self.products = {
            "Tomatoes": {"price": 3500, "farmer": "John Mukasa", "unit": "kg"},
            "Onions": {"price": 2800, "farmer": "Mary Nakato", "unit": "kg"},
            "Irish Potatoes": {"price": 2200, "farmer": "Peter Ssemakula", "unit": "kg"},
            "Sweet Potatoes": {"price": 1800, "farmer": "Grace Nansubuga", "unit": "kg"},
            "Bananas": {"price": 1500, "farmer": "David Kiwanuka", "unit": "bunch"},
            "Matooke": {"price": 2000, "farmer": "Sarah Nalubega", "unit": "bunch"},
            "Cabbage": {"price": 1200, "farmer": "James Wasswa", "unit": "head"},
            "Carrots": {"price": 4000, "farmer": "Rose Nakirijja", "unit": "kg"},
            "Beans": {"price": 6500, "farmer": "Moses Bbosa", "unit": "kg"},
            "Groundnuts": {"price": 8000, "farmer": "Agnes Nakabugo", "unit": "kg"},
            "Maize": {"price": 2500, "farmer": "Francis Lugoba", "unit": "kg"},
            "Rice": {"price": 4500, "farmer": "Betty Namukasa", "unit": "kg"},
            "Pineapples": {"price": 3000, "farmer": "Robert Kiprotich", "unit": "piece"},
            "Mangoes": {"price": 2500, "farmer": "Jane Akello", "unit": "kg"},
            "Avocados": {"price": 5000, "farmer": "Paul Ocitti", "unit": "kg"},
            "Green Peppers": {"price": 6000, "farmer": "Lucy Atim", "unit": "kg"},
            "Eggplants": {"price": 3500, "farmer": "Samuel Opio", "unit": "kg"},
            "Okra": {"price": 4500, "farmer": "Margaret Acan", "unit": "kg"},
            "Spinach": {"price": 2000, "farmer": "George Akena", "unit": "bunch"},
            "Lettuce": {"price": 1500, "farmer": "Catherine Aber", "unit": "head"}
        }
        
        self.filtered_products = self.products.copy()
        self.setup_ui()
        
    def setup_ui(self):
        # Main title
        title_frame = tk.Frame(self.root, bg="#2e7d32", height=80)
        title_frame.pack(fill="x", pady=(0, 10))
        title_frame.pack_propagate(False)
        
        title_label = tk.Label(
            title_frame,
            text="🌾 FARMERS MARKETPLACE UGANDA 🇺🇬",
            font=("Arial", 20, "bold"),
            bg="#2e7d32",
            fg="white"
        )
        title_label.pack(expand=True)
        
        subtitle_label = tk.Label(
            title_frame,
            text="Fresh Farm Products Direct from Ugandan Farmers",
            font=("Arial", 12),
            bg="#2e7d32",
            fg="#e8f5e8"
        )
        subtitle_label.pack()
        
        # Main container
        main_container = tk.Frame(self.root, bg="#f0f8f0")
        main_container.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Left panel - Products
        left_panel = tk.Frame(main_container, bg="white", relief="solid", bd=1)
        left_panel.pack(side="left", fill="both", expand=True, padx=(0, 10))
        
        # Search section
        search_frame = tk.Frame(left_panel, bg="white")
        search_frame.pack(fill="x", padx=15, pady=15)
        
        search_label = tk.Label(
            search_frame,
            text="🔍 Search Products:",
            font=("Arial", 12, "bold"),
            bg="white"
        )
        search_label.pack(anchor="w")
        
        self.search_var = tk.StringVar()
        self.search_var.trace('w', self.filter_products)
        
        search_entry = tk.Entry(
            search_frame,
            textvariable=self.search_var,
            font=("Arial", 11),
            width=40
        )
        search_entry.pack(fill="x", pady=(5, 10))
        
        # Products display
        products_label = tk.Label(
            left_panel,
            text="🥬 Available Products:",
            font=("Arial", 14, "bold"),
            bg="white",
            fg="#2e7d32"
        )
        products_label.pack(anchor="w", padx=15)
        
        # Products frame with scrollbar
        products_container = tk.Frame(left_panel, bg="white")
        products_container.pack(fill="both", expand=True, padx=15, pady=(10, 15))
        
        canvas = tk.Canvas(products_container, bg="white")
        scrollbar = ttk.Scrollbar(products_container, orient="vertical", command=canvas.yview)
        self.products_frame = tk.Frame(canvas, bg="white")
        
        self.products_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=self.products_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Right panel - Cart
        right_panel = tk.Frame(main_container, bg="white", relief="solid", bd=1, width=300)
        right_panel.pack(side="right", fill="y")
        right_panel.pack_propagate(False)
        
        # Cart header
        cart_header = tk.Frame(right_panel, bg="#4caf50", height=60)
        cart_header.pack(fill="x")
        cart_header.pack_propagate(False)
        
        cart_title = tk.Label(
            cart_header,
            text="🛒 Shopping Cart",
            font=("Arial", 14, "bold"),
            bg="#4caf50",
            fg="white"
        )
        cart_title.pack(expand=True)
        
        # Cart items
        cart_container = tk.Frame(right_panel, bg="white")
        cart_container.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.cart_display = scrolledtext.ScrolledText(
            cart_container,
            height=15,
            font=("Arial", 9),
            bg="#f9f9f9",
            state="disabled"
        )
        self.cart_display.pack(fill="both", expand=True)
        
        # Cart total
        self.total_label = tk.Label(
            right_panel,
            text="Total: UGX 0",
            font=("Arial", 12, "bold"),
            bg="white",
            fg="#2e7d32"
        )
        self.total_label.pack(pady=10)
        
        # Cart buttons
        buttons_frame = tk.Frame(right_panel, bg="white")
        buttons_frame.pack(fill="x", padx=10, pady=(0, 15))
        
        checkout_btn = tk.Button(
            buttons_frame,
            text="💳 Checkout",
            command=self.checkout,
            font=("Arial", 11, "bold"),
            bg="#ff9800",
            fg="white",
            height=2,
            cursor="hand2"
        )
        checkout_btn.pack(fill="x", pady=(0, 5))
        
        clear_cart_btn = tk.Button(
            buttons_frame,
            text="🗑️ Clear Cart",
            command=self.clear_cart,
            font=("Arial", 10),
            bg="#f44336",
            fg="white",
            cursor="hand2"
        )
        clear_cart_btn.pack(fill="x")
        
        # Load products
        self.display_products()
        
    def display_products(self):
        # Clear existing products
        for widget in self.products_frame.winfo_children():
            widget.destroy()
            
        row = 0
        for product_name, product_info in self.filtered_products.items():
            # Product card
            card_frame = tk.Frame(
                self.products_frame,
                bg="#f8f9fa",
                relief="solid",
                bd=1
            )
            card_frame.pack(fill="x", pady=5, padx=5)
            
            # Product info
            info_frame = tk.Frame(card_frame, bg="#f8f9fa")
            info_frame.pack(side="left", fill="both", expand=True, padx=10, pady=8)
            
            name_label = tk.Label(
                info_frame,
                text=f"🥕 {product_name}",
                font=("Arial", 11, "bold"),
                bg="#f8f9fa",
                anchor="w"
            )
            name_label.pack(anchor="w")
            
            farmer_label = tk.Label(
                info_frame,
                text=f"👨‍🌾 {product_info['farmer']}",
                font=("Arial", 9),
                bg="#f8f9fa",
                fg="#666",
                anchor="w"
            )
            farmer_label.pack(anchor="w")
            
            price_label = tk.Label(
                info_frame,
                text=f"💰 UGX {product_info['price']:,} per {product_info['unit']}",
                font=("Arial", 10, "bold"),
                bg="#f8f9fa",
                fg="#2e7d32",
                anchor="w"
            )
            price_label.pack(anchor="w")
            
            # Add to cart section
            cart_frame = tk.Frame(card_frame, bg="#f8f9fa")
            cart_frame.pack(side="right", padx=10, pady=8)
            
            qty_label = tk.Label(
                cart_frame,
                text="Qty:",
                font=("Arial", 9),
                bg="#f8f9fa"
            )
            qty_label.pack(side="left")
            
            qty_spinbox = tk.Spinbox(
                cart_frame,
                from_=1,
                to=50,
                width=5,
                font=("Arial", 9),
                value=1
            )
            qty_spinbox.pack(side="left", padx=(5, 10))
            
            add_btn = tk.Button(
                cart_frame,
                text="+ Add",
                command=lambda p=product_name, q=qty_spinbox: self.add_to_cart(p, q),
                font=("Arial", 9, "bold"),
                bg="#4caf50",
                fg="white",
                cursor="hand2",
                width=8
            )
            add_btn.pack(side="left")
            
            row += 1
            
    def filter_products(self, *args):
        search_term = self.search_var.get().lower()
        if search_term:
            self.filtered_products = {
                name: info for name, info in self.products.items()
                if search_term in name.lower() or search_term in info['farmer'].lower()
            }
        else:
            self.filtered_products = self.products.copy()
        self.display_products()
        
    def add_to_cart(self, product_name, qty_spinbox):
        try:
            quantity = int(qty_spinbox.get())
            if quantity <= 0:
                messagebox.showerror("Error", "Quantity must be greater than 0!")
                return
                
            if product_name in self.cart:
                self.cart[product_name]['quantity'] += quantity
            else:
                self.cart[product_name] = {
                    'quantity': quantity,
                    'price': self.products[product_name]['price'],
                    'unit': self.products[product_name]['unit'],
                    'farmer': self.products[product_name]['farmer']
                }
            
            self.update_cart_display()
            messagebox.showinfo("Added!", f"Added {quantity} {self.products[product_name]['unit']} of {product_name} to cart!")
            
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid quantity!")
            
    def update_cart_display(self):
        self.cart_display.config(state="normal")
        self.cart_display.delete(1.0, tk.END)
        
        total = 0
        for product, details in self.cart.items():
            item_total = details['quantity'] * details['price']
            total += item_total
            
            cart_text = f"🥕 {product}\n"
            cart_text += f"   👨‍🌾 {details['farmer']}\n"
            cart_text += f"   📦 {details['quantity']} {details['unit']}\n"
            cart_text += f"   💰 UGX {item_total:,}\n"
            cart_text += "   " + "─" * 25 + "\n\n"
            
            self.cart_display.insert(tk.END, cart_text)
            
        self.cart_display.config(state="disabled")
        self.total_label.config(text=f"Total: UGX {total:,}")
        
    def clear_cart(self):
        if self.cart:
            if messagebox.askyesno("Confirm", "Are you sure you want to clear the cart?"):
                self.cart.clear()
                self.update_cart_display()
        else:
            messagebox.showinfo("Info", "Cart is already empty!")
            
    def checkout(self):
        if not self.cart:
            messagebox.showwarning("Warning", "Your cart is empty!")
            return
            
        # Generate receipt
        self.generate_receipt()
        
    def generate_receipt(self):
        receipt_window = tk.Toplevel(self.root)
        receipt_window.title("🧾 Purchase Receipt")
        receipt_window.geometry("500x600")
        receipt_window.configure(bg="white")
        receipt_window.resizable(False, False)
        
        # Receipt header
        header_frame = tk.Frame(receipt_window, bg="#2e7d32", height=80)
        header_frame.pack(fill="x")
        header_frame.pack_propagate(False)
        
        receipt_title = tk.Label(
            header_frame,
            text="🧾 PURCHASE RECEIPT",
            font=("Arial", 16, "bold"),
            bg="#2e7d32",
            fg="white"
        )
        receipt_title.pack(expand=True)
        
        # Receipt content
        content_frame = tk.Frame(receipt_window, bg="white")
        content_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Store info
        store_info = f"""
🌾 FARMERS MARKETPLACE UGANDA
📍 Kampala, Central Region
📞 +256-700-123456
📧 info@farmersmarketplace.ug

Receipt #: FM{datetime.now().strftime('%Y%m%d%H%M%S')}
Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
{'═' * 45}
"""
        
        info_label = tk.Label(
            content_frame,
            text=store_info,
            font=("Courier", 10),
            bg="white",
            anchor="w",
            justify="left"
        )
        info_label.pack(anchor="w")
        
        # Items
        items_text = "ITEMS PURCHASED:\n" + "─" * 45 + "\n"
        total = 0
        
        for product, details in self.cart.items():
            item_total = details['quantity'] * details['price']
            total += item_total
            
            items_text += f"{product}\n"
            items_text += f"  Farmer: {details['farmer']}\n"
            items_text += f"  Qty: {details['quantity']} {details['unit']} @ UGX {details['price']:,}\n"
            items_text += f"  Subtotal: UGX {item_total:,}\n\n"
            
        items_text += "═" * 45 + "\n"
        items_text += f"TOTAL: UGX {total:,}\n"
        items_text += "═" * 45 + "\n\n"
        items_text += "Thank you for supporting local farmers!\n"
        items_text += "🌾 Fresh • Local • Sustainable 🌾"
        
        receipt_text = scrolledtext.ScrolledText(
            content_frame,
            font=("Courier", 9),
            bg="#f9f9f9",
            height=20,
            state="normal"
        )
        receipt_text.pack(fill="both", expand=True)
        receipt_text.insert(tk.END, items_text)
        receipt_text.config(state="disabled")
        
        # Buttons
        buttons_frame = tk.Frame(receipt_window, bg="white")
        buttons_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        new_order_btn = tk.Button(
            buttons_frame,
            text="🛒 New Order",
            command=lambda: self.new_order(receipt_window),
            font=("Arial", 11, "bold"),
            bg="#4caf50",
            fg="white",
            cursor="hand2"
        )
        new_order_btn.pack(side="left", padx=(0, 10))
        
        close_btn = tk.Button(
            buttons_frame,
            text="❌ Close",
            command=receipt_window.destroy,
            font=("Arial", 11),
            bg="#666",
            fg="white",
            cursor="hand2"
        )
        close_btn.pack(side="left")
        
    def new_order(self, receipt_window):
        self.cart.clear()
        self.update_cart_display()
        receipt_window.destroy()
        messagebox.showinfo("Success", "Ready for new order! Cart has been cleared.")
        
    def run(self):
        self.root.mainloop()

# Run the application
if __name__ == "__main__":
    app = FarmersMarketplace()
    app.run()