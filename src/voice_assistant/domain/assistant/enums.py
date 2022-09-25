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


class Message(enum.Enum):
    """Шаблоны ответов ассистента."""

    WELCOME_HELP_MESSAGE = """Привет! Я голосовой ассистент NETFLIX-VOICE-ASSISTANT, что бы узнать мои возможности
    скажите  Что ты умеешь?"""
    ERROR_MESSAGE = "Что-то пошло не так, попробуйте ещё раз."
    INTENT_NOT_FOUND = "Я не понимаю, что вы хотите узнать... пожалуйста переформулируйте вопрос"
    NOT_FOUND_MESSAGE_TEMPLATE = "По запросу {search_query} - ничего не найдено, повторите вопрос."
    HELP = """
    Скажите кто снимался в фильме..., что бы узнать актеров из фильма,
    расскажи про фильм..., для получения описания фильма,
    кто режиссер фильма..., что бы узнать режиссера,
    какой рейтинг у фильма..., что бы узнать рейтинг,
    найди фильм режиссера..., что бы получить фильмы определенного режиссера
    """
    # Ответы на интенты
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
