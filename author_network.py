import requests
import xml.etree.ElementTree as ET
import networkx as nx
from pyvis.network import Network
import time

# PubMed API Base URL
PUBMED_API_BASE = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"

# Define authors to search (these will be color-coded)
searched_authors = [
    "Suraiya Rasheed",
    "Bryan Holland"
]  # Removed middle initials to improve matching

# Function to normalize names (ignores case and middle initials)
def normalize_name(name):
    return " ".join(name.lower().split())  # Remove extra spaces & lowercase

# Function to fetch PubMed article IDs for a given author
def fetch_pubmed_ids_by_author(author, max_results=50):
    query = f"{author}[Author]"
    search_url = f"{PUBMED_API_BASE}esearch.fcgi?db=pubmed&term={query}&retmax={max_results}&retmode=json"
    response = requests.get(search_url).json()
    time.sleep(1)  # Prevent API overload
    return response.get("esearchresult", {}).get("idlist", [])

# Function to fetch article details (authors only, no titles)
def fetch_article_details(article_ids):
    articles = []
    batch_size = 10  # Fetch in batches of 10 to avoid API overload

    for i in range(0, len(article_ids), batch_size):
        batch_ids = article_ids[i:i+batch_size]
        details_url = f"{PUBMED_API_BASE}efetch.fcgi?db=pubmed&id={','.join(batch_ids)}&retmode=xml"
        response = requests.get(details_url)
        root = ET.fromstring(response.content)
        
        for article in root.findall(".//PubmedArticle"):
            authors = []
            for author in article.findall(".//Author"):
                last_name = author.find("LastName")
                first_name = author.find("ForeName")
                if last_name is not None and first_name is not None:
                    full_name = f"{first_name.text} {last_name.text}"
                    authors.append(normalize_name(full_name))  # Normalize name
            if authors:
                articles.append(authors)

        time.sleep(2)  # Prevent PubMed API rate limits

    return articles

# Step 1: Fetch articles for all searched authors
all_article_ids = set()
for author in searched_authors:
    article_ids = fetch_pubmed_ids_by_author(author)
    all_article_ids.update(article_ids)
    print(f"✅ Found {len(article_ids)} articles for {author}")

# Step 2: Fetch details for all collected articles
selected_papers = fetch_article_details(list(all_article_ids))

# Step 3: Create co-authorship network using NetworkX
G = nx.Graph()
normalized_searched_authors = {normalize_name(name) for name in searched_authors}  # Normalize for matching

for authors in selected_papers:
    for author in authors:
        if author not in G:
            G.add_node(author, node_type="author")
        for co_author in authors:
            if author != co_author:
                if G.has_edge(author, co_author):
                    G[author][co_author]['weight'] += 1
                else:
                    G.add_edge(author, co_author, weight=1)

# Print debug info to confirm nodes/edges are being created
print(f"Total Nodes: {len(G.nodes())}")
print(f"Total Edges: {len(G.edges())}")

# Step 4: Convert NetworkX graph to Pyvis network
net = Network(height="1000px", width="100%", notebook=False, bgcolor="#222222", font_color="white")

if len(G.nodes()) == 0:
    print("❌ No nodes found. Check if the PubMed query returned results.")
else:
    # Color-code searched authors differently
    for node in G.nodes():
        if normalize_name(node) in normalized_searched_authors:
            color = "red"  # Highlight the searched authors
            size = 20  # Make them slightly larger
        else:
            color = "#1f78b4"  # Default color for other co-authors
            size = G.degree(node) * 2 + 10  # Size based on connections

        net.add_node(node, title=node, color=color, size=size)

    # Hide weak edges
    for edge in G.edges():
        weight = G[edge[0]][edge[1]]["weight"]
        if weight > 1:  # Keep only meaningful collaborations
            net.add_edge(edge[0], edge[1], value=weight, physics=False)

    # Disable physics (faster loading)
    net.toggle_physics(False)

    # Use hierarchical layout
    net.set_options("""
    var options = {
      "layout": {
        "hierarchical": {
          "enabled": true,
          "direction": "UD",
          "sortMethod": "directed"
        }
      },
      "edges": {
        "smooth": false
      }
    }
    """)

    # Step 5: Save and open the interactive HTML file
    output_file = "author_network.html"
    net.save_graph(output_file)
    print(f"✅ Author network complete! Open '{output_file}' in a browser.")
