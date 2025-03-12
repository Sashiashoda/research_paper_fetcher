import requests
import csv
from typing import List, Dict

# Define the PubMed API URL
PUBMED_API_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
EFETCH_API_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"

def fetch_paper_ids(query: str, max_results: int = 100) -> List[str]:
    """Fetches PubMed paper IDs based on the query."""
    params = {
        'db': 'pubmed',
        'term': query,
        'retmax': max_results,
        'retmode': 'xml'
    }
    response = requests.get(PUBMED_API_URL, params=params)
    if response.status_code == 200:
        # Extract IDs from XML response
        ids = response.text.split('<Id>')[1:]
        return [id.split('</Id>')[0] for id in ids]
    else:
        print("Error fetching paper IDs.")
        return []

def fetch_paper_details(paper_id: str) -> Dict:
    """Fetch details of a paper (title, authors, etc.) by PubMed ID."""
    params = {
        'db': 'pubmed',
        'id': paper_id,
        'retmode': 'xml'
    }
    response = requests.get(EFETCH_API_URL, params=params)
    if response.status_code == 200:
        # Parse the XML response to extract paper details (you can use an XML parser here)
        # For simplicity, let's assume it returns a basic dict format
        # You should replace this with actual XML parsing logic
        return {
            'PubmedID': paper_id,
            'Title': "Paper Title",  # Extract from XML
            'Publication Date': "2025-03-11",  # Extract from XML
            'Non-academic Author(s)': "Author 1, Author 2",  # Extract from XML
            'Company Affiliation(s)': "Pharma Corp",  # Extract from XML
            'Corresponding Author Email': "corresponding.author@example.com",  # Extract from XML
        }
    else:
        print(f"Error fetching paper details for {paper_id}")
        return {}

def save_to_csv(papers: List[Dict], filename: str):
    """Saves the fetched paper details to a CSV file."""
    keys = papers[0].keys() if papers else []
    with open(filename, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=keys)
        writer.writeheader()
        writer.writerows(papers)

def main(query: str, output_filename: str = 'papers.csv'):
    """Main function to fetch papers based on a query and save to CSV."""
    paper_ids = fetch_paper_ids(query)
    if not paper_ids:
        print("No papers found.")
        return
    
    papers = []
    for paper_id in paper_ids:
        details = fetch_paper_details(paper_id)
        if details:
            papers.append(details)
    
    if papers:
        save_to_csv(papers, output_filename)
        print(f"Saved {len(papers)} papers to {output_filename}")
    else:
        print("No papers to save.")
