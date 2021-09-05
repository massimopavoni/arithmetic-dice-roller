import re
from random import choices

from sympy import parse_expr


class RollerError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class Roller:
    def __init__(self):
        self.expression = ''
        self.__nx_regex = re.compile(r'([1-9]\d*)x\(')
        self.__dices_regex = re.compile(r'([1-9]\d*)[dD]([1-9]\d*|[fF%](?!\d))')
        self.no_nx_expression = ''
        self.rolls = []
        self.no_dices_expression = ''
        self.final_result = None

    def roll(self, expression, label=''):
        self.expression = expression
        self.no_nx_expression = self.__parse_nx_operators(self.expression)
        self.no_dices_expression, self.rolls = self.__parse_dices(self.no_nx_expression)
        try:
            self.final_result = int(parse_expr(self.no_dices_expression))
        except Exception as ex:
            raise RollerError(f"Roller error -> Could not parse arithmetic expression.\n"
                              f"An exception of type {type(ex).__name__} occurred. Arguments:\n{ex.args}")

    def __parse_nx_operators(self, expression):
        nx_operators = [[m.group(1), [m.start(), m.end() - 1]] for m in self.__nx_regex.finditer(expression)]
        for nxo in nx_operators[::-1]:
            nxo[1].append(nxo[1][1] + self.__find_closing_bracket(expression[nxo[1][1]:]))
            inner_expression = expression[nxo[1][1]:nxo[1][2] + 1]
            expression = "{}({}{}".format(expression[:nxo[1][0]], '+'.join([inner_expression] * int(nxo[0])),
                                          expression[nxo[1][2]:])
        return expression

    @staticmethod
    def __find_closing_bracket(string):
        counter = 0
        for index, character in enumerate(string):
            if character == '(':
                counter += 1
            elif character == ')':
                counter -= 1
            if counter == 0:
                return index
        raise RollerError("Roller error -> Could not match balanced parentheses.")

    def __parse_dices(self, expression):
        dices = self.__dices_regex.findall(expression)
        rolls = []
        for dice in dices:
            dice_amount = int(dice[0])
            if dice[1].lower() == 'f':
                dice_amount *= 4
                dice_type = range(-1, 2)
            elif dice[1] == '%':
                dice_type = range(1, 101)
            else:
                dice_type = range(1, int(dice[1]) + 1)
            rolls.append([0, choices(dice_type, k=dice_amount)])
            rolls[-1][0] = sum(rolls[-1][1])
        return self.__dices_regex.sub('{}', expression).format(*[roll[0] for roll in rolls]), rolls
