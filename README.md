# arithmetic-dice-roller
[![GitHub release (latest by date including pre-releases)](https://img.shields.io/github/v/release/massimopavoni/arithmetic-dice-roller?include_prereleases)](https://github.com/massimopavoni/arithmetic-dice-roller/releases)
[![PyPI Package](https://img.shields.io/pypi/v/arithmetic-dice-roller)](https://pypi.org/project/arithmetic-dice-roller/)
[![GitHub License](https://img.shields.io/github/license/massimopavoni/arithmetic-dice-roller)](https://github.com/massimopavoni/arithmetic-dice-roller/blob/main/LICENSE)
[![GitHub Pipenv locked Python version](https://img.shields.io/github/pipenv/locked/python-version/massimopavoni/arithmetic-dice-roller)](https://www.python.org/downloads/release/python-3100/)

A handy dice roller with extended notation and arithmetic expressions' management.

The package aims to provide an easy-to-use implementation of a dice roller application with multiple operators' options and automatic results calculation.

### Dependencies
- [SymPy](https://www.sympy.org) ([LICENSE](https://github.com/sympy/sympy/blob/master/LICENSE))

### Syntax
Chosen syntax is inspired to the one from the [CritDice mobile app](https://www.critdice.com/) (you can check the [advanced notation](https://www.critdice.com/roll-advanced-dice) for similarities with this package).

The output object once the expression has been evaluated ("rolled") contains:
- the original expression
- the expression without repeated sub-expressions
- the expressions with evaluated dice rolls
- the list of dice rolls (for beautifying purposes)
- the final evaluated result
- the optional label for the whole expression

If the package is being used as a part of another project, you can just import the `Roller` class and use the `roll` function.  
A simple console script (`arithmetic-dice-roller`) is also provided, which requires an input with an expression and an optional label for it, separated by a space.  

Every expression must not present any spaces, and can contain any number of dice rolls (big numbers and complex calculations may affect execution time), given the following format is respected:  
`[dice amount]d[die type][operator]` where **dice number** can be omitted for default 1, **d** is case-insensitive and **dice type** can be any integer, `f` (for fudge die, case-insensitive) or `%` (for percentage, equal to typing in `d100`).  
**Operator** can be of three different types, with only the third omitting some results (because or rerolls):
- keeping or dropping a number of dice (`[K|k|X|x][amount]`, any of the four combinations of keep/drop highest/lowest followed by how many needs to be kept or dropped)
- counting successes and failures (`[<=|>=][success threshold]f[<=|>=][failure threshold]`, any of the two comparison operators and a threshold for success/failure, with **f** being case-insensitive and the failure part being optional)
- rerolling until the condition is satisfied (critics or comparison) or once (`[!|R|r][|<=|>=][threshold]`, any of the three operators for rerolling and any of the three comparison operators, putting none means equality)

Repeating sub-expressions is also supported: these are expanded before any other parsing operations, and can be used to repeat rolls (and not multiply the result) writing the same sub-expression multiple times.  
The format is `[repetitions]x([sub-expression])`, and the sub-expression (and all the expression in general) must have matching brackets.

The final arithmetic expression without dice notation is evaluated using [SymPy](https://www.sympy.org/en/index.html), so any kind of arithmetic operation is allowed inside expressions, to provide a nice tool for complex rolls.

<br>

_Feel free to suggest and submit modifications to this guide, as any kind of help is always very much appreciated and welcomed._