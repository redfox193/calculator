import tkinter as tk
from tkinter import messagebox
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP


class FinancialCalculator:
    def __init__(self, root):
        self.root = root
        root.bind("<Control-KeyPress>", self.keypress)
        self.root.title("Финансовый калькулятор")

        student_info = "Гончаров Сергей Витальевич\nКурс: 3\nГруппа: 11\nГод: 2024"
        label_info = tk.Label(root, text=student_info, justify="left")
        label_info.grid(row=0, column=0, columnspan=5, pady=10)

        self.number1_entry = tk.Entry(root)
        self.number1_entry.grid(row=1, column=0, padx=5, pady=5)

        self.operation_var = tk.StringVar(value="+")
        operation_frame = tk.Frame(root)
        operation_frame.grid(row=1, column=1, padx=5, pady=5)

        self.addition_radio = tk.Radiobutton(operation_frame, text="+", variable=self.operation_var, value="+")
        self.addition_radio.pack(side="left")
        self.subtraction_radio = tk.Radiobutton(operation_frame, text="-", variable=self.operation_var, value="-")
        self.subtraction_radio.pack(side="left")
        self.multiplication_radio = tk.Radiobutton(operation_frame, text="*", variable=self.operation_var, value="*")
        self.multiplication_radio.pack(side="left")
        self.division_radio = tk.Radiobutton(operation_frame, text="/", variable=self.operation_var, value="/")
        self.division_radio.pack(side="left")

        self.number2_entry = tk.Entry(root)
        self.number2_entry.grid(row=1, column=2, padx=5, pady=5)

        calculate_button = tk.Button(root, text="Вычислить", command=self.calculate)
        calculate_button.grid(row=1, column=3, padx=5, pady=5)

        self.result_label = tk.Label(root, text="", font=("Arial", 12))
        self.result_label.grid(row=2, column=0, columnspan=5, pady=10)

    def keypress(self, e):
        if e.keycode == 86 and e.keysym != 'v':
            self.cmd_paste()
        elif e.keycode == 67 and e.keysym != 'c':
            self.cmd_copy()
        elif e.keycode == 88 and e.keysym != 'x':
            self.cmd_cut()

    def cmd_copy(self):
        widget = self.root.focus_get()
        if isinstance(widget, tk.Entry) or isinstance(widget, tk.Text):
            widget.event_generate("<<Copy>>")

    def cmd_cut(self):
        widget = self.root.focus_get()
        if isinstance(widget, tk.Entry) or isinstance(widget, tk.Text):
            widget.event_generate("<<Cut>>")

    def cmd_paste(self):
        widget = self.root.focus_get()
        if isinstance(widget, tk.Entry) or isinstance(widget, tk.Text):
            widget.event_generate("<<Paste>>")

    def convert_to_decimal(self, value):
        try:
            if any(c.isalpha() for c in value):
                raise ValueError('alpha')

            value = value.replace(",", ".").strip()
            if value.count('.') > 1 or '  ' in value:
                raise ValueError

            if '.' in value:
                left, right = value.split('.')
                if ' ' in right:
                    raise ValueError
            else:
                left = value

            float(value.replace(' ', ''))

            parts = left.split()
            if len(parts) > 1:
                for i, part in enumerate(parts):
                    if i == 0 and len(part) > 3:
                        raise ValueError
                    if i != 0 and len(part) != 3:
                        raise ValueError

            value = value.replace(' ', '')
            return Decimal(value)
        except ValueError as e:
            if str(e) != 'alpha':
                messagebox.showerror("Ошибка", f"Некорректное значение: '{value}'")
            else:
                messagebox.showerror("Ошибка", f"Некорректное значение: '{value}' Нельзя вводить буквы!")
            return None

    def format_result(self, value: str):
        minus = ''
        if '-' in value:
            minus = '-'
            value = value[1:]

        left, right = '', ''
        if '.' in value:
            left, right = value.split('.')
        else:
            left = value

        while right and right[-1] == '0':
            right = right[:-1]

        parts = []
        if len(left) <= 3:
            parts.append(left)
        else:
            part = ''
            for i in range(len(left) - 1, -1, -1):
                part = left[i] + part
                if len(part) == 3:
                    parts = [part] + parts
                    part = ''
            if part:
                parts = [part] + parts
        left = ' '.join(parts)

        if '.' in value and right:
            return minus + left + '.' + right
        else:
            return minus + left

    def calculate(self):
        number1 = self.convert_to_decimal(self.number1_entry.get())
        number2 = self.convert_to_decimal(self.number2_entry.get())

        if number1 is None or number2 is None:
            return

        operation = self.operation_var.get()

        try:
            if operation == "+":
                result = number1 + number2
                result = result.quantize(Decimal('1.000000'), rounding=ROUND_HALF_UP)
            elif operation == "-":
                result = number1 - number2
                result = result.quantize(Decimal('1.000000'), rounding=ROUND_HALF_UP)
            elif operation == "*":
                result = number1 * number2
                result = result.quantize(Decimal('1.000000'), rounding=ROUND_HALF_UP)
            elif operation == "/":
                if number2 == Decimal('0'):
                    messagebox.showerror("Ошибка", "Деление на ноль невозможно!")
                    return
                result = number1 / number2
                result = result.quantize(Decimal('1.000000'), rounding=ROUND_HALF_UP)
            else:
                messagebox.showerror("Ошибка", "Неизвестная операция!")
                return
        except (InvalidOperation, OverflowError):
            messagebox.showerror("Ошибка", "Ошибка при выполнении операции!")
            return

        min_value = Decimal('-1_000_000_000_000.000000')
        max_value = Decimal('1_000_000_000_000.000000')

        if result < min_value or result > max_value:
            self.result_label.config(text="Переполнение диапазона!")
        else:
            self.result_label.config(text=f"Результат: {self.format_result(result.to_eng_string())}")


if __name__ == "__main__":
    root = tk.Tk()
    app = FinancialCalculator(root)
    root.mainloop()
