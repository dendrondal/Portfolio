import sqlite3
import os
from content_management import content


def main():
    FUNC_TEMPLATE='''
    
    @app.route('ROUTE', methods=['GET', 'POST'])
    def CURRENTTITLE():
        return render_template('CURRENTHTML', curTitle='CURTOPIC', 
                                curSummary='CURSUMMARY')


    '''

    c = content()
    for page in c:
        try:
            ROUTE = page[2]
            CURRENTTITLE = page[0].replace("-","_").replace(" ","_").replace(",","").replace("/","").replace(")","").replace("(","").replace(".","").replace("!","").replace(":","-").replace("'","").lower()
            CURRENTHTML = (page[2]+'.html')
            CURTOPIC = page[0]
            CURSUMMARY = page[1]
            os.makedirs('/static/pages/' + CURRENTTITLE)
            print(FUNC_TEMPLATE.replace("CURRENTTITLE", CURRENTTITLE).replace("ROUTE", ROUTE).replace("CURRENTHTML", CURRENTHTML).replace("CURTOPIC", CURTOPIC).replace("CURSUMMARY", CURSUMMARY))
        except Exception as e:
            print(str(e))


if __name__ == '__main__':
    main()
