from flask import Flask
from presentation.controllers import presentation_bp

app = Flask(__name__)
app.secret_key = "chave_secreta_multicamadas"

app.register_blueprint(presentation_bp)

if __name__ == '__main__':
    app.run(debug=True, port=5001)
