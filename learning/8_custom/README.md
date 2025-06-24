Spot how we havce to use a lamda function to get access to the context so we can pull out the topic.

Session state is the most fundamental way for agents operating within the same invocation (and thus sharing the same Session object via the InvocationContext) to communicate passively.

You can either pull it out with a lamda function as below

We could possibly also use 
```python
story_generator = LlmAgent(
    name="StoryGenerator",
    model=GEMINI_2_FLASH,
    instruction=lambda ctx: f"""You are a story writer. Write a short story (around 100 words) 
    based on the topic: {ctx.state.get("topic", "unknown topic")}""",
    input_schema=None,
    output_key="current_story", 
```

or actually use the prompt to extract it for you. 

```python
story_generator = LlmAgent(
    name="StoryGenerator",
    model=GEMINI_2_FLASH,
    instruction="""You are a story writer. Write a short story (around 100 words) 
    based on the the topic stored in the session state key 'topic'""",
    input_schema=None,
    output_key="current_story",  # Key for storing output in session state
)
```
