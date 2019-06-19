from flask import Flask, render_template
from requests_html import HTMLSession
from collections import namedtuple
from itertools import filterfalse


projects = ['scikit-learn/scikit-learn',
            'keras-team/keras',
            'ericml/pyjanitor',
            'pallets/flask',
            'pallets/click',
            'kennethreitz/requests',
            'pymc-devs/pymc3'
            'mongodb/mongo-python-driver',
            'marshmallow-code/marshmallow',
            'DistrictDataLabs/yellowbrick',
            'maxpumperla/hyperas'
            'zalando/connexion']


def get_text(response):
    div = response.html.find('div.code-list-item')
    for block in div:
        yield block.text.split('\n')


def get_link(response):
    #TODO Make this give all links containing 'blob' and not ending in line #s.
    href = response.html.find('a', containing='blob')
    for link in href:
        yield link.absolute_links


def get_description(text):
    yield ': '.join([text[1], text[2]])


def get_code(text):
    yield [line for line in filterfalse(lambda x: x.isdigit(), text[5:])]


def search(query):
    results = []
    sess = HTMLSession()
    code_block = namedtuple('Block', 'title link description code')
    for project in projects:
        r = sess.get(f'https://github.com/{project}/search?q={query}&unscoped_q={query}')
        for text in get_text(r):
            fields = [text[0],
                      next(get_link(r)),
                      next(get_description(text)),
                      next(get_code(text))]
            results.append(code_block._make(fields))
    return results


app = Flask(__name__)


@app.route('/<query>')
def search_results(query):
    results = search(query)
    if len(results) == 0:
        results = 'No use cases found'
    return render_template('results.html', results=results)


if __name__ == '__main__':
    app.run()