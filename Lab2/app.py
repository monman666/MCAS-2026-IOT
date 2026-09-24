from flask import Flask, render_template, redirect, url_for

app = Flask(__name__)

images = [
    "images/pic1.jpg",
    "images/pic2.jpg",
    "images/pic3.jpg",
]

current_index = 0


@app.route("/")
def index():
    img = images[current_index]

    return render_template(
        "index.html",
        image=img,
        idx=current_index,
        total=len(images),
    )


@app.route("/next")
def next_img():
    global current_index

    # 最後一張再按下一張，會回到第一張
    current_index = (current_index + 1) % len(images)

    return redirect(url_for("index"))


@app.route("/prev")
def prev_img():
    global current_index

    # 第一張再按上一張，會跳到最後一張
    current_index = (current_index - 1) % len(images)

    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050, debug=True)