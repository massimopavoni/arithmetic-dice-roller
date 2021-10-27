from arithmetic_dice_roller.roller import Roller, RollerError


def main():
    command = input()
    args = command.split(' ', 1)
    try:
        if len(args) == 1:
            if not args[0]:
                print("\nUsage:\n  arithmetic-dice-roller <expression> [label]\n\n"
                      f"Check syntax: https://github.com/Damax00/arithmetic-dice-roller/blob/main/README.md#Syntax")
                return
            roller = Roller(args[0])
        else:
            roller = Roller(args[0], args[1])
        roller.roll()
        print(f"\nLabel: {roller.label}\nOriginal expression: {roller.expression}\n"
              f"Expanded expression: {roller.no_nx_expression}\nRolls:\n" +
              '\n'.join(f" - {roll}" for roll in roller.rolls) +
              f"\nEvaluated expression: {roller.no_dice_expression}\nFinal result: {roller.final_result}")
    except RollerError as error:
        print(error.message)


if __name__ == '__main__':
    main()
