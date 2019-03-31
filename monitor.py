import conf


if conf.game == 'Simple':
    import Games.Simple.Monitor.NaderMon as Monitor
elif conf.game == 'Snake':
    import Games.Snake.Monitor.Monitor as Monitor


def main():
    Monitor.run()


if __name__ == "__main__":
    main()
