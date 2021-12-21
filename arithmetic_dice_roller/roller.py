from heapq import nlargest, nsmallest
from operator import eq as operator_eq, le as operator_le, ge as operator_ge
from random import choice as random_choice, choices as random_choices
from re import compile as regex_compile

from sympy import parse_expr as sympy_parse_expr


class RollerError(Exception):
    """
    Roller exception handling.
    """

    def __init__(self, message):
        """
        Class init function
        :param message: the message to deliver
        """
        self.message = message
        super().__init__(self.message)


class Roller:
    """
    Parsing and evaluation of arithmetic expressions with dice syntax and various operators.
    Attributes:
        expression: the original expression given in input
        no_nx_expression: the expression in its extended form, without the repeater operator 'nx'
        rolls: the list of dice results
        no_dice_expression: the expression without dice syntax, which is replaces with the total results
        final_result: the evaluation of the expression
        label: an optional description for the expression
    """

    def __init__(self, expression, label=''):
        """
        Class init function
        :param expression: the expression itself
        :param label: an optional description for the expression
        """
        self.__nx_regex = regex_compile(r'([1-9]\d*)x\(')
        self.__dice_regex = regex_compile(
            r'(([1-9]\d*)?[dD]([1-9]\d*|[fF%](?!\d))(?:([KkXxRr!])(?:(?:(?:(?<=[Rr!])(<=|>=))?([1-9]\d*))?)|(<=|>=)([1-9]\d*)(?:[fF](<=|>=)([1-9]\d*))?)?)')
        self.__comparison_operators = {
            '': operator_eq,
            '<=': operator_le,
            '>=': operator_ge
        }
        self.expression = expression
        self.no_nx_expression = ''
        self.rolls = []
        self.no_dice_expression = ''
        self.final_result = None
        self.label = label

    def roll(self):
        """
        Parse and evaluate an arithmetic expression with dice syntax and various operators.
        :return: nothing
        """
        self.no_nx_expression = self.__parse_nx_operators(self.expression)
        self.no_dice_expression, self.rolls = self.__parse_dice(self.no_nx_expression)
        try:
            self.final_result = int(sympy_parse_expr(self.no_dice_expression))
        except Exception as ex:
            # If sympy fails to evaluate the final expression, the syntax was not followed
            # (some dice substrings were not replaced)
            raise RollerError(f"\nRoller error -> Could not parse following arithmetic expression:\n"
                              f"{self.no_dice_expression}\nA syntax check is advised "
                              f"(https://github.com/massimopavoni/arithmetic-dice-roller/blob/main/README.md#Syntax)\n"
                              f"An exception of type {type(ex).__name__} occurred. Arguments:\n{ex.args}\n")

    def __parse_nx_operators(self, expression):
        """
        Extract extended for of the expression by repeating the correct sub-expression.
        :param expression: the expression to extend
        :return: the extended expression
        """
        # Create a list from the matches with the number of repetitions and the indexes of the substring
        nx_operators = [[m.group(1), [m.start(), m.end() - 1]] for m in self.__nx_regex.finditer(expression)]
        # Expression is extended from right to left to avoid changing indexes
        for nxo in nx_operators[::-1]:
            # Append the index of the correct closing bracket
            nxo[1].append(nxo[1][1] + self.__find_closing_bracket(expression[nxo[1][1]:]))
            # Get expression to repeat
            inner_expression = expression[nxo[1][1]:nxo[1][2] + 1]
            # Extend
            expression = "{}({}{}".format(expression[:nxo[1][0]], '+'.join([inner_expression] * int(nxo[0])),
                                          expression[nxo[1][2]:])
        return expression

    @staticmethod
    def __find_closing_bracket(string):
        """
        Find correct closing bracket iteratively.
        :param string: the substring in which to search the correct closing bracket
        :return: the index of the closing bracket found
        """
        # Just using a counter to match balanced brackets
        counter = 0
        for index, character in enumerate(string):
            match character:
                case '(':
                    counter += 1
                case ')':
                    counter -= 1
            if counter == 0:
                return index
        # Getting to the end of the substring without returning means that the counter is not 0
        raise RollerError("\nRoller error -> Could not match balanced brackets.")

    def __parse_dice(self, expression):
        """
        Parse dice substrings following the syntax and roll them.
        :param expression: the expression to parse
        :return: tuple of the expression with evaluated rolls and the list of rolls
        """
        # Find all the dice substrings that follow dice syntax
        dice_groups = self.__dice_regex.findall(expression)
        rolls = []
        for dice_groups in dice_groups:
            # Parse number and type of dice
            dice_amount = 1 if not dice_groups[1] else int(dice_groups[1])
            is_fudge = False
            match dice_groups[2].lower():
                # Fudge
                case 'f':
                    dice_type = range(-1, 2)
                    is_fudge = True
                # Percentage
                case '%':
                    dice_type = range(1, 101)
                # All the others
                case _:
                    dice_type = range(1, int(dice_groups[2]) + 1)
            # Operators that need to check each roll after it has been evaluated
            if dice_groups[3] in ['R', 'r', '!']:
                comparison_operator = self.__comparison_operators[dice_groups[4]]
                if not dice_groups[5]:
                    if dice_groups[3] == '!':
                        comparison_value = 4 if is_fudge else dice_type.stop - 1
                    else:
                        comparison_value = -4 if is_fudge else 1
                else:
                    comparison_value = int(dice_groups[5])
                rolls.append(self.__reroll(dice_amount, dice_type, is_fudge,
                                           dice_groups[3], comparison_operator, comparison_value))
            else:
                # In all the other cases all the rolls are immediately evaluated
                results = []
                if is_fudge:
                    rolls.append([0, [[0, random_choices(dice_type, k=4)] for _ in range(0, dice_amount)]])
                    for i, roll in enumerate(rolls[-1][1]):
                        results.append(sum(roll[1]))
                        rolls[-1][1][i][0] = results[-1]
                else:
                    rolls.append([0, random_choices(dice_type, k=dice_amount)])
                    results = rolls[-1][1]
                # Operators that modify the result after having evaluated all the rolls
                keep_drop_amount = 1 if not dice_groups[5] else int(dice_groups[5])
                match dice_groups[3]:
                    # Keep highest
                    case 'K':
                        rolls[-1][0] = sum(nlargest(keep_drop_amount, results))
                    # Keep lowest
                    case 'k':
                        rolls[-1][0] = sum(nsmallest(keep_drop_amount, results))
                    # Drop highest
                    case 'X':
                        rolls[-1][0] = sum(nsmallest(dice_amount - keep_drop_amount, results))
                    # Drop lowest
                    case 'x':
                        rolls[-1][0] = sum(nlargest(dice_amount - keep_drop_amount, results))
                    # Successes/failures or none
                    case _:
                        # Count successes?
                        if dice_groups[6]:
                            comparison_operator = self.__comparison_operators[dice_groups[6]]
                            rolls[-1][0] = sum(map(lambda r: comparison_operator(r, int(dice_groups[7])), results))
                            # Count failures?
                            if dice_groups[8]:
                                comparison_operator = self.__comparison_operators[dice_groups[8]]
                                rolls[-1][0] -= sum(map(lambda r: comparison_operator(r, int(dice_groups[9])), results))
                                if rolls[-1][0] < 0:
                                    rolls[-1][0] = 0
                        else:
                            rolls[-1][0] = sum(results)
            rolls[-1].insert(0, dice_groups[0])
        return self.__dice_regex.sub('{}', expression).format(*[roll[1] for roll in rolls]), rolls

    @staticmethod
    def __reroll(dice_amount, dice_type, is_fudge, dice_operator, comparison_operator, comparison_value):
        """
        Roll with operators that need to check each single result.
        :param dice_amount: the amount of dice to roll
        :param dice_type: the range of the random choice representing the dice
        :param is_fudge: whether the die type is fudge or not
        :param dice_operator: the specified reroll operator
        :param comparison_operator: the type of comparison to check
        :param comparison_value: the value for the comparison
        :return: array with the total result and the partial results
        """
        results = []
        fudge_components = []
        fudge_results = []
        # Each roll must be checked after being evaluated
        for i in range(0, dice_amount):
            # First roll
            if is_fudge:
                fudge_components = random_choices(dice_type, k=4)
                current_result = sum(fudge_components)
            else:
                current_result = random_choice(dice_type)
            # If the comparison is true, reroll occurs
            while comparison_operator(current_result, comparison_value):
                # If it's an exploding dice, partial result needs not to be lost
                if dice_operator == '!':
                    if is_fudge:
                        fudge_results.append([sum(fudge_components), fudge_components])
                    results.append(current_result)
                # In any case, reroll occurs
                if is_fudge:
                    fudge_components = random_choices(dice_type, k=4)
                    current_result = sum(fudge_components)
                else:
                    current_result = random_choice(dice_type)
                # But if it's a reroll once operator, the loop is exited
                if dice_operator == 'r':
                    break
            # Partial result is added
            if is_fudge:
                fudge_results.append([sum(fudge_components), fudge_components])
            results.append(current_result)
        return [sum(results), fudge_results if is_fudge else results]
