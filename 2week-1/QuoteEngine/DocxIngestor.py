from .IngestorInterface import Importinterface
import docx
from .QuoteModel import quotemodel
class docxingestor(Importinterface):

    allowed_extensions=['docx']

    @classmethod
    def parse(cls, path: str) -> list:
        if not cls.can_ingest(path):
            raise Exception('cannot ingest exception')
        
        dogs=[]
        doc=docx.Document(path)

        for para in doc.paragraphs:
            if para.text != "":
                parse= para.text.split('-')
                new_dog=quotemodel(parse[0],parse[1])
                dogs.append(new_dog)

        return dogs


