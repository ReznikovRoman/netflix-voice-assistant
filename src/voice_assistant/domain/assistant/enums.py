import enum


class AssistantProviderSlug(str, enum.Enum):
    """Провайдер голосового ассистента."""

    YANDEX_ALICE = "yandex_alice"
