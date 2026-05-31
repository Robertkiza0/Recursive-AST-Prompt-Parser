import ast
import subprocess

class ASTPromptCompressor:
    def __init__(self, source_file):
        self.source_file = source_file

    def extract_skeleton(self):
        """Lit un fichier Python et extrait uniquement la structure (classes et fonctions)."""
        print(f"[AST] Parsing {self.source_file} using Python's Abstract Syntax Tree...")
        with open(self.source_file, "r", encoding="utf-8") as f:
            code_content = f.read()

        # Transformation du code en arbre syntaxique (AST)
        tree = ast.parse(code_content)
        skeleton = []

        # On parcourt chaque élément de l'arbre
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                skeleton.append(f"Class: {node.name}")
            elif isinstance(node, ast.FunctionDef):
                # Récupère les arguments de la fonction
                args = [arg.arg for arg in node.args.args]
                skeleton.append(f"  Function: {node.name}({', '.join(args)})")

        return "\n".join(skeleton)

    def ask_llm_to_document(self, skeleton_text):
        """Envoie le squelette compressé à Llama 3.2 pour générer une documentation."""
        print("[AST] Sending compressed structure to Llama 3.2...")
        
        prompt = (
            f"You are a Senior Software Architect. Read this compressed code skeleton "
            f"(it only contains class and function names to save memory):\n\n"
            f"{skeleton_text}\n\n"
            f"Write a 3-sentence high-level technical summary of what this architecture does. "
            f"Be concise."
        )

        try:
            result = subprocess.run(
                ['ollama', 'run', 'llama3.2', prompt],
                capture_output=True, text=True, encoding='utf-8'
            )
            return result.stdout.strip()
        except FileNotFoundError:
            return "Error: Ollama or Llama 3.2 not responding."

# --- ZONE DE TEST LIVE ---
if __name__ == "__main__":
    # 1. On génère un gros fichier de code complexe fictif pour notre test
    complex_code = """
class DatabaseManager:
    def __init__(self, db_url):
        self.db_url = db_url
    
    def connect(self):
        # Imagine 50 lignes de code complexe ici
        print("Connected to DB")
        
    def save_user(self, user_id, data):
        # Imagine 100 lignes de calculs ici
        return True

class PaymentGateway:
    def process_transaction(self, amount, currency):
        # Code secret et complexe de paiement
        return "SUCCESS"
"""
    
    with open("complex_system.py", "w", encoding="utf-8") as f:
        f.write(complex_code)

    # 2. On lance notre agent de compression
    compressor = ASTPromptCompressor("complex_system.py")
    
    # Étape AST
    compressed_structure = compressor.extract_skeleton()
    print(f"\n--- COMPRESSED STRUCTURE SENT TO LLM ---\n{compressed_structure}\n----------------------------------------\n")
    
    # Étape LLM
    summary = compressor.ask_llm_to_document(compressed_structure)
    print(f"--- LLM ARCHITECTURE SUMMARY ---\n{summary}\n--------------------------------")
