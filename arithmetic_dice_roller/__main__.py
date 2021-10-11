from arithmetic_dice_roller.roller import Roller, RollerError


def main():
    command = input()
    args = command.split(' ', 1)
    roller = Roller()
    try:
        if len(args) > 1:
            roller.roll(args[0], args[1])
        else:
            roller.roll(args[0])
        print(f"Label: {roller.label}\nOriginal expression: {roller.expression}\n"
              f"Expanded expression: {roller.no_nx_expression}\nRolls: {roller.rolls}\n"
              f"Evaluated expression: {roller.no_dice_expression}\nFinal result: {roller.final_result}")
    except RollerError as error:
        print(error.message)


if __name__ == '__main__':
    main()
