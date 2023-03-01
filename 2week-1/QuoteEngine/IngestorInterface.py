from abc import ABC,abstractmethod

class Importinterface(ABC):

    allowed_extensions=['docx','pdf','csv','txt']

    @classmethod
    def can_ingest(cls,path):
        ext=path.split('.')[-1]
        return ext in cls.allowed_extensions
    
    @classmethod
    @abstractmethod
    def parse(cls,path:str) -> list:
        pass 
