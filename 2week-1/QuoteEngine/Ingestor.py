from .IngestorInterface import Importinterface
from .DocxIngestor import docxingestor
from .CSVIngestor import csvingestor
from .TXTIngestor import txtingestor
from .PDFIngestor import pdfingestor


class ingestor(Importinterface):
    ingestors = [docxingestor, csvingestor,txtingestor,pdfingestor]
    
    @classmethod
    def parse(cls, path: str):
        for ingestor in cls.ingestors:
            if ingestor.can_ingest(path):
                return ingestor.parse(path)
