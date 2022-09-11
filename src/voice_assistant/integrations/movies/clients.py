class MovieClient:
    """Клиент для работы с сервисом Netflix Movies."""

    async def find_movie_by_name(self, name: str, /):
        """Поиск фильма по названию."""
