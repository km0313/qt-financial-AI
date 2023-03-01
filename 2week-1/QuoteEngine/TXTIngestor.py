from .IngestorInterface import Importinterface
from .QuoteModel import quotemodel
import re
class txtingestor(Importinterface):

    allowed_extensions=['txt']

    @classmethod
    def parse(cls, path: str) -> list:
        if not cls.can_ingest(path):
            raise Exception('cannot ingest exception')
        
        dogs=[]
        files_rep=open(path,'r')

        for lines in files_rep.readlines():
            for line in re.split('[\ufeff|\n]',lines):
                if line!='':
                    parsed=line.split(' - ')
                    new_dog=quotemodel(parsed[0],parsed[1])
                    dogs.append(new_dog)


        return dogs