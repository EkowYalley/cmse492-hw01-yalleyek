CMSE 492: Project Repository - hw01-yalleyek
1. Overview
The purpose of this project is to automate the processing of regional sales data and customer lookups to generate high-level business summaries. This repository takes raw transaction logs, cleans and merges them with customer metadata, and produces both tabular summaries and data visualizations.

Repository Structure:

Plaintext
hw01-yalleyek/
├── datafiles/          # Raw input CSVs (sales and customers)
├── pyfiles/            # Main analysis script and helper modules
│   └── my_scripts/     # Core data cleaning logic
├── outputs/            # Generated results (CSVs and PNGs)
├── environment.yml     # Conda environment configuration
└── README.md           # This file
2. Data
The analysis relies on two primary files located in the datafiles/ directory:

sales_jan.csv: Contains transaction records including dates, amounts, and region codes.

customer_lookup.csv: A mapping file used to connect sales data to specific customer demographics.
Both files are provided as standard CSVs. If the data needs to be reset, ensure these files are placed in the datafiles/ folder before running the script.

3. Environment Setup
To ensure all dependencies (including the seaborn library used for the personal modification) are installed, follow these steps using Conda or Miniforge:

Step 1: Create the environment

PowerShell
conda env create -f environment.yml
Step 2: Activate the environment

PowerShell
conda activate cmse492-env
4. Reproduce a Result
To reproduce the analysis and generate the summary files, execute the following command from the root of the repository:

PowerShell
python pyfiles/analysis.py
Expected Results:
Upon completion, the following files will be created/updated in the outputs/ folder:

summary_by_region.csv: A processed table of regional metrics.

revenue_by_region.png: A bar chart showing total revenue.

metric_correlations.png: A heatmap showing relationships between data variables.

5. Personal Analysis
I modified the analysis pipeline to include a Statistical Correlation Heatmap.

Modification: I integrated the seaborn library into analysis.py to calculate a correlation matrix of all numeric variables in the summary table.

Impact: This allows users to see not just the "totals" per region, but also how strongly variables like quantity and revenue are linked, helping identify outliers or data trends.

New Output: The process now generates outputs/metric_correlations.png.

6. Troubleshooting
Path Errors: The script is designed to be run from the root directory (hw01-yalleyek). If you run it from inside pyfiles or datafiles, you will receive a FileNotFoundError. Always use python pyfiles/analysis.py.

ModuleNotFoundError: Ensure you have deactivated any existing .venv or base environments before activating cmse492-env to avoid library conflicts.

Encoding Issues: On some Windows systems, if the environment.yml is not recognized, ensure it is saved with UTF-8 encoding.

7. Containerized Execution (Docker)
For users who prefer not to manage local Python environments, this repository includes a Dockerfile to run the analysis in an isolated container.

Step 1: Build the Image
Build the Docker image using the following command from the root directory:

Bash
docker build -t project-analysis-docker .
Step 2: Run the Analysis
Run the container. This will trigger analysis.py automatically and print the results to your terminal:

Bash
docker run --name analysis-container project-analysis-docker
Step 3: Retrieve Outputs
Because Docker containers run in an isolated file system, you must copy the generated results (the CSV and PNG files) back to your local machine to view them:

Bash
docker cp analysis-container:/app/outputs ./docker_results
This command creates a new folder called docker_results on your computer containing all the files generated during the Docker run.

Why this is the ultimate "Reproducibility" step
By following these steps, a user doesn't even need to have Python installed on their computer. Docker handles the OS, the Python version, and the library installations (Pandas, Seaborn, etc.) internally based on the instructions in your Dockerfile.

Final Cleanup
Once you have copied your files, you can remove the container to save space:

Bash
docker rm analysis-container