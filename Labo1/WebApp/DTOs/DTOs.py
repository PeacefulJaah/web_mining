from dataclasses import dataclass
from typing import Optional

@dataclass
class MovieDTO:
    rank : int
    title : str      
    year : int      
    duration : str
    rating : float 
    votes : str
    certificate: Optional[str] = None
    url: Optional[str] = None
    poster_url: Optional[str] = None
    
@dataclass
class YearAvgDTO:
    year : int
    doc_count : int
    avg : int   
     
@dataclass
class CountMovieDTO:
    value : int
    relation: str
    
@dataclass 
class SearchMovieDTO:
    score : float 
    movie : MovieDTO
