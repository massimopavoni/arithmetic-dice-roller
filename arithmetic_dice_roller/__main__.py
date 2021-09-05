from arithmetic_dice_roller.roller import Roller, RollerError


def main():
    command = input()
    args = command.split(' ')
    roller = Roller()
    try:
        if len(args) > 1:
            roller.roll(args[0], args[1])
        else:
            roller.roll(args[0])
        print(roller.expression)
        print(roller.no_nx_expression)
        print(roller.rolls)
        print(roller.no_dices_expression)
        print(roller.final_result)
    except RollerError as error:
        print(error.message)


if __name__ == '__main__':
    main()
