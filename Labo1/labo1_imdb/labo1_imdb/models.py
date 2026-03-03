from elasticsearch_dsl import Document, Text, Keyword, Integer, Float

class MovieDocument(Document):
    rank = Keyword()
    title = Text()        
    year = Integer()      
    duration = Keyword()
    certificate = Keyword()
    rating = Float()      
    votes = Keyword()
    url = Keyword()
    poster_url = Keyword()

    class Index:
        name = 'movies' 