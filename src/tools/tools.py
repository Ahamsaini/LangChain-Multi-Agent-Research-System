from langchain.tools import tool
import requests
import os
from dotenv import load_dotenv
from tavily import TavilyClient
from rich import print
from  bs4 import BeautifulSoup
from readability import Document
import trafilatura
import re


load_dotenv()
tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

@tool
def web_search(query:str)-> str:
    """
    Search the web for recent and reliable information on a topic . Return Titles , URL_s and  , content etc
    """
    results = tavily.search(query=query, max_result=5)
 
    out=[]
    for r in results['results']:
        out.append(
            f"Title : {r['title']}\nURL:{r['url']}\nSnippet:{r['content'][:300]}\n"
        )
    return "\n-----\n".join(out)    


@tool
def scrape_url(url: str) -> str:
    """
    Scrape and extract clean readable content from a URL.
    Uses multiple extraction strategies for better reliability.
    """
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/124.0 Safari/537.36"
        ),
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": "https://www.google.com",
    }

    try:
        response = requests.get(
            url,
            headers=headers,
            timeout=15
        )
        response.raise_for_status()

        html = response.text

        # -------------------------------------------------
        # 1. Try Trafilatura
        # -------------------------------------------------
        extracted = trafilatura.extract(
            html,
            include_comments=False,
            include_tables=False,
            include_links=True,
            favor_precision=True
        )

        if extracted and len(extracted.strip()) > 200:
            return extracted.strip()

        # -------------------------------------------------
        # 2. Try readability
        # -------------------------------------------------
        try:
            doc = Document(html)

            title = doc.title()
            summary_html = doc.summary()

            soup = BeautifulSoup(summary_html, "html.parser")

            # Remove unwanted elements
            for tag in soup(["script", "style", "noscript"]):
                tag.decompose()

            text = soup.get_text(separator="\n", strip=True)

            if text and len(text) > 200:
                if title:
                    return f"{title.strip()}\n\n{text.strip()}"
                return text.strip()

        except Exception:
            pass

        # -------------------------------------------------
        # 3. BeautifulSoup fallback
        # -------------------------------------------------
        soup = BeautifulSoup(html, "html.parser")

        # Remove elements that usually don't contain useful content
        for tag in soup([
            "script",
            "style",
            "noscript",
            "svg",
            "nav",
            "footer",
            "header",
            "aside",
            "form"
        ]):
            tag.decompose()

        # Prefer common article/content containers
        content = (
            soup.find("article")
            or soup.find("main")
            or soup.find("body")
        )

        if not content:
            raise ValueError("Could not find readable content on the page.")

        text = content.get_text(separator="\n", strip=True)

        # -------------------------------------------------
        # 4. Clean extracted text
        # -------------------------------------------------
        lines = []

        for line in text.splitlines():
            line = re.sub(r"\s+", " ", line).strip()

            if line:
                lines.append(line)

        text = "\n".join(lines)

        if not text:
            raise ValueError("No readable text could be extracted.")

        return text

    except requests.exceptions.Timeout:
        return f"Error: Request timed out while scraping {url}"

    except requests.exceptions.HTTPError as e:
        return f"Error: HTTP error while scraping {url}: {e}"

    except requests.exceptions.RequestException as e:
        return f"Error: Failed to fetch {url}: {e}"

    except Exception as e:
        return f"Error: Failed to extract content from {url}: {e}"


