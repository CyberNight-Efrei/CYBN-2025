from flask import Flask, render_template, request, session, redirect, url_for, flash
from PIL import Image
import random, io, os, base64

app = Flask(__name__)
app.secret_key = os.environ.get("FLAG", "CYBN{flag}")

# --- Slot coordinates ---
HOTBAR = [(48, 450), (102, 450), (156, 450), (210, 450), (264, 450), (318, 450), (372, 450), (426, 450), (480, 450)]
INV = [(48, 276), (102, 276), (156, 276), (210, 276), (264, 276), (318, 276), (372, 276), (426, 276), (480, 276),
       (48, 330), (102, 330), (156, 330), (210, 330), (264, 330), (318, 330), (372, 330), (426, 330), (480, 330),
       (48, 384), (102, 384), (156, 384), (210, 384), (264, 384), (318, 384), (372, 384), (426, 384), (480, 384)]
ARMOR = [(48, 48), (48, 102), (48, 156), (48, 210)]
CRAFT = [(318, 78), (372, 78), (318, 132), (372, 132), (486, 108)]
OFF = [(255, 210)]
SLOTS = [*HOTBAR, *INV, *ARMOR, *CRAFT, *OFF]

BASE_PATH = os.path.join("static", "base.png")
PANE_PATH = os.path.join("static", "pane.png")


def generate_inventory(round_number):
    base = Image.open(BASE_PATH).convert("RGBA")
    pane = Image.open(PANE_PATH).convert("RGBA")

    chosen_slots = random.sample(range(len(SLOTS)), k=round_number)

    for i in chosen_slots:
        x, y = SLOTS[i]
        base.alpha_composite(pane, (x - pane.width // 2, y - pane.height // 2))

    buf = io.BytesIO()
    base.save(buf, format="PNG")
    buf.seek(0)
    encoded = base64.b64encode(buf.getvalue()).decode("utf-8")

    return encoded, chosen_slots


@app.route("/")
def index():
    session.clear()

    session["round"] = 1
    session["completed"] = False

    return redirect(url_for("challenge"))


@app.route("/challenge")
def challenge():
    round_num = session.get("round", 1)

    if round_num > 8:
        return redirect(url_for("success"))

    img_base64, chosen_slots = generate_inventory(round_num)
    session["solution"] = chosen_slots

    print(session["solution"])

    return render_template("index.html", round=round_num, img_b64=img_base64)


@app.route("/submit", methods=["POST"])
def submit():
    answer = request.form.get("slots", "")
    try:
        user_slots = sorted([int(x.strip()) for x in answer.split(",") if x.strip()])
    except ValueError:
        flash("⚠️ Invalid input format!", "error")
        session["round"] = 1

        return redirect(url_for("challenge"))

    if user_slots == sorted(session.get("solution", [])):
        session["round"] += 1

        if session["round"] > 8:
            session["completed"] = True

            return redirect(url_for("success"))

        return redirect(url_for("challenge"))

    flash("❌ One pane was wrong, start over!", "error")

    session["round"] = 1
    session["completed"] = False

    return redirect(url_for("challenge"))


@app.route("/success")
def success():
    if not session.get("completed"):
        flash("⚠️ You must solve all rounds to reach this page!", "error")
        return redirect(url_for("challenge"))
    
    flag = os.environ.get("FLAG", "CYBN{flag}")
    return render_template("success.html", flag=flag)


if __name__ == "__main__":
    app.run(debug=True)
