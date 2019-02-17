from flask import Flask, render_template
import sqlite3

app = Flask(__name__)


def content():
    conn = sqlite3.connect('posts.sqlite')
    c = conn.cursor()
    c.execute('SELECT * FROM Posts')
    return c


@app.route('/')
def main_page():
    pages = [article for article in content()]
    rows = [pages[i:i + 3] for i in range(0, len(pages), 3)]
    return render_template('index.html', data=rows)


@app.route('/projects/localvore', methods=['GET', 'POST'])
def localvore():
    return render_template('/projects/localvore.html', curTitle='Localvore',
                           curSummary='Menu planner helping people eat locally and minimize food waste.')


@app.route('/projects/thoughts_on_reproducibility', methods=['GET', 'POST'])
def thoughts_on_reproducibility():
    return render_template('/projects/thoughts_on_reproducibility.html', curTitle='Thoughts on Reproducibility',
                           curSummary='Outlining current approaches to reproducibility in data science')


@app.route('/projects/this_website', methods=['GET', 'POST'])
def this_website():
    return render_template('/projects/this_website.html', curTitle='This website',
                           curSummary='How this website was made!')


@app.route('/projects/predicting_semiconductor_properties', methods=['GET', 'POST'])
def predicting_semiconductor_properties():
    return render_template('/projects/predicting_semiconductor_properties.html',
                           curTitle='Predicting Semiconductor Properties',
                           curSummary='Kaggle competition predicting semiconductor performance from X-ray crystal data.')


@app.route('/pages/deploying_a_kaggle_model', methods=['GET', 'POST'])
def deploying_a_kaggle_model():
    return render_template('/pages/deploying_a_kaggle_model.html', curTitle='Deploying a Kaggle Model',
                           curSummary='How to make a RESTful API from a previously constructed ML model')


if __name__ == '__main__':
    app.run()
