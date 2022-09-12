"""Flask server for diary card app."""

from flask import Flask, session, request, flash, render_template, redirect
import crud
import os

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "")

@app.route('/')
def index():
    """View function for homepage."""

    return "Hello, World!"


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
