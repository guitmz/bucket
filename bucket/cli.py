from prompt_toolkit import prompt
from prompt_toolkit.history import InMemoryHistory
from prompt_toolkit.contrib.completers import WordCompleter
from bucket.cmdparser import CmdParser
from bucket.const import AVAILABLE_COMMANDS


command_completer = WordCompleter(
    AVAILABLE_COMMANDS,
    ignore_case=True
)


def main():
    history = InMemoryHistory()
    parser = CmdParser()
    try:
        print('Bucket v1.0 - Welcome!')
        print('If you press esc-!, you can enter system commands.')
        while True:
            cmd = prompt(">_ ",
                         history=history,
                         completer=command_completer,
                         complete_while_typing=False,
                         enable_system_bindings=True)
            if cmd:
                parser.parse(cmd)
    except (EOFError, KeyboardInterrupt):
        print('GoodBye!')
