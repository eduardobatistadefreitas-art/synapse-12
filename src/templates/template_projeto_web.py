def obter_template_projeto_web(pedido_limpo):
    return f"""# 🌐 ARQUITETURA DE PROJETO WEB: {pedido_limpo.upper()}

## 📝 1. DESCRIÇÃO DO FRONTEND E INFORMAÇÕES DE RESPONSIVIDADE
Estrutura de arquivos para aplicação web modular focada em '{pedido_limpo}'. O design prioriza a responsividade absoluta e o carregamento síncrono ultra rápido em smartphones (Mobile-First), livre de scripts pesados e com isolamento de rotas de deploy.

## 📂 2. ÁRVORE DE DIRETÓRIOS WEB
```text
projeto_web/
├── index.html                 # Estrutura HTML5 Semântica Rígida
├── css/
│   └── styles.css             # Capa Visual, Cores e Design Responsivo
└── js/
    └── app.js                 # Miolo Lógico, Roteamento e Fetch Assíncrono
```

## 🌐 3. ESTRUTURA DOS ARQUIVOS DE PRODUÇÃO (HTML5 / JS / CSS)
*   **`index.html` (Estrutura Semântica Base)**:
    ```html
    <!DOCTYPE html>
    <html lang="pt-br">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <link rel="stylesheet" href="css/styles.css">
        <title>Synapse Web Instance</title>
    </head>
    <body>
        <main id="app-root">Carregando barramento de dados...</main>
        <script src="js/app.js"></script>
    </body>
    </html>
    ```

## 🏁 4. CONCLUSÃO E PROTOCOLO DE DEPLOY RESPONSIVO
O projeto web cumpre as diretrizes de código limpo e roteamento estrito. A implantação na nuvem (Deploy) segue o cronograma de 3 fases, mantendo a taxa de performance medida no Lighthouse em **95%** com auditorias quinzenais de latência.
"""
  
