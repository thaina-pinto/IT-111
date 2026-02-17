import random

# Functions to manage the dice game state

def new_game():
    """Initialize and return a fresh game state dictionary."""
    state = {
        "turn": 1,
        "target": None,
        "over": False,
        "msg": ""
    }
    return state


def validate_roll(value):
    """Check if the dice value is valid. Returns True or False."""
    try:
        num = int(value)
    except (TypeError, ValueError):
        return False
    return 2 <= num <= 12


def generate_roll():
    """Simulate rolling two dice by generating a random sum."""
    die1 = random.randint(1, 6)
    die2 = random.randint(1, 6)
    return die1 + die2


def first_turn_outcome(roll):
    """Determine the outcome for the opening roll.
    Returns: 'lose', 'win', or 'continue'
    """
    losing_numbers = {2, 3, 12}
    winning_numbers = {7, 11}

    if roll in losing_numbers:
        return "lose"
    elif roll in winning_numbers:
        return "win"
    else:
        return "continue"


def later_turn_outcome(roll, target):
    """Determine the outcome for rolls after the first.
    Returns: 'lose', 'win', or 'continue'
    """
    if roll == 7:
        return "lose"
    elif roll == target:
        return "win"
    else:
        return "continue"


def take_turn(state, roll_value=None):
    """
    Execute one turn of the dice game.
    
    Parameters:
        state: the current game state dict
        roll_value: optional integer for the dice roll (None = random)
    
    Returns:
        A dictionary with the turn results and updated state.
    """
    # Don't allow play if game ended
    if state["over"]:
        return {
            "rolled": None,
            "turn_num": state["turn"],
            "message": state["msg"],
            "target": state["target"],
            "game_over": True,
            "err": "Game has ended. Please start a new game."
        }

    # Get the dice roll
    if roll_value is not None:
        if not validate_roll(roll_value):
            return {
                "rolled": None,
                "turn_num": state["turn"],
                "message": state["msg"],
                "target": state["target"],
                "game_over": False,
                "err": "Invalid input! Enter a number from 2 to 12."
            }
        rolled = int(roll_value)
    else:
        rolled = generate_roll()

    # Save current turn number before any changes
    current_turn = state["turn"]

    # Figure out what happened
    if current_turn == 1:
        outcome = first_turn_outcome(rolled)
    else:
        outcome = later_turn_outcome(rolled, state["target"])

    # Apply the outcome
    err_msg = None
    if outcome == "lose":
        state["over"] = True
        state["msg"] = "Rolled {}. You lose!".format(rolled)
    elif outcome == "win":
        state["over"] = True
        state["msg"] = "Rolled {}. You win!".format(rolled)
    else:
        # Game keeps going
        if current_turn == 1:
            state["target"] = rolled
            state["msg"] = "Rolled {}. Point is now {}. Keep rolling!".format(rolled, rolled)
        else:
            state["msg"] = "Rolled {}. Not a match. Try again!".format(rolled)
        state["turn"] += 1

    return {
        "rolled": rolled,
        "turn_num": current_turn,
        "message": state["msg"],
        "target": state["target"],
        "game_over": state["over"],
        "err": err_msg
    }
