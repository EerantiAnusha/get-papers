from typing import List, Tuple

def is_non_academic(affiliation: str) -> bool:
    academic_keywords = [
        "university", "college", "institute", "school",
        "hospital", "department", "centre", "center"
    ]
    affiliation = affiliation.lower()
    return all(keyword not in affiliation for keyword in academic_keywords)

def extract_company_authors(authors: List[dict]) -> Tuple[List[str], List[str], str]:
    names = []
    companies = []
    email = None

    for author in authors:
        affil = author.get("affiliation", "")
        if affil and is_non_academic(affil):
            names.append(author.get("name", ""))
            companies.append(affil)
            if not email and author.get("email"):
                email = author["email"]

    return names, companies, email or "Not Available"
