# Netflix Voice Assistant
Голосовой ассистент в онлайн-кинотеатре _Netflix_.

## Технологии
- FastAPI
- Провайдеры голосовых ассистентов:
  - Yandex.Alice

## АПИ
- Запросы от провайдеров голосовых ассистентов
  - `POST api/v1/assistants/requests/process/{provider}`
  - Пример запроса для Яндекс.Диалогов
  ```json
    {
     "meta": {
         "locale": "ru-RU",
         "timezone": "UTC",
         "client_id": "ru.yandex.searchplugin/7.16 (none none; android 4.4.2)",
         "interfaces": {
           "screen": {},
           "payments": {},
           "account_linking": {}
         }
       },
       "session": {
         "message_id": 0,
         "session_id": "15e198c1-b253-4d9b-bc85-2342041cca24",
         "skill_id": "8e1e7cf2-ecb8-44f5-8bd5-ae9f81af84a1",
         "user": {
           "user_id": "E23287D09682BCCE01A4166E320B66E3EA523168C14C5396F40D38B681119E40"
         },
         "application": {
           "application_id": "033D1EA63A397A83CB963D34578CF7C95760656317DCD623450F438285FB40DD"
         },
         "user_id": "033D1EA63A397A83CB963D34578CF7C95760656317DCD623450F438285FB40DD",
         "new": true
       },
       "request": {
         "command": "расскажи о фильме тор",
         "original_utterance": "расскажи о фильме тор",
         "nlu": {
           "tokens": [
             "расскажи",
             "о",
             "фильме",
             "тор"
           ],
           "entities": [],
           "intents": {
             "film_description": {
               "slots": {
                 "search_query": {
                   "type": "YANDEX.STRING",
                   "tokens": {
                     "start": 3,
                     "end": 4
                   },
                   "value": "тор"
                 }
               }
             }
           }
         },
         "markup": {
           "dangerous_context": false
         },
         "type": "SimpleUtterance"
       },
       "state": {
         "session": {},
         "user": {},
         "application": {}
       },
       "version": "1.0"
    }
  ```
  - Пример тела ответа для Яндекс.Диалоги
    ```json
      {
        "text": "По запросу тор - ничего не найдено 😒,  повторите вопрос.",
        "response": {
          "text": "По запросу тор - ничего не найдено 😒,  повторите вопрос.",
          "end_session": false
        },
        "version": "1.0",
        "session_state": {
          "intent": "film_description",
          "search_query": "тор"
        }
      }
    ```
