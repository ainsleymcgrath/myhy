"""Test the functionality from urlquery.py."""
import pytest

from myhy import Lisp


@pytest.fixture
def simple_lisp():
    """Add some simple operators to a Lisp()."""
    lisp = Lisp()

    @lisp.operator
    def eq(*args):
        normalized = (int(a) if str(a).isdigit() else a for a in args)
        return len(set(normalized)) == 1

    @lisp.operator
    def add(*args):
        try:
            return sum(map(int, args))
        except ValueError:
            return "".join(args)

    @lisp.operator(name="lol")
    def laugh(*_):
        return "hahaha"

    return lisp


@pytest.mark.parametrize(
    "expression, expected",
    [
        ("(add 2 4)", 6),
        ("(add (add 2 8) 4)", 14),
        ("(eq 1 2)", False),
        ("(eq 3 (add 1 2) (add 3 0))", True),
        ("(eq pee pee)", True),
        ("()", None),
        ("(fart heart (eq 3 (add 1 2)) art)", ["fart", "heart", True, "art"]),
        ("(add har dee har)", "hardeehar"),
        ("(sup)", "sup"),
        # quirk! single-item s-expressions evaluate to their contents
        ("(sup (pup) (up up))", ["sup", "pup", ["up", "up"]]),
        # try a func with a configured name
        ("(lol wheeeee)", "hahaha"),
        ("(laugh 1)", ["laugh", "1"]),
    ],
)
def test_simple_lisp(simple_lisp, expression, expected):
    """Verify the outputs of s-expressions in the configured lisp."""
    actual = simple_lisp.evaluate(expression)
    assert expected == actual
