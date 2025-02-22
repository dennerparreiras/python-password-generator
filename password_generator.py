import random
import string
import sys
import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.font import Font
import os

class PasswordGeneratorGUI:
    def __init__(self, root):
        """Initialize the GUI window and components"""
        self.root = root
        self.root.title("Password Generator by @dennerparreiras")
        self.root.geometry("500x600")
        self.root.configure(bg='#f0f0f0')
        self.root.resizable(False, False)
        
        # Set window icon if available
        try:
            # Try to load from current directory first
            if os.path.exists("password_icon.ico"):
                self.root.iconbitmap("password_icon.ico")
            else:
                # If running as executable, try to load from temporary directory
                import sys
                if getattr(sys, 'frozen', False):
                    base_path = sys._MEIPASS
                    icon_path = os.path.join(base_path, "password_icon.ico")
                    if os.path.exists(icon_path):
                        self.root.iconbitmap(icon_path)
                    else:
                        print(f"Icon not found in {icon_path}")
                else:
                    print("Icon not found in current directory")
        except Exception as e:
            print(f"Could not load window icon: {str(e)}")
        
        # Styles
        style = ttk.Style()
        style.configure('Title.TLabel', font=('Helvetica', 16, 'bold'), padding=10)
        style.configure('Section.TLabel', font=('Helvetica', 11, 'bold'), padding=5)
        style.configure('Custom.TEntry', padding=5)
        style.configure('Custom.TCheckbutton', font=('Helvetica', 10))
        style.configure('Generate.TButton', font=('Helvetica', 11, 'bold'), padding=10)
        style.configure('Credits.TLabel', font=('Helvetica', 9))
        
        # Create main frame with padding
        main_frame = ttk.Frame(root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Title
        ttk.Label(
            main_frame, 
            text="Password Generator", 
            style='Title.TLabel'
        ).grid(row=0, column=0, columnspan=2, sticky=tk.W, pady=(0,20))
        
        # Password length section
        ttk.Label(
            main_frame, 
            text="Password Length:", 
            style='Section.TLabel'
        ).grid(row=1, column=0, sticky=tk.W, pady=5)
        
        self.length_var = tk.StringVar(value="16")
        self.length_entry = ttk.Entry(
            main_frame, 
            textvariable=self.length_var, 
            width=10, 
            style='Custom.TEntry'
        )
        self.length_entry.grid(row=1, column=1, sticky=tk.W, pady=5)
        
        # Character types section
        ttk.Label(
            main_frame, 
            text="Character Types:", 
            style='Section.TLabel'
        ).grid(row=2, column=0, columnspan=2, sticky=tk.W, pady=(20,10))
        
        # Create frames for each character type
        self.create_character_type_section(main_frame, 3, "Uppercase Letters", string.ascii_uppercase)
        self.create_character_type_section(main_frame, 4, "Lowercase Letters", string.ascii_lowercase)
        self.create_character_type_section(main_frame, 5, "Numbers", "0123456789")
        self.create_character_type_section(main_frame, 6, "Special Characters", "!@#$%^&*()_+-=[]{}|;:,.<>?")
        
        # Generated password section
        ttk.Label(
            main_frame, 
            text="Generated Password:", 
            style='Section.TLabel'
        ).grid(row=7, column=0, columnspan=2, sticky=tk.W, pady=(20,5))
        
        self.password_var = tk.StringVar()
        self.password_entry = ttk.Entry(
            main_frame, 
            textvariable=self.password_var, 
            width=40, 
            style='Custom.TEntry',
            font=('Courier', 12)
        )
        self.password_entry.grid(row=8, column=0, columnspan=2, sticky=tk.W+tk.E, pady=5)
        
        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=9, column=0, columnspan=2, pady=20)
        
        ttk.Button(
            button_frame, 
            text="Generate Password", 
            command=self.generate_password,
            style='Generate.TButton'
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            button_frame, 
            text="Copy", 
            command=self.copy_password,
            style='Generate.TButton'
        ).pack(side=tk.LEFT, padx=5)
        
        # Credits section
        credits_frame = ttk.Frame(main_frame)
        credits_frame.grid(row=10, column=0, columnspan=2, pady=(20,0))
        
        # Developer credit
        ttk.Label(
            credits_frame,
            text="Developed by ",
            style='Credits.TLabel'
        ).pack(side=tk.LEFT)
        
        # Create clickable link style
        link_font = Font(family='Helvetica', size=9, underline=True)
        
        # Developer link
        developer_link = tk.Label(
            credits_frame,
            text="@dennerparreiras",
            fg='blue',
            cursor='hand2',
            font=link_font
        )
        developer_link.pack(side=tk.LEFT)
        developer_link.bind('<Button-1>', lambda e: self.open_link("https://github.com/dennerparreiras"))
        
        # GitHub project section
        github_frame = ttk.Frame(main_frame)
        github_frame.grid(row=11, column=0, columnspan=2, pady=(5,10))
        
        github_link = tk.Label(
            github_frame,
            text="View project on GitHub",
            fg='blue',
            cursor='hand2',
            font=link_font
        )
        github_link.pack(side=tk.BOTTOM)
        github_link.bind('<Button-1>', lambda e: self.open_link("https://github.com/dennerparreiras/python-password-generator"))

    def create_character_type_section(self, parent, row, label, default_chars):
        """Create a section for each character type with checkbox and entry"""
        frame = ttk.Frame(parent)
        frame.grid(row=row, column=0, columnspan=2, sticky=tk.W+tk.E, pady=5)
        
        # Create and store checkbox variable
        checkbox_var = tk.BooleanVar(value=True)
        setattr(self, f"use_{label.lower().replace(' ', '_')}", checkbox_var)
        
        # Create and store characters variable
        chars_var = tk.StringVar(value=default_chars)
        setattr(self, f"chars_{label.lower().replace(' ', '_')}", chars_var)
        
        # Create checkbox
        ttk.Checkbutton(
            frame, 
            text=label,
            variable=checkbox_var,
            style='Custom.TCheckbutton'
        ).pack(side=tk.LEFT, padx=(0,10))
        
        # Create entry
        ttk.Entry(
            frame,
            textvariable=chars_var,
            width=40,
            style='Custom.TEntry'
        ).pack(side=tk.LEFT, fill=tk.X, expand=True)

    def generate_password(self):
        """Generate password based on GUI settings"""
        try:
            length = int(self.length_var.get())
            if length < 1:
                raise ValueError("Password length must be at least 1")
            
            # Get all character type settings
            char_types = [
                ('uppercase_letters', self.use_uppercase_letters, self.chars_uppercase_letters),
                ('lowercase_letters', self.use_lowercase_letters, self.chars_lowercase_letters),
                ('numbers', self.use_numbers, self.chars_numbers),
                ('special_characters', self.use_special_characters, self.chars_special_characters)
            ]
            
            # Check if at least one type is selected
            if not any(type_var.get() for _, type_var, _ in char_types):
                raise ValueError("Please select at least one character type")
            
            # Build character set
            chars = ''
            for _, type_var, chars_var in char_types:
                if type_var.get():
                    chars += chars_var.get()
            
            # Generate and validate password
            while True:
                password = ''.join(random.choice(chars) for _ in range(length))
                
                # Verify that password contains at least one character from each selected type
                valid = True
                for _, type_var, chars_var in char_types:
                    if type_var.get():
                        if not any(c in chars_var.get() for c in password):
                            valid = False
                            break
                
                if valid:
                    break
            
            self.password_var.set(password)
            
        except ValueError as e:
            messagebox.showerror("Error", str(e))
    
    def copy_password(self):
        """Copy generated password to clipboard"""
        password = self.password_var.get()
        if password:
            self.root.clipboard_clear()
            self.root.clipboard_append(password)
            messagebox.showinfo("Success", "Password copied to clipboard!")
        else:
            messagebox.showwarning("Warning", "No password generated to copy!")

    def open_link(self, url):
        """Open URL in default web browser"""
        import webbrowser
        webbrowser.open_new(url)

def main():
    root = tk.Tk()
    app = PasswordGeneratorGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main() 