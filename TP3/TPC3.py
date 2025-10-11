
import re

texto = """# Relatório de Progresso 

## 2025: O Ano do Aprendizado 

Este ano tem sido **fundamental** para aprofundar os nossos conhecimentos em [página da UC](http://www.uc.pt), especialmente em [tpc3.md](relatorios/tpc3.pdf). A disciplina tem sido um *excelente desafio*.

### Revisão de Módulos 

Para o próximo passo, vamos focar-nos em três áreas principais:

1.  Revisitar o **módulo re**.
2.  Garantir a correta conversão de *todos* os elementos.
3.  Implementar o tratamento de listas numeradas.

Isto será essencial para o projeto final.

### Imagem de Exemplo

A imagem seguinte mostra a complexidade do problema: ![diagrama de conversão](http://www.exemplo.com/diagrama.png)."""


def conversor_markdown_html (texto):
    texto_html = re.sub(r'^\#\s+(.*?)\s*$', r'<h1>\1</h1>', texto, flags=re.MULTILINE)
    texto_html = re.sub(r'^\#\#\s+(.*?)\s*$', r'<h2>\1</h2>', texto_html, flags=re.MULTILINE)
    texto_html = re.sub(r'^\#\#\#\s+(.*?)\s*$', r'<h3>\1</h3>', texto_html, flags=re.MULTILINE)
    texto_html = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', texto_html)
    texto_html = re.sub(r'\*(.*?)\*', r'<i>\1</i>', texto_html)
    texto_html = re.sub(r'^\d+\.\s+(.*?)\s*$', r'<li>\1</li>', texto_html, flags=re.MULTILINE)
    
    if '<li>' in texto_html:
        texto_html = re.sub(r'(<li>.*</li>)', r'<ol>\n\1\n</ol>', texto_html, flags=re.DOTALL)

    texto_html = re.sub(r' \[(.*?)\]\((.*?)\)', r' <a href="\2">\1</a>', texto_html)
    texto_html = re.sub(r'\!\[(.*?)\]\((.*?)\)', r' <img src="\2" alt="\1"/>', texto_html)
    return(texto_html)

print(conversor_markdown_html(texto))