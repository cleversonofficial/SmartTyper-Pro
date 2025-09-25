"""
Testes básicos para SmartTyper Pro - Sem dependências de GUI
"""
import pytest
import sys
import os


class TestBasicFunctionality:
    """Testes básicos que não dependem de GUI"""
    
    def test_python_version(self):
        """Testa se a versão do Python é adequada"""
        assert sys.version_info >= (3, 8)
    
    def test_imports_basic(self):
        """Testa importações básicas do Python"""
        import tkinter
        import threading
        import json
        import time
        from datetime import datetime
        assert True
    
    def test_json_operations(self):
        """Testa operações básicas com JSON"""
        import json
        
        test_data = {"test": "value", "number": 123}
        json_str = json.dumps(test_data)
        parsed_data = json.loads(json_str)
        
        assert parsed_data == test_data
        assert json_str is not None
    
    def test_file_operations(self):
        """Testa operações básicas de arquivo"""
        import tempfile
        
        # Cria um arquivo temporário
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
            f.write("test content")
            temp_file = f.name
        
        try:
            # Verifica se o arquivo foi criado
            assert os.path.exists(temp_file)
            
            # Lê o conteúdo
            with open(temp_file, 'r') as f:
                content = f.read()
            assert content == "test content"
            
        finally:
            # Remove o arquivo temporário
            if os.path.exists(temp_file):
                os.unlink(temp_file)
    
    def test_threading_basics(self):
        """Testa funcionalidades básicas de threading"""
        import threading
        import time
        
        result = []
        
        def worker():
            time.sleep(0.1)
            result.append("done")
        
        thread = threading.Thread(target=worker)
        thread.start()
        thread.join()
        
        assert "done" in result
    
    def test_time_operations(self):
        """Testa operações básicas com tempo"""
        import time
        from datetime import datetime
        
        current_time = datetime.now()
        timestamp = time.time()
        
        assert isinstance(current_time, datetime)
        assert isinstance(timestamp, float)
        assert timestamp > 0
    
    def test_math_operations(self):
        """Testa operações matemáticas básicas"""
        import math
        
        assert math.sqrt(16) == 4
        assert math.pi > 3.14
        assert math.e > 2.7
    
    def test_string_operations(self):
        """Testa operações básicas com strings"""
        test_string = "SmartTyper Pro"
        
        assert len(test_string) > 0
        assert "Smart" in test_string
        assert test_string.upper() == "SMARTTYPER PRO"
        assert test_string.lower() == "smarttyper pro"


class TestModuleStructure:
    """Testa a estrutura básica do módulo"""
    
    def test_smarttyper_file_exists(self):
        """Testa se o arquivo principal existe"""
        smarttyper_file = "SmartTyper_Pro.py"
        assert os.path.exists(smarttyper_file)
    
    def test_requirements_file_exists(self):
        """Testa se o arquivo de requirements existe"""
        requirements_file = "requirements.txt"
        assert os.path.exists(requirements_file)
    
    def test_docs_directory_exists(self):
        """Testa se o diretório de documentação existe"""
        docs_dir = "docs"
        assert os.path.exists(docs_dir)
        assert os.path.isdir(docs_dir)


if __name__ == "__main__":
    pytest.main([__file__])
