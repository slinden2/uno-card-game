class Config:

    # UI
    ICON = "cards/icon.ico"
    LOGO = "cards/logo.png"
    BACK_OF_CARD_NORMAL = "cards/back.png"
    BACK_OF_CARD_LEFT = "cards/back_vert_left.png"
    BACK_OF_CARD_RIGHT = "cards/back_vert_right.png"
    BACK_OF_CARD_TOP = "cards/back_horiz_top.png"
    TITLE_FONT = {"family": "Helvetica",
                  "size": 50,
                  "weight": "bold"}
    SETTING_FONT = {"family": "Helvetica",
                    "size": 18}
    HELP_TITLE = {"family": "Helvetica",
                  "size": 18,
                  "underline": 1}
    ROUND_FONT = {"family": "Helvetica",
                  "size": 18,
                  "weight": "bold"}
    POINT_FONT = {"family": "Helvetica",
                  "size": 12}

    # HELP
    PARAGRAPH_1 = "The aim of the game is to be the first player to score 20 - 500 points, achieved (usually over several rounds of play) by being the first to play all of one's own cards and scoring points for the cards still held by the other players."
    PARAGRAPH_2 = "The deck consists of 108 cards: four each of \"Wild\" and \"Wild Draw Four,\" and 25 each of four different colors (red, yellow, green, blue). Each color consists of one zero, two each of 1 through 9, and two each of \"Skip,\" \"Draw Two,\" and \"Reverse.\" These last three types are known as \"action cards.\""
    PARAGRAPH_3 = "To start a hand, seven cards are dealt to each player, and the top card of the remaining deck is flipped over and set aside to begin the discard pile. The player to the dealer's left plays first unless the first card on the discard pile is an action or Wild card (see below). On a player's turn, they must do one of the following:"
    BULLET_1 = "• play one card matching the discard in color, number, or symbol"
    BULLET_2 = "• play a Wild card, or a playable Wild Draw Four card (see restriction below)"
    BULLET_3 = "• draw the top card from the deck, then play it if possible"
    HELP_TABLE = [("Card", "Effect when played from hand", "Effect as first card"),
                  ("Skip", "Next player in sequence misses a turn",
                   "Player to dealer's left misses a turn"),
                  ("Reverse", "Order of play switches directions (clockwise to counterclockwise, or vice versa)	",
                   "Dealer plays first; play proceeds counterclockwise"),
                  ("Draw Two (+2)", "Next player in sequence draws two cards and misses a turn",
                   "Player to dealer's left draws two cards and misses a turn"),
                  ("Wild", "Player declares the next color to be matched (may be used on any turn even if the player has matching color)",
                   "Player to dealer's left declares the first color to be matched and plays a card in it"),
                  ("Wild Draw Four/Draw Four Wild (+4 and wild)", "Player declares the next color to be matched; next player in sequence draws four cards and misses a turn. May be legally played only if the player has no cards of the current color (see Penalties).", "Return card to the deck, shuffle, flip top card to start discard pile")]
    PARAGRAPH_4 = "Cards are played by laying them face-up on top of the discard pile. Play proceeds clockwise around the table."
    PARAGRAPH_5 = "Action or Wild cards have the following effects:"
    LINK_TEXT = "Wikipedia"
    HELP_LINK = "https://en.wikipedia.org/wiki/Uno_(card_game)"
    HELP_TABLE_TITLE = {"size": 10,
                        "weight": "bold"}

    # GAME
    CARD_COLORS = ["red", "yel", "gre", "blu"]
    SPECIAL_COLOR = 'spc'
    PLAYER_QTY = 2
    WINNING_POINTS = 500
    CARD_PATH = "cards/"
