from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search
from fastapi import FastAPI
from labo1_imdb.labo1_imdb.models import MovieDocument

client = Elasticsearch("http://localhost:9200")

app = FastAPI()

@app.get("/api/v1/movie/hit/{year}")
async def topMovieByYear(year: int):
    s = MovieDocument.search(using=client) \
        .filter("term", year=year) \
        .sort("-rating", "rank")

    response = s.execute()

    return [hit.to_dict() for hit in response]

@app.get("/api/v1/year/avg")
async def AvgRatingByYear():
    s = MovieDocument.search(using=client).extra(size=0)
        
    s.aggs.bucket('per_year', 'terms', field="year", size=100, order={"_key": "desc"}) \
        .metric('avg_by_year', 'avg', field='rating')
    response = s.execute()

    resultat = []
    for bucket in response.aggregations.per_year.buckets:
        resultat.append({
            "year": bucket.key,
            "doc_count": bucket.doc_count,
            "avg": round(bucket.avg_by_year.value, 2) if bucket.avg_by_year.value else None
        })
    return resultat

@app.get("/api/v1/movies/count")
async def CountNbMovies():
    s = MovieDocument.search(using=client)    
    response = s.execute()
    return response.hits.total

@app.get("/api/v1/search/{mots_cle}")
async def searchByTitle(mots_cle: str):
    s = MovieDocument.search(using=client) \
        .query("multi_match", query=mots_cle, fields=['title^5', 'year^2', 'rating', 'rank'], lenient=True)
    response = s.execute()
        
    resultat = []
    for bucket in response:
        resultat.append({
            "score": round(bucket.meta.score, 2),
            "movie": bucket.to_dict()
        })
    return resultat

@app.get("/api/v1/movies/title/{title}")
async def searchByTitle(title: str):
    s = MovieDocument.search(using=client) \
        .filter("wildcard", **{"title.raw": f"*{title}*"}) \
        .sort("-rating", "rank")

    response = s.execute()

    return [hit.to_dict() for hit in response]           
        
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
    
