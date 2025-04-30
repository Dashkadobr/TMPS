import math
import tkinter as tk
from tkinter import messagebox
from abc import ABC, abstractmethod

# ------------------------------ PATTERN: COMPOSITE ------------------------------
class Expression(ABC):
    @abstractmethod
    def evaluate(self):
        pass

class Number(Expression):
    def __init__(self, value: float):
        self.value = value
    def evaluate(self):
        return self.value

class BinaryOperation(Expression):
    def __init__(self, left: Expression, right: Expression):
        self.left, self.right = left, right
    @abstractmethod
    def evaluate(self):
        pass

class Add(BinaryOperation):
    def evaluate(self): return self.left.evaluate() + self.right.evaluate()

class Subtract(BinaryOperation):
    def evaluate(self): return self.left.evaluate() - self.right.evaluate()

class Multiply(BinaryOperation):
    def evaluate(self): return self.left.evaluate() * self.right.evaluate()

class Divide(BinaryOperation):
    def evaluate(self):
        d = self.right.evaluate()
        if d == 0:
            raise ZeroDivisionError("Деление на ноль!")
        return self.left.evaluate() / d

class Power(BinaryOperation):
    def evaluate(self): return self.left.evaluate() ** self.right.evaluate()

class UnaryOperation(Expression):
    def __init__(self, operand: Expression):
        self.operand = operand
    @abstractmethod
    def evaluate(self):
        pass

# ------------------------------- PATTERN: ADAPTER -------------------------------
class MathFunctionAdapter(UnaryOperation):
    def __init__(self, operand: Expression, func):
        super().__init__(operand)
        self.func = func
    def evaluate(self):
        return self.func(self.operand.evaluate())

# ------------------------------ PATTERN: DECORATOR ------------------------------
def log_operation(func):
    def wrapper(*args, **kw):
        res = func(*args, **kw)
        print(f"{args[0].__class__.__name__} -> {res}")
        return res
    return wrapper

class AddWithLogging(Add):
    @log_operation
    def evaluate(self):
        return super().evaluate()

# ------------------------------- PATTERN: PROXY --------------------------------
class LazyExpressionProxy(Expression):
    def __init__(self, real_expr: Expression):
        self.real_expr = real_expr
        self._cached = None
    def evaluate(self):
        if self._cached is None:
            print("Ленивая оценка...")
            self._cached = self.real_expr.evaluate()
        else:
            print("Кэшированный результат.")
        return self._cached

# ------------------------------- PATTERN: FACADE -------------------------------
class CalculatorFacade:
    def calculate(self, expr: Expression) -> float:
        return expr.evaluate()

# --------------------------------- PARSER --------------------------------------
def tokenize(s: str):
    tokens, i = [], 0
    while i < len(s):
        c = s[i]
        if c.isspace(): i += 1; continue
        if c.isdigit() or c == '.':
            num = c; i += 1
            while i < len(s) and (s[i].isdigit() or s[i] == '.'):
                num += s[i]; i += 1
            tokens.append(num)
        elif c.isalpha():
            idn = c; i += 1
            while i < len(s) and s[i].isalpha():
                idn += s[i]; i += 1
            tokens.append(idn)
        elif c in '+-*/^()':
            tokens.append(c); i += 1
        else:
            raise ValueError(f"Непонятный символ «{c}»")
    return tokens

class Parser:
    def __init__(self, tokens, mode_var):
        self.tokens, self.pos = tokens, 0
        self.mode_var = mode_var  # "rad" или "deg"
    def cur(self): return self.tokens[self.pos] if self.pos < len(self.tokens) else None
    def eat(self, t):
        if self.cur() == t:
            self.pos += 1
        else:
            raise ValueError(f"Ожидали «{t}», а встретили «{self.cur()}»")
    def parse(self):
        expr = self.parse_expression()
        if self.cur() is not None:
            raise ValueError("Лишние данные после разбора")
        return expr

    def parse_expression(self):
        node = self.parse_term()
        while self.cur() in ('+','-'):
            op = self.cur(); self.eat(op)
            right = self.parse_term()
            node = AddWithLogging(node, right) if op == '+' else Subtract(node, right)
        return node

    def parse_term(self):
        node = self.parse_power()
        while self.cur() in ('*','/'):
            op = self.cur(); self.eat(op)
            right = self.parse_power()
            node = Multiply(node, right) if op == '*' else Divide(node, right)
        return node

    def parse_power(self):
        node = self.parse_factor()
        if self.cur() == '^':
            self.eat('^')
            right = self.parse_power()  # правоассоц.
            node = Power(node, right)
        return node

    def parse_factor(self):
        tok = self.cur()
        if tok is None:
            raise ValueError("Неполное выражение")
        # число
        try:
            val = float(tok); self.eat(tok)
            return Number(val)
        except:
            pass
        # функция или тригонометрия
        if tok.isalpha():
            name = tok; self.eat(tok)
            self.eat('(')
            expr = self.parse_expression()
            self.eat(')')
            if name in ('sin','cos','tan'):
                f = getattr(math, name)
                if self.mode_var.get() == 'deg':
                    f = (lambda x, f=f: f(math.radians(x)))
                return MathFunctionAdapter(expr, f)
            elif name == 'sqrt':
                return MathFunctionAdapter(expr, math.sqrt)
            elif name == 'log':
                return MathFunctionAdapter(expr, math.log)
            else:
                raise ValueError(f"Неизвестная функция «{name}»")
        # скобки
        if tok == '(':
            self.eat('(')
            expr = self.parse_expression()
            self.eat(')')
            return expr

        raise ValueError(f"Непредвиденный токен «{tok}»")

def build_expression(s, mode_var):
    tokens = tokenize(s)
    parser = Parser(tokens, mode_var)
    expr = parser.parse()
    return LazyExpressionProxy(expr)

# --------------------------------- GUI ----------------------------------------
class CalculatorGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Расширяемый калькулятор")
        self.resizable(False, False)
        self.mode_var = tk.StringVar(value="rad")

        # 1) Переключатель Rad/Deg
        tk.Radiobutton(self, text="Rad", variable=self.mode_var, value="rad").grid(row=0, column=0, columnspan=2)
        tk.Radiobutton(self, text="Deg", variable=self.mode_var, value="deg").grid(row=0, column=2, columnspan=2)

        # 2) Окно ввода
        self.display = tk.Entry(self, font=("Arial",20), justify='right')
        self.display.grid(row=1, column=0, columnspan=5, sticky="we", padx=5, pady=5)

        # 3) Кнопки
        buttons = [
            ('7',2,0),('8',2,1),('9',2,2),('/',2,3),('sqrt',2,4),
            ('4',3,0),('5',3,1),('6',3,2),('*',3,3),('^',3,4),
            ('1',4,0),('2',4,1),('3',4,2),('-',4,3),('log',4,4),
            ('0',5,0),('.',5,1),('(',5,2),(')',5,3),('+',5,4),
            ('C',6,0),('←',6,1),('sin',6,2),('cos',6,3),('tan',6,4),
        ]
        for (txt,r,c) in buttons:
            btn = tk.Button(self, text=txt, width=5, height=2,
                            command=lambda t=txt: self.on_button(t))
            btn.grid(row=r, column=c, padx=2, pady=2)

        # 4) Большая кнопка "=" внизу
        eq = tk.Button(self, text='=', width=27, height=2, command=lambda: self.on_button('='))
        eq.grid(row=7, column=0, columnspan=5, padx=2, pady=5)

    def on_button(self, t):
        if t == 'C':
            self.display.delete(0, tk.END)
        elif t == '←':
            s = self.display.get()
            self.display.delete(0, tk.END)
            self.display.insert(0, s[:-1])
        elif t == '=':
            self.compute()
        else:
            if t in ('sin','cos','tan','sqrt','log'):
                self.display.insert(tk.END, t + '(')
            else:
                self.display.insert(tk.END, t)

    def compute(self):
        expr_text = self.display.get()
        try:
            expr = build_expression(expr_text, self.mode_var)
            result = CalculatorFacade().calculate(expr)
            self.display.delete(0, tk.END)
            self.display.insert(0, str(round(result, 6)))
        except Exception as e:
            messagebox.showerror("Ошибка", str(e))

if __name__ == "__main__":
    CalculatorGUI().mainloop()
