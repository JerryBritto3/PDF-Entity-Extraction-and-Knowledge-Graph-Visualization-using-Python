# PDF Entity Extraction and Knowledge Graph Visualization using Python

## Project Description:
This is an assignment project from Defectech company. This project is completed by Jerrybritto Johnbritto.

It demonstrates a Python-based pipeline to extract structured knowledge from unstructured PDF documents and visualize it as a knowledge graph (KG). Using Python, the system reads PDFs, identifies key entities such as people, emails, and organizations, and builds a graph representing relationships between them. The graph is dynamically laid out for readability, with organizations at the top, members below, and emails at the bottom. The largest organizations are placed first to prevent overlapping nodes.

The pipeline is modular and scalable, allowing each stage—PDF reading, entity extraction, graph construction, and visualization—to run independently. This design makes it easy to extend the project by adding more entity types, such as roles or departments, or by integrating interactive graph visualization tools like Neo4j. The project also includes multiple layout options to compare default, vertical, and custom layered graphs, demonstrating the importance of layout design in knowledge visualization.

## Features:
- Extracts entities (Name, Email, Organization) from PDF documents.
- Removes duplicates and clean noisy data automatically.
- Builds a knowledge graph using NetworkX.
- Custom vertical layout with dynamic spacing and largest-first organization ordering.
- Wraps long labels to fit inside nodes for better readability.
- Color-coded nodes for Person, Email, and Organization.
- Exportable graphs for use in presentations or reports.

## Project Files:
+ ai_legends_email_report.pdf -> Sample PDF used for extraction.
+ txt_entity_kg.py -> Main Python code implementing extraction, graph construction, and visualization.
+ presentation.pptx -> Presentation slides describing the project, approach, code, and outputs.

## Setup & Requirements:
**Prerequisites**:
- Python 3.7+
- Required Python libraries: pip install pdfplumber networkx matplotlib textwrap (if you don't have them already copy and paste this code on your terminal to install).

## Usage:
1. Clone the repository.
2. Run the Py script.

## Outputs:
+ Extracted Entries: You will see a console print of all unique entities displayed on the terminal.
+ Knowledge Graph: Visual graph showing relationships between organizations, people, and emails.
