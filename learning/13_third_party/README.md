Benefit of this is we don't have to do all the heavy lifting. It's already taken care of by langchain

The docs say use langchain_community tavily-python but TavilySearchResults was deprecated in 
LangChain 0.3.25 and will be removed in 1.0.
Instead install langchain-tavily and import as `from langchain_tavily import TavilySearch`
and use TavilySearch()


For github search see https://docs.github.com/en/apps/creating-github-apps/registering-a-github-app/registering-a-github-app to get everything set up.
You do need to install the app. In the app settings, there's an "Install App" in the left menu
Include the full path to the private key as well.

See https://python.langchain.com/docs/integrations/tools/ for a massive list of tools