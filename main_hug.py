from wikidataintegrator.wdi_helpers import PubmedItem
import hug


@hug.get('/get_or_create')
def get_or_create(pmid:int):
    p = PubmedItem(pmid)
    wdid = p.get_or_create()
    return {'success': True,
            'result': wdid}


if __name__ == '__main__':
    hug.API(__name__).http.serve()