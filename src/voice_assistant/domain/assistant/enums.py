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
    NOT_RECOGNIZED = "intent_not_recognized"
    HELP = "YANDEX.WHAT_CAN_YOU_DO"


class DefaultResponseMessage(str, enum.Enum):
    """Ответы голосового ассистента по умолчанию."""

    WELCOME_HELP_MESSAGE = (
        "Привет! Я голосовой ассистент Netflix, что бы узнать мои возможности скажите  Что ты умеешь?"
    )
    ERROR_MESSAGE = "Что-то пошло не так, попробуйте ещё раз."
    INTENT_NOT_FOUND = "Я не понимаю, что вы хотите узнать... пожалуйста переформулируйте вопрос"
    NOT_FOUND_MESSAGE_TEMPLATE = "По запросу {search_query} - ничего не найдено, повторите вопрос."
    HELP = (
        "Скажите кто снимался в фильме ..., чтобы узнать актеров из фильма, "
        "расскажи про фильм..., для получения описания фильма, "
        "кто режиссер фильма..., чтобы узнать режиссера, "
        "какой рейтинг у фильма..., чтобы узнать рейтинг, "
        "найди фильмы режиссера..., чтобы получить фильмы определенного режиссера"
    )


class ResponseMessageTemplate(list[str], enum.Enum):
    """Шаблоны ответов на запросы пользователя."""

    FIND_BY_DIRECTOR_MESSAGE_LIST = [
        "Режиссер {director} участвовал в {films}",
        "{director} режиссировал в {films}",
    ]

    FILM_RATING_MESSAGE_LIST = [
        "Рейтинг фильма {film} {rating}",
        "Пользователи оценили фильм {film} на {rating}",
        "По моей информации рейтинг фильма {film} составляет {rating}",
    ]

    FILM_DIRECTOR_MESSAGE_LIST = [
        "Режиссер фильма {director} - {film}",
        "В фильме {film} режиссировал {director}",
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
