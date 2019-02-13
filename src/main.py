from ui.root import UnoCardGame


def main():
    app = UnoCardGame()
    app.mainloop()


if __name__ == "__main__":
    main()


# TODO New features
# When the deck is empty and no one is able to play a card
# the game should end in draw automatically.
