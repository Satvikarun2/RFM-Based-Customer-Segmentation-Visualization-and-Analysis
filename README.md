OVERVIEW
This project provides a web-based dashboard for analyzing customer behavior using the RFM (Recency, Frequency, Monetary) model. It segments customers based on their purchasing habits and visualizes the data to support marketing decisions.

🚀 Features
Calculates RFM metrics from transaction data

Assigns RFM scores and segments customers into:

Champions

Loyal Customers

Recent Customers

At Risk

Others

Displays a summary table of the top 10 customers

Generates insightful visualizations:

Recency Distribution

Frequency vs. Monetary Scatterplot

Monetary Boxplot

Recency vs. Frequency Scatterplot

Segment Distribution Chart

🧩 Technologies Used
Python (Pandas, Seaborn, Matplotlib)

Flask (for the web app)

HTML/CSS (for the frontend display)

Bootstrap-like responsive layout using flexbox

📁 Project Structure
php
project/
│
├── app.py                     # Main Flask app
├── customer_segment.csv       # Input customer transaction data
├── templates/
│   └── index.html             # Dashboard HTML template
├── static/
│   └── images/                # Auto-generated plots saved here
│       ├── recency_distribution.png
│       ├── freq_vs_monetary.png
│       ├── monetary_boxplot.png
│       ├── recency_vs_frequency.png
│       └── segment_distribution.png
└── README.md                  # You are here
📈 How It Works
Data Loading: Reads customer_segment.csv and filters out invalid entries.

RFM Metrics:

Recency: Days since last purchase.

Frequency: Number of unique invoices.

Monetary: Total purchase value.

Scoring: Each RFM metric is binned into quartiles (1 to 4).

Segmentation: Customers are classified based on their RFM scores using a rule-based system.

Visualization: Saves plots to static/images and displays them in the dashboard.

Rendering: The Flask route renders the index.html with top customer data and plots.

📷 Sample Visuals
Recency Distribution

Frequency vs. Monetary

Monetary Outliers (Boxplot)

Recency vs. Frequency

Customer Segment Distribution

All visuals are dynamically generated and saved under /static/images/.

🛠️ How to Run Locally
1. Clone the repository
bash
git clone https://github.com/your-repo/rfm-dashboard.git
cd rfm-dashboard
2. Install dependencies
bash
pip install flask pandas matplotlib seaborn
3. Run the Flask app
bash
python app.py
The dashboard will be accessible at http://127.0.0.1:5000.

📌 Notes
Ensure customer_segment.csv is present in the root directory.

The app automatically creates and saves plots each time it runs.

Update customer_segment.csv to refresh the dashboard with new data.

