import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP, ROUND_HALF_EVEN, ROUND_FLOOR, ROUND_DOWN


class FinancialCalculator:
    def __init__(self, root):
        self.root = root
        self.last_result = None
        root.bind("<Control-KeyPress>", self.keypress)
        self.root.title("Финансовый калькулятор")

        student_info = "Гончаров Сергей Витальевич\nКурс: 3\nГруппа: 11\nГод: 2024"
        label_info = tk.Label(root, text=student_info, justify="left")
        label_info.grid(row=0, column=0, columnspan=11, pady=10)

        self.number1_entry = tk.Entry(root, width=15)
        self.number1_entry.insert(0, "0")
        self.number1_entry.grid(row=1, column=0, padx=5, pady=5)

        self.number2_entry = tk.Entry(root, width=15)
        self.number2_entry.insert(0, "0")
        self.number2_entry.grid(row=1, column=3, padx=5, pady=5)

        self.number3_entry = tk.Entry(root, width=15)
        self.number3_entry.insert(0, "0")
        self.number3_entry.grid(row=1, column=5, padx=5, pady=5)

        self.number4_entry = tk.Entry(root, width=15)
        self.number4_entry.insert(0, "0")
        self.number4_entry.grid(row=1, column=8, padx=5, pady=5)

        self.operation1_var = tk.StringVar(value="+")
        self.operation1_combo = ttk.Combobox(root, textvariable=self.operation1_var, values=["+", "-", "*", "/"],
                                             state="readonly", width=2)
        self.operation1_combo.grid(row=1, column=1, padx=5)

        self.operation2_var = tk.StringVar(value="+")
        self.operation2_combo = ttk.Combobox(root, textvariable=self.operation2_var, values=["+", "-", "*", "/"],
                                             state="readonly", width=2)
        self.operation2_combo.grid(row=1, column=4, padx=5)

        self.operation3_var = tk.StringVar(value="+")
        self.operation3_combo = ttk.Combobox(root, textvariable=self.operation3_var, values=["+", "-", "*", "/"],
                                             state="readonly", width=2)
        self.operation3_combo.grid(row=1, column=7, padx=5)

        # Static labels
        tk.Label(root, text="(").grid(row=1, column=2)
        tk.Label(root, text=")").grid(row=1, column=6)
        tk.Label(root, text="=").grid(row=1, column=9)

        calculate_button = tk.Button(root, text="вычислить", command=self.calculate)
        calculate_button.grid(row=1, column=10, padx=5, pady=5)

        self.result_label = tk.Label(root, text="", font=("Arial", 12))
        self.result_label.grid(row=2, column=0, columnspan=11, pady=10)

        self.label_2 = tk.Label(root, text="выбор вида округления:", font=("Arial", 10))
        self.label_2.grid(row=3, column=0, columnspan=2, pady=5)

        self.rounding_var = tk.StringVar(value="математическое")
        self.rounding_combo = ttk.Combobox(root, textvariable=self.rounding_var, values=["математическое", "бухгалтерское", "усечение"],
                                           state="readonly", width=20)
        self.rounding_combo.grid(row=3, column=2, columnspan=3, pady=5)
        self.rounding_combo.bind("<<ComboboxSelected>>", lambda e: self.update_rounding())

        self.rounded_result_label = tk.Label(root, text="", font=("Arial", 12))
        self.rounded_result_label.grid(row=4, column=0, columnspan=11, pady=10)


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

    def get_result(self, number1, number2, operation: str):
        result = None
        if operation == "+":
            result = number1 + number2
            result = result.quantize(Decimal('1.0000000000'), rounding=ROUND_HALF_UP)
        elif operation == "-":
            result = number1 - number2
            result = result.quantize(Decimal('1.0000000000'), rounding=ROUND_HALF_UP)
        elif operation == "*":
            result = number1 * number2
            result = result.quantize(Decimal('1.0000000000'), rounding=ROUND_HALF_UP)
        elif operation == "/":
            if number2 == Decimal('0'):
                messagebox.showerror("Ошибка", "Деление на ноль невозможно!")
                return result
            result = number1 / number2
            result = result.quantize(Decimal('1.0000000000'), rounding=ROUND_HALF_UP)

        min_value = Decimal('-100_000_000_000_000.000000')
        max_value = Decimal('100_000_000_000_000.000000')

        if result < min_value or result > max_value:
            self.result_label.config(text="Переполнение допустимого диапазона в процессе вычислений!")
            return None
        return result


    def calculate(self):
        self.result_label.config(text="")
        self.rounded_result_label.config(text="")
        self.last_result = None

        number1 = self.convert_to_decimal(self.number1_entry.get())
        number2 = self.convert_to_decimal(self.number2_entry.get())
        number3 = self.convert_to_decimal(self.number3_entry.get())
        number4 = self.convert_to_decimal(self.number4_entry.get())

        if number1 is None or number2 is None or number3 is None or number4 is None:
            return

        operation_1 = self.operation1_combo.get()
        operation_2 = self.operation2_combo.get()
        operation_3 = self.operation3_combo.get()

        result_1 = self.get_result(number2, number3, operation_2)
        if result_1 is None:
            return

        if operation_3 in ['*', '/'] and operation_1 in ['+', '-']:
            result_2 = self.get_result(result_1, number4, operation_3)
            if result_2 is None:
                return

            result_3 = self.get_result(number1, result_2, operation_1)
            if result_3 is None:
                return
        else:
            result_2 = self.get_result(number1, result_1, operation_1)
            if result_2 is None:
                return

            result_3 = self.get_result(result_2, number4, operation_3)
            if result_3 is None:
                return

        result = result_3.quantize(Decimal('1.000000'), rounding=ROUND_HALF_UP)

        self.last_result = result
        self.result_label.config(text=f"Результат: {self.format_result(self.last_result.to_eng_string())}")
        self.update_rounding()

    def update_rounding(self):
        if self.last_result is None:
            return
        rounded_result = self.last_result

        rounding_method = self.rounding_var.get()
        if rounding_method == "математическое":
            rounded_result = rounded_result.quantize(Decimal('1'), rounding=ROUND_HALF_UP)
        elif rounding_method == "бухгалтерское":
            rounded_result = rounded_result.quantize(Decimal('1'), rounding=ROUND_HALF_EVEN)
        elif rounding_method == "усечение":
            rounded_result = rounded_result.quantize(Decimal('1'), rounding=ROUND_DOWN)

        self.rounded_result_label.config(
            text=f"Округлённый результат: {self.format_result(rounded_result.to_eng_string())}")


if __name__ == "__main__":
    root = tk.Tk()
    app = FinancialCalculator(root)
    root.mainloop()
