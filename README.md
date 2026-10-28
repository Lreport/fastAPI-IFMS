# Gerenciador de Atividades

Eae prof. Rogério, fiz esse projeto para organizar melhor as atividades de cada matéria ao longo do semestre.

## Como executar


1. Abra a pasta do projeto no VS Code e abra um terminal.
2. Na primeira execução, crie o ambiente virtual e instale as dependências:

   ```powershell
   python -m venv .venv
   .\.venv\Scripts\python.exe -m pip install -r requirements.txt
   ```

3. Inicie o servidor:

   ```powershell
   .\.venv\Scripts\python.exe -m uvicorn main:app --reload
   ```

4. Com o servidor em execução, acesse o [Swagger](http://127.0.0.1:8000/docs).

Deixe o terminal aberto enquando usa o sistema. Para encerrar, de **Ctrl+C**.

## Duvida

Quando você exclui uma atividade e depois você pesquisa ela, utilizando os métodos get, retorna uma lista vazia, o correto seria retornar um erro ou está certo assim? Acho que o certo erro seria valido se o método nao funcionasse, não é ?