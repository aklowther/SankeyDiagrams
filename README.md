# Sankey Diagrams

## Build the Docker image
```bash
docker build -t sankey-diagrams .
```

## Run the Docker container

This both runs the container but also mounts the active Python files, so when a change is made, it becomes available within the container to test.  Even without that benefit, the volume is needed to be able to access the outputs.

```bash
docker run -it --rm -v "$(pwd):/usr/src/app" -w /usr/src/app --name sankey-diagrams sankey-diagrams salary_sankey_csv_plotly.py salary.csv
```

`salary.csv`, the input file, is generated from Google Sheets.

