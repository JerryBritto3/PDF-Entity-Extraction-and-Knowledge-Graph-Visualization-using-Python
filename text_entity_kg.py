# Defectech  Assignment - Entities Extraction and Knowledge graph visualization using Python
# Jerry britto John britto

#Importing required libraries
import pdfplumber        # Reads PDF text
import re                # Regex for email extraction
import networkx as nx    # For building the Knowledge Graph
import matplotlib.pyplot as plt # For plotting
import matplotlib.patches as mpatches # For legend patches
import textwrap   # built-in Python text wrapping

#1. Reading all texts from our pdf
def read_pdf_text(pdf_path):
    """
    Reads all text from PDF and returns a clean list of lines.
    Empty lines are removed.
    """
    lines = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                # Splitting text into lines and removing empty lines
                page_lines = [line.strip() for line in text.split("\n") if line.strip()]
                lines.extend(page_lines)
    return lines

#2. Extracting required entities
def extract_entities(lines):
    """
    Extracting full Name, Email, and Organization from PDF text.
    Filtering out leadiing prefixes and other junks.
    """
    people = [] # list to store extracted tuples
    email_pattern = re.compile(r"[\w\.-]+@[\w\.-]+\.\w+") # email regex

    for line in lines:
        # find all email addresses in this line
        emails = email_pattern.findall(line)
        if not emails:
            continue  # skip lines with no email
        
        for email in emails:
            # extracting name from text before email
            name_part = line.split(email)[0].strip()

            # removing any leading prefixes
            name_part = re.sub(r"^(From:|To:)\s*", "", name_part, flags=re.IGNORECASE)
            name_part = name_part.replace("<", "").strip()
            # remove trailing commas or colons
            name_part = name_part.rstrip(",:")
            
            # skipping obvious non-name lines
            if len(name_part) < 3:
                continue

            # get organization from email domain
            org = email.split("@")[1].split(".")[0].capitalize()

            if name_part: 
                people.append((name_part, email, org))

    # removing duplicates based on email
    unique_people = []
    seen_emails = set()
    for p in people:
        if p[1] not in seen_emails:
            unique_people.append(p)
            seen_emails.add(p[1])

    return unique_people

#3. Building Knowledge Graph
def build_kg(people):
    """
    Building a KG with Name, Email, and Organization.
    """
    G = nx.Graph() # Create an empty graph
    
    for name, email, org in people:
        # Adding nodes with type attribute
        G.add_node(name, type="person")
        G.add_node(email, type="email")
        G.add_node(org, type="org")
        # Connecting person to email and organization
        G.add_edge(name, email)
        G.add_edge(name, org)
        
    return G

#3(i) Helper function for Word based wrapping
def wrap_text(text, width=18):
    """
    This wraps the text using word boundaries and returns multi-line string.
    """
    return textwrap.fill(text, width=width)

#4. Drawing graph
def draw_graph(G):
    """
    Made a custom vertical layout for better visualization:
    ORG -> NAME -> EMAIL
    Organizations ordered by number of members (largest first)
    Dynamically spacing large organizations to avoid overlaps.
    """
    plt.figure(figsize=(26, 14))

    pos = {}

    # Grouping people by org
    org_people = {}
    for node, data in G.nodes(data=True):
        if data["type"] == "person":
            for neighbor in G.neighbors(node):
                if G.nodes[neighbor]["type"] == "org":
                    org_people.setdefault(neighbor, []).append(node)
    
    # Sort orgs by number of members (largest first)
    org_people_sort = dict( sorted(org_people.items(), key=lambda x: len(x[1]), reverse=True))

    # Assigning positions dynamically
    current_x = 0        # tracks where next org starts
    member_spacing = 12  # horizontal gap between members
    org_padding = 4      # gap between orgs

    for org, people in org_people_sort.items():

        width = len(people) * member_spacing
        center = current_x + width / 2

        # Org node
        pos[org] = (center, 4)

        # Placing Person nodes under org
        for i, person in enumerate(people):

            x = current_x + i * member_spacing
            pos[person] = (x, 2)

            # Placing email under person
            for neighbor in G.neighbors(person):
                if G.nodes[neighbor]["type"] == "email":
                    pos[neighbor] = (x, 1)

        current_x += width + org_padding  # Moving x for next org
        
    # Assigning colors
    colors = []

    for node, data in G.nodes(data=True):
        if data["type"] == "person":
            colors.append("skyblue")
        elif data["type"] == "org":
            colors.append("orange")
        else:
            colors.append("violet")
            
    # Wrapped labels
    labels = {}

    for node, data in G.nodes(data=True):
        if data["type"] in ["person", "email"]:
            labels[node] = wrap_text(node, width=15)
        else:
            labels[node] = node

    # Drawing graph
    nx.draw(
        G, pos, labels=labels, node_color=colors, node_size=6500, font_size=8,
    )

    # Adding legend
    plt.legend(handles=[
        mpatches.Patch(color="orange", label="Organization"),
        mpatches.Patch(color="skyblue", label="Person"),
        mpatches.Patch(color="violet", label="Email")
    ])

    plt.title("Team Knowledge Graph")
    plt.axis("off")
    plt.show()
    
# Main pipeline
if __name__ == "__main__":

    pdf_path = "ai_legends_email_report.pdf"
    lines = read_pdf_text(pdf_path)
    people = extract_entities(lines)
    
    print("Extracted entries:")
    for p in people:
        print(p)

    # Build graph
    G = build_kg(people)
    # Draw graph
    draw_graph(G)
    
    
