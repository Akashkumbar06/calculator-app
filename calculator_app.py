import ast
import operator

# Supported operators
OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
    ast.FloorDiv: operator.floordiv,
    ast.USub: operator.neg,
    ast.UAdd: operator.pos
}


def calculate(node):
    """Safely calculate an arithmetic expression."""

    if isinstance(node, ast.Constant):
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError("Invalid value")

    elif isinstance(node, ast.UnaryOp):
        operation = OPERATORS.get(type(node.op))
        if operation is None:
            raise ValueError("Unsupported operator")
        return operation(calculate(node.operand))

    elif isinstance(node, ast.BinOp):
        operation = OPERATORS.get(type(node.op))
        if operation is None:
            raise ValueError("Unsupported operator")

        left = calculate(node.left)
        right = calculate(node.right)

        # Prevent division/modulo by zero
        if isinstance(node.op, (ast.Div, ast.FloorDiv, ast.Mod)) and right == 0:
            raise ZeroDivisionError("Cannot divide by zero")

        return operation(left, right)

    else:
        raise ValueError("Invalid expression")


def evaluate(expression):
    """Convert expression into an AST and calculate it."""
    tree = ast.parse(expression, mode="eval")
    return calculate(tree.body)


def show_history(history):
    """Display calculation history."""

    if not history:
        print("\nNo calculation history available.")
        return

    print("\n========== HISTORY ==========")

    for number, calculation in enumerate(history, start=1):
        print(f"{number}. {calculation}")

    print("=============================")


def main():
    history = []

    print("\n======================================")
    print("        PYTHON CLI CALCULATOR")
    print("======================================")
    print("Supported operations:")
    print("  +   Addition")
    print("  -   Subtraction")
    print("  *   Multiplication")
    print("  /   Division")
    print("  //  Floor Division")
    print("  %   Modulus")
    print("  **  Power")
    print("  ()  Parentheses")
    print("--------------------------------------")
    print("Commands:")
    print("  history  - Show calculation history")
    print("  clear    - Clear calculation history")
    print("  help     - Show commands")
    print("  exit     - Exit calculator")
    print("======================================")

    while True:

        expression = input("\nCalculator >>> ").strip()

        # Exit
        if expression.lower() in ["exit", "quit", "q"]:
            print("\nThank you for using the calculator!")
            break

        # History
        elif expression.lower() == "history":
            show_history(history)

        # Clear history
        elif expression.lower() == "clear":
            history.clear()
            print("History cleared successfully.")

        # Help
        elif expression.lower() == "help":
            print("\nAvailable commands:")
            print("  history  -> Display previous calculations")
            print("  clear    -> Clear calculation history")
            print("  help     -> Display help")
            print("  exit     -> Exit the program")

        # Empty input
        elif expression == "":
            print("Please enter an expression.")

        # Calculation
        else:
            try:
                result = evaluate(expression)

                calculation = f"{expression} = {result}"
                history.append(calculation)

                print(f"Result: {result}")

            except ZeroDivisionError:
                print("Error: Division by zero is not allowed.")

            except (SyntaxError, ValueError):
                print("Error: Invalid expression.")
                print("Example: 10 + 5 * 2")

            except Exception as error:
                print(f"Error: {error}")


if __name__ == "__main__":
    main()