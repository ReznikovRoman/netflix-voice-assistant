from .clients import MovieClient


class MovieRepository:
    """Репозиторий для работы с данными из сервиса Netflix Movies."""

    def __init__(self, movie_client: MovieClient) -> None:
        assert isinstance(movie_client, MovieClient)
        self._movie_client = movie_client

    async def find_movie_by_name(self, name: str, /):
        return await self._movie_client.find_movie_by_name(name)
