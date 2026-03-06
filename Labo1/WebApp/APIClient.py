import requests
from urllib.parse import urljoin
import dto.DTOs as dto
class APIClient:
    def __init__(self, url_server: str):
        self.url_server = url_server
        self.session = requests.Session()
        
        self.session.headers.update({
            "Content-Type": "application/json",
            "Accept": "application/json"
        })

    def _make_request(self, methode: str, endpoint: str, **kwargs):
        url = urljoin(self.url_server, endpoint)
        reponse = self.session.request(methode, url, **kwargs)
        reponse.raise_for_status() 
        return reponse.json()

    def getTopMovieByYear(self, year: int) -> list[dto.MovieDTO]:
        """Route GET /api/v1/movie/hit/{year}"""
        response = self._make_request("GET", f"api/v1/movie/hit/{year}")
        return [dto.MovieDTO(**donnee) for donnee in response]

    def getAvgRatingByYear(self) -> list[dto.YearAvgDTO]:
        """Route GET /api/v1/year/avg"""
        response = self._make_request("GET", "api/v1/year/avg")
        return [dto.YearAvgDTO(**donnee) for donnee in response]

    def getCountNbMovies(self) -> dto.CountMovieDTO:
        """Route GET /api/v1/movies/count"""
        response = self._make_request("GET", "api/v1/movies/count")
        return dto.CountMovieDTO(**response)

    def searchByKeyword(self, mots_cle: str) -> list[dto.SearchMovieDTO]:
        """Route GET /api/v1/search/{mots_cle}"""
        response = self._make_request("GET", f"api/v1/search/{mots_cle}")
        
        resultat = []
        for item in response:
            movie_dto = dto.MovieDTO(**item["movie"])
            search_dto = dto.SearchMovieDTO(score=item["score"], movie=movie_dto)
            resultat.append(search_dto)
        return resultat

    def searchByTitle(self, title: str) -> list[dto.MovieDTO]:
        """Route GET /api/v1/movies/title/{title}"""
        response = self._make_request("GET", f"api/v1/movies/title/{title}")
        return [dto.MovieDTO(**donnee) for donnee in response]