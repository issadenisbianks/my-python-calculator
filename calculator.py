import tkinter as tk
from tkinter import font as tkfont
import math

class CalculatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Modern Calculator")
        self.root.geometry("350x520")
        self.root.configure(bg="#17171C")
        self.root.minsize(300, 450)

        # Set taskbar icon if available (optional)
        # self.root.iconbitmap("calculator.ico")

        # Color Palette
        self.colors = {
            "bg": "#17171C",          # Main window background
            "display_bg": "#17171C",  # Display area background
            "text_primary": "#FFFFFF",# Main digit text
            "text_muted": "#747477",  # Muted expression text
            "num_btn": "#2E2F38",     # Number buttons background
            "num_btn_hover": "#3E3F4A", # Number buttons hover
            "op_btn": "#FF9F0A",      # Operator buttons background (orange)
            "op_btn_hover": "#FFB03B",  # Operator buttons hover
            "fn_btn": "#4E505F",      # Function buttons background (grey)
            "fn_btn_hover": "#5E6070",  # Function buttons hover
            "btn_active": "#1C1C1E"   # Click feedback overlay color
        }

        # Application State
        self.current_input = ""      # Active number/operator sequence
        self.expression = ""         # Full history expression
        self.is_result_shown = False # Flag to clear display on next digit press

        # UI Layout setup
        self.setup_fonts()
        self.create_display_area()
        self.create_buttons_grid()
        self.setup_grid_weights()
        self.bind_keyboard()

    def setup_fonts(self):
        """Initializes custom fonts for the display and buttons."""
        self.font_display_main = tkfont.Font(family="Segoe UI", size=32, weight="bold")
        self.font_display_sub = tkfont.Font(family="Segoe UI", size=14)
        self.font_buttons = tkfont.Font(family="Segoe UI", size=16, weight="bold")

    def create_display_area(self):
        """Creates the display area at the top of the calculator."""
        self.display_frame = tk.Frame(self.root, bg=self.colors["display_bg"])
        self.display_frame.pack(fill="both", expand=True, padx=20, pady=(20, 10))

        # Sub-label for displaying the current expression/history
        self.expression_label = tk.Label(
            self.display_frame,
            text="",
            anchor="e",
            bg=self.colors["display_bg"],
            fg=self.colors["text_muted"],
            font=self.font_display_sub,
            justify="right"
        )
        self.expression_label.pack(fill="x", pady=(5, 0))

        # Main-label for displaying the current entry or result
        self.result_label = tk.Label(
            self.display_frame,
            text="0",
            anchor="e",
            bg=self.colors["display_bg"],
            fg=self.colors["text_primary"],
            font=self.font_display_main,
            justify="right"
        )
        self.result_label.pack(fill="x", expand=True, pady=(5, 5))

    def create_buttons_grid(self):
        """Creates the grid of buttons at the bottom of the calculator."""
        self.buttons_frame = tk.Frame(self.root, bg=self.colors["bg"])
        self.buttons_frame.pack(fill="both", expand=True, padx=15, pady=(0, 15))

        # Button specs: (text, row, col, columnspan, type)
        # Types: 'num' (numbers), 'op' (operators), 'fn' (functions)
        button_specs = [
            ("AC", 0, 0, 1, "fn"), ("±", 0, 1, 1, "fn"), ("%", 0, 2, 1, "fn"), ("÷", 0, 3, 1, "op"),
            ("7",  1, 0, 1, "num"), ("8", 1, 1, 1, "num"), ("9", 1, 2, 1, "num"), ("×", 1, 3, 1, "op"),
            ("4",  2, 0, 1, "num"), ("5", 2, 1, 1, "num"), ("6", 2, 2, 1, "num"), ("−", 2, 3, 1, "op"),
            ("1",  3, 0, 1, "num"), ("2", 3, 1, 1, "num"), ("3", 3, 2, 1, "num"), ("+", 3, 3, 1, "op"),
            ("0",  4, 0, 2, "num"), ("·", 4, 2, 1, "num"), ("=", 4, 3, 1, "op")
        ]

        self.buttons = {}  # Dictionary to keep track of button widgets by character/label
        
        for text, row, col, col_span, btn_type in button_specs:
            # Select colors based on button type
            bg_color = self.colors[f"{btn_type}_btn"]
            hover_color = self.colors[f"{btn_type}_btn_hover"]
            
            # Create Custom styled Tkinter Button
            btn = tk.Button(
                self.buttons_frame,
                text=text,
                bg=bg_color,
                fg=self.colors["text_primary"],
                font=self.font_buttons,
                relief="flat",
                borderwidth=0,
                activebackground=self.colors["btn_active"],
                activeforeground=self.colors["text_primary"],
                command=lambda t=text: self.handle_press(t)
            )
            btn.grid(row=row, column=col, columnspan=col_span, sticky="nsew", padx=4, pady=4)
            
            # Setup hover effects
            btn.bind("<Enter>", lambda e, b=btn, hc=hover_color: b.configure(bg=hc))
            btn.bind("<Leave>", lambda e, b=btn, bc=bg_color: b.configure(bg=bc))
            
            # Save reference
            self.buttons[text] = btn

    def setup_grid_weights(self):
        """Configures row and column weights to make the layout responsive."""
        # Row 0 is the display, rows 1-5 are the buttons
        for r in range(5):
            self.buttons_frame.rowconfigure(r, weight=1)
        for c in range(4):
            self.buttons_frame.columnconfigure(c, weight=1)

    def bind_keyboard(self):
        """Binds physical keyboard keys to calculator inputs."""
        self.root.bind("<Key>", self.handle_key_press)
        self.root.bind("<Return>", lambda e: self.handle_press("="))
        self.root.bind("<BackSpace>", lambda e: self.handle_press("DEL"))
        self.root.bind("<Escape>", lambda e: self.handle_press("AC"))

    def handle_key_press(self, event):
        """Translates keyboard events into calculator actions."""
        char = event.char
        # Handle digits and basic operators
        if char in "0123456789":
            self.handle_press(char)
        elif char == ".":
            self.handle_press("·")
        elif char == "+":
            self.handle_press("+")
        elif char == "-":
            self.handle_press("−")
        elif char == "*":
            self.handle_press("×")
        elif char == "/":
            self.handle_press("÷")
        elif char == "%":
            self.handle_press("%")
        elif char == "=":
            self.handle_press("=")

    def handle_press(self, val):
        """Applies application logic depending on which key is clicked."""
        # Visual flash feedback when keyboard triggers button
        button_map = {
            "·": "·", ".": "·", "+": "+", "−": "−", "-": "−",
            "×": "×", "*": "×", "÷": "÷", "/": "÷", "=": "=", "\r": "="
        }
        mapped_key = button_map.get(val, val)
        if mapped_key in self.buttons:
            self.flash_button(self.buttons[mapped_key])

        # State Reset on error
        if self.result_label.cget("text") == "Error":
            self.clear_all()

        if val == "AC":
            self.clear_all()
        elif val == "DEL":
            self.backspace()
        elif val == "±":
            self.toggle_sign()
        elif val == "%":
            self.apply_percent()
        elif val in ["+", "−", "×", "÷"]:
            self.add_operator(val)
        elif val == "=":
            self.calculate()
        elif val == "·":
            self.add_decimal()
        else: # Number digit
            self.add_digit(val)

    def flash_button(self, button):
        """Flashes the button briefly to show interactive feedback."""
        original_bg = button.cget("bg")
        button.configure(bg=self.colors["btn_active"])
        self.root.after(100, lambda: button.configure(bg=original_bg))

    def clear_all(self):
        """Resets the state of the calculator display."""
        self.current_input = ""
        self.expression = ""
        self.is_result_shown = False
        self.update_display("0", "")

    def backspace(self):
        """Deletes the last character from the active entry input."""
        if self.is_result_shown:
            self.expression = ""
            self.is_result_shown = False
            
        if self.current_input:
            self.current_input = self.current_input[:-1]
            display_val = self.current_input if self.current_input else "0"
            self.update_display(display_val, self.expression)

    def toggle_sign(self):
        """Negates the current input."""
        if self.is_result_shown:
            self.current_input = self.result_label.cget("text").replace(",", "")
            self.expression = ""
            self.is_result_shown = False

        if not self.current_input:
            self.current_input = "0"

        if self.current_input.startswith("-"):
            self.current_input = self.current_input[1:]
        else:
            if self.current_input != "0" and self.current_input != "":
                self.current_input = "-" + self.current_input
                
        self.update_display(self.current_input, self.expression)

    def apply_percent(self):
        """Divides the current input by 100."""
        if self.is_result_shown:
            self.current_input = self.result_label.cget("text").replace(",", "")
            self.expression = ""
            self.is_result_shown = False

        val = self.current_input if self.current_input else "0"
        try:
            res = float(val) / 100.0
            # Remove trailing decimal zero if integer
            self.current_input = str(int(res)) if res.is_integer() else str(res)
            self.update_display(self.current_input, self.expression)
        except Exception:
            self.update_display("Error", "")

    def add_digit(self, digit):
        """Appends a digit to the current input sequence."""
        if self.is_result_shown:
            self.current_input = ""
            self.expression = ""
            self.is_result_shown = False

        # Limit numbers to max 12 digits to prevent overflowing the UI
        if len(self.current_input.replace("-", "").replace(".", "")) >= 12:
            return

        if self.current_input == "0":
            self.current_input = digit
        else:
            self.current_input += digit

        self.update_display(self.current_input, self.expression)

    def add_decimal(self):
        """Appends a decimal point to the current input if one isn't present."""
        if self.is_result_shown:
            self.current_input = "0"
            self.expression = ""
            self.is_result_shown = False

        if not self.current_input:
            self.current_input = "0"

        if "." not in self.current_input:
            self.current_input += "."
            self.update_display(self.current_input, self.expression)

    def add_operator(self, op):
        """Appends the active input and operator to the running expression."""
        if self.is_result_shown:
            # Start a new expression from the previous result
            prev_result = self.result_label.cget("text").replace(",", "")
            self.expression = f"{prev_result} {op} "
            self.current_input = ""
            self.is_result_shown = False
        else:
            if not self.current_input and not self.expression:
                # If nothing exists, default starting from 0
                self.expression = f"0 {op} "
            elif not self.current_input and self.expression:
                # User changed operator, replace the trailing operator
                self.expression = self.expression[:-3] + f" {op} "
            else:
                # Append current input and operator to expression
                self.expression += f"{self.current_input} {op} "
                self.current_input = ""

        self.update_display("0", self.expression)

    def calculate(self):
        """Evaluates the full mathematical expression."""
        if not self.expression and not self.current_input:
            return

        # Prepare final math statement
        if self.current_input:
            eval_expr = self.expression + self.current_input
        else:
            # If equal is pressed right after operator, evaluate operator with itself or trim it
            eval_expr = self.expression.strip()
            if eval_expr.endswith(("+", "−", "×", "÷")):
                eval_expr = eval_expr[:-1].strip()

        # Map display symbols back to python operators
        python_expr = eval_expr.replace("÷", "/").replace("×", "*").replace("−", "-")

        # Sanitize input expression for security
        allowed_chars = set("0123456789+-*/. ")
        if not all(c in allowed_chars for c in python_expr):
            self.update_display("Error", "")
            return

        try:
            # Handle empty expression
            if not python_expr.strip():
                return
                
            result = eval(python_expr)
            
            # Format the output result
            if isinstance(result, float) and result.is_integer():
                result = int(result)
            
            # Set application state
            self.current_input = ""
            self.expression = ""
            self.is_result_shown = True
            
            # Formatted display string
            self.update_display(str(result), eval_expr + " =")
        except ZeroDivisionError:
            self.update_display("Error", eval_expr + " =")
        except Exception:
            self.update_display("Error", "")

    def format_display_val(self, val_str):
        """Formats standard values with commas for thousands and limits size."""
        if val_str == "Error":
            return "Error"
        if not val_str:
            return "0"

        # Check negative
        is_neg = val_str.startswith("-")
        clean_str = val_str[1:] if is_neg else val_str

        # Split decimal
        parts = clean_str.split(".")
        int_part = parts[0]
        dec_part = parts[1] if len(parts) > 1 else None

        # Apply scientific notation for excessively large numbers
        try:
            num = float(val_str)
            if abs(num) >= 1e12 or (0 < abs(num) < 1e-7):
                return f"{num:.6e}"
        except ValueError:
            pass

        # Format integer component with thousands separators
        try:
            if int_part:
                formatted_int = f"{int(int_part):,}"
            else:
                formatted_int = "0"
        except ValueError:
            formatted_int = int_part

        formatted_val = f"-{formatted_int}" if is_neg else formatted_int
        
        if dec_part is not None:
            formatted_val += "." + dec_part

        # Auto shrink font if number gets long
        str_len = len(formatted_val)
        if str_len > 12:
            new_size = max(16, int(32 - (str_len - 12) * 1.5))
            self.font_display_main.configure(size=new_size)
        else:
            self.font_display_main.configure(size=32)

        return formatted_val

    def update_display(self, main_text, sub_text):
        """Helper to set main display and history expression texts."""
        formatted_main = self.format_display_val(main_text)
        self.result_label.configure(text=formatted_main)
        self.expression_label.configure(text=sub_text)

if __name__ == "__main__":
    root = tk.Tk()
    app = CalculatorApp(root)
    root.mainloop()
