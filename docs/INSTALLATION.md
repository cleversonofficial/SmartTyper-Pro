# 📦 Guia de Instalação - SmartTyper Pro

## 🔧 Pré-requisitos

### Sistema Operacional
- **Windows 10/11** (recomendado)
- **Linux** (Ubuntu 18.04+)
- **macOS** (10.14+)

### Python
- **Python 3.8** ou superior
- **pip** (gerenciador de pacotes)

### Verificar Instalação
```bash
python --version
pip --version
```

## 📥 Instalação

### Método 1: Via GitHub (Recomendado)
```bash
# Clone o repositório
git clone https://github.com/cleversonofficial/SmartTyper-Pro.git

# Navegue para o diretório
cd SmartTyper-Pro

# Instale as dependências
pip install -r requirements.txt

# Execute a aplicação
python SmartTyper_Pro.py
```

### Método 2: Download Direto
1. Baixe o arquivo `SmartTyper_Pro.py`
2. Instale as dependências:
   ```bash
   pip install pyautogui
   ```
3. Execute a aplicação:
   ```bash
   python SmartTyper_Pro.py
   ```

### Método 3: Ambiente Virtual (Recomendado para Desenvolvedores)
```bash
# Criar ambiente virtual
python -m venv smarttyper_env

# Ativar ambiente virtual
# Windows:
smarttyper_env\Scripts\activate
# Linux/macOS:
source smarttyper_env/bin/activate

# Instalar dependências
pip install -r requirements.txt

# Executar aplicação
python SmartTyper_Pro.py
```

## 🚀 Executável (Windows)

### Download do Executável
1. Baixe `SmartTyper_Pro.exe` da seção [Releases](https://github.com/cleversonofficial/SmartTyper-Pro/releases)
2. Execute o arquivo diretamente
3. **Não precisa** instalar Python ou dependências

### Criar Executável (Desenvolvedores)
```bash
# Instalar PyInstaller
pip install pyinstaller

# Criar executável
pyinstaller --onefile --windowed --name="SmartTyper_Pro" SmartTyper_Pro.py
```

## 🔧 Solução de Problemas

### Erro: "pyautogui não encontrado"
```bash
pip install pyautogui
```

### Erro: "tkinter não encontrado"
- **Windows**: Instale Python completo (não apenas runtime)
- **Linux**: `sudo apt-get install python3-tk`
- **macOS**: `brew install python-tk`

### Erro: "Permissão negada"
```bash
# Windows (PowerShell como Administrador)
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Linux/macOS
sudo pip install pyautogui
```

### Antivírus bloqueando
- Adicione exceção para o arquivo/pasta
- Desative temporariamente o antivírus durante a instalação

## 📋 Dependências

### Principais
- `pyautogui>=0.9.54` - Automação de digitação
- `tkinter` - Interface gráfica (built-in)

### Opcionais
- `pyinstaller` - Para criar executáveis
- `pillow` - Para processamento de imagens

## 🎯 Verificação da Instalação

### Teste Básico
```python
import tkinter as tk
import pyautogui

print("✅ Tkinter funcionando")
print("✅ PyAutoGUI funcionando")
print("✅ Instalação concluída com sucesso!")
```

### Teste da Aplicação
1. Execute `python SmartTyper_Pro.py`
2. Verifique se a interface abre
3. Teste as funcionalidades básicas

## 📞 Suporte

Se encontrar problemas durante a instalação:

1. **Verifique** os pré-requisitos
2. **Consulte** a seção de solução de problemas
3. **Abra uma issue** no GitHub
4. **Entre em contato** via LinkedIn

---

**Desenvolvido por CleverDev Solutions** 🚀
