import plotly.graph_objects as go
import json
import sys

# Read data from file
if len(sys.argv) < 2:
    print("Error: Please provide the path to the JSON file as an argument.")
    sys.exit(1)

file_path = sys.argv[1]
try:
    with open(file_path, 'r') as file:
        links = json.load(file)
except FileNotFoundError:
    print(f"Error: File '{file_path}' not found.")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: File '{file_path}' contains invalid JSON.")
    sys.exit(1)

# Calculate total salary value for unknown values
total_outgoing = sum(link["value"] for link in links if link["source"] == "Salary")

# Process links and handle unknown values
processed_links = []
for link in links:
    processed_link = link.copy()
    if processed_link.get("value") == "unknown":
        processed_link["value"] = total_outgoing * 0.1
    elif isinstance(processed_link.get("value"), str) and processed_link["value"].lower() == "unknown":
        processed_link["value"] = total_outgoing * 0.1
    processed_links.append(processed_link)

# Define nodes dynamically from processed links
nodes = list(set(link["source"] for link in processed_links) | set(link["target"] for link in processed_links))
node_indices = {name: i for i, name in enumerate(nodes)}

# Build Sankey diagram
fig = go.Figure(data=[go.Sankey(
    node=dict(
        pad=15,
        thickness=20,
        line=dict(color="black", width=0.5),
        label=nodes
    ),
    link=dict(
        source=[node_indices[link["source"]] for link in processed_links],
        target=[node_indices[link["target"]] for link in processed_links],
        value=[link["value"] for link in processed_links],
        color=[link["color"] for link in processed_links],
        customdata=[[f"{link['value']}"] for link in processed_links],
        hovertemplate='%{source.label} → %{target.label}<br>Value: %{value}'+
                    '<extra></extra>',
        line=dict(width=0.5, color='black')
    )
)])

fig.update_layout(
    title_text="Salary Flow Breakdown",
    font=dict(
        family="Arial, sans-serif",
        size=14,
        color="black"
    ),
    title_font=dict(
        family="Arial, sans-serif",
        size=18,
        color="black"
    ),
    width=1200,
    height=800,
    margin=dict(l=50, r=50, t=80, b=50),
    showlegend=False
)
fig.show()


# Save the figure as an image and HTML file
import os

output_dir = 'output'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
    print(f"Created output directory '{output_dir}'")

fig.write_image(f'{output_dir}/salary_distribution.png')
fig.write_html(f"{output_dir}/salary_sankey_plotly.html")
print(f"Sankey diagram saved as 'salary_distribution.png' in the '{output_dir}' directory")
