import csv
import re
import openai
import os
from collections import Counter

class SimpleRAGSystem:
    def __init__(self, documentation_path, training_data_path):
        self.documentation = self._load_documentation(documentation_path)
        self.training_data = self._load_csv_data(training_data_path)
        self.documents = self._prepare_documents()
        
        # Initialize OpenAI client
        self.client = openai.OpenAI(
            api_key=os.getenv("OPENAI_API_KEY"),
            base_url=os.getenv("OPENAI_API_BASE")
        )

    def _load_documentation(self, path):
        with open(path, "r") as f:
            return f.read()

    def _load_csv_data(self, path):
        data = []
        with open(path, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                data.append(row)
        return data

    def _prepare_documents(self):
        docs = [self.documentation]
        # Add rows from training data as documents
        for row in self.training_data:
            doc_text = f"Loan Application ID: {row['Loan_ID']}\n"
            for key, value in row.items():
                if key != "Loan_ID":
                    doc_text += f"{key}: {value}\n"
            docs.append(doc_text)
        return docs

    def _simple_similarity(self, query, document):
        """Simple keyword-based similarity scoring"""
        query_words = set(re.findall(r'\w+', query.lower()))
        doc_words = set(re.findall(r'\w+', document.lower()))
        
        # Count common words
        common_words = query_words.intersection(doc_words)
        
        # Simple scoring based on common words and document length
        if len(query_words) == 0:
            return 0
        
        score = len(common_words) / len(query_words)
        return score

    def retrieve_documents(self, query, top_k=3):
        scores = []
        for i, doc in enumerate(self.documents):
            score = self._simple_similarity(query, doc)
            scores.append((score, i))
        
        # Sort by score and get top k
        scores.sort(reverse=True)
        top_indices = [idx for _, idx in scores[:top_k]]
        return [self.documents[i] for i in top_indices]

    def generate_response(self, query, retrieved_docs):
        context = "\n\n".join(retrieved_docs)
        
        prompt = f"""You are a helpful assistant that answers questions about loan applications based on the provided context. 
        Use only the information from the context to answer the question. If the information is not available in the context, say so.

        Context:
        {context}

        Question: {query}

        Answer:"""

        try:
            response = self.client.chat.completions.create(
                model="gpt-4.1-mini",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that answers questions about loan applications based on provided context."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=500,
                temperature=0.3
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error generating response: {str(e)}"

    def ask_question(self, query):
        retrieved_docs = self.retrieve_documents(query)
        response = self.generate_response(query, retrieved_docs)
        return {
            "query": query,
            "retrieved_documents": retrieved_docs,
            "response": response
        }

