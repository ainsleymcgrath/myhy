"""Provide an API for implementing a LISP.

Public API is the Lisp() class.
An instance of Lisp() is a registry for any lisp operators (aka functions) that you
want available in s-expressions.

Take this idiotic language for example:
    lisp = Lisp()

    @lisp.operator
    def scream(*args):
        return 'AAAAAHHHHHHH'

    @lisp.operator
    def lose_it(*args):
        return 'I AM LOSING IT'

The above would get you a lisp that has 2 varidaic functions.
Functions in lisp share the name of their python implementations.

    lisp.evalute('(hey)')  ==  'hey'
    lisp.evaluate('(scream 1 2 a b)') == 'AAAAAHHHHHHH'
    lisp.evaluate('(lose_it (123))') == 'I AM LOSING IT'

Rules & quirks:
    - Everything is understood as strings and your functions will have to deal
        with any and all type conversion.
    - An s-expression containing a single atom unwraps to that atom.
        i.e. (1) evaluates to 1
    - An s-expression containing multiple elements evaluates every element.
        Atoms stay atoms.
        i.e. (hey (sup) (hey hi) (scream 1)) evaluates to:
            ["hey", "sup", ["hey", "hi"], "SCREAM"]

See unit tests for more info.
"""


import re
from functools import partial

S_EXPRESSION = re.compile(r"^\((.*)\)$")
SPACE = " "
LEFT_PAREN = "("
RIGHT_PAREN = ")"


def unwrap(expression):
    """Take the parens of a string-represntation of an s-experssion.
    If it's not an s-expression, just return the string."""
    match = S_EXPRESSION.match(expression)
    if match is not None:
        return match.group(1)
    return expression


def is_s_expr(expression):
    """Predicate to see if a string is an s-expression."""
    chars = list(expression)
    first_char, last_char = chars[0], chars[-1]
    return first_char == LEFT_PAREN and last_char == RIGHT_PAREN


def take_til_end_s_expr(it):
    """Slight jank. Take elements from a string iterator until right paren seen."""
    nested_s_expr = ""
    found_end = False

    while not found_end:
        nxt = next(it, "")
        nested_s_expr += nxt
        if nxt == LEFT_PAREN:
            # a more deeply nested expr!
            nested_s_expr += take_til_end_s_expr(it)
            continue

        if nxt == RIGHT_PAREN or nxt == "":
            found_end = True

    return nested_s_expr


def elements(expression):
    """Break out the elements of an s-expression into a list of strings.
    List members are either atoms or (string representations of) s-expressions."""
    output = []
    build_el = []
    it = iter(unwrap(expression))

    for char in it:
        if char == LEFT_PAREN:
            nested_s_expr = take_til_end_s_expr(it)
            output.append(LEFT_PAREN + nested_s_expr)
            continue

        if char != SPACE:
            build_el.append(char)
            continue

        if len(build_el):
            if char == SPACE:
                output.append("".join(build_el))
                build_el = []
                continue

    if len(build_el):
        lastel = "".join(build_el)
        output.append(lastel)

    return output


class Lisp:
    """Use an instance to register plain functions as keywords in your mini language.
    After registration, `.evaluate()` is the public API for parsing and executing
    s-expressions.
    """

    def __init__(self):
        self._operators = {}

    def operator(self, func=None, name=None):
        """Decorate functions so they become functions in your mini language."""
        if func is None and name is not None:
            return partial(self.operator, name=name)

        self._operators[name or func.__name__] = func
        return func

    def evaluate(self, expression):
        """Evaluate an s-expression, using any registered functions as intended."""
        els = elements(expression)
        if els == []:
            return None

        first, *rest = els

        if is_s_expr(first):
            return self.evaluate(first)

        if first in self._operators:
            fn = self._operators[first]
            args = map(self.evaluate, rest)
            return fn(*args)

        if len(rest):
            return [self.evaluate(r) for r in els]

        return first