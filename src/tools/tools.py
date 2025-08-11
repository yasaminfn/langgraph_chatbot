from langchain_tavily import TavilySearch
import requests
import json #the format we want to retrieve
import os
from langchain.tools import tool
from dotenv import load_dotenv

load_dotenv()
TAVILY_API_KEY=os.getenv("TAVILY_API_KEY")

tavily_tool = TavilySearch(max_results=2)

# Wrap Tavily call to handle errors
@tool
def safe_tavily(query: str) -> str:
    """does a tavily search based on the query

    Args:
        query (str)

    Returns:
        str: search results
    """
    try:
        result = tavily_tool.invoke({"query": query})
        if not result:
            return "No results returned from Tavily."
        print("Tavily raw result:", result)
        return str(result)
    
    except json.JSONDecodeError as e:
        return f"Tavily JSON error: {e}"
    except requests.exceptions.RequestException as e:
        return f"Tavily network error: {e}"
    except Exception as e:
        return f"Tavily unknown error: {e}"

TOOLs = [safe_tavily]
