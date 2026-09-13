from src.tools.tools import web_search , scrape_url
from rich import print
r=web_search.invoke("What is the latest news of the openai new LLm model . and is the name and version of this model")
# output=web_search("Latest news on AI research")
# print(output)
# result = scrape_url("https://blog.google/innovation-and-ai/products")
# print(result)
print(r)