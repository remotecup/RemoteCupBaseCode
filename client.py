import conf


if conf.game == 'Simple':
    import Games.Simple.Client.Python.Client as Client
elif conf.game == 'Snake':
    import Games.Snake.Client.Python.Client as Client


def main():
    Client.run()


if __name__ == "__main__":
    main()
