import random
from config import Config
from deck import Deck
from player import Player
from feed import Feed


class Game:

    def __init__(self):
        """This class contais the logic of the UNO card game.
        """
        self.players = []
        self.draw_deck = Deck()
        self.discard_deck = Deck()
        self.colors = Config.CARD_COLORS
        self.wc_color = Config.SPECIAL_COLOR # wc = wildcard
        self.feed = Feed(50)

        self._init_game_variables()

    def _init_game_variables(self):
        """This method is called at the beginning of
        every game."""
        self.round_num = 1
        self.in_turn = 0
        self._starting_player = 0
        self._game_direction = 1
        self.card_drawn = False
        self.card_drawn_computer = False
        self.turn_played = False
        self.turn_played_computer = False
        self.round_played = False
        self.game_played = False
        
        # True if the next players turn is going to be passed.
        self.passing = False
        self.color_queried = False

    def create_player(self, name, is_computer):
        """Create a new player to the game.
        
        :param name: Name of the player
        :param is_computer: Define if a player is controlled
                            by the player or automatically."""
        self.players.append(Player(name, is_computer))

    def start_first_game(self):
        self.player_qty = len(self.players)
        self.winning_points = Config.WINNING_POINTS
        self.play_game()

    def start_new_game(self):
        for player in self.players:
            player.resetoi()
        self._init_game_variables()
        self.play_game()

    def start_new_round(self):
        self._game_direction = 1
        self.color_queried = False
        self.passing = 0
        self.play_game()

    def play_game(self):
        state = "game" if self.round_num == 1 else "round"
        self.feed.add_msg(
            f"New {state} begins. Round number is {self.round_num}.")
        self.round_played = False
        self.draw_deck.create_deck()
        self.draw_deck.shuffle()
        self._deal_starting_cards()
        self.draw_deck.turn_deck()
        self._deal_first_card_to_discard_deck()

        if self.round_num > 1:
            self._define_starting_player()

        if self.in_turn != 0:
            self._play_computer_turns()

    def _define_starting_player(self):
        if self._starting_player < self.player_qty - 1:
            self._starting_player += 1
            self.in_turn = self._starting_player
        else:
            self._starting_player, self.in_turn = 0, 0

    def _get_player_in_turn(self):
        return self.players[self.in_turn]

    def _get_next_player(self):
        """Returns the next player.
        """
        if self._game_direction == 1:

            if self.in_turn < self.player_qty - 1:
                return self.players[self.in_turn + 1]
            else:
                return self.players[0]

        else:
            if self.in_turn == 0:
                return self.players[self.player_qty - 1]
            else:
                return self.players[self.in_turn - 1]

    def _next_player(self):
        """Used for changing the turn.
        """
        if self._game_direction == 1:

            if self.in_turn == self.player_qty - 1:
                self.in_turn = 0
            else:
                self.in_turn += 1

        else:
            if self.in_turn == 0:
                self.in_turn = self.player_qty - 1
            else:
                self.in_turn -= 1

    def _deal_starting_cards(self):
        """Deal starting hands to all players
        in game.
        """
        for _ in range(0, 7):
            for player in self.players:
                player.draw_card(self.draw_deck.deal_card())
        for player in self.players:
            player.get_hand().sort()

    def _deal_first_card_to_discard_deck(self):
        """Deal first card to the discard deck.
        The first can't be an action card.
        """
        while True:
            starting_card = self.draw_deck.deal_card()

            if starting_card.get_value() > 9:
                self.draw_deck.add_card(starting_card)
                continue

            self.discard_deck.add_card(starting_card)
            break

    def _destroy_all_hands(self):
        """After every round the hands are destroyed.
        """
        for player in self.players:
            player.destroy_hand()

    def play_card(self, card):
        """This method is called from ui.py file when 
        the player clicks a card in his hand.
        """
        self.turn_played_computer = False
        player = self._get_player_in_turn()
        card = player.get_hand()[card]
        self._play_card(card)

        self._execute_win_check(player)
        if self.round_played:
            return

        if self.turn_played:
            self._pass_turn_to_computer()

    def draw_card(self):
        self._draw_card()

    def pass_turn(self):
        self.turn_played_computer = False
        self._pass_turn()

        if self.turn_played:
            self._pass_turn_to_computer()

    def pass_players_turn(self):
        self.turn_played_computer = False
        self.passing = False
        self.feed.add_msg(f"Players turn has been passed.")
        self._pass_turn_to_computer()

    def receive_color(self, color):
        """Receive wildcard color from GUI.
        """
        self.color_queried = False
        self.turn_played = True
        self.wc_color = color
        self.feed.add_msg(f"Wild Card color is {color}.")
        self._pass_turn_to_computer()

    def _pass_turn_to_computer(self):
        self._next_player()
        self._play_computer_turns()

    def _end_turn(self, player):
        self.card_drawn_computer = False
        self.turn_played_computer = False
        winner = self._execute_win_check(player)
        self._next_player()
        return winner

    def _play_computer_turns(self):
        """The method runs after the player has completed
        his turn and plays all of the computer players turns.

        Computer first tries to draw a card, then he tries to play
        one of the cards in his hand and if no card is played,
        the computer passes his turn.
        """
        while self.in_turn != 0:
            computer = self._get_player_in_turn()

            if self.passing:
                self._next_player()
                self.passing = False
                self.feed.add_msg(
                    f"{computer.get_name()}'s turn has been passed.")
                continue

            hand = computer.get_hand()
            random.shuffle(hand)
            self._draw_card()

            for card in hand:
                self._play_card(card)

                if self.color_queried:
                    self.wc_color = random.choice(self.colors)
                    self.feed.add_msg(f"Wild Card color is {self.wc_color}.")
                    self.color_queried = False

                if self.turn_played_computer:
                    break

            else:
                self._pass_turn()

            voittaja = self._end_turn(computer)
            if voittaja:
                break

        self.turn_played_computer = True
        self.turn_played = False
        self.card_drawn = False
        self.players[0].get_hand().sort()

    def _execute_win_check(self, player):
        if self._check_winner(player):
            self._count_points()
            self._destroy_all_hands()
            self.feed.add_msg(
                f"Round {self.round_num} ended. The winner is {player.get_name()}.")
            self.round_num += 1
            self.round_played = True

            if self._check_winning_points():
                self.game_played = True

            return player

    def _draw_card(self):
        player = self._get_player_in_turn()

        if self._approve_draw():
            player.draw_card(self.draw_deck.deal_card())

            if not player.is_computer():
                player.get_hand().sort()

    def _approve_draw(self):
        """The method checks if the player can has the right
        to draw a card. The player is not allowed to draw
        a new card, if one or more cards in his hand
        could be played.

        The player can't draw more than one card during
        his turn.
        """
        player = self._get_player_in_turn()
        hand = player.get_hand()

        for card in hand:

            # check if player has a card that could be played
            if self._approve_played_card(card):
                return False

        # check if player has already drawn a card
        if self.card_drawn and not player.is_computer():
            return False

        # check if computer has already drawn a card
        if self.card_drawn_computer and player.is_computer():
            return False

        self.feed.add_msg(f"{player.get_name()} draws a card.")
        self.card_drawn = True

        if player.is_computer():
            self.card_drawn_computer = True

        return True

    def _pass_turn(self):
        player = self._get_player_in_turn()

        if self.card_drawn or len(self.draw_deck) == 0:
            self.feed.add_msg(f"{player.get_name()} passes.")
            self.turn_played = True
            
        if player.is_computer() and (self.card_drawn_computer or 
                                     len(self.draw_deck) == 0):
            self.turn_played_computer = True

    def _play_card(self, card):
        """Method executes actions related to the played card.
        """
        player = self._get_player_in_turn()
        if self._approve_played_card(card):

            # reset wild card color
            if self.wc_color != Config.SPECIAL_COLOR:
                self.wc_color = Config.SPECIAL_COLOR

            if card.action:
                self._process_action_card(card)

            player.play_turn(card)
            self.discard_deck.add_card(card)

            if not self.color_queried:
                self.turn_played = True

            self.feed.add_msg(f"{player.get_name()} played a {card} card.")

            if player.is_computer():
                self.turn_played_computer = True

    def _approve_played_card(self, played_card):
        """Check if the played card is allowed.
        """
        cmp_card = self.discard_deck.get_last_card()

        if (played_card.compare_color(cmp_card) or
                played_card.compare_value(cmp_card) or
                played_card.compare_to_wildcard(self.wc_color) or
                played_card.is_wildcard()):
            return True

        return False

    def _process_action_card(self, played_card):
        """Execute operations related to action cards.
        """
        # ohitus
        if played_card.get_value() == 10:
            self.passing = True

        # suunnanvaihto
        elif played_card.get_value() == 11:
            self._change_direction()

        # nosta 2
        elif played_card.get_value() == 12:
            self.passing = True
            next_player = self._get_next_player()

            for _ in range(0, 2):
                next_player.draw_card(self.draw_deck.deal_card())

        elif played_card.get_value() == 13 or played_card.get_value() == 14:
            self._process_wild_card(played_card)

    def _process_wild_card(self, played_card):
        self.color_queried = True

        if played_card.get_value() == 14:
            self.passing = True
            next_player = self._get_next_player()

            for _ in range(0, 4):
                next_player.draw_card(self.draw_deck.deal_card())

    def _change_direction(self):
        self._game_direction *= -1

    def _check_winner(self, player):
        """Check if there are cards left in the players hand.
        If not, the player wins."""
        if len(player.get_hand()) == 0:
            player.wins()
            return True
        else:
            return False

    def _count_points(self):
        winner = self._get_player_in_turn()
        for player in self.players:
            for card in player.get_hand():
                winner.add_points(card.get_points())

    def _check_winning_points(self):
        """Check if one of the players has reached the point
        amount needed for a win.
        """
        for player in self.players:

            if player.get_points() >= self.winning_points:
                self.feed.add_msg(f"{player.get_name()} wins the game!")

                return True
            return False
