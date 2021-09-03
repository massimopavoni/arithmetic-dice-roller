from arithmetic_dice_roller.roller import Roller


def main():
    command = input().lower()
    args = command.split(' ')
    roller = Roller()
    if len(args) > 1:
        roller.roll(args[0], args[1])
    else:
        roller.roll(args[0])


if __name__ == '__main__':
    main()
