import tkinter as tk
from tkinter import font as tkfont
from math import sqrt, factorial, log10, log, sin, cos, tan, radians

class Calculator(tk.Tk):
    def __init__(self):
        super().__init__()
        
        self.title(" Abdo Calculator")
        self.geometry("400x600")
        self.minsize(300, 500)
        self.configure(bg="#f0f0f0")
        
        # Custom font
        self.default_font = tkfont.Font(family="Arial", size=12)
        self.large_font = tkfont.Font(family="Arial", size=20)
        
        # Variables
        self.current_input = tk.StringVar(value="0")
        self.history = tk.StringVar(value="")
        self.operation = None
        self.stored_value = None
        self.reset_input = False
        self.scientific_mode = False
        
        self.create_widgets()
        self.bind_events()
        
    def create_widgets(self):
        # Configure grid
        self.grid_columnconfigure(0, weight=1)
        for i in range(6):
            self.grid_rowconfigure(i, weight=1)
        
        # History display
        self.history_label = tk.Label(
            self, textvariable=self.history, 
            font=self.default_font, anchor="e", 
            bg="#f0f0f0", fg="#666", padx=10
        )
        self.history_label.grid(row=0, column=0, columnspan=4, sticky="nsew")
        
        # Main display
        self.display = tk.Label(
            self, textvariable=self.current_input, 
            font=self.large_font, anchor="e", 
            bg="#f0f0f0", fg="#000", padx=10, pady=20
        )
        self.display.grid(row=1, column=0, columnspan=4, sticky="nsew")
        
        # Button layout
        buttons = [
            ('C', 2, 0), ('±', 2, 1), ('%', 2, 2), ('/', 2, 3),
            ('7', 3, 0), ('8', 3, 1), ('9', 3, 2), ('*', 3, 3),
            ('4', 4, 0), ('5', 4, 1), ('6', 4, 2), ('-', 4, 3),
            ('1', 5, 0), ('2', 5, 1), ('3', 5, 2), ('+', 5, 3),
            ('0', 6, 0), ('.', 6, 1), ('=', 6, 2), ('Sci', 6, 3)
        ]
        
        # Scientific buttons (hidden by default)
        self.sci_buttons = [
            ('√', 2, 4), ('x²', 2, 5), ('x³', 2, 6), ('^', 2, 7),
            ('sin', 3, 4), ('cos', 3, 5), ('tan', 3, 6), ('log', 3, 7),
            ('ln', 4, 4), ('n!', 4, 5), ('π', 4, 6), ('e', 4, 7),
            ('(', 5, 4), (')', 5, 5), ('DEL', 5, 6), ('AC', 5, 7)
        ]
        
        # Create buttons
        self.button_dict = {}
        
        for (text, row, col) in buttons:
            btn = self.create_button(text)
            btn.grid(row=row, column=col, sticky="nsew", padx=1, pady=1)
            self.button_dict[(row, col)] = btn
            
        # Initially hide scientific buttons
        self.sci_button_dict = {}
        for (text, row, col) in self.sci_buttons:
            btn = self.create_button(text)
            btn.grid(row=row, column=col, sticky="nsew", padx=1, pady=1)
            btn.grid_remove()
            self.sci_button_dict[(row, col)] = btn
            
        # Configure scientific columns
        for col in range(4, 8):
            self.grid_columnconfigure(col, weight=1)
    
    def create_button(self, text):
        bg_color = "#e0e0e0"
        fg_color = "#000"
        
        if text in ['C', 'AC', 'DEL']:
            bg_color = "#ff6b6b"
            fg_color = "#fff"
        elif text in ['+', '-', '*', '/', '=', '^']:
            bg_color = "#4e9af1"
            fg_color = "#fff"
        elif text == 'Sci':
            bg_color = "#6bff6b"
            fg_color = "#000"
            
        return tk.Button(
            self, text=text, font=self.default_font,
            bg=bg_color, fg=fg_color, relief="flat",
            command=lambda t=text: self.on_button_click(t)
        )
    
    def bind_events(self):
        # Keyboard bindings
        for num in range(10):
            self.bind(str(num), lambda e, n=num: self.on_button_click(str(n)))
            
        self.bind('.', lambda e: self.on_button_click('.'))
        self.bind('+', lambda e: self.on_button_click('+'))
        self.bind('-', lambda e: self.on_button_click('-'))
        self.bind('*', lambda e: self.on_button_click('*'))
        self.bind('/', lambda e: self.on_button_click('/'))
        self.bind('=', lambda e: self.on_button_click('='))
        self.bind('<Return>', lambda e: self.on_button_click('='))
        self.bind('<BackSpace>', lambda e: self.on_button_click('DEL'))
        self.bind('<Escape>', lambda e: self.on_button_click('AC'))
        self.bind('<Key-c>', lambda e: self.on_button_click('C'))
        
        # Window resize
        self.bind('<Configure>', self.on_window_resize)
    
    def on_window_resize(self, event):
        # Adjust font sizes based on window dimensions
        width = self.winfo_width()
        base_size = max(10, min(20, width // 20))
        
        self.default_font.configure(size=base_size)
        self.large_font.configure(size=base_size + 8)
    
    def on_button_click(self, button_text):
        current = self.current_input.get()
        
        try:
            if button_text in '0123456789':
                if current == '0' or self.reset_input:
                    self.current_input.set(button_text)
                    self.reset_input = False
                else:
                    self.current_input.set(current + button_text)
                    
            elif button_text == '.':
                if '.' not in current:
                    self.current_input.set(current + '.')
                elif self.reset_input:
                    self.current_input.set('0.')
                    self.reset_input = False
                    
            elif button_text == '±':
                if current.startswith('-'):
                    self.current_input.set(current[1:])
                else:
                    self.current_input.set('-' + current)
                    
            elif button_text == 'C':
                self.current_input.set('0')
                
            elif button_text == 'AC':
                self.current_input.set('0')
                self.history.set('')
                self.operation = None
                self.stored_value = None
                
            elif button_text == 'DEL':
                if len(current) > 1:
                    self.current_input.set(current[:-1])
                else:
                    self.current_input.set('0')
                    
            elif button_text == '%':
                value = float(current) / 100
                self.current_input.set(str(value))
                
            elif button_text in ['+', '-', '*', '/', '^']:
                if self.operation and not self.reset_input:
                    self.calculate_result()
                    
                self.stored_value = float(current)
                self.operation = button_text
                self.history.set(f"{current} {button_text}")
                self.reset_input = True
                
            elif button_text == '=':
                if self.operation:
                    self.calculate_result()
                    self.operation = None
                    
            # Scientific operations
            elif button_text == '√':
                value = float(current)
                if value >= 0:
                    self.current_input.set(str(sqrt(value)))
                else:
                    self.current_input.set('Error')
                    
            elif button_text == 'x²':
                value = float(current)
                self.current_input.set(str(value ** 2))
                
            elif button_text == 'x³':
                value = float(current)
                self.current_input.set(str(value ** 3))
                
            elif button_text == 'sin':
                value = float(current)
                self.current_input.set(str(sin(radians(value))))
                
            elif button_text == 'cos':
                value = float(current)
                self.current_input.set(str(cos(radians(value))))
                
            elif button_text == 'tan':
                value = float(current)
                self.current_input.set(str(tan(radians(value))))
                
            elif button_text == 'log':
                value = float(current)
                if value > 0:
                    self.current_input.set(str(log10(value)))
                else:
                    self.current_input.set('Error')
                    
            elif button_text == 'ln':
                value = float(current)
                if value > 0:
                    self.current_input.set(str(log(value)))
                else:
                    self.current_input.set('Error')
                    
            elif button_text == 'n!':
                value = int(float(current))
                if value >= 0:
                    self.current_input.set(str(factorial(value)))
                else:
                    self.current_input.set('Error')
                    
            elif button_text == 'π':
                self.current_input.set(str(3.141592653589793))
                
            elif button_text == 'e':
                self.current_input.set(str(2.718281828459045))
                
            elif button_text == '(' or button_text == ')':
                # Placeholder for future parenthesis functionality
                pass
                
            elif button_text == 'Sci':
                self.toggle_scientific_mode()
                
        except Exception as e:
            self.current_input.set('Error')
    
    def calculate_result(self):
        try:
            current_value = float(self.current_input.get())
            
            if self.operation == '+':
                result = self.stored_value + current_value
            elif self.operation == '-':
                result = self.stored_value - current_value
            elif self.operation == '*':
                result = self.stored_value * current_value
            elif self.operation == '/':
                result = self.stored_value / current_value
            elif self.operation == '^':
                result = self.stored_value ** current_value
                
            # Format result to avoid .0 for whole numbers
            if result.is_integer():
                self.current_input.set(str(int(result)))
            else:
                self.current_input.set(str(result))
                
            self.history.set(f"{self.stored_value} {self.operation} {current_value} =")
            self.reset_input = True
            
        except ZeroDivisionError:
            self.current_input.set('Error')
            self.history.set('')
            self.operation = None
            self.stored_value = None
    
    def toggle_scientific_mode(self):
        self.scientific_mode = not self.scientific_mode
        
        if self.scientific_mode:
            # Show scientific buttons
            for btn in self.sci_button_dict.values():
                btn.grid()
            # Resize window
            self.geometry("800x600")
        else:
            # Hide scientific buttons
            for btn in self.sci_button_dict.values():
                btn.grid_remove()
            # Resize window back
            self.geometry("400x600")

if __name__ == "__main__":
    app = Calculator()
    app.mainloop()