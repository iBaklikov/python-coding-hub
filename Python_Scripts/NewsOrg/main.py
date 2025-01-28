import os
try:
    import newsapi 
except ImportError:
    os.system('pip install newsapi-python')
# import newsapi


from newsapi import NewsApiClient

# Initialize the NewsAPI client
newsapi = NewsApiClient(api_key='6ecb0257274e46d89bc026f9ad5177a0')

def get_top_headlines(query=None, sources=None, category=None, language='en', country=None):
    """
    Fetches top headlines using NewsAPI.

    Args:
        query (str, optional): Keywords or phrases to search for.
        sources (str, optional): Comma-separated list of news sources to filter.
        category (str, optional): News category (e.g., business, tepip chnology).
        language (str, optional): Language of the news articles (default is 'en').
        country (str, optional): Country code to filter news (e.g., 'us', 'gb').

    Returns:
        list: A list of top headline articles.
    """
    try:
        top_headlines = newsapi.get_top_headlines(
            q=query,
            sources=sources,
            category=category,
            language=language,
            country=country
        )

        if top_headlines.get("status") == "ok":
            return top_headlines.get("articles", [])
        else:
            print("Error fetching top headlines:", top_headlines.get("message"))
            return []
    except Exception as e:
        print("Error in get_top_headlines:", e)
        return []

def get_everything(query=None, sources=None, domains=None, from_param=None, to=None, language='en', sort_by=None, page=1):
    """
    Fetches all articles using NewsAPI.

    Args:
        query (str, optional): Keywords or phrases to search for.
        sources (str, optional): Comma-separated list of news sources to filter.
        domains (str, optional): Comma-separated list of domains to filter.
        from_param (str, optional): Start date for articles (YYYY-MM-DD).
        to (str, optional): End date for articles (YYYY-MM-DD).
        language (str, optional): Language of the news articles (default is 'en').
        sort_by (str, optional): Sorting parameter (e.g., relevancy, popularity, publishedAt).
        page (int, optional): Page number for pagination (default is 1).

    Returns:
        list: A list of articles.
    """
    try:
        all_articles = newsapi.get_everything(
            q=query,
            sources=sources,
            domains=domains,
            from_param=from_param,
            to=to,
            language=language,
            sort_by=sort_by,
            page=page
        )

        if all_articles.get("status") == "ok":
            return all_articles.get("articles", [])
        else:
            print("Error fetching articles:", all_articles.get("message"))
            return []
    except Exception as e:
        print("Error in get_everything:", e)
        return []

def get_sources(category=None, language='en', country=None):
    """
    Fetches available news sources using NewsAPI.

    Args:
        category (str, optional): News category to filter sources.
        language (str, optional): Language of the news sources (default is 'en').
        country (str, optional): Country code to filter sources (e.g., 'us', 'gb').

    Returns:
        list: A list of news sources.
    """
    try:
        sources = newsapi.get_sources(
            category=category,
            language=language,
            country=country
        )

        if sources.get("status") == "ok":
            return sources.get("sources", [])
        else:
            print("Error fetching sources:", sources.get("message"))
            return []
    except Exception as e:
        print("Error in get_sources:", e)
        return []

if __name__ == "__main__":
    # Replace 'your_api_key_here' with your actual NewsAPI key.

    # Fetch top headlines
    # headlines = get_top_headlines(query="python", sources='techcrunch', category="technology", language="en", country="us")
    # print("Top Headlines:")
    # for idx, article in enumerate(headlines, start=1):
    #     print(f"{idx}. {article['title']}")

    # # Fetch all articles matching a query
    # articles = get_everything(query="ai", domains="techcrunch.com", from_param="2025-01-20", to="2025-01-27", sort_by="relevancy")
    # print("\nAll Articles:")
    # for idx, article in enumerate(articles, start=1):
    #     print(f"{idx}. {article['title']}")

    # Fetch available news sources
    sources = get_sources(category="Any", language="en", country="us")
    print("\nSources:")
    for source in sources:
        print(f"- {source['name']}: {source['description']}")