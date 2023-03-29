from flask import Flask, render_template_string, request

app = Flask(__name__)


@app.route("/")
def no_filter():
    payload = request.args.get("payload")
    payload = "Buenos dias" if not payload else payload

    template = f"<body><p>{payload}</p></body>"

    return render_template_string(template)


if __name__ == "__main__":
    app.run(debug=True)
