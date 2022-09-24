import enum


class AssistantProviderSlug(str, enum.Enum):
    """Провайдер голосового ассистента."""

    YANDEX_ALICE = "yandex_alice"


class IntentChoice(str, enum.Enum):
    """Список намерений пользователя."""

    FILM_DESCRIPTION = "film_description"
    FILM_ACTORS = "actors_in_the_film"
    FILM_DIRECTORS = "film_director"
    FILM_RATING = "film_rating"
    SEARCH_BY_DIRECTOR = "search_by_director"
    NOT_RECOGNIZED = "not_recognized"


class Message(enum.Enum):
    """Шаблоны ответов ассистента."""

    ON_ERROR_MESSAGE = "Что-то пошло не так, попробуйте ещё раз."
    WELCOME_MESSAGE = "я могу подсказать: описание фильмов, назвать режиссера фильма"

    FALLBACK_MESSAGE = "Извините, я вас не поняла. Пожалуйста, переформулируйте запрос."
    ON_WELCOME_HELP_MESSAGE = "Что бы узнать описание навыка - используйте команду - Что ты умеешь?"
    ON_FILM_HELP_MESSAGE = """
    Что бы получить описание фильма - используйте команду - "расскажи о фильме..".
    Что бы выйти - используйте команду - Хватит.
    """
    WHAT_CAN_YOU_DO_MESSAGE = "Мой навык в том, что бы искать фильмы и предоставлять информацию о них."
    FIELD_INFO_IS_NOT_EXISTS_MESSAGE = "К сожалению информация по этому полю отсутствует"
    NOT_FOUND_MESSAGE_TEMPLATE = "По запросу {search_query} - ничего не найдено, переформулируйте запрос."

    # Ответы на интенты
    FIND_BY_DIRECTOR_MESSAGE_LIST = [
        "Режиссер {director} участвовал в {film}",
        "{director} режиссировал в {film}",
    ]

    FILM_RATING_MESSAGE_LIST = [
        "Рейтинг фильма {film} {rating}",
        "Пользователи оценили фильм {film} на {rating}",
        "По моей информации рейтинг фильма {film} составляет {rating}",
    ]

    FILM_DIRECTOR_MESSAGE_LIST = [
        "Режиссер фильма {director} - {film}",
        "В фильме {director} режиссировал {film}",
    ]

    ACTORS_IN_FILM_MESSAGE_LIST = [
        "В фильме {film} участвовали: {actors}",
        "В фильме {film} снимались: {actors}",
        "В картине {film} снимались: {actors}",
    ]

    FILM_DESCRIPTION_MESSAGE_LIST = [
        "Рассказываю о фильме {film} {description}",
        "Вот что я могу рассказать о фильме {film} {description}",
        "Описание фильма {film} {description}",
    ]
