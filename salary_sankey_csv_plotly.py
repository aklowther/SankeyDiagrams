import plotly.graph_objects as go
import pandas as pd
import os
import sys

# Read data from file
if len(sys.argv) < 2:
    print("Error: Please provide the path to the CSV file as an argument.")
    sys.exit(1)

# Read data from CSV file
csv_file = sys.argv[1]
try:
    df = pd.read_csv(csv_file)
except FileNotFoundError:
    print(f"Error: File '{csv_file}' not found.")
    exit(1)
except pd.errors.EmptyDataError:
    print(f"Error: File '{csv_file}' is empty.")
    exit(1)
except pd.errors.ParserError:
    print(f"Error: File '{csv_file}' contains invalid CSV data.")
    exit(1)

# Define nodes dynamically from the data
nodes = list(set(df["source"]) | set(df["target"]))
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
        source=[node_indices[src] for src in df["source"]],
        target=[node_indices[tgt] for tgt in df["target"]],
        value=df["value"],
        color=df["color"],
        customdata=[[f"{val}"] for val in df["value"]],
        hovertemplate='%{source.label} → %{target.label}<br>Value: %{value}<extra></extra>',
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
output_dir = 'output'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
    print(f"Created output directory '{output_dir}'")

fig.write_image(f'{output_dir}/salary_distribution.png')
fig.write_html(f"{output_dir}/salary_sankey_plotly.html")
print(f"Sankey diagram saved as 'salary_distribution.png' in the '{output_dir}' directory")
