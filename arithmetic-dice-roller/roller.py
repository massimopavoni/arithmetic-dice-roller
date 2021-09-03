import re
from random import choices


class Roller:
    def __init__(self):
        self.expression = ''
        self.nx_regex = re.compile(r'([1-9]\d*)x\(([0-9()+\-*/%d]*)\)')
        self.rolls_regex = re.compile(r'([1-9]\d*)d([1-9]\d*)')

    def roll(self, expression, label=''):
        self.expression = expression
        no_nx_expression = self.__parse_x_times()
        no_rolls_expression, rolls = self.__replace_rolls(no_nx_expression)
        print(self.expression)
        print(no_nx_expression)
        print(rolls)
        print(no_rolls_expression)

    def __parse_x_times(self):
        nx_operators = self.nx_regex.findall(self.expression)
        return self.nx_regex.sub('({})', self.expression).format(
            *['+'.join([nxo[1]] * int(nxo[0])) for nxo in nx_operators])

    def __replace_rolls(self, expression):
        dices = self.rolls_regex.findall(expression)
        rolls = []
        for dice in dices:
            rolls.append([0, choices(range(1, int(dice[1]) + 1), k=int(dice[0]))])
            rolls[-1][0] = sum(rolls[-1][1])
        return self.rolls_regex.sub('{}', expression).format(*[roll[0] for roll in rolls]), rolls


if __name__ == '__main__':
    command = input().lower()
    args = command.split(' ')
    roller = Roller()
    if len(args) > 1:
        roller.roll(args[0], args[1])
    else:
        roller.roll(args[0])
