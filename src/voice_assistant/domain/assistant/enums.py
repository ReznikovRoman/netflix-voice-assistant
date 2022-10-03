import enum


class AssistantProviderSlug(str, enum.Enum):
    """Voice assistant provider."""

    YANDEX_ALICE = "yandex_alice"


class IntentChoice(str, enum.Enum):
    """Available intents."""

    FILM_DESCRIPTION = "film_description"
    FILM_ACTORS = "actors_in_the_film"
    FILM_DIRECTORS = "film_director"
    FILM_RATING = "film_rating"
    SEARCH_BY_DIRECTOR = "search_by_director"
    NOT_RECOGNIZED = "intent_not_recognized"
    MISSING_SEARCH_QUERY = "missing_search_query"
    HELP = "YANDEX.WHAT_CAN_YOU_DO"


class DefaultResponseMessage(str, enum.Enum):
    """Default voice assistant responses."""

    WELCOME_HELP_MESSAGE = (
        "Hi! I'm Netflix voice assistant 😉, to find out my features say 'What can you do?'🙈"
    )
    ERROR_MESSAGE = "Something went wrong 🫣, try once again."
    INTENT_NOT_FOUND = "I didn't get your question... please ask again 🧐"
    MISSING_SEARCH_QUERY = (
        "You haven't specified what exactly do you want to know about?😏 Refine your search, "
        "for example say 'Tell me about movie 'Pulp fiction'.'"
    )
    NOT_FOUND_MESSAGE_TEMPLATE = "Nothing was found on '{search_query}' 😒, please ask again."
    HELP = (
        "Ask 'Who starred in movie ...', to know film crew, 👥"
        "'Tell me about movie ...', to get a description of the movie, 🎥"
        "'Who is the director of the movie ...', to know the director, 🧔"
        "'What is the rating of the film ...', to get film's rating, 📈"
        "'Find director's movies ...', to get films of a certain director 🎥"
    )


class ResponseMessageTemplate(list[str], enum.Enum):
    """Response templates."""

    FIND_BY_DIRECTOR_MESSAGE_LIST = [
        "Director {director} participated in {films}",
        "{director} directed in {films}",
    ]

    FILM_RATING_MESSAGE_LIST = [
        "Rating of the film '{film}' - {rating}",
        "Users rated the film '{film}' by {rating}",
        "According to my information, the rating of the film '{film}' is {rating}",
    ]

    FILM_DIRECTOR_MESSAGE_LIST = [
        "The director of the film '{film}' - {director}",
        "Movie '{film}' was directed by {director}",
    ]

    ACTORS_IN_FILM_MESSAGE_LIST = [
        "In the film '{film}' participated: {actors}",
        "In the film '{film}' starred: {actors}",
        "In the movie '{film}' starred: {actors}",
    ]

    FILM_DESCRIPTION_MESSAGE_LIST = [
        "I'm telling you about the movie '{film}': {description}",
        "Here's what I can tell you about the film '{film}': {description}",
        "Description of the film '{film}': {description}",
    ]
