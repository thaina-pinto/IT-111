from flask import Flask, render_template, request, session, redirect, url_for
from games.dice_game import new_game, take_turn

app = Flask(__name__)
app.secret_key = "my_flask_dice_app_2026"


@app.route("/")
def index():
    """Show the dice game page."""
    # Load game from session or create one
    if "game_state" not in session:
        session["game_state"] = new_game()

    gs = session["game_state"]
    return render_template("dice.html",
                           turn=gs["turn"],
                           target=gs["target"],
                           over=gs["over"],
                           msg=gs["msg"],
                           roll_result=None,
                           error=None)


@app.route("/roll", methods=["POST"])
def roll():
    """Handle a dice roll submission."""
    if "game_state" not in session:
        session["game_state"] = new_game()

    gs = session["game_state"]

    # Read user input from the form
    user_input = request.form.get("dice_val", "").strip()

    if user_input == "":
        # No input means random roll
        info = take_turn(gs, roll_value=None)
    else:
        info = take_turn(gs, roll_value=user_input)

    # Save updated state back to session
    session["game_state"] = gs
    session.modified = True
