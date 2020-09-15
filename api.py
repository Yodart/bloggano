from flask import Flask
from users import users
from auth import auth

app = Flask(__name__)
app.register_blueprint(auth)
app.register_blueprint(users)


if __name__ == '__main__':
    app.run(debug=True)
