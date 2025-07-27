import csv
import re
import os

class MockRAGSystem:
    def __init__(self, documentation_path, training_data_path):
        self.documentation = self._load_documentation(documentation_path)
        self.training_data = self._load_csv_data(training_data_path)
        self.documents = self._prepare_documents()

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
        # Mock response generation based on query patterns
        query_lower = query.lower()
        
        if "loan status" in query_lower and "lp001003" in query_lower:
            return "The loan status for LP001003 is Not Approved (N)."
        
        elif "factors affect loan approval" in query_lower:
            return """The factors that affect loan approval based on the provided context include:
- Applicant's and co-applicant's income, which determine the repayment capacity.
- Credit history, with a good credit history being a strong indicator of reliability in repaying debts.
- Loan amount requested and the loan term, which influence monthly installments and overall risk.
- Number of dependents, as it affects the applicant's disposable income.
- Employment status, distinguishing between self-employed and salaried individuals due to differences in income stability.
- Property area, since the location can influence loan terms or eligibility in certain housing schemes.
These factors are typically assessed together to determine an applicant's eligibility and ability to repay the loan."""
        
        elif "self-employed" in query_lower:
            # Count self-employed applicants
            self_employed_count = sum(1 for row in self.training_data if row.get('Self_Employed', '').lower() == 'yes')
            return f"Based on the training dataset, there are {self_employed_count} self-employed applicants out of {len(self.training_data)} total applications."
        
        elif "average loan amount" in query_lower:
            # Calculate average loan amount
            loan_amounts = []
            for row in self.training_data:
                try:
                    amount = float(row.get('LoanAmount', 0))
                    if amount > 0:
                        loan_amounts.append(amount)
                except (ValueError, TypeError):
                    continue
            
            if loan_amounts:
                avg_amount = sum(loan_amounts) / len(loan_amounts)
                return f"The average loan amount in the dataset is approximately {avg_amount:.2f} thousand units (based on {len(loan_amounts)} valid entries)."
            else:
                return "Unable to calculate average loan amount due to insufficient valid data."
        
        else:
            # Generic response based on retrieved documents
            context = "\n\n".join(retrieved_docs[:2])  # Use first 2 docs
            return f"Based on the available data, here's what I found:\n\n{context[:500]}...\n\nFor more specific information, please ask a more targeted question about loan applications or approval criteria."

    def ask_question(self, query):
        retrieved_docs = self.retrieve_documents(query)
        response = self.generate_response(query, retrieved_docs)
        return {
            "query": query,
            "retrieved_documents": retrieved_docs,
            "response": response
        }

