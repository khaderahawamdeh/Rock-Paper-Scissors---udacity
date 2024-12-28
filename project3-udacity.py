"""Engage in a Rock, Paper, Scissors game against different AI players."""

import random

options = ["rock", "paper", "scissors"]


class Participant:
    """Base class for participants in the game."""

    def play(self):
        """Provide the participant's move."""
        return "rock"

    def update(self, own_move, opponent_move):
        """Update knowledge based on the round result."""
        pass


class FixedRockPlayer(Participant):
    """Always chooses 'rock'."""

    def play(self):
        """Provide the participant's move."""
        return "rock"


class RandomMovePlayer(Participant):
    """Selects a random move."""

    def play(self):
        """Return a random move from the options."""
        return random.choice(options)


class UserPlayer(Participant):
    """Handles input for a human participant."""

    def play(self):
        """Get the human player's move via input."""
        while True:
            user_input = (
                input("Choose your move (rock, paper, scissors,"
                      "or 'quit' to stop): ")
                .strip()
                .lower()
            )
            if user_input in options:
                return user_input
            elif user_input in ["quit", "q"]:
                return "quit"
            print(f"'{user_input}' is not valid. Please try again.")


class MirrorPlayer(Participant):
    """Mimics the opponent's previous move."""

    def __init__(self):
        """Initialize MirrorPlayer with no prior move."""
        self.last_opponent_move = None

    def play(self):
        """Play the last opponent's move or a random move initially."""
        if self.last_opponent_move is None:
            return random.choice(options)
        return self.last_opponent_move

    def update(self, own_move, opponent_move):
        """Update the last opponent's move."""
        self.last_opponent_move = opponent_move


class SequentialPlayer(Participant):
    """Cycles through the moves in order."""

    def __init__(self):
        """Initialize SequentialPlayer with no prior move."""
        self.last_move = None

    def play(self):
        """Play the next move in sequence."""
        if self.last_move is None:
            return random.choice(options)
        next_move = (options.index(self.last_move) + 1) % len(options)
        return options[next_move]

    def update(self, own_move, opponent_move):
        """Update the last move played."""
        self.last_move = own_move


def determine_winner(choice1, choice2):
    """Check if choice1 beats choice2."""
    return (
        (choice1 == "rock" and choice2 == "scissors")
        or (choice1 == "scissors" and choice2 == "paper")
        or (choice1 == "paper" and choice2 == "rock")
    )


class Match:
    """Handles the game mechanics."""

    def __init__(self, participant1, participant2):
        """Initialize a new match with two participants."""
        self.participant1 = participant1
        self.participant2 = participant2
        self.score1 = 0
        self.score2 = 0

    def play_turn(self):
        """Execute a single turn of the game."""
        move1 = self.participant1.play()
        if move1 == "quit":
            return False

        move2 = self.participant2.play()
        print(f"Player 1: {move1}  Player 2: {move2}")

        if determine_winner(move1, move2):
            print("Player 1 wins the round!")
            self.score1 += 1
        elif determine_winner(move2, move1):
            print("Player 2 wins the round!")
            self.score2 += 1
        else:
            print("It's a tie this round!")

        print(f"Final Scores -> Player 1: {self.score1}, "
              f"Player 2: {self.score2}")
        self.participant1.update(move1, move2)
        self.participant2.update(move2, move1)
        return True

    def start_game(self):
        """Start and manage the complete game flow."""
        print("Let the game begin!")
        round_count = 1
        while True:
            print(f"Round {round_count}:")
            if not self.play_turn():
                break
            round_count += 1

        print("Game over!")
        print(f"Final Scores -> Player 1: {self.score1},"
              "Player 2: {self.score2}")
        if self.score1 > self.score2:
            print("Player 1 is the champion!")
        elif self.score2 > self.score1:
            print("Player 2 is the champion!")
        else:
            print("It's a draw!")


if __name__ == "__main__":
    """Setup and start the game based on opponent choice."""
    print(
        "Select your opponent:\n"
        "1. RandomMovePlayer\n"
        "2. MirrorPlayer\n"
        "3. SequentialPlayer\n"
        "4. FixedRockPlayer"
    )
    opponent_choice = input("Enter the number of your choice: ")

    if opponent_choice == "1":
        opponent = RandomMovePlayer()
    elif opponent_choice == "2":
        opponent = MirrorPlayer()
    elif opponent_choice == "3":
        opponent = SequentialPlayer()
    elif opponent_choice == "4":
        opponent = FixedRockPlayer()
    else:
        print("Invalid choice! Defaulting to RandomMovePlayer.")
        opponent = RandomMovePlayer()

    game = Match(UserPlayer(), opponent)
    game.start_game()
