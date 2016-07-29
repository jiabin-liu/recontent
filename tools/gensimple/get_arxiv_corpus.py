# Freija Descamps <freija@gmail.com> July 2016
# modified to download arxiv corpus

import os
import wget

URL = 'https://dl.dropboxusercontent.com/u/99220436/recontent-data/arx/'

CORPUS_NAME = 'arx1501'

MMFILE = CORPUS_NAME + '.mm'
DICTFILE = CORPUS_NAME + '_wordids.txt'
SIMMATRIX = CORPUS_NAME + '-lsi.index'
LSIMODEL = CORPUS_NAME + '.lsi_model'
LSIPROJ = CORPUS_NAME + '.lsi_model.projection'
#LSIPROJNPY=CORPUS_NAME + '.lsi_model.projection.u.npy'
ARTICLEDICT = CORPUS_NAME + '_adict.json'
#NPYINDEX = CORPUS_NAME + '-lsi.index.index.npy'

DEFAULT_DICT_SIZE = 100000


def main(argv=None):
    # first clean up
    try:
        os.remove(MMFILE)
        os.remove(DICTFILE)
        os.remove(SIMMATRIX)
        os.remove(LSIMODEL)
        os.remove(ARTICLEDICT)
        os.remove(LSIPROJ)
        #os.remove(NPYINDEX)
        #os.remove(LSIPROJNPY)
    except OSError:
        pass

    wget.download(URL + MMFILE)
    wget.download(URL + DICTFILE)
    wget.download(URL + SIMMATRIX)
    wget.download(URL + LSIMODEL)
    wget.download(URL + ARTICLEDICT)
    wget.download(URL + LSIPROJ)
    #wget.download(URL + NPYINDEX)
    #wget.download(URL + LSIPROJNPY)
    

if __name__ == "__main__":
    main()
