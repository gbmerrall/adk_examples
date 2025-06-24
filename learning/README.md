Folder layout
-------------
 - If you're using adk_web you need a top level directory to run adk_web from.  `adk web` then uses those directory names to list the agents available.

```text
    parent_folder/      <-- run from here
      agent_1/
        __init__.py
        agent.py
        .env
      agent_2/
        __init__.py
        agent.py
```
 - You need a .env file. This can go in the parent folder as python-dotenv will look up the tree
 - async seems pretty important. My guess this is for performance
 - You always need an \_\_init\_\_.py which contains

    ```
    from . import agent
    ```
 - That infers that you also need an agent.py as well!
 - agent.py can either be the main script or you can have it beside the actual running script. e.g. agent.py + main.py

 - agent.py is where we define the agent behavious including callbacks etc