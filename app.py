from flask import Flask, render_template
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

app = Flask(__name__)

# Ensure required folders
os.makedirs("static/images", exist_ok=True)

@app.route("/")
def rfm_dashboard():
    # Load and clean data
    df = pd.read_csv("customer_segment.csv", encoding='ISO-8859-1')
    df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])
    df = df.dropna(subset=['CustomerID'])

    # RFM calculations
    latest_date = df['InvoiceDate'].max()
    rfm = df.groupby('CustomerID').agg({
        'InvoiceDate': lambda x: (latest_date - x.max()).days,
        'InvoiceNo': 'nunique',
        'Quantity': lambda x: (x * df.loc[x.index, 'UnitPrice']).sum()
    })
    rfm.columns = ['Recency', 'Frequency', 'Monetary']
    rfm = rfm.reset_index()

    # Scoring each RFM component (1-4 quartiles)
    rfm['R'] = pd.qcut(rfm['Recency'], 4, labels=[4, 3, 2, 1]).astype(int)
    rfm['F'] = pd.qcut(rfm['Frequency'].rank(method='first'), 4, labels=[1, 2, 3, 4]).astype(int)
    rfm['M'] = pd.qcut(rfm['Monetary'], 4, labels=[1, 2, 3, 4]).astype(int)

    # Combine scores into one RFM Score
    rfm['RFM_Score'] = rfm['R'].astype(str) + rfm['F'].astype(str) + rfm['M'].astype(str)

    # Define segmentation rules
    def segment_customer(row):
        r, f, m = row['R'], row['F'], row['M']
        if r >= 3 and f >= 3 and m >= 3:
            return 'Champions'
        elif r >= 2 and f >= 3:
            return 'Loyal Customers'
        elif r >= 3 and f <= 2:
            return 'Recent Customers'
        elif r == 1 and f >= 3:
            return 'At Risk'
        else:
            return 'Others'

    rfm['Segment'] = rfm.apply(segment_customer, axis=1)

    # Save sample RFM + Segment as HTML table
    table_data = rfm[['CustomerID', 'Recency', 'Frequency', 'Monetary', 'RFM_Score', 'Segment']].head(10).to_dict(orient='records')
    table_columns = ['CustomerID', 'Recency', 'Frequency', 'Monetary', 'RFM_Score', 'Segment']

    # Plotting functions
    def save_plot(func, filename):
        plt.figure(figsize=(6, 4))
        func()
        plt.tight_layout()
        plt.savefig(f"static/images/{filename}")
        plt.close()

    save_plot(lambda: sns.histplot(rfm['Recency'], bins=30, kde=True, color='skyblue'),
              "recency_distribution.png")
    save_plot(lambda: sns.scatterplot(data=rfm, x='Frequency', y='Monetary', alpha=0.7),
              "freq_vs_monetary.png")
    save_plot(lambda: sns.boxplot(y=rfm['Monetary'], color='lightgreen'),
              "monetary_boxplot.png")
    save_plot(lambda: sns.scatterplot(data=rfm, x='Recency', y='Frequency', alpha=0.6, color='salmon'),
              "recency_vs_frequency.png")
    save_plot(lambda: sns.countplot(y='Segment', data=rfm, order=rfm['Segment'].value_counts().index, palette='Set2'),
              "segment_distribution.png")

    return render_template("index.html",
                           table_data=table_data,
                           table_columns=table_columns,
                           charts=[
                               ("Recency Distribution", "recency_distribution.png"),
                               ("Frequency vs Monetary", "freq_vs_monetary.png"),
                               ("Monetary Boxplot", "monetary_boxplot.png"),
                               ("Recency vs Frequency", "recency_vs_frequency.png"),
                               ("Customer Segment Distribution", "segment_distribution.png"),
                           ])

if __name__ == "__main__":
    app.run(debug=True)
