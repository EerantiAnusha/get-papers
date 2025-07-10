import requests
import xml.etree.ElementTree as ET
from typing import List, Dict

def search_pubmed(query: str) -> List[str]:
    url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
    params = {
        "db": "pubmed",
        "term": query,
        "retmode": "json",
        "retmax": 20
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()
    return data["esearchresult"]["idlist"]

def fetch_details(pubmed_ids: List[str]) -> List[Dict]:
    url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
    params = {
        "db": "pubmed",
        "id": ",".join(pubmed_ids),
        "retmode": "xml"
    }
    response = requests.get(url, params=params)
    root = ET.fromstring(response.content)
    results = []

    for article in root.findall(".//PubmedArticle"):
        data = {
            "PubmedID": article.findtext(".//PMID"),
            "Title": article.findtext(".//ArticleTitle"),
            "PublicationDate": article.findtext(".//PubDate/Year") or "Unknown",
            "Authors": []
        }

        for author in article.findall(".//Author"):
            name = f"{author.findtext('LastName', '')} {author.findtext('ForeName', '')}".strip()
            affiliation = author.findtext(".//AffiliationInfo/Affiliation", "")
            email = next((word for word in affiliation.split() if "@" in word), None)

            data["Authors"].append({
                "name": name,
                "affiliation": affiliation,
                "email": email
            })

        results.append(data)

    return results
