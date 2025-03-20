"""
Simple Windows Calculator Application

A calculator with standard and additional operations
using Tkinter for the GUI.
"""

import tkinter as tk
import math
from abc import ABC, abstractmethod
from typing import Callable, Dict, Optional, Union


class CalculatorError(Exception):
    """Base exception class for calculator errors."""

    pass


class DivisionByZeroError(CalculatorError):
    """Exception raised when attempting to divide by zero."""

    def __init__(self):
        super().__init__("Error: Division by zero")


class Operation(ABC):
    """Abstract base class for calculator operations."""

    @abstractmethod
    def execute(self, x: float, y: float = None) -> float:
        """Execute the operation on one or two operands."""
        pass


class Addition(Operation):
    """Addition operation."""

    def execute(self, x: float, y: float) -> float:
        return x + y


class Subtraction(Operation):
    """Subtraction operation."""

    def execute(self, x: float, y: float) -> float:
        return x - y


class Multiplication(Operation):
    """Multiplication operation."""

    def execute(self, x: float, y: float) -> float:
        return x * y


class Division(Operation):
    """Division operation."""

    def execute(self, x: float, y: float) -> float:
        if y == 0:
            raise DivisionByZeroError()
        return x / y


class Pi(Operation):
    """Pi (π) constant operation."""

    def execute(self, x: float, y: float = None) -> float:
        return math.pi


class Percentage(Operation):
    """Percentage operation."""

    def execute(self, x: float, y: float = None) -> float:
        if y is not None:
            return (x * y) / 100
        return x / 100


class Reciprocal(Operation):
    """Reciprocal (1/x) operation."""

    def execute(self, x: float, y: float = None) -> float:
        if x == 0:
            raise DivisionByZeroError()
        return 1 / x


class Square(Operation):
    """Square (x²) operation."""

    def execute(self, x: float, y: float = None) -> float:
        return x * x


class SquareRoot(Operation):
    """Square root operation."""

    def execute(self, x: float, y: float = None) -> float:
        if x < 0:
            raise CalculatorError("Cannot calculate square root of negative number")
        return math.sqrt(x)


class Calculator:
    """Calculator engine that handles the calculation logic."""

    def __init__(self):
        self.binary_operations: Dict[str, Operation] = {
            "+": Addition(),
            "-": Subtraction(),
            "*": Multiplication(),
            "/": Division(),
            "%": Percentage(),
        }

        self.unary_operations: Dict[str, Operation] = {
            "1/x": Reciprocal(),
            "x²": Square(),
            "√": SquareRoot(),
            "π": Pi(),  # Add the Pi operation
        }

        self.reset()

    def reset(self) -> None:
        """Reset the calculator state."""
        self.first_operand: Optional[float] = None
        self.second_operand: Optional[float] = None
        self.operation: Optional[str] = None
        self.result: Optional[float] = None

    def set_first_operand(self, value: float) -> None:
        """Set the first operand."""
        self.first_operand = value

    def set_operation(self, operation: str) -> None:
        """Set the operation to perform."""
        if (
            operation is not None
            and operation not in self.binary_operations
            and operation not in self.unary_operations
        ):
            raise CalculatorError(f"Unsupported operation: {operation}")
        self.operation = operation

    def set_second_operand(self, value: float) -> None:
        """Set the second operand."""
        self.second_operand = value

    def calculate(self) -> float:
        """Perform the calculation and return the result."""
        if self.first_operand is None:
            raise CalculatorError("First operand not set")

        if self.operation is None:
            # If no operation is set, just return the first operand
            return self.first_operand

        try:
            # Handle unary operations (operations that only need one operand)
            if self.operation in self.unary_operations:
                operation_obj = self.unary_operations[self.operation]
                self.result = operation_obj.execute(self.first_operand)
                return self.result

            # Handle binary operations (operations that need two operands)
            if self.second_operand is None:
                raise CalculatorError("Second operand not set")

            operation_obj = self.binary_operations[self.operation]
            self.result = operation_obj.execute(self.first_operand, self.second_operand)
            return self.result

        except DivisionByZeroError as e:
            raise e
        except Exception as e:
            raise CalculatorError(f"Calculation error: {str(e)}")

    def perform_unary_operation(self, operation: str, operand: float) -> float:
        """Perform a unary operation directly."""
        if operation not in self.unary_operations:
            raise CalculatorError(f"Unsupported unary operation: {operation}")

        try:
            operation_obj = self.unary_operations[operation]
            return operation_obj.execute(operand)
        except Exception as e:
            raise CalculatorError(f"Calculation error: {str(e)}")

    def negate(self, value: float) -> float:
        """Negate a value (change sign)."""
        return -value


class CalculatorApp:
    """GUI application for the calculator."""

    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Python Calculator")
        self.root.resizable(False, False)
        self.root.configure(bg="#f0f0f0")

        # Set the window icon (optional)
        # self.root.iconbitmap('calculator.ico')

        # Calculator engine
        self.calculator = Calculator()

        # Display variables
        self.current_input = ""
        self.waiting_for_operand = False
        self.last_operation_is_equals = False

        # Create the display
        self.create_display()

        # Create the buttons
        self.create_buttons()

        # Setup keyboard shortcuts
        self.setup_keyboard_shortcuts()

    def create_display(self) -> None:
        """Create the calculator display."""
        self.display_var = tk.StringVar()
        self.display_var.set("0")

        display_frame = tk.Frame(self.root, bg="#f0f0f0")
        display_frame.pack(padx=10, pady=10, fill=tk.BOTH)

        self.display = tk.Entry(
            display_frame,
            textvariable=self.display_var,
            font=("Arial", 24),
            bd=5,
            relief=tk.RIDGE,
            justify=tk.RIGHT,
            state="readonly",
        )
        self.display.pack(fill=tk.BOTH, ipady=8)

    def create_buttons(self) -> None:
        """Create the calculator buttons."""
        buttons_frame = tk.Frame(self.root, bg="#f0f0f0")
        buttons_frame.pack(padx=10, pady=5)

        # Configure grid to be responsive
        for i in range(4):
            buttons_frame.columnconfigure(i, weight=1)
        for i in range(6):
            buttons_frame.rowconfigure(i, weight=1)

        # Button layout in a 4x6 grid
        # fmt:off
        button_layout = [
            [('%', self.percentage_pressed), ('π', self.pi_pressed), ('C', self.clear_pressed),
             ('⌫', self.backspace_pressed)],
            [('1/x', self.unary_operation_pressed), ('x²', self.unary_operation_pressed),
             ('√', self.unary_operation_pressed), ('/', self.operation_pressed)],
            [('7', self.digit_pressed), ('8', self.digit_pressed), ('9', self.digit_pressed),
             ('*', self.operation_pressed)],
            [('4', self.digit_pressed), ('5', self.digit_pressed), ('6', self.digit_pressed),
             ('-', self.operation_pressed)],
            [('1', self.digit_pressed), ('2', self.digit_pressed), ('3', self.digit_pressed),
             ('+', self.operation_pressed)],
            [('±', self.negate_pressed), ('0', self.digit_pressed), ('.', self.decimal_pressed),
             ('=', self.equals_pressed)]
        ]
        # fmt:on

        # Define color scheme
        # fmt:off
        color_scheme = {
            "digit": {"bg": "#e0e0e0", "fg": "black"},
            "operation": {"bg": "#d0d0d0", "fg": "black"},
            "equals": {"bg": "#4caf50", "fg": "white"},
            "clear": {"bg": "#ff9800", "fg": "white"},
            "backspace": {"bg": "#f44336", "fg": "white"},
            "unary": {"bg": "#9e9e9e", "fg": "white"},
            "other": {"bg": "#bbbbbb", "fg": "black"},
            "empty": {"bg": "#f0f0f0", "fg": "black"},
        }
        # fmt:on

        # Create and place buttons according to the layout
        for row_idx, row in enumerate(button_layout):
            for col_idx, (text, command) in enumerate(row):
                if text == "":  # Empty slot
                    continue

                # Determine button type and appearance
                button_type = "other"
                if text.isdigit() or text == ".":
                    button_type = "digit"
                elif text in ["+", "-", "*", "/"]:
                    button_type = "operation"
                elif text == "=":
                    button_type = "equals"
                elif text == "C":
                    button_type = "clear"
                elif text == "⌫":
                    button_type = "backspace"
                elif text in ["1/x", "x²", "√", "π"]:  # Add π to the unary operations
                    button_type = "unary"

                # Create the button with appropriate styling
                btn = tk.Button(
                    buttons_frame,
                    text=text,
                    font=("Arial", 16),
                    width=5,
                    height=2,
                    bg=color_scheme[button_type]["bg"],
                    fg=color_scheme[button_type]["fg"],
                    activebackground="#c0c0c0",
                    command=lambda t=text, cmd=command: cmd(t) if cmd else None,
                )
                btn.grid(row=row_idx, column=col_idx, padx=2, pady=2, sticky="nsew")

    def setup_keyboard_shortcuts(self) -> None:
        """Setup keyboard shortcuts for the calculator."""
        # Quit application with Q or Escape
        self.root.bind("<q>", self.quit_application)
        self.root.bind("<Q>", self.quit_application)
        self.root.bind("<Escape>", lambda event: self.clear_pressed("C"))
        # self.quit_application)

        # Enter/Return key acts as equals
        self.root.bind("<Return>", self.equals_pressed)
        self.root.bind("<space>", self.equals_pressed)

        # Number keys
        for digit in range(10):
            self.root.bind(
                str(digit), lambda event, d=digit: self.digit_pressed(str(d))
            )

        # Basic operations
        self.root.bind("+", lambda event: self.operation_pressed("+"))
        self.root.bind("-", lambda event: self.operation_pressed("-"))
        self.root.bind("*", lambda event: self.operation_pressed("*"))
        self.root.bind("/", lambda event: self.operation_pressed("/"))

        # Decimal point
        self.root.bind(".", lambda event: self.decimal_pressed("."))

        # Backspace
        self.root.bind("<BackSpace>", self.backspace_pressed)

        # Clear with 'c' key
        self.root.bind("c", lambda event: self.clear_pressed("C"))
        self.root.bind("C", lambda event: self.clear_pressed("C"))

    def quit_application(self, event=None) -> None:
        """Quit the application."""
        self.root.quit()

    def digit_pressed(self, digit: str) -> None:
        """Handle digit button press."""
        if self.waiting_for_operand or self.last_operation_is_equals:
            self.display_var.set(digit)
            self.waiting_for_operand = False
            self.last_operation_is_equals = False
        else:
            current = self.display_var.get()
            if current == "0" and digit != "0":
                self.display_var.set(digit)
            else:
                self.display_var.set(current + digit)

    def decimal_pressed(self, _: str) -> None:
        """Handle decimal point button press."""
        if self.waiting_for_operand or self.last_operation_is_equals:
            self.display_var.set("0.")
            self.waiting_for_operand = False
            self.last_operation_is_equals = False
        else:
            current = self.display_var.get()
            if "." not in current:
                self.display_var.set(current + ".")

    def operation_pressed(self, operation: str) -> None:
        """Handle operation button press."""
        try:
            value = float(self.display_var.get())

            # If we already have a pending operation, calculate the intermediate result
            if (
                self.calculator.operation is not None
                and self.calculator.first_operand is not None
            ):
                self.calculator.set_second_operand(value)
                result = self.calculator.calculate()
                self.display_var.set(str(self.format_result(result)))
                self.calculator.set_first_operand(result)
            else:
                self.calculator.set_first_operand(value)

            self.calculator.set_operation(operation)
            self.waiting_for_operand = True
            self.last_operation_is_equals = False

        except CalculatorError as e:
            self.display_var.set(str(e))
            self.waiting_for_operand = True

    def equals_pressed(self, _: str) -> None:
        """Handle equals button press."""
        try:
            # If equals was just pressed, don't do anything
            if self.last_operation_is_equals:
                return

            # Get the second operand
            value = float(self.display_var.get())

            # If there's no operation pending, just display the current value
            if self.calculator.operation is None:
                self.calculator.set_first_operand(value)
                self.display_var.set(str(self.format_result(value)))
                self.last_operation_is_equals = True
                return

            self.calculator.set_second_operand(value)

            # Calculate and display the result
            result = self.calculator.calculate()
            self.display_var.set(str(self.format_result(result)))

            # Reset for next calculation but keep the result as first operand
            self.calculator.set_first_operand(result)
            self.calculator.set_operation(None)
            self.waiting_for_operand = True
            self.last_operation_is_equals = True

        except CalculatorError as e:
            self.display_var.set(str(e))
            self.calculator.reset()
            self.waiting_for_operand = True

    def clear_pressed(self, _: str) -> None:
        """Handle clear button press."""
        self.calculator.reset()
        self.display_var.set("0")
        self.waiting_for_operand = False
        self.last_operation_is_equals = False

    def unary_operation_pressed(self, operation: str) -> None:
        """Handle unary operation button press (1/x, x², √)."""
        try:
            value = float(self.display_var.get())
            result = self.calculator.perform_unary_operation(operation, value)
            self.display_var.set(str(self.format_result(result)))
            self.calculator.set_first_operand(result)
            self.waiting_for_operand = True
            self.last_operation_is_equals = True
        except CalculatorError as e:
            self.display_var.set(str(e))
            self.waiting_for_operand = True

    def percentage_pressed(self, _: str) -> None:
        """Handle percentage button press."""
        try:
            value = float(self.display_var.get())

            # If we're in the middle of a calculation, apply percentage to first operand
            if (
                self.calculator.operation is not None
                and self.calculator.first_operand is not None
            ):
                percentage_value = (self.calculator.first_operand * value) / 100
                self.display_var.set(str(self.format_result(percentage_value)))
            else:
                # Otherwise just convert the current value to a percentage
                percentage_value = value / 100
                self.display_var.set(str(self.format_result(percentage_value)))
                self.calculator.set_first_operand(percentage_value)

            self.waiting_for_operand = True

        except CalculatorError as e:
            self.display_var.set(str(e))
            self.waiting_for_operand = True

    def pi_pressed(self, _: str) -> None:
        """Handle pi button press (π)."""
        try:
            result = self.calculator.perform_unary_operation(
                "π", 0
            )  # The value parameter is not used
            self.display_var.set(str(self.format_result(result)))
            self.calculator.set_first_operand(result)
            self.waiting_for_operand = True
            self.last_operation_is_equals = True
        except CalculatorError as e:
            self.display_var.set(str(e))
            self.waiting_for_operand = True

    def negate_pressed(self, _: str) -> None:
        """Handle negate button press (±)."""
        try:
            value = float(self.display_var.get())
            negated_value = self.calculator.negate(value)
            self.display_var.set(str(self.format_result(negated_value)))
        except CalculatorError as e:
            self.display_var.set(str(e))
            self.waiting_for_operand = True

    def backspace_pressed(self, _: str) -> None:
        """Handle backspace button press."""
        if self.waiting_for_operand or self.last_operation_is_equals:
            # If we're waiting for an operand, clear doesn't make sense,
            # so we'll just reset to 0
            self.display_var.set("0")
            self.waiting_for_operand = False
        else:
            current = self.display_var.get()
            if len(current) > 1:
                self.display_var.set(current[:-1])
            else:
                self.display_var.set("0")

    def format_result(self, value: float) -> Union[int, float]:
        """Format the result to remove trailing zeros if needed."""
        if value == int(value):
            return int(value)
        return value


def main():
    """Main entry point for the calculator application."""
    root = tk.Tk()
    app = CalculatorApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
