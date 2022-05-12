import os

from dotenv import load_dotenv
from flask import Flask
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('TOKEN')


@app.route('/', methods=['GET', 'POST'])
def index():
    return 'main page'


def main():
    app.run(debug=True)


if __name__ == '__main__':
    main()