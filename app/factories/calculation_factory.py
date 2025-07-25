## calculation_factory.py
## IS 601 Module 11
## Evan Garvey

from app.operations import add, subtract, multiply, divide

class OperationFactory:
    @staticmethod
    def get_operation(operator: str):
        if operator == 'add':
            return add
        elif operator == 'subtract':
            return subtract
        elif operator == 'multiply':
            return multiply
        elif operator == 'divide':
            return divide
        else:
            raise ValueError(f"Unsupported operation: {operator}")