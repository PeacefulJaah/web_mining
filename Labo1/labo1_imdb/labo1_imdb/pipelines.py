# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from elasticsearch_dsl import connections
from .models import MovieDocument

class Labo1ImdbPipeline:
    def __init__(self):
        connections.create_connection(hosts=['http://localhost:9200'])
        MovieDocument.init()
    
    def process_item(self, item, spider):
        try:
            annee = int(item["year"]) if item["year"] else 0
        except ValueError:
            annee = 0  
        try:
            rank = int(item["rank"].replace('#','')) if item["rank"] else 0
        except ValueError:
            rank = 0  
        try:
            note = float(item["rating"]) if item["rating"] else 0.0
        except ValueError:
            note = 0.0
            
        movie = MovieDocument(
            meta={'id': item["url"]},
            rank=rank,
            title=item["title"],
            year=annee,
            duration=item["duration"],
            rating=note,
            votes=item["votes"],
        )        
        movie.save()
        return item