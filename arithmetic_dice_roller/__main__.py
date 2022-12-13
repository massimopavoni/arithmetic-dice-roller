"""
arithmetic-dice-roller
Copyright (C) 2021  Massimo Pavoni

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

from argparse import ArgumentParser
from importlib import metadata

from arithmetic_dice_roller.roller import Roller, RollerError

parser = ArgumentParser(prog=metadata.metadata('arithmetic-dice-roller')['name'],
                        description=metadata.metadata('arithmetic-dice-roller')['summary'])
parser.add_argument('-v', '--version', action='version',
                    version=f"%(prog)s {metadata.version('arithmetic-dice-roller')}")
parser.add_argument('expression', help="The expression to evaluate.")
parser.add_argument('label', nargs='*', default='', help="A label to associate with the expression.")


def main():
    args = parser.parse_args()
    roller = Roller(args.expression, ' '.join(args.label))
    try:
        roller.roll()
        if roller.label:
            print(f"\nLabel: {roller.label}")
        print(f"\nOriginal expression: {roller.expression}\n"
              f"\nExpanded expression: {roller.no_nx_expression}\n"
              f"\nRolls:\n" + '\n'.join(f" - {roll}" for roll in roller.rolls) + '\n' +
              f"\nEvaluated expression: {roller.no_dice_expression}\n"
              f"\nFinal result: {roller.final_result}\n")
    except RollerError as error:
        print(error.message)


if __name__ == '__main__':
    main()
