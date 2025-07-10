import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

import argparse
import csv
from get_papers.pubmed import search_pubmed, fetch_details
from get_papers.utils import extract_company_authors

def main():
    parser = argparse.ArgumentParser(description="Fetch PubMed papers with non-academic authors.")
    parser.add_argument("query", help="PubMed search query")
    parser.add_argument("-f", "--file", help="CSV output filename")
    parser.add_argument("-d", "--debug", action="store_true", help="Enable debug info")
    args = parser.parse_args()

    print("Starting PubMed search...")  # Optional: helpful debug line

    ids = search_pubmed(args.query)
    if args.debug:
        print(f"Found {len(ids)} paper IDs")

    papers = fetch_details(ids)

    results = []
    for paper in papers:
        authors = paper["Authors"]
        names, companies, email = extract_company_authors(authors)

        if names:
            results.append({
                "PubmedID": paper["PubmedID"],
                "Title": paper["Title"],
                "Publication Date": paper["PublicationDate"],
                "Non-academic Author(s)": "; ".join(names),
                "Company Affiliation(s)": "; ".join(set(companies)),
                "Corresponding Author Email": email
            })

    if not results:
        print("No papers found with non-academic authors.")
        return

    if args.file:
        with open(args.file, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=results[0].keys())
            writer.writeheader()
            writer.writerows(results)
        print(f"Results written to {args.file}")
    else:
        for row in results:
            print(row)

if __name__ == "__main__":
    main()
