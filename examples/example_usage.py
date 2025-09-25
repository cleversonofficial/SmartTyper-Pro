#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Exemplo de Uso - SmartTyper Pro
Desenvolvido por CleverDev Solutions
"""

import tkinter as tk
from tkinter import messagebox
import pyautogui
import time

def exemplo_basico():
    """
    Exemplo básico de uso do SmartTyper Pro
    """
    print("🚀 SmartTyper Pro - Exemplo de Uso")
    print("=" * 50)
    
    # Texto de exemplo
    texto_exemplo = """
    Olá! Este é um exemplo de uso do SmartTyper Pro.
    
    O SmartTyper Pro é uma aplicação Python moderna para automação de digitação.
    
    Funcionalidades principais:
    • Interface moderna com 5 abas
    • Sistema de templates
    • Estatísticas de digitação
    • Temas claro/escuro
    • Atalhos de teclado
    • Modo de teste
    • Backup automático
    
    Desenvolvido por CleverDev Solutions
    """
    
    print("📝 Texto de exemplo:")
    print(texto_exemplo)
    print("\n" + "=" * 50)
    
    # Configurações de exemplo
    configuracao = {
        "tempo_inicio": 5,
        "intervalo_teclas": 0.05,
        "modo": "caractere"
    }
    
    print("⚙️ Configurações recomendadas:")
    for chave, valor in configuracao.items():
        print(f"  {chave}: {valor}")
    
    print("\n" + "=" * 50)
    print("🎯 Para usar:")
    print("1. Execute: python SmartTyper_Pro.py")
    print("2. Cole o texto na área principal")
    print("3. Configure os tempos")
    print("4. Clique em 'INICIAR DIGITAÇÃO'")
    print("5. Posicione o cursor onde deseja digitar")
    
    return texto_exemplo, configuracao

def exemplo_templates():
    """
    Exemplo de templates disponíveis
    """
    templates = {
        "Profissional": {
            "Email Formal": """
            Prezado(a) Sr(a).
            
            Espero que esta mensagem o(a) encontre bem.
            
            Gostaria de entrar em contato para discutir [assunto].
            
            Atenciosamente,
            [Seu nome]
            """,
            "Proposta Comercial": """
            Prezado(a) Cliente,
            
            Temos o prazer de apresentar nossa proposta para [serviço/produto].
            
            Nossa solução oferece:
            • Benefício 1
            • Benefício 2
            • Benefício 3
            
            Valor: R$ [valor]
            Prazo: [prazo]
            
            Aguardamos seu retorno.
            
            Atenciosamente,
            [Seu nome]
            """
        },
        "Pessoal": {
            "Convite": """
            Olá [nome]!
            
            Espero que esteja tudo bem.
            
            Gostaria de convidá-lo(a) para [evento] que acontecerá no dia [data] às [hora] em [local].
            
            Será um prazer ter sua presença!
            
            Abraços,
            [Seu nome]
            """,
            "Agradecimento": """
            Olá [nome],
            
            Muito obrigado(a) por [motivo].
            
            Foi muito importante para mim e realmente aprecio sua [ação].
            
            Um abraço,
            [Seu nome]
            """
        }
    }
    
    print("📝 Templates Disponíveis:")
    print("=" * 50)
    
    for categoria, template_list in templates.items():
        print(f"\n🏷️ {categoria}:")
        for nome, conteudo in template_list.items():
            print(f"  • {nome}")
            print(f"    {conteudo.strip()[:100]}...")
    
    return templates

def exemplo_estatisticas():
    """
    Exemplo de estatísticas de digitação
    """
    stats_exemplo = {
        "sessoes_totais": 15,
        "caracteres_digitados": 12500,
        "tempo_total": 1800,  # segundos
        "velocidade_media": 416.7,  # CPM
        "melhor_velocidade": 520.0,  # CPM
        "sessoes": [
            {"data": "25/09/2025 10:30", "caracteres": 500, "velocidade": 450.0},
            {"data": "25/09/2025 11:15", "caracteres": 750, "velocidade": 520.0},
            {"data": "25/09/2025 14:20", "caracteres": 300, "velocidade": 380.0}
        ]
    }
    
    print("📊 Estatísticas de Exemplo:")
    print("=" * 50)
    print(f"Sessões Totais: {stats_exemplo['sessoes_totais']}")
    print(f"Caracteres Digitados: {stats_exemplo['caracteres_digitados']:,}")
    print(f"Tempo Total: {stats_exemplo['tempo_total']}s")
    print(f"Velocidade Média: {stats_exemplo['velocidade_media']:.1f} CPM")
    print(f"Melhor Velocidade: {stats_exemplo['melhor_velocidade']:.1f} CPM")
    
    print("\n📈 Histórico de Sessões:")
    for sessao in stats_exemplo['sessoes']:
        print(f"  {sessao['data']} - {sessao['velocidade']:.1f} CPM ({sessao['caracteres']} chars)")
    
    return stats_exemplo

def exemplo_atalhos():
    """
    Exemplo de atalhos de teclado
    """
    atalhos = {
        "Ctrl+S": "Salvar texto atual",
        "Ctrl+O": "Carregar arquivo",
        "F5": "Iniciar digitação",
        "ESC": "Parar digitação",
        "Ctrl+T": "Alternar tema",
        "Ctrl+N": "Limpar texto",
        "Ctrl+H": "Mostrar estatísticas"
    }
    
    print("⌨️ Atalhos de Teclado:")
    print("=" * 50)
    
    for atalho, descricao in atalhos.items():
        print(f"{atalho:12} - {descricao}")
    
    return atalhos

def main():
    """
    Função principal do exemplo
    """
    print("🎯 SmartTyper Pro - Exemplos de Uso")
    print("Desenvolvido por CleverDev Solutions")
    print("=" * 60)
    
    # Executar exemplos
    exemplo_basico()
    print("\n")
    
    exemplo_templates()
    print("\n")
    
    exemplo_estatisticas()
    print("\n")
    
    exemplo_atalhos()
    print("\n")
    
    print("=" * 60)
    print("✅ Exemplos concluídos!")
    print("🚀 Para usar o SmartTyper Pro, execute: python SmartTyper_Pro.py")
    print("📖 Consulte a documentação em docs/ para mais informações")
    print("=" * 60)

if __name__ == "__main__":
    main()
