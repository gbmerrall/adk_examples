Run UI etc with `adk web` from the 'app' directory

You can also run the API itself which is more 'deployment-like'. To do this run  `adk api-server` 


**Making requests**

First get a session token  
```sh
curl -X POST http://localhost:8000/apps/google_search_agent/users/u_123/sessions/s_123 \
  -H "Content-Type: application/json" \
  -d '{"state": {"key1": "value1", "key2": 42}}'
```

The post body is optional. Uou can use this to customize the agent's pre-existing state (dict) when creating the session.

Now make a request either to run or run_sse. run_sse returns as Server-Sent-Events, which is a stream of event objects. Suitable for those who want to be notified as soon as the event is available. 

You can set streaming to true to enable token-level streaming, which means the response will be returned to you in multiple chunks


```sh
curl -X POST http://localhost:8000/run \
-H "Content-Type: application/json" \
-d '{
"appName": "google_search_agent",
"userId": "u_123",
"sessionId": "s_123",
"newMessage": {
    "role": "user",
    "parts": [{
    "text": "Hey whats the weather in new york today"
    }]
}
}'
```

```sh
curl -X POST http://localhost:8000/run_sse \
-H "Content-Type: application/json" \
-d '{
"appName": "google_search_agent",
"userId": "u_123",
"sessionId": "s_123",
"newMessage": {
    "role": "user",
    "parts": [{
    "text": "Hey whats the weather in new york today"
    }]
},
"streaming": false
}'
```