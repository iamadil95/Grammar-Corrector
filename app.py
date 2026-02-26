from flask import Flask, render_template, request
from model import correct_grammar
import os

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    corrected_text = ""
    original_text = ""

    if request.method == "POST":
        original_text = request.form.get("text")

        if original_text:
            corrected_text = correct_grammar(original_text)

    return render_template(
        "index.html",
        original=original_text,
        corrected=corrected_text
    )

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)