from elasticsearch_dsl import Document, Text, Keyword, Integer, Float

class MovieDocument(Document):
    rank = Integer()
    title = Text(fields={'raw': Keyword()})        
    year = Integer()      
    duration = Keyword()
    rating = Float()      
    votes = Keyword()

    class Index:
        name = 'movies-top-250' 