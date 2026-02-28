"""
RAG Chatbot untuk query dokumen panduan - VERSI NONAKTIF SEMENTARA
"""
import streamlit as st
import requests
import json
import os
from typing import List, Dict
import hashlib

# RAG Chatbot dinonaktifkan sementara karena masalah dependency
class RAGChatbot:
    def __init__(self, model_name='mistral:latest'):
        self.model_name = model_name
        self.ollama_url = 'http://localhost:11434'
        self.documents_loaded = False
        st.warning("⚠️ RAG Chatbot sedang dalam perbaikan. Fitur ini akan segera hadir.")
    
    def check_ollama(self):
        """Check if Ollama is available"""
        return False
    
    def load_pdf_document(self, pdf_file, doc_id: str = "dataset_guide"):
        """Load PDF document - dinonaktifkan"""
        st.error("RAG Chatbot sedang dalam perbaikan. Fitur tidak tersedia.")
        return False
    
    def _split_text(self, text: str, chunk_size: int = 500, overlap: int = 100) -> List[str]:
        """Split text - placeholder"""
        return []
    
    def query_documents(self, query: str, n_results: int = 3) -> str:
        """Query documents - dinonaktifkan"""
        return "RAG Chatbot sedang dalam perbaikan. Silakan gunakan tab lain untuk analisis."
    
    def get_column_explanation(self, column: str) -> str:
        """Get column explanation - dinonaktifkan"""
        return "Fitur ini sedang dalam perbaikan."
    
    def suggest_features_for_modeling(self) -> str:
        """Get feature suggestions - dinonaktifkan"""
        return "Fitur ini sedang dalam perbaikan."