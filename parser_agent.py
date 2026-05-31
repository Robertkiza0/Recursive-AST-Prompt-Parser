import ast

class ASTPromptCompressor:
    def __init__(self, file_path):
        self.file_path = file_path

    def compress_for_llm(self):
        """Analyse le code source et extrait uniquement la structure pour économiser les tokens du LLM."""
        with open(self.file_path, "r") as source:
            tree = ast.parse(source.read())

        compressed_prompt = f"--- Structure Analysis of {self.file_path} for LLM Context ---\n"
        
        for node in ast.walk(tree):
            # Si l'agent repère une déclaration de classe
            if isinstance(node, ast.ClassDef):
                compressed_prompt += f"Class Found: {node.name}\n"
            
            # Si l'agent repère une fonction ou méthode
            elif isinstance(node, ast.FunctionDef):
                # Extraction des arguments de la fonction
                args = [arg.arg for arg in node.args.args]
                compressed_prompt += f"  -> Method: {node.name}({', '.join(args)})\n"
                
        return compressed_prompt

# --- SCRIPT DE TEST ---
if __name__ == "__main__":
    # Étape 1: Création d'un faux code source Python complexe avec classes et fonctions
    complex_code = """
class DataPipeline:
    def __init__(self, source_url):
        self.source = source_url
        
    def fetch_data(self):
        # Imagine 100 lignes de logique complexe ici
        pass
        
    def process_language_model(self, model_name, token_limit):
        # Logique complexe d'agent de traitement
        return True
"""
    with open("complex_source.py", "w") as f:
        f.write(complex_code)
        
    # Étape 2: Notre agent compresse ce fichier pour le rendre "LLM-Ready"
    compressor = ASTPromptCompressor("complex_source.py")
    result_prompt = compressor.compress_for_llm()
    
    print(result_prompt)
    
    # Nettoyage
    import os
    if os.path.exists("complex_source.py"):
        os.remove("complex_source.py")
