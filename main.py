import settings


def main() -> None:
    for rule in settings.rules:
        rule.run()
    exit()


if __name__ == '__main__':
    main()
