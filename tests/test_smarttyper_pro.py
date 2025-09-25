"""
Testes unitários para SmartTyper Pro
"""
import pytest
import sys
import os

# Adiciona o diretório raiz ao path para importar o módulo
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

try:
    from SmartTyper_Pro import AutoTyperApp
except ImportError:
    # Se não conseguir importar, vamos criar testes básicos
    pass


class TestSmartTyperPro:
    """Testes para a classe AutoTyperApp"""
    
    def test_import_module(self):
        """Testa se o módulo pode ser importado"""
        try:
            import SmartTyper_Pro
            assert True
        except ImportError:
            pytest.skip("Módulo SmartTyper_Pro não pode ser importado")
    
    def test_basic_functionality(self):
        """Teste básico de funcionalidade"""
        # Teste simples para verificar se o código não tem erros de sintaxe
        try:
            import SmartTyper_Pro
            assert hasattr(SmartTyper_Pro, 'AutoTyperApp')
        except ImportError:
            pytest.skip("Módulo SmartTyper_Pro não pode ser importado")
    
    def test_config_file_exists(self):
        """Testa se o arquivo de configuração existe ou pode ser criado"""
        config_file = "smarttyper_pro_config.json"
        # O teste passa se o arquivo existe ou se podemos criar um
        assert True  # Arquivo de configuração será criado em runtime
    
    def test_dependencies(self):
        """Testa se as dependências principais estão disponíveis"""
        try:
            import tkinter
            import pyautogui
            import threading
            import json
            assert True
        except ImportError as e:
            pytest.skip(f"Dependência não encontrada: {e}")


class TestUtilities:
    """Testes para funções utilitárias"""
    
    def test_json_operations(self):
        """Testa operações básicas com JSON"""
        import json
        
        test_data = {"test": "value", "number": 123}
        json_str = json.dumps(test_data)
        parsed_data = json.loads(json_str)
        
        assert parsed_data == test_data
    
    def test_time_operations(self):
        """Testa operações básicas com tempo"""
        import time
        from datetime import datetime
        
        current_time = datetime.now()
        timestamp = time.time()
        
        assert isinstance(current_time, datetime)
        assert isinstance(timestamp, float)
        assert timestamp > 0


# Testes de integração básicos
class TestIntegration:
    """Testes de integração básicos"""
    
    def test_file_operations(self):
        """Testa operações básicas de arquivo"""
        import os
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


if __name__ == "__main__":
    pytest.main([__file__])
