import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import openai
import os

class RAGSystemWithLLM:
    def __init__(self, documentation_path, training_data_path):
        self.documentation = self._load_documentation(documentation_path)
        self.training_data = pd.read_csv(training_data_path)
        self.vectorizer = TfidfVectorizer()
        self.documents = self._prepare_documents()
        self.document_embeddings = self.vectorizer.fit_transform(self.documents)
        
        # Initialize OpenAI client
        self.client = openai.OpenAI(
            api_key=os.getenv("OPENAI_API_KEY"),
            base_url=os.getenv("OPENAI_API_BASE")
        )

    def _load_documentation(self, path):
        with open(path, "r") as f:
            return f.read()

    def _prepare_documents(self):
        docs = [self.documentation]
        # Add rows from training data as documents
        for index, row in self.training_data.iterrows():
            doc_text = f"Loan Application ID: {row['Loan_ID']}\n"
            for col in self.training_data.columns:
                if col != "Loan_ID":
                    doc_text += f"{col}: {row[col]}\n"
            docs.append(doc_text)
        return docs

    def retrieve_documents(self, query, top_k=3):
        query_embedding = self.vectorizer.transform([query])
        similarities = cosine_similarity(query_embedding, self.document_embeddings)[0]
        top_indices = similarities.argsort()[-top_k:][::-1]
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

if __name__ == "__main__":
    rag_system = RAGSystemWithLLM("loan_data_documentation.md", "/home/ubuntu/upload/TrainingDataset.csv")
    print("RAG System with LLM initialized. Number of documents:", len(rag_system.documents))
    
    # Example queries
    queries = [
        "What is the loan status for LP001003?",
        "What factors affect loan approval?",
        "How many applicants are self-employed?",
        "What is the average loan amount?"
    ]
    
    for query in queries:
        print(f"\n{'='*50}")
        print(f"Query: {query}")
        result = rag_system.ask_question(query)
        print(f"Response: {result['response']}")

