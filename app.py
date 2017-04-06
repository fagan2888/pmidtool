import sys
sys.path.insert(0, "/home/gstupp/projects/WikidataIntegrator")
import flask
import traceback
from flask import Flask, request, redirect
from wikidataintegrator import wdi_login
from wikidataintegrator.wdi_helpers import PubmedItem

from local import WDUSER, WDPASS

login = wdi_login.WDLogin(user=WDUSER, pwd=WDPASS)
app = Flask(__name__)

@app.route('/')
def home():
    return "See <a href='https://www.wikidata.org/wiki/Wikidata:WikiProject_Source_MetaData/PMIDTool'>here</a> for more info"

@app.route('/get_or_create/<ext_id>')
def get_or_create_med(ext_id=None):
    return run(ext_id, 'MED')


def run(ext_id, id_type='MED'):
    try:
        p = PubmedItem(ext_id, id_type)
        qid = p.get_or_create(login)
    except Exception as e:
        traceback.print_exc()
        return flask.jsonify({'success': False, 'message': str(e)})
    if qid:
        return flask.jsonify({'success': True, 'result': qid, 'errors': p.errors, 'warnings': p.warnings})
    else:
        return flask.jsonify({'success': False, 'errors': p.errors, 'warnings': p.warnings})



@app.route('/get_or_create')
def get_or_create():
    id_type = request.args.get('id_type')
    ext_id = request.args.get('ext_id')
    if not ext_id:
        return flask.jsonify({'success': False, 'message': "ext_id is required"})
    return run(ext_id, id_type)

if __name__ == '__main__':
    app.run(host='0.0.0.0')
