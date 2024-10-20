import tkinter as tk
from tkinter import messagebox
from decimal import Decimal


class FinancialCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Финансовый калькулятор")

        student_info = "Гончаров Сергей Витальевич\nКурс: 3\nГруппа: 11\nГод: 2024"
        label_info = tk.Label(root, text=student_info, justify="left")
        label_info.grid(row=0, column=0, columnspan=4, pady=10)

        self.number1_entry = tk.Entry(root)
        self.number1_entry.grid(row=1, column=0, padx=5, pady=5)

        self.operation_var = tk.StringVar(value="+")
        operation_frame = tk.Frame(root)
        operation_frame.grid(row=1, column=1, padx=5, pady=5)

        self.addition_radio = tk.Radiobutton(operation_frame, text="+", variable=self.operation_var, value="+")
        self.addition_radio.pack(side="left")
        self.subtraction_radio = tk.Radiobutton(operation_frame, text="-", variable=self.operation_var, value="-")
        self.subtraction_radio.pack(side="right")

        self.number2_entry = tk.Entry(root)
        self.number2_entry.grid(row=1, column=2, padx=5, pady=5)

        calculate_button = tk.Button(root, text="Вычислить", command=self.calculate)
        calculate_button.grid(row=1, column=3, padx=5, pady=5)

        self.result_label = tk.Label(root, text="", font=("Arial", 12))
        self.result_label.grid(row=2, column=0, columnspan=4, pady=10)

    def convert_to_decimal(self, value):
        try:
            if 'e' in value:
                raise ValueError
            float(value.replace(",", "."))
        except ValueError:
            messagebox.showerror("Ошибка", f"Некорректное значение: '{value}'")
            return None
        return Decimal(value.replace(",", "."))

    def calculate(self):
        number1 = self.convert_to_decimal(self.number1_entry.get())
        number2 = self.convert_to_decimal(self.number2_entry.get())

        if number1 is None or number2 is None:
            return

        operation = self.operation_var.get()

        if operation == "+":
            result = number1 + number2
        elif operation == "-":
            result = number1 - number2
        else:
            messagebox.showerror("Ошибка", "Неизвестная операция!")
            return

        min_value = Decimal('-1_000_000_000_000.000000')
        max_value = Decimal('1_000_000_000_000.000000')

        if result < min_value or result > max_value:
            self.result_label.config(text="Переполнение диапазона!")
        else:
            self.result_label.config(text=f"Результат: {result}")


if __name__ == "__main__":
    root = tk.Tk()
    app = FinancialCalculator(root)
    root.mainloop()

