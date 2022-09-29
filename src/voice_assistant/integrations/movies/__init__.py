from .repositories import MovieRepository
from .version import __version__

# XXX: Для сборки пакета setuptools'ами
try:
    from .asynchronous import AsyncMovieClient, AsyncMoviesSession, init_async_movie_client
    from .clients import MovieClient, init_movie_client
    from .http import MoviesSession
except ImportError:
    pass

__all__ = [
    "__version__",
    "MoviesSession",
    "MovieClient",
    "init_movie_client",
    "AsyncMoviesSession",
    "AsyncMovieClient",
    "init_async_movie_client",
    "MovieRepository",
]
