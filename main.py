import settings
from classes.Rule import Rule


def main() -> None:
    Rule.process_all(settings.rules)
    exit()


if __name__ == '__main__':
    main()
