from flask import Blueprint, request, jsonify
from flask_cors import cross_origin
import sys
import os

# Add the src directory to the path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from mock_rag import MockRAGSystem

rag_bp = Blueprint('rag', __name__)

# Initialize RAG system
rag_system = None

def init_rag_system():
    global rag_system
    if rag_system is None:
        documentation_path = os.path.join(os.path.dirname(__file__), '..', 'loan_data_documentation.md')
        training_data_path = os.path.join(os.path.dirname(__file__), '..', 'TrainingDataset.csv')
        rag_system = MockRAGSystem(documentation_path, training_data_path)
    return rag_system

@rag_bp.route('/chat', methods=['POST'])
@cross_origin()
def chat():
    try:
        data = request.get_json()
        if not data or 'message' not in data:
            return jsonify({'error': 'Message is required'}), 400
        
        message = data['message']
        
        # Initialize RAG system if not already done
        rag = init_rag_system()
        
        # Get response from RAG system
        result = rag.ask_question(message)
        
        return jsonify({
            'response': result['response'],
            'query': result['query']
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@rag_bp.route('/health', methods=['GET'])
@cross_origin()
def health():
    return jsonify({'status': 'healthy', 'message': 'RAG system is running'})

