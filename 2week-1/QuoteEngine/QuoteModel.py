class quotemodel():
    def __init__(self,quote,author):
        self.body=quote
        self.author=author

    def __repr__(self):
        return f'{self.body}-{self.author}'
        