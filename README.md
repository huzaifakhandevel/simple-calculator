# 🧮 Simple Calculator (Python)

A basic desktop calculator built with **Python** and **Tkinter**. It has a clean light-themed interface, works with both mouse and keyboard, and shows the **execution time** of every calculation.

<!-- To show a screenshot: save it in this folder as screenshot.png, then replace this whole comment with the line: ![Calculator Screenshot](screenshot.png) -->

## ✨ Features

- Basic operations: **Addition (+)**, **Subtraction (−)**, **Multiplication (×)**, **Division (÷)**
- **Percentage (%)** and **decimal** support
- **C** button to clear everything and **⌫** button to delete the last digit
- **Execution time** shown for every calculation (unit changes automatically: µs, ms or s)
- Total program run time printed in the terminal when the window is closed
- Friendly error handling (for example, dividing by zero shows a message instead of crashing)
- Clean **light theme** with button hover effects
- Full **keyboard support**

## 🛠️ Technologies Used

- **Python 3**
- **Tkinter** (comes built-in with Python, no extra installation needed)

## 📋 Requirements

- Python 3.8 or newer installed on your computer
- On Linux only, Tkinter may need to be installed once: `sudo apt install python3-tk`

## 🚀 How to Run

1. Download or clone this project.
2. Open the project folder in a terminal (or in VS Code).
3. Run:

```bash
python calculator.py
```

(On Mac/Linux you may need to use `python3 calculator.py`.)

In VS Code, you can also open `calculator.py` and click the **▶ Run Python File** button at the top right.

## 🎮 How to Use

Click the buttons with your mouse, or use the keyboard:

| Key | Action |
|-----|--------|
| `0` – `9` | Enter numbers |
| `.` | Decimal point |
| `+` `-` `*` `/` | Add, subtract, multiply, divide |
| `%` | Percentage |
| `Enter` | Show result (=) |
| `Backspace` | Delete last digit |
| `Esc` | Clear everything |

**Example:** Press `5`, `×`, `6`, then `=` to get `30`. The execution time (for example `⏱ 22.50 µs`) appears below the result.

## ⏱️ About Execution Time

The program measures how long each calculation takes using Python's `time.perf_counter()`. The time is displayed below the result, and the unit is chosen automatically:

| Time taken | Shown as |
|------------|----------|
| Less than 1000 µs | `µs` (microseconds) |
| Less than 1000 ms | `ms` (milliseconds) |
| Longer | `s` (seconds) |

## 📁 Project Structure

```
Calculator/
├── calculator.py   # Main program (UI + calculator logic)
└── README.md       # Project documentation
```

## 🧠 How the Code Is Organized

- **Colors & Fonts:** all theme colors are defined at the top, so the look can be changed easily.
- **`build_display()`:** creates the result screen.
- **`build_buttons()`:** creates the button grid and hover effects.
- **`press()`, `calculate()`, `clear()`, `backspace()`:** the calculator logic.
- **`format_time()`:** converts the measured time into µs, ms or s.

## 🔮 Future Improvements

- Calculation history list
- Dark mode toggle
- Memory buttons (M+, M−, MR)

## 👤 Author

**[Your Name]**
Made as a beginner-level Python project.
