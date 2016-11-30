from prompt_toolkit import prompt
from prompt_toolkit.history import InMemoryHistory
from bucket.cmdparser import CmdParser


def main():
    history = InMemoryHistory()
    parser = CmdParser()
    try:
        while True:
            cmd = prompt(">_ ", history=history)
            parser.parse(cmd)
    except (EOFError, KeyboardInterrupt):
        print('GoodBye!')


if __name__ == '__main__':
    main()
