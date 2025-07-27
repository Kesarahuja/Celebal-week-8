# Celebal-week-8
# Celebal - Week 8: Document Clustering for Topic Modelling

This repository contains the work done during **Week 8** of the Celebal Data Science Internship Program.  
The focus of this week was on **Natural Language Processing (NLP)** using **unsupervised learning** techniques, specifically **Document Clustering** for **Topic Modeling**.

---

## 🧠 Problem Statement

To analyze a collection of documents and automatically group them into clusters that reflect underlying topics, using NLP techniques like vectorization and clustering algorithms.

---

## 📂 Project Structure

```
Celebal-week-8/
│
├── Data/                     # Raw and preprocessed text data
├── Notebooks/               # Jupyter notebooks with step-by-step code
├── Outputs/                 # Visualizations and clustering results
├── utils.py                 # Utility functions for preprocessing
├── requirements.txt         # Python dependencies
└── README.md                # Project overview
```

---

## 🧪 Techniques Used

- Text Preprocessing:
  - Lowercasing, stopword removal, stemming
- Vectorization:
  - TF-IDF (Term Frequency-Inverse Document Frequency)
- Clustering:
  - KMeans
  - Hierarchical Clustering
- Dimensionality Reduction:
  - PCA / t-SNE (for visualization)
- Evaluation:
  - Silhouette Score
  - Elbow Method

---

## 📊 Sample Results

- Clustered documents based on themes such as politics, technology, sports, etc.
- Visualized topic separation using 2D scatter plots
- Identified most frequent words in each topic cluster

---

## 🚀 How to Run

1. **Clone the repository**

```bash
git clone https://github.com/Kesarahuja/Celebal-week-8.git
cd Celebal-week-8
```

2. **Create a virtual environment (optional but recommended)**

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Run the notebooks**

Open the Jupyter notebooks in the `Notebooks/` directory to explore clustering step by step.

---

## 🧠 Learnings

- Gained hands-on experience with unsupervised NLP.
- Learned to evaluate clustering effectiveness.
- Understood the role of dimensionality reduction in visualization.

---

## 📌 Future Improvements

- Experiment with LDA (Latent Dirichlet Allocation)
- Use larger or domain-specific datasets
- Deploy as a web app for interactive topic discovery

---
