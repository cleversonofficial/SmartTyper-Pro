import tkinter as tk
from tkinter import scrolledtext, messagebox, ttk, filedialog, colorchooser
import pyautogui
import threading
import time
import json
import os
import webbrowser
import shutil
from datetime import datetime
import math

class AutoTyperApp:
    def __init__(self, root):
        self.root = root
        self.root.title("⚡ SmartTyper Pro - Sua Automação de Digitação")
        self.root.geometry("600x700")
        self.root.resizable(True, True)
        
        # Variáveis de controle
        self.is_typing = False
        self.stop_typing = False
        self.config_file = "smarttyper_pro_config.json"
        self.backup_dir = "backups"
        self.templates_dir = "templates"
        self.stats_file = "typing_stats.json"
        
        # Variáveis de tema
        self.current_theme = "light"
        self.themes = {
            "light": {
                "bg": "#ffffff",
                "fg": "#000000",
                "select_bg": "#0078d4",
                "text_bg": "#f8f9fa",
                "text_fg": "#212529"
            },
            "dark": {
                "bg": "#2d2d2d",
                "fg": "#ffffff",
                "select_bg": "#0078d4",
                "text_bg": "#1e1e1e",
                "text_fg": "#ffffff"
            }
        }
        
        # Variáveis de estatísticas
        self.typing_stats = {
            "total_sessions": 0,
            "total_characters": 0,
            "total_time": 0,
            "average_speed": 0,
            "best_speed": 0,
            "sessions": []
        }
        
        # Criar diretórios necessários
        self.create_directories()
        
        # Carregar configurações salvas
        self.load_config()
        
        # Configurar estilo
        self.setup_styles()

        # Frame principal
        main_frame = ttk.Frame(root, padding="10")
        main_frame.pack(fill="both", expand=True)

        # Criar interface moderna
        self.create_modern_ui(main_frame)

    def setup_styles(self):
        """Configura estilos modernos para a interface"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configurar cores personalizadas
        style.configure('Title.TLabel', font=('Segoe UI', 14, 'bold'))
        style.configure('Header.TLabel', font=('Segoe UI', 10, 'bold'))
        style.configure('Success.TButton', font=('Segoe UI', 10, 'bold'))
        style.configure('Danger.TButton', font=('Segoe UI', 10, 'bold'))

    def load_config(self):
        """Carrega configurações salvas do arquivo JSON"""
        self.config = {
            'start_delay': 5,
            'char_interval': 0.05,
            'typing_mode': 'character',
            'last_texts': [],
            'theme': 'light',
            'auto_backup': True,
            'test_mode': False,
            'keyboard_shortcuts': True,
            'custom_colors': {}
        }
        
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    saved_config = json.load(f)
                    self.config.update(saved_config)
                    self.current_theme = self.config.get('theme', 'light')
            except:
                pass  # Usar configurações padrão se houver erro
        
        # Carregar estatísticas
        self.load_stats()
        
        # Carregar templates
        self.load_templates()

    def save_config(self):
        """Salva configurações no arquivo JSON"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)
        except:
            pass

    def create_directories(self):
        """Cria diretórios necessários"""
        for directory in [self.backup_dir, self.templates_dir]:
            if not os.path.exists(directory):
                os.makedirs(directory)

    def load_stats(self):
        """Carrega estatísticas de digitação"""
        if os.path.exists(self.stats_file):
            try:
                with open(self.stats_file, 'r', encoding='utf-8') as f:
                    self.typing_stats = json.load(f)
            except:
                pass

    def save_stats(self):
        """Salva estatísticas de digitação"""
        try:
            with open(self.stats_file, 'w', encoding='utf-8') as f:
                json.dump(self.typing_stats, f, indent=2, ensure_ascii=False)
        except:
            pass

    def load_templates(self):
        """Carrega templates de texto"""
        self.templates = {
            "Profissional": {
                "Email Formal": "Prezado(a) Sr(a).\n\nEspero que esta mensagem o(a) encontre bem.\n\nGostaria de entrar em contato para discutir [assunto].\n\nAtenciosamente,\n[Seu nome]",
                "Proposta Comercial": "Prezado(a) Cliente,\n\nTemos o prazer de apresentar nossa proposta para [serviço/produto].\n\nNossa solução oferece:\n• Benefício 1\n• Benefício 2\n• Benefício 3\n\nValor: R$ [valor]\nPrazo: [prazo]\n\nAguardamos seu retorno.\n\nAtenciosamente,\n[Seu nome]"
            },
            "Pessoal": {
                "Convite": "Olá [nome]!\n\nEspero que esteja tudo bem.\n\nGostaria de convidá-lo(a) para [evento] que acontecerá no dia [data] às [hora] em [local].\n\nSerá um prazer ter sua presença!\n\nAbraços,\n[Seu nome]",
                "Agradecimento": "Olá [nome],\n\nMuito obrigado(a) por [motivo].\n\nFoi muito importante para mim e realmente aprecio sua [ação].\n\nUm abraço,\n[Seu nome]"
            },
            "Acadêmico": {
                "Trabalho Acadêmico": "UNIVERSIDADE [NOME]\nCURSO: [Nome do Curso]\nDISCIPLINA: [Nome da Disciplina]\nPROFESSOR(A): [Nome do Professor]\n\nTÍTULO DO TRABALHO\n\n[Seu nome]\n[Data]",
                "Relatório": "RELATÓRIO DE [ATIVIDADE]\n\n1. INTRODUÇÃO\n[Texto da introdução]\n\n2. DESENVOLVIMENTO\n[Texto do desenvolvimento]\n\n3. CONCLUSÃO\n[Texto da conclusão]\n\nReferências:\n[Referências bibliográficas]"
            }
        }

    def apply_theme(self, theme_name):
        """Aplica tema selecionado"""
        self.current_theme = theme_name
        theme = self.themes[theme_name]
        
        # Configurar cores do tema
        self.root.configure(bg=theme['bg'])
        
        # Atualizar área de texto
        if hasattr(self, 'text_area'):
            self.text_area.configure(
                bg=theme['text_bg'],
                fg=theme['text_fg'],
                selectbackground=theme['select_bg']
            )
        
        # Salvar tema atual
        self.config['theme'] = theme_name
        self.save_config()

    def toggle_theme(self):
        """Alterna entre tema claro e escuro"""
        new_theme = "dark" if self.current_theme == "light" else "light"
        self.apply_theme(new_theme)
        self.status_label.config(text=f"Tema alterado para: {new_theme.title()}")

    def setup_keyboard_shortcuts(self):
        """Configura atalhos de teclado"""
        if not self.config.get('keyboard_shortcuts', True):
            return
            
        # Atalhos principais
        self.root.bind('<Control-s>', lambda e: self.save_text())
        self.root.bind('<Control-o>', lambda e: self.load_file())
        self.root.bind('<F5>', lambda e: self.start_typing_thread())
        self.root.bind('<Escape>', lambda e: self.stop_typing_action())
        self.root.bind('<Control-t>', lambda e: self.toggle_theme())
        self.root.bind('<Control-n>', lambda e: self.clear_text())
        self.root.bind('<Control-h>', lambda e: self.show_stats())

    def save_text(self):
        """Salva texto atual"""
        text = self.text_area.get("1.0", tk.END).strip()
        if text:
            filename = f"texto_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            filepath = os.path.join(self.backup_dir, filename)
            try:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(text)
                self.status_label.config(text=f"Texto guardado com carinho: {filename} 💾")
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao salvar: {str(e)}")

    def auto_backup(self):
        """Backup automático do texto"""
        if self.config.get('auto_backup', True):
            text = self.text_area.get("1.0", tk.END).strip()
            if text and len(text) > 10:  # Só faz backup de textos significativos
                filename = f"auto_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
                filepath = os.path.join(self.backup_dir, filename)
                try:
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(text)
                except:
                    pass

    def show_stats(self):
        """Mostra estatísticas de digitação"""
        stats_window = tk.Toplevel(self.root)
        stats_window.title("📊 Estatísticas de Digitação")
        stats_window.geometry("500x400")
        stats_window.resizable(False, False)
        
        # Frame principal
        main_frame = ttk.Frame(stats_window, padding="20")
        main_frame.pack(fill="both", expand=True)
        
        # Título
        ttk.Label(main_frame, text="📊 Estatísticas de Digitação", 
                 font=("Segoe UI", 16, "bold")).pack(pady=(0, 20))
        
        # Estatísticas
        stats_text = f"""
        📈 Sessões Totais: {self.typing_stats['total_sessions']}
        ⌨️ Caracteres Digitados: {self.typing_stats['total_characters']:,}
        ⏱️ Tempo Total: {self.format_time(self.typing_stats['total_time'])}
        🚀 Velocidade Média: {self.typing_stats['average_speed']:.1f} CPM
        🏆 Melhor Velocidade: {self.typing_stats['best_speed']:.1f} CPM
        """
        
        ttk.Label(main_frame, text=stats_text, font=("Consolas", 12)).pack(pady=10)
        
        # Botão fechar
        ttk.Button(main_frame, text="Fechar", command=stats_window.destroy).pack(pady=20)

    def format_time(self, seconds):
        """Formata tempo em formato legível"""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        seconds = int(seconds % 60)
        
        if hours > 0:
            return f"{hours}h {minutes}m {seconds}s"
        elif minutes > 0:
            return f"{minutes}m {seconds}s"
        else:
            return f"{seconds}s"

    def update_stats(self, characters, duration):
        """Atualiza estatísticas após digitação"""
        self.typing_stats['total_sessions'] += 1
        self.typing_stats['total_characters'] += characters
        self.typing_stats['total_time'] += duration
        
        # Calcular velocidade (caracteres por minuto)
        speed = (characters / duration) * 60 if duration > 0 else 0
        
        # Atualizar melhor velocidade
        if speed > self.typing_stats['best_speed']:
            self.typing_stats['best_speed'] = speed
        
        # Calcular velocidade média
        total_sessions = self.typing_stats['total_sessions']
        if total_sessions > 0:
            self.typing_stats['average_speed'] = (
                self.typing_stats['total_characters'] / 
                self.typing_stats['total_time'] * 60
            )
        
        # Adicionar sessão ao histórico
        session = {
            'date': datetime.now().strftime('%d/%m/%Y %H:%M'),
            'characters': characters,
            'duration': duration,
            'speed': speed
        }
        self.typing_stats['sessions'].append(session)
        
        # Manter apenas as últimas 50 sessões
        self.typing_stats['sessions'] = self.typing_stats['sessions'][-50:]
        
        # Salvar estatísticas
        self.save_stats()

    def create_modern_ui(self, parent):
        """Cria interface moderna com ttk widgets"""
        
        # Título principal
        title_label = ttk.Label(parent, text="⚡ SmartTyper Pro", style='Title.TLabel')
        title_label.pack(pady=(0, 20))
        
        # Notebook para organizar em abas
        notebook = ttk.Notebook(parent)
        notebook.pack(fill="both", expand=True, pady=(0, 10))
        
        # Aba principal - Digitação
        main_tab = ttk.Frame(notebook)
        notebook.add(main_tab, text="✍️ Digitar")
        
        # Aba configurações
        config_tab = ttk.Frame(notebook)
        notebook.add(config_tab, text="⚙️ Ajustes")
        
        # Aba histórico
        history_tab = ttk.Frame(notebook)
        notebook.add(history_tab, text="📚 Histórico")
        
        # Criar conteúdo das abas
        self.create_main_tab(main_tab)
        self.create_config_tab(config_tab)
        self.create_history_tab(history_tab)
        self.create_templates_tab(notebook)
        self.create_stats_tab(notebook)
        
        # Barra de status
        self.create_status_bar(parent)
        
        # Seção de redes sociais do criador
        self.create_creator_section(parent)
        
        # Configurar atalhos de teclado
        self.setup_keyboard_shortcuts()
        
        # Aplicar tema inicial
        self.apply_theme(self.current_theme)

    def create_main_tab(self, parent):
        """Cria conteúdo da aba principal"""
        
        # Frame para texto
        text_frame = ttk.LabelFrame(parent, text="O que você quer digitar? 😊", padding="10")
        text_frame.pack(fill="both", expand=True, pady=(0, 10))
        
        # Contador de caracteres
        char_count_frame = ttk.Frame(text_frame)
        char_count_frame.pack(fill="x", pady=(0, 5))
        
        ttk.Label(char_count_frame, text="Caracteres:", style='Header.TLabel').pack(side="left")
        self.char_count_label = ttk.Label(char_count_frame, text="0")
        self.char_count_label.pack(side="left", padx=(5, 0))
        
        # Área de texto
        self.text_area = scrolledtext.ScrolledText(
            text_frame, 
            wrap=tk.WORD, 
            height=12, 
            font=("Consolas", 10),
            bg="#f8f9fa",
            fg="#212529"
        )
        self.text_area.pack(fill="both", expand=True)
        self.text_area.bind('<KeyRelease>', self.update_char_count)
        
        # Botões de arquivo
        file_frame = ttk.Frame(text_frame)
        file_frame.pack(fill="x", pady=(10, 0))
        
        ttk.Button(file_frame, text="Carregar Arquivo", command=self.load_file).pack(side="left", padx=(0, 5))
        ttk.Button(file_frame, text="Limpar", command=self.clear_text).pack(side="left")
        
        # Frame de configurações rápidas
        quick_config_frame = ttk.LabelFrame(parent, text="Configurações do seu jeito ⚙️", padding="10")
        quick_config_frame.pack(fill="x", pady=(0, 10))
        
        # Configurações em grid
        config_grid = ttk.Frame(quick_config_frame)
        config_grid.pack(fill="x")
        
        # Tempo de início
        ttk.Label(config_grid, text="Esperar quanto tempo antes de começar?").grid(row=0, column=0, sticky="w", padx=(0, 10))
        self.start_delay_var = tk.StringVar(value=str(self.config['start_delay']))
        self.start_delay_entry = ttk.Entry(config_grid, textvariable=self.start_delay_var, width=10)
        self.start_delay_entry.grid(row=0, column=1, padx=(0, 20))
        
        # Intervalo entre caracteres
        ttk.Label(config_grid, text="Quanto tempo entre cada letra?").grid(row=0, column=2, sticky="w", padx=(0, 10))
        self.char_interval_var = tk.StringVar(value=str(self.config['char_interval']))
        self.char_interval_entry = ttk.Entry(config_grid, textvariable=self.char_interval_var, width=10)
        self.char_interval_entry.grid(row=0, column=3)
        
        # Modo de digitação
        ttk.Label(config_grid, text="Modo:").grid(row=1, column=0, sticky="w", padx=(0, 10), pady=(10, 0))
        self.typing_mode_var = tk.StringVar(value=self.config['typing_mode'])
        mode_combo = ttk.Combobox(config_grid, textvariable=self.typing_mode_var, 
                                 values=['character', 'word'], state='readonly', width=10)
        mode_combo.grid(row=1, column=1, padx=(0, 20), pady=(10, 0))
        
        # Modo de teste
        self.test_mode_var = tk.BooleanVar(value=self.config.get('test_mode', False))
        test_check = ttk.Checkbutton(config_grid, text="Testar sem digitar de verdade", variable=self.test_mode_var)
        test_check.grid(row=1, column=2, padx=(0, 20), pady=(10, 0))
        
        # Backup automático
        self.auto_backup_var = tk.BooleanVar(value=self.config.get('auto_backup', True))
        backup_check = ttk.Checkbutton(config_grid, text="Salvar automaticamente", variable=self.auto_backup_var)
        backup_check.grid(row=1, column=3, pady=(10, 0))
        
        # Botões de controle
        control_frame = ttk.Frame(parent)
        control_frame.pack(fill="x", pady=(0, 10))
        
        self.start_button = ttk.Button(control_frame, text="🚀 Vamos começar!", 
                                      style='Success.TButton', command=self.start_typing_thread)
        self.start_button.pack(side="left", padx=(0, 10), fill="x", expand=True)
        
        self.stop_button = ttk.Button(control_frame, text="⏹️ Parar tudo", 
                                     style='Danger.TButton', command=self.stop_typing_action,
                                     state="disabled")
        self.stop_button.pack(side="left", fill="x", expand=True)
        
        # Botões adicionais
        extra_frame = ttk.Frame(parent)
        extra_frame.pack(fill="x", pady=(0, 10))
        
        ttk.Button(extra_frame, text="💾 Guardar texto", command=self.save_text).pack(side="left", padx=(0, 5))
        ttk.Button(extra_frame, text="🌙 Mudar visual", command=self.toggle_theme).pack(side="left", padx=(0, 5))
        ttk.Button(extra_frame, text="📊 Ver como fui", command=self.show_stats).pack(side="left")
        
        # Barra de progresso
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(parent, variable=self.progress_var, 
                                          mode='determinate', length=400)
        self.progress_bar.pack(fill="x", pady=(0, 10))
        
        # Aviso de segurança
        warning_frame = ttk.Frame(parent)
        warning_frame.pack(fill="x")
        
        warning_text = "💡 Dica: Coloque o cursor onde quer que apareça o texto!"
        ttk.Label(warning_frame, text=warning_text, foreground="orange", 
                 font=("Segoe UI", 9)).pack()

    def create_config_tab(self, parent):
        """Cria aba de configurações avançadas"""
        
        # Configurações de segurança
        security_frame = ttk.LabelFrame(parent, text="Segurança e Proteção 🛡️", padding="10")
        security_frame.pack(fill="x", pady=(0, 10))
        
        self.failsafe_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(security_frame, text="Ativar parada de emergência (mover mouse para canto superior esquerdo)",
                       variable=self.failsafe_var).pack(anchor="w")
        
        # Configurações de digitação
        typing_frame = ttk.LabelFrame(parent, text="Como Digitar Melhor ⌨️", padding="10")
        typing_frame.pack(fill="x", pady=(0, 10))
        
        # Validação de entrada
        validation_frame = ttk.Frame(typing_frame)
        validation_frame.pack(fill="x")
        
        ttk.Label(validation_frame, text="Verificações de segurança:").pack(anchor="w")
        self.validate_input_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(validation_frame, text="Verificar caracteres especiais",
                       variable=self.validate_input_var).pack(anchor="w")
        
        # Botão salvar configurações
        ttk.Button(parent, text="💾 Guardar Preferências", 
                  command=self.save_config).pack(pady=10)

    def create_history_tab(self, parent):
        """Cria aba de histórico de textos"""
        
        # Lista de textos anteriores
        history_frame = ttk.LabelFrame(parent, text="Seus Textos Salvos 📚", padding="10")
        history_frame.pack(fill="both", expand=True, pady=(0, 10))
        
        # Listbox com scrollbar
        listbox_frame = ttk.Frame(history_frame)
        listbox_frame.pack(fill="both", expand=True)
        
        self.history_listbox = tk.Listbox(listbox_frame, height=10)
        scrollbar = ttk.Scrollbar(listbox_frame, orient="vertical", command=self.history_listbox.yview)
        self.history_listbox.configure(yscrollcommand=scrollbar.set)
        
        self.history_listbox.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Botões do histórico
        history_buttons = ttk.Frame(history_frame)
        history_buttons.pack(fill="x", pady=(10, 0))
        
        ttk.Button(history_buttons, text="Usar este texto", 
                  command=self.load_from_history).pack(side="left", padx=(0, 5))
        ttk.Button(history_buttons, text="Apagar este texto", 
                  command=self.remove_from_history).pack(side="left")
        
        # Atualizar lista do histórico
        self.update_history_list()

    def create_templates_tab(self, notebook):
        """Cria aba de templates de texto"""
        templates_tab = ttk.Frame(notebook)
        notebook.add(templates_tab, text="📝 Modelos")
        
        # Frame principal
        main_frame = ttk.Frame(templates_tab, padding="10")
        main_frame.pack(fill="both", expand=True)
        
        # Categorias
        categories_frame = ttk.LabelFrame(main_frame, text="Escolha uma categoria 📂", padding="10")
        categories_frame.pack(fill="x", pady=(0, 10))
        
        self.template_category_var = tk.StringVar(value="Profissional")
        category_combo = ttk.Combobox(categories_frame, textvariable=self.template_category_var,
                                    values=list(self.templates.keys()), state='readonly')
        category_combo.pack(side="left", padx=(0, 10))
        category_combo.bind('<<ComboboxSelected>>', self.update_template_list)
        
        # Lista de templates
        templates_frame = ttk.LabelFrame(main_frame, text="Modelos Prontos 📄", padding="10")
        templates_frame.pack(fill="both", expand=True, pady=(0, 10))
        
        # Listbox com scrollbar
        listbox_frame = ttk.Frame(templates_frame)
        listbox_frame.pack(fill="both", expand=True)
        
        self.templates_listbox = tk.Listbox(listbox_frame, height=8)
        scrollbar = ttk.Scrollbar(listbox_frame, orient="vertical", command=self.templates_listbox.yview)
        self.templates_listbox.configure(yscrollcommand=scrollbar.set)
        
        self.templates_listbox.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Botões de template
        template_buttons = ttk.Frame(templates_frame)
        template_buttons.pack(fill="x", pady=(10, 0))
        
        ttk.Button(template_buttons, text="Usar este modelo", 
                  command=self.use_template).pack(side="left", padx=(0, 5))
        ttk.Button(template_buttons, text="Ver como fica", 
                  command=self.preview_template).pack(side="left")
        
        # Atualizar lista inicial
        self.update_template_list()

    def create_stats_tab(self, notebook):
        """Cria aba de estatísticas"""
        stats_tab = ttk.Frame(notebook)
        notebook.add(stats_tab, text="📈 Como fui")
        
        # Frame principal
        main_frame = ttk.Frame(stats_tab, padding="20")
        main_frame.pack(fill="both", expand=True)
        
        # Estatísticas principais
        stats_frame = ttk.LabelFrame(main_frame, text="Suas Conquistas 🏆", padding="15")
        stats_frame.pack(fill="x", pady=(0, 20))
        
        # Grid de estatísticas
        stats_grid = ttk.Frame(stats_frame)
        stats_grid.pack(fill="x")
        
        # Sessões totais
        ttk.Label(stats_grid, text="📈 Vezes que você usou:", font=("Segoe UI", 10, "bold")).grid(row=0, column=0, sticky="w", padx=(0, 20))
        self.total_sessions_label = ttk.Label(stats_grid, text=str(self.typing_stats['total_sessions']), font=("Consolas", 12))
        self.total_sessions_label.grid(row=0, column=1, sticky="w")
        
        # Caracteres totais
        ttk.Label(stats_grid, text="⌨️ Letras que você digitou:", font=("Segoe UI", 10, "bold")).grid(row=1, column=0, sticky="w", padx=(0, 20), pady=(10, 0))
        self.total_chars_label = ttk.Label(stats_grid, text=f"{self.typing_stats['total_characters']:,}", font=("Consolas", 12))
        self.total_chars_label.grid(row=1, column=1, sticky="w", pady=(10, 0))
        
        # Tempo total
        ttk.Label(stats_grid, text="⏱️ Tempo total digitando:", font=("Segoe UI", 10, "bold")).grid(row=2, column=0, sticky="w", padx=(0, 20), pady=(10, 0))
        self.total_time_label = ttk.Label(stats_grid, text=self.format_time(self.typing_stats['total_time']), font=("Consolas", 12))
        self.total_time_label.grid(row=2, column=1, sticky="w", pady=(10, 0))
        
        # Velocidade média
        ttk.Label(stats_grid, text="🚀 Você digita em média:", font=("Segoe UI", 10, "bold")).grid(row=3, column=0, sticky="w", padx=(0, 20), pady=(10, 0))
        self.avg_speed_label = ttk.Label(stats_grid, text=f"{self.typing_stats['average_speed']:.1f} letras por minuto", font=("Consolas", 12))
        self.avg_speed_label.grid(row=3, column=1, sticky="w", pady=(10, 0))
        
        # Melhor velocidade
        ttk.Label(stats_grid, text="🏆 Seu recorde pessoal:", font=("Segoe UI", 10, "bold")).grid(row=4, column=0, sticky="w", padx=(0, 20), pady=(10, 0))
        self.best_speed_label = ttk.Label(stats_grid, text=f"{self.typing_stats['best_speed']:.1f} letras por minuto", font=("Consolas", 12))
        self.best_speed_label.grid(row=4, column=1, sticky="w", pady=(10, 0))
        
        # Botões de ação
        action_frame = ttk.Frame(main_frame)
        action_frame.pack(fill="x")
        
        ttk.Button(action_frame, text="🔄 Atualizar", command=self.refresh_stats).pack(side="left", padx=(0, 10))
        ttk.Button(action_frame, text="📊 Ver gráfico", command=self.show_chart).pack(side="left", padx=(0, 10))
        ttk.Button(action_frame, text="🗑️ Apagar tudo", command=self.clear_stats).pack(side="left")

    def update_template_list(self, event=None):
        """Atualiza lista de templates baseada na categoria selecionada"""
        category = self.template_category_var.get()
        self.templates_listbox.delete(0, tk.END)
        
        if category in self.templates:
            for template_name in self.templates[category].keys():
                self.templates_listbox.insert(tk.END, template_name)

    def use_template(self):
        """Usa template selecionado"""
        selection = self.templates_listbox.curselection()
        if selection:
            category = self.template_category_var.get()
            template_name = self.templates_listbox.get(selection[0])
            template_text = self.templates[category][template_name]
            
            # Substituir texto atual
            self.text_area.delete("1.0", tk.END)
            self.text_area.insert("1.0", template_text)
            self.update_char_count()
            self.status_label.config(text=f"Modelo '{template_name}' pronto para usar! 😊")

    def preview_template(self):
        """Mostra preview do template"""
        selection = self.templates_listbox.curselection()
        if selection:
            category = self.template_category_var.get()
            template_name = self.templates_listbox.get(selection[0])
            template_text = self.templates[category][template_name]
            
            # Janela de preview
            preview_window = tk.Toplevel(self.root)
            preview_window.title(f"Como fica: {template_name}")
            preview_window.geometry("600x400")
            
            # Área de texto para preview
            preview_text = scrolledtext.ScrolledText(preview_window, wrap=tk.WORD, height=20)
            preview_text.pack(fill="both", expand=True, padx=10, pady=10)
            preview_text.insert("1.0", template_text)
            preview_text.config(state="disabled")
            
            # Botão fechar
            ttk.Button(preview_window, text="Fechar", command=preview_window.destroy).pack(pady=10)

    def refresh_stats(self):
        """Atualiza estatísticas na aba"""
        self.total_sessions_label.config(text=str(self.typing_stats['total_sessions']))
        self.total_chars_label.config(text=f"{self.typing_stats['total_characters']:,}")
        self.total_time_label.config(text=self.format_time(self.typing_stats['total_time']))
        self.avg_speed_label.config(text=f"{self.typing_stats['average_speed']:.1f} letras por minuto")
        self.best_speed_label.config(text=f"{self.typing_stats['best_speed']:.1f} letras por minuto")

    def show_chart(self):
        """Mostra gráfico de estatísticas"""
        if not self.typing_stats['sessions']:
            messagebox.showinfo("Info", "Ainda não tem nada para mostrar! Use o app primeiro 😊")
            return
            
        # Janela de gráfico simples
        chart_window = tk.Toplevel(self.root)
        chart_window.title("📈 Sua Evolução")
        chart_window.geometry("600x400")
        
        # Texto simples com histórico
        chart_text = scrolledtext.ScrolledText(chart_window, wrap=tk.WORD, height=20)
        chart_text.pack(fill="both", expand=True, padx=10, pady=10)
        
        chart_content = "📈 SEU HISTÓRICO DE DIGITAÇÃO\n\n"
        for session in self.typing_stats['sessions'][-20:]:  # Últimas 20 sessões
            chart_content += f"{session['date']} - {session['speed']:.1f} letras/min ({session['characters']} letras)\n"
        
        chart_text.insert("1.0", chart_content)
        chart_text.config(state="disabled")

    def clear_stats(self):
        """Limpa todas as estatísticas"""
        if messagebox.askyesno("Confirmar", "Tem certeza que quer apagar tudo? 😅"):
            self.typing_stats = {
                'total_sessions': 0,
                'total_characters': 0,
                'total_time': 0,
                'average_speed': 0,
                'best_speed': 0,
                'sessions': []
            }
            self.save_stats()
            self.refresh_stats()
            self.status_label.config(text="Tudo apagado! Começando do zero 🆕")

    def create_status_bar(self, parent):
        """Cria barra de status"""
        self.status_frame = ttk.Frame(parent)
        self.status_frame.pack(fill="x", pady=(10, 0))
        
        self.status_label = ttk.Label(self.status_frame, text="Tudo pronto! Pode começar 😊", 
                                    relief="sunken", anchor="w")
        self.status_label.pack(fill="x")

    def create_creator_section(self, parent):
        """Cria seção com informações do criador"""
        creator_frame = ttk.LabelFrame(parent, text="🚀 Desenvolvido por CleverDev Solutions", padding="10")
        creator_frame.pack(fill="x", pady=(10, 0))
        
        # Frame para os botões
        buttons_frame = ttk.Frame(creator_frame)
        buttons_frame.pack(fill="x")
        
        # Botão GitHub
        github_button = ttk.Button(
            buttons_frame, 
            text="🐙 GitHub", 
            command=self.open_github,
            style='Success.TButton'
        )
        github_button.pack(side="left", padx=(0, 10), fill="x", expand=True)
        
        # Botão LinkedIn
        linkedin_button = ttk.Button(
            buttons_frame, 
            text="💼 LinkedIn", 
            command=self.open_linkedin,
            style='Success.TButton'
        )
        linkedin_button.pack(side="left", fill="x", expand=True)
        
        # Texto informativo
        info_text = "💡 Soluções Inteligentes em Desenvolvimento | React & Node.js Expert"
        ttk.Label(creator_frame, text=info_text, font=("Segoe UI", 9), 
                 foreground="gray").pack(pady=(10, 0))

    def open_github(self):
        """Abre o perfil do GitHub do criador"""
        try:
            webbrowser.open("https://github.com/cleversonofficial")
            self.status_label.config(text="GitHub aberto no navegador")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao abrir GitHub: {str(e)}")

    def open_linkedin(self):
        """Abre o perfil do LinkedIn do criador"""
        try:
            webbrowser.open("https://www.linkedin.com/in/cleversonsilvaofficial/")
            self.status_label.config(text="LinkedIn aberto no navegador")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao abrir LinkedIn: {str(e)}")

    def update_char_count(self, event=None):
        """Atualiza contador de caracteres"""
        text = self.text_area.get("1.0", tk.END).strip()
        char_count = len(text)
        self.char_count_label.config(text=str(char_count))

    def load_file(self):
        """Carrega texto de arquivo"""
        file_path = filedialog.askopenfilename(
            title="Selecionar arquivo de texto",
            filetypes=[("Arquivos de texto", "*.txt"), ("Todos os arquivos", "*.*")]
        )
        
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    self.text_area.delete("1.0", tk.END)
                    self.text_area.insert("1.0", content)
                    self.update_char_count()
                    self.status_label.config(text=f"Arquivo carregado: {os.path.basename(file_path)}")
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao carregar arquivo: {str(e)}")

    def clear_text(self):
        """Limpa o texto da área de digitação"""
        self.text_area.delete("1.0", tk.END)
        self.update_char_count()
        self.status_label.config(text="Texto apagado! Começando do zero 🆕")

    def update_history_list(self):
        """Atualiza lista do histórico"""
        self.history_listbox.delete(0, tk.END)
        for i, text_info in enumerate(self.config['last_texts']):
            preview = text_info['text'][:50] + "..." if len(text_info['text']) > 50 else text_info['text']
            date_str = text_info['date']
            self.history_listbox.insert(tk.END, f"{date_str} - {preview}")

    def load_from_history(self):
        """Carrega texto selecionado do histórico"""
        selection = self.history_listbox.curselection()
        if selection:
            index = selection[0]
            text_info = self.config['last_texts'][index]
            self.text_area.delete("1.0", tk.END)
            self.text_area.insert("1.0", text_info['text'])
            self.update_char_count()
            self.status_label.config(text="Texto do histórico carregado! 😊")

    def remove_from_history(self):
        """Remove item selecionado do histórico"""
        selection = self.history_listbox.curselection()
        if selection:
            index = selection[0]
            del self.config['last_texts'][index]
            self.save_config()
            self.update_history_list()
            self.status_label.config(text="Texto removido do histórico! 🗑️")

    def add_to_history(self, text):
        """Adiciona texto ao histórico"""
        if text.strip():
            text_info = {
                'text': text,
                'date': datetime.now().strftime("%d/%m/%Y %H:%M")
            }
            self.config['last_texts'].insert(0, text_info)
            # Manter apenas os últimos 10 textos
            self.config['last_texts'] = self.config['last_texts'][:10]
            self.save_config()
            self.update_history_list()

    def stop_typing_action(self):
        """Para a digitação em andamento"""
        self.stop_typing = True
        self.status_label.config(text="Parando tudo... ⏹️")

    def start_typing_thread(self):
        """
        Inicia o processo de digitação em uma nova thread para não travar a UI.
        """
        if self.is_typing:
            messagebox.showwarning("Aviso", "Já está digitando! Espere terminar 😊")
            return
            
        try:
            text_to_type = self.text_area.get("1.0", tk.END).strip()
            start_delay = float(self.start_delay_var.get())
            char_interval = float(self.char_interval_var.get())
            typing_mode = self.typing_mode_var.get()

            # Validações
            if not text_to_type:
                messagebox.showerror("Ops!", "Esqueceu de digitar algo! 😅")
                return
                
            if start_delay < 0 or start_delay > 300:
                messagebox.showerror("Ei!", "O tempo de espera deve ser entre 0 e 300 segundos! 🤔")
                return
                
            if char_interval < 0.001 or char_interval > 10:
                messagebox.showerror("Ei!", "O intervalo entre letras deve ser entre 0.001 e 10 segundos! 🤔")
                return
            
            # Salvar configurações atuais
            self.config['start_delay'] = start_delay
            self.config['char_interval'] = char_interval
            self.config['typing_mode'] = typing_mode
            self.config['test_mode'] = self.test_mode_var.get()
            self.config['auto_backup'] = self.auto_backup_var.get()
            self.save_config()
            
            # Adicionar ao histórico
            self.add_to_history(text_to_type)
            
            # Usar threading para que a interface não congele durante o time.sleep()
            typing_thread = threading.Thread(
                target=self.run_typing_logic, 
                args=(text_to_type, start_delay, char_interval, typing_mode),
                daemon=True
            )
            typing_thread.start()

        except ValueError:
            messagebox.showerror("Ops!", "Por favor, digite números válidos nos campos de tempo! 😊")

    def run_typing_logic(self, text, delay, interval, mode):
        """
        Contém a lógica de espera e digitação melhorada.
        """
        self.is_typing = True
        self.stop_typing = False
        start_time = time.time()
        
        # Atualizar interface
        self.start_button.config(state="disabled", text=f"🚀 Começando em {int(delay)}s...")
        self.stop_button.config(state="normal")
        self.progress_var.set(0)
        
        # Configurar failsafe
        pyautogui.FAILSAFE = self.failsafe_var.get()
        
        # Verificar modo de teste
        test_mode = self.test_mode_var.get()
        if test_mode:
            self.status_label.config(text="🧪 Modo de teste - Só simulando 😊")
        
        try:
            # Contagem regressiva com atualização da barra de progresso
            total_time = delay + (len(text) * interval)
            elapsed_time = 0
            
            for i in range(int(delay), 0, -1):
                if self.stop_typing:
                    return
                    
                mode_text = "🧪 TESTE" if test_mode else "⌨️ DIGITAÇÃO"
                self.start_button.config(text=f"{mode_text} - Começando em {i}s...")
                self.status_label.config(text=f"Começando em {i} segundos... ⏰")
                
                # Atualizar progresso da contagem regressiva
                countdown_progress = ((delay - i) / delay) * 30  # 30% para contagem
                self.progress_var.set(countdown_progress)
                
                time.sleep(1)
                elapsed_time += 1
            
            if self.stop_typing:
                return
                
            mode_text = "🧪 Simulando..." if test_mode else "⌨️ Digitando..."
            self.start_button.config(text=mode_text)
            self.status_label.config(text="Fazendo a mágica acontecer... ✨")
            
            # Digitação baseada no modo
            if mode == 'word':
                words = text.split()
                total_words = len(words)
                
                for i, word in enumerate(words):
                    if self.stop_typing:
                        return
                    
                    if not test_mode:
                        pyautogui.write(word)
                        # Adicionar espaço entre palavras (exceto na última)
                        if i < total_words - 1:
                            pyautogui.write(' ')
                    
                    # Atualizar progresso
                    typing_progress = 30 + ((i + 1) / total_words) * 70  # 70% para digitação
                    self.progress_var.set(typing_progress)
                    
                    if interval > 0:
                        time.sleep(interval)
            else:
                # Modo caractere por caractere
                total_chars = len(text)
                
                for i, char in enumerate(text):
                    if self.stop_typing:
                        return
                    
                    if not test_mode:
                        pyautogui.write(char)
                    
                    # Atualizar progresso
                    typing_progress = 30 + ((i + 1) / total_chars) * 70  # 70% para digitação
                    self.progress_var.set(typing_progress)
                    
                    if interval > 0:
                        time.sleep(interval)
            
            if not self.stop_typing:
                self.progress_var.set(100)
                end_time = time.time()
                duration = end_time - start_time
                
                # Atualizar estatísticas
                self.update_stats(len(text), duration)
                
                # Backup automático
                self.auto_backup()
                
                success_text = "✅ Simulação concluída!" if test_mode else "✅ Pronto! Texto no lugar certo! 🎉"
                self.status_label.config(text=success_text)
                messagebox.showinfo("Sucesso", success_text)
                
        except pyautogui.FailSafeException:
            self.status_label.config(text="⚠️ Parou por segurança")
            messagebox.showwarning("Parou!", "Você moveu o mouse para o canto superior esquerdo - parada de emergência ativada! 🛡️")
        except Exception as e:
            self.status_label.config(text=f"❌ Ops! Algo deu errado: {str(e)}")
            messagebox.showerror("Ops!", f"Algo deu errado durante a digitação: {str(e)} 😅")
        finally:
            # Reabilitar interface
            self.is_typing = False
            self.stop_typing = False
            self.start_button.config(state="normal", text="🚀 Vamos começar!")
            self.stop_button.config(state="disabled")
            self.progress_var.set(0)


if __name__ == "__main__":
    # Configuração de segurança do PyAutoGUI
    # Se você mover o mouse para o canto superior esquerdo da tela, o script irá parar.
    pyautogui.FAILSAFE = True

    # Configurações adicionais do PyAutoGUI
    pyautogui.PAUSE = 0.1  # Pausa entre comandos
    
    try:
        root = tk.Tk()
        app = AutoTyperApp(root)
        
        # Configurar fechamento da janela
        def on_closing():
        if app.is_typing:
            if messagebox.askokcancel("Sair", "Ainda está digitando! Quer mesmo sair? 😊"):
                app.stop_typing = True
                root.destroy()
            else:
                root.destroy()
        
        root.protocol("WM_DELETE_WINDOW", on_closing)
        root.mainloop()
        
    except Exception as e:
        messagebox.showerror("Ops!", f"Algo deu errado ao abrir o app: {str(e)} 😅")