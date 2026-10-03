"""
Basic Calculator - Python (Tkinter)
Features: Execution time (auto unit), Addition, Subtraction, Multiplication, Division, Percentage,
          Decimal, Clear (C), Backspace, Keyboard support
Theme: Light
"""

import tkinter as tk
import time   # execution time calculate karne ke liye

# ------------------------------------------------------------------
# 1) COLORS & FONTS (UI ka design yahan se control hota hai)
# ------------------------------------------------------------------
BG_COLOR = "#F3F6FB"        # window ka background (light)
DISPLAY_BG = "#FFFFFF"      # display screen ka background
TEXT_COLOR = "#1F2937"      # normal text
SUBTEXT_COLOR = "#6B7280"   # upar wali chhoti history line

NUM_BG = "#FFFFFF"          # number buttons
NUM_HOVER = "#EEF2F7"
OP_BG = "#DCE8FF"           # operator buttons (+ - x /)
OP_HOVER = "#C7DAFF"
CLEAR_BG = "#FFE0E0"        # C aur backspace
CLEAR_HOVER = "#FFC9C9"
EQUAL_BG = "#2563EB"        # equal button (blue)
EQUAL_HOVER = "#1D4ED8"

FONT_DISPLAY = ("Segoe UI", 30, "bold")
FONT_HISTORY = ("Segoe UI", 12)
FONT_BUTTON = ("Segoe UI", 16, "bold")

OPERATORS = ["+", "−", "×", "÷"]   # display par jo symbols dikhte hain


# ------------------------------------------------------------------
# TIME FORMAT FUNCTION (unit khud badal jata hai)
# ------------------------------------------------------------------
def format_time(seconds):
    """Seconds lekar sahi unit mein text banata hai: µs, ms ya s."""
    micro = seconds * 1_000_000          # seconds ko microseconds mein badlo
    if micro < 1000:                     # 1000 µs se kam -> µs
        return f"{micro:.2f} µs"
    elif micro < 1_000_000:              # 1000 ms se kam -> ms
        return f"{micro / 1000:.2f} ms"
    else:                                # warna seconds
        return f"{micro / 1_000_000:.2f} s"


# ------------------------------------------------------------------
# 2) CALCULATOR CLASS (poora program yahan hai)
# ------------------------------------------------------------------
class Calculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Simple Calculator")
        self.root.geometry("340x550")
        self.root.resizable(False, False)
        self.root.configure(bg=BG_COLOR)

        self.expression = ""            # user ne ab tak jo likha
        self.just_calculated = False    # kya abhi "=" dabaya gaya?

        self.history_text = tk.StringVar(value="")
        self.display_text = tk.StringVar(value="0")
        self.time_text = tk.StringVar(value="⏱ --")

        self.build_display()
        self.build_buttons()

        # Keyboard se bhi chalane ke liye
        self.root.bind("<Key>", self.on_key)

    # ---------------- UI: Display ----------------
    def build_display(self):
        frame = tk.Frame(self.root, bg=DISPLAY_BG, padx=15, pady=10)
        frame.pack(fill="x", padx=15, pady=(20, 10))

        tk.Label(frame, textvariable=self.history_text, font=FONT_HISTORY,
                 bg=DISPLAY_BG, fg=SUBTEXT_COLOR, anchor="e").pack(fill="x")

        tk.Label(frame, textvariable=self.display_text, font=FONT_DISPLAY,
                 bg=DISPLAY_BG, fg=TEXT_COLOR, anchor="e").pack(fill="x")

        # Execution time ka label (display ke neeche)
        tk.Label(frame, textvariable=self.time_text, font=("Segoe UI", 9),
                 bg=DISPLAY_BG, fg="#8A94A6", anchor="e").pack(fill="x")

    # ---------------- UI: Buttons ----------------
    def build_buttons(self):
        grid = tk.Frame(self.root, bg=BG_COLOR)
        grid.pack(fill="both", expand=True, padx=10, pady=(0, 15))

        # Har row mein buttons: (text, type)
        layout = [
            [("C", "clear"), ("⌫", "clear"), ("%", "op"), ("÷", "op")],
            [("7", "num"), ("8", "num"), ("9", "num"), ("×", "op")],
            [("4", "num"), ("5", "num"), ("6", "num"), ("−", "op")],
            [("1", "num"), ("2", "num"), ("3", "num"), ("+", "op")],
            [("0", "num"), (".", "num"), ("=", "equal"), None],
        ]

        colors = {
            "num": (NUM_BG, NUM_HOVER, TEXT_COLOR),
            "op": (OP_BG, OP_HOVER, "#1E40AF"),
            "clear": (CLEAR_BG, CLEAR_HOVER, "#B91C1C"),
            "equal": (EQUAL_BG, EQUAL_HOVER, "#FFFFFF"),
        }

        for r, row in enumerate(layout):
            grid.rowconfigure(r, weight=1)
            for c, item in enumerate(row):
                grid.columnconfigure(c, weight=1)
                if item is None:
                    continue
                text, kind = item
                bg, hover, fg = colors[kind]

                btn = tk.Button(
                    grid, text=text, font=FONT_BUTTON, bg=bg, fg=fg,
                    activebackground=hover, activeforeground=fg,
                    relief="flat", bd=0, cursor="hand2",
                    command=lambda t=text: self.on_button(t),
                )
                # "=" button 2 columns lega
                span = 2 if text == "=" else 1
                btn.grid(row=r, column=c, columnspan=span,
                         sticky="nsew", padx=4, pady=4)

                # Hover effect (mouse upar aaye to color badle)
                btn.bind("<Enter>", lambda e, b=btn, h=hover: b.config(bg=h))
                btn.bind("<Leave>", lambda e, b=btn, o=bg: b.config(bg=o))

    # ---------------- Button / Keyboard handling ----------------
    def on_button(self, value):
        if value == "C":
            self.clear()
        elif value == "⌫":
            self.backspace()
        elif value == "=":
            self.calculate()
        else:
            self.press(value)

    def on_key(self, event):
        key = event.char
        mapping = {"*": "×", "/": "÷", "-": "−"}
        if key in "0123456789.+%":
            if key != "":
                self.on_button(key)
        elif key in mapping:
            self.on_button(mapping[key])
        elif event.keysym in ("Return", "KP_Enter"):
            self.calculate()
        elif event.keysym == "BackSpace":
            self.backspace()
        elif event.keysym == "Escape":
            self.clear()

    # ---------------- Logic ----------------
    def press(self, value):
        # Result aane ke baad naya number likha to naye sire se shuru
        if self.just_calculated:
            if value not in OPERATORS and value != "%":
                self.expression = ""
            self.just_calculated = False
            self.history_text.set("")

        if value in OPERATORS:
            if self.expression == "":
                if value == "−":            # shuru mein sirf minus allowed
                    self.expression = "−"
                    self.update_display()
                return
            if self.expression == "−":
                return
            if self.expression[-1] in OPERATORS:   # double operator na ho
                self.expression = self.expression[:-1]

        elif value == "%":
            if self.expression == "" or self.expression[-1] in OPERATORS + ["%"]:
                return

        elif value == ".":
            current = self.current_number()
            if "." in current:               # ek number mein 2 dot nahi
                return
            if current == "":
                value = "0."

        self.expression += value
        self.update_display()

    def current_number(self):
        """Aakhri number nikalta hai (last operator ke baad wala hissa)."""
        number = ""
        for ch in reversed(self.expression):
            if ch in OPERATORS or ch == "%":
                break
            number = ch + number
        return number

    def clear(self):
        self.expression = ""
        self.just_calculated = False
        self.history_text.set("")
        self.display_text.set("0")
        self.time_text.set("⏱ --")

    def backspace(self):
        if self.just_calculated:
            return
        self.expression = self.expression[:-1]
        self.update_display()

    def calculate(self):
        if self.expression == "":
            return

        expr = self.expression
        # Aakhir mein operator ho to hata do (jaise "5+")
        while expr and expr[-1] in OPERATORS:
            expr = expr[:-1]
        if expr == "" or expr == "−":
            return

        # Display symbols ko Python symbols mein badlo
        python_expr = (expr.replace("×", "*").replace("÷", "/")
                           .replace("−", "-").replace("%", "/100"))

        start = time.perf_counter()        # timer start

        try:
            result = eval(python_expr)     # sirf numbers aur + - * / hain, safe hai
            result = float(result)
            if result.is_integer() and abs(result) < 1e15:
                result_text = str(int(result))
            else:
                result_text = f"{result:.10g}"
        except ZeroDivisionError:
            self.history_text.set(expr + " =")
            self.display_text.set("Cannot ÷ by 0")
            self.expression = ""
            self.just_calculated = False
            return
        except Exception:
            self.display_text.set("Error")
            self.expression = ""
            self.just_calculated = False
            return

        end = time.perf_counter()          # timer stop
        time_str = format_time(end - start)  # sahi unit ke saath time text
        self.time_text.set(f"⏱ {time_str}")
        print(f"{expr} = {result_text}   (Execution time: {time_str})")

        self.history_text.set(expr + " =")
        self.display_text.set(result_text)
        self.expression = result_text.replace("-", "−")
        self.just_calculated = True

    def update_display(self):
        self.display_text.set(self.expression if self.expression else "0")


# ------------------------------------------------------------------
# 3) PROGRAM START
# ------------------------------------------------------------------
if __name__ == "__main__":
    program_start = time.perf_counter()
    window = tk.Tk()
    Calculator(window)
    window.mainloop()
    total = time.perf_counter() - program_start
    print(f"Program total run time: {total:.2f} seconds")
