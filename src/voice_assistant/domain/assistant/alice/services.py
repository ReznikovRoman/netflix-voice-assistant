from .schemes import AliceRequest, AliceResponse


class AliceService:
    """Голосовой ассистент на основе Алисы."""

    def process_request(self, context: AliceRequest):
        """
        Обработчик запросов с яндекс диалогов.

        Args:
            context: AliceRequest
        Returns: AliceResponse
        """
        answer = "Hi! I`m bot"
        if context.request.nlu.tokens:
            match context.request.nlu.intents.intent_name:
                case "search_by_director":
                    value = context.request.nlu.intents.search_by_director.get("slots").get("person_name").get("value")
                    answer = f"search_by_director {value}"
                case "actors_in_the_film":
                    value = context.request.nlu.intents.actors_in_the_film.get("slots").get("movie_name").get("value")
                    answer = f"actors_in_the_film {value}"
                case "film_director":
                    value = context.request.nlu.intents.film_director.get("slots").get("movie_name").get("value")
                    answer = f"film_director {value}"
                case "movie_duration":
                    value = context.request.nlu.intents.movie_duration.get("slots").get("movie_name").get("value")
                    answer = f"movie_duration {value}"
                case "find_film":
                    value = context.request.nlu.intents.find_film.get("slots").get("movie_name").get("value")
                    answer = f"find_film {value}"
                case "empty":
                    answer = "empty"

        return AliceResponse(
            meta=context.meta,
            session=context.session,
            version=context.version,
            response={
                "text": answer,
                "end_session": False,
            },
        )
