import flask
from flask import Flask, request, redirect
from wikidataintegrator import wdi_login
from wikidataintegrator.wdi_helpers import PubmedItem

from local import WDUSER, WDPASS

login = wdi_login.WDLogin(user=WDUSER, pwd=WDPASS)
app = Flask(__name__)


def batch():
    pmids = request.args.get('pmids', '')
    d = {}
    for pmid in pmids.split(","):
        p = PubmedItem(pmid)
        d[pmid] = p.get_or_create(login)
    return flask.jsonify({'success': True, 'result': d})


@app.route('/')
def home():
    return "See <a href='https://www.wikidata.org/wiki/Wikidata:WikiProject_Source_MetaData/PMIDTool'>here</a> for more info"


@app.route('/get_or_create')
@app.route('/get_or_create/<pmid>')
def get_or_create(pmid=None):
    if pmid == None:
        return batch()
    else:
        p = PubmedItem(pmid)
        wdid = p.get_or_create(login)
        if wdid:
            return flask.jsonify({'success': True, 'result': wdid})
        else:
            return flask.jsonify({'success': False})



if __name__ == '__main__':
    app.run(host='0.0.0.0')
