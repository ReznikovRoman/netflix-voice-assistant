# Netflix Voice Assistant
_Netflix_ voice assistant.

## Stack
- [FastAPI](https://fastapi.tiangolo.com/)
- Voice assistant providers:
  - [Yandex.Alice/Yandex.Dialogs](https://yandex.ru/dev/dialogs/alice/doc/about.html)

## API
- Request from voice assistant provider
  - `POST api/v1/assistants/requests/process/{provider}`
  - e.g. request from Yandex.Dialogs
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
         "command": "tell me about film pulp fiction",
         "original_utterance": "tell me about film pulp fiction",
         "nlu": {
           "tokens": [
             "tell",
             "me",
             "about",
             "film",
             "pulp fiction"
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
                   "value": "pulp fiction"
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
  - e.g. response for Yandex.Dialogs
    ```json
      {
        "text": "Couldn't find anything for `pulp fiction`.",
        "response": {
          "text": "Couldn't find anything for `pulp fiction`.",
          "end_session": false
        },
        "version": "1.0",
        "session_state": {
          "intent": "film_description",
          "search_query": "pulp fiction"
        }
      }
    ```
