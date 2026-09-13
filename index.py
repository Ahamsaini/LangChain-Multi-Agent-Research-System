from langchain_groq import ChatGroq



llm = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0,
    api_key="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"
    # other params...
)
output=llm.invoke("hello")
print(output)