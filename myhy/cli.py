from argparse import ArgumentParser
from importlib import import_module

from myhy import Lisp

_parser = ArgumentParser()
_parser.add_argument("lisp_instance", help="A Python module.path.to:your_lisp.")
_parser.add_argument(
    "-c", "--code", dest="code", help="Run the given string as DSL code."
)


class ParsedCliDependencies:
    code: str
    lisp: Lisp

    def __init__(self, parser: ArgumentParser) -> None:
        args = parser.parse_args()
        lisp_path: str = args.lisp_instance
        lisp_module, lisp_instance = lisp_path.split(":")

        self.code: str = args.code
        try:
            self.lisp: Lisp = getattr(import_module(lisp_module), lisp_instance)
        except ModuleNotFoundError:
            print(f"No such module '{lisp_module}'")
        except AttributeError:
            print(f"No attribute '{lisp_instance}' in module '{lisp_path}'")


def cli() -> None:
    deps = ParsedCliDependencies(_parser)
    result = deps.lisp.evaluate(deps.code)
    print(result)
