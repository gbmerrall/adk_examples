### Requesting a session

export APP_URL="https://adk-default-service-name-1072261851642.us-central1.run.app"

COMMAND

```sh
curl -X POST $APP_URL/apps/1_hello_world/users/user_123/sessions/session_abc \
    -H "Content-Type: application/json"
```

OUTPUT
```json
{"id":"session_abc","appName":"1_hello_world","userId":"user_123","state":{},"events":[],"lastUpdateTime":1750052469.8702555}
```

### Sending a message

COMMAND
```sh
curl -X POST \
    "$APP_URL/run" \
    -H "Content-Type: application/json" \
    -d '{
    "app_name": "1_hello_world",
    "user_id": "user_123",
    "session_id": "session_abc",
    "new_message": {
        "role": "user",
        "parts": [{
        "text": "Roll a 50 sided die"
        }]
    },
    "streaming": false
    }'
```

OUTPUT

```json
[
    {
        "content": {
            "parts": [
                {
                    "functionCall": {
                        "id": "adk-d98c7dbd-b808-42a1-94af-61320d522e82",
                        "args": {
                            "sides": 50
                        },
                        "name": "roll_die"
                    }
                }
            ],
            "role": "model"
        },
        "usageMetadata": {
            "candidatesTokenCount": 5,
            "candidatesTokensDetails": [
                {
                    "modality": "TEXT",
                    "tokenCount": 5
                }
            ],
            "promptTokenCount": 555,
            "promptTokensDetails": [
                {
                    "modality": "TEXT",
                    "tokenCount": 555
                }
            ],
            "totalTokenCount": 560,
            "trafficType": "ON_DEMAND"
        },
        "invocationId": "e-98e9c6ef-f1d5-4129-955c-fe78d3611c1c",
        "author": "hello_world_agent",
        "actions": {
            "stateDelta": {},
            "artifactDelta": {},
            "requestedAuthConfigs": {}
        },
        "longRunningToolIds": [],
        "id": "uolapJWG",
        "timestamp": 1750052502.569582
    },
    {
        "content": {
            "parts": [
                {
                    "functionResponse": {
                        "id": "adk-d98c7dbd-b808-42a1-94af-61320d522e82",
                        "name": "roll_die",
                        "response": {
                            "result": 13
                        }
                    }
                }
            ],
            "role": "user"
        },
        "invocationId": "e-98e9c6ef-f1d5-4129-955c-fe78d3611c1c",
        "author": "hello_world_agent",
        "actions": {
            "stateDelta": {
                "rolls": [
                    50,
                    8,
                    13
                ]
            },
            "artifactDelta": {},
            "requestedAuthConfigs": {}
        },
        "id": "1pMoqAFd",
        "timestamp": 1750052502.990774
    },
    {
        "content": {
            "parts": [
                {
                    "text": "I rolled a 50 sided die and got 13.\n"
                }
            ],
            "role": "model"
        },
        "usageMetadata": {
            "candidatesTokenCount": 15,
            "candidatesTokensDetails": [
                {
                    "modality": "TEXT",
                    "tokenCount": 15
                }
            ],
            "promptTokenCount": 565,
            "promptTokensDetails": [
                {
                    "modality": "TEXT",
                    "tokenCount": 565
                }
            ],
            "totalTokenCount": 580,
            "trafficType": "ON_DEMAND"
        },
        "invocationId": "e-98e9c6ef-f1d5-4129-955c-fe78d3611c1c",
        "author": "hello_world_agent",
        "actions": {
            "stateDelta": {},
            "artifactDelta": {},
            "requestedAuthConfigs": {}
        },
        "id": "Q7gQktaR",
        "timestamp": 1750052502.992469
    }
]
```