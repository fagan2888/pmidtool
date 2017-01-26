import flask
from flask import Flask
from wikidataintegrator import wdi_login
from wikidataintegrator.wdi_helpers import PubmedItem

from local import WDUSER, WDPASS

login = wdi_login.WDLogin(user=WDUSER, pwd=WDPASS)
app = Flask(__name__)


@app.route('/get_or_create/<pmid>')
def get_or_create(pmid):
    p = PubmedItem(pmid)
    wdid = p.get_or_create(login)
    if wdid:
        return flask.jsonify({'success': True,
                              'result': wdid})
    else:
        return flask.jsonify({'success': False})


if __name__ == '__main__':
    app.run(host='0.0.0.0')
