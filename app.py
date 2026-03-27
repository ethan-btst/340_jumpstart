from flask import *
from flask_session import Session
from PIL import Image
import os
import io
import base64

app = Flask(__name__)


app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"

Session(app)

@app.route("/", methods=("GET", "POST"))
def chat():
    if "current_response" not in session:
        session["current_response"] = ""
    if "current_image" not in session:
        session["current_image"] = ""

    if request.method == "POST":
        if request.form["submit"] == "Submit":
            if "image" not in request.files:
                return redirect(request.url)
            image = request.files["image"]
            if image.filename == "":
                return redirect(request.url)

            # Handle image upload. For now, just store in session as base64 string
            img_byte_arr = io.BytesIO()
            Image.open(image).save(img_byte_arr, format="JPEG")
            session["current_image"] = base64.b64encode(img_byte_arr.getvalue()).decode()

            # Handle user questions. For now echo input
            if request.form["chatbox"] == "":
                session["current_response"] = "Report goes here"
            else:
                session["current_response"] = request.form["chatbox"]


        elif request.form["submit"] == "Clear response":
            session["current_response"] = ""
            session["current_image"] = ""

        return redirect(request.url)

    if request.method == "GET":
        return render_template(
            "default.html",
            result=session["current_response"],
            image=session["current_image"],
        )

    return render_template(
        "default.html"
    )