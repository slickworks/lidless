import sys


def accept_changes():
    return prompt_yn("Proceed?")


def error(msg):
    print(msg)
    sys.exit(1)


def prompt_yn(msg):
    while True:
        try:
            print("> " + msg + ' (y/n)')
            selection = input("> ").lower()[0]
            assert selection in ('y', 'n')
            return selection == 'y'
        except KeyboardInterrupt:
            quit() 
        except AssertionError:
            print('Enter y or n:')
