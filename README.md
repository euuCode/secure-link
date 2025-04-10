
# Secure Link


## Tutorial Completo para Instalar, Configurar, Testar e Lançar o SecureLink


Bem-vindo ao tutorial detalhado para o SecureLink, uma ferramenta de cibersegurança para criar links seguros e temporários em Python, Electron, e React. Este guia é para o Linux Mint, mas pode ser adaptado para Windows. Siga os passos no seu ritmo tranquilo, mantendo o uso ético apenas no notebook pessoal como cobaia autorizada.

---

### 1. Pré-requisitos
- Python 3.11+ (ou superior)
- Node.js 16+ e npm 7+ (ou superiores)
- Bibliotecas Python: cryptography, reportlab, flask
- Dependências Node.js: electron, python-shell

---

### 2. Verifique o Ambiente e a Pasta
- Objetivo: Confirmar que você está no Linux Mint, com os arquivos corretos na pasta /home/euumarcin/Área de Trabalho/securelink.

1. Abra o terminal no Linux Mint.
2. Navegue até a pasta securelink:
cd /home/euumarcin/Área\ de\ Trabalho/securelink


- Se der erro, confirme no Explorer (Navegação de Arquivos) se a pasta existe. Se o nome for diferente (ex.: securitylink), ajuste:
cd /home/euumarcin/Área\ de\ Trabalho/securitylink

3. Liste os arquivos na pasta:
ls


- Deve listar: backend.py, main.js, index.html, e package.json.
- Se faltar algum, crie os arquivos usando nano ou vim:
  - Para backend.py:
nano backend.py

- Cole o código abaixo e salve com Ctrl+O, Enter, Ctrl+X.
- Repita para main.js, index.html, e package.json (códigos abaixo).

---

### 3. Instale as Dependências Python (Back-end)
- Objetivo: Garantir que o backend.py (Flask) funcione corretamente.

1. Certifique que o Python 3.11+ está instalado:
python3 --version


- Deve mostrar algo como Python 3.13.0. Se for antigo, atualize:
sudo apt update
sudo apt install python3 python3-pip -y


2. Instale as bibliotecas Python:
pip install cryptography reportlab flask


- Se der erro de permissão, use virtualenv:
python3 -m venv venv
source venv/bin/activate
pip install cryptography reportlab flask



3. Verifique as instalações:
pip list | grep -E 'cryptography|reportlab|flask'


- Deve listar:
cryptography   42.0.5
reportlab      4.1.0
flask          3.0.3


---

### 4. Instale o Node.js e o npm (Front-end)
- Objetivo: Garantir que o npm e as dependências do Electron estejam instalados e atualizados.

1. Instale o Node.js e o npm:
sudo apt update
sudo apt install nodejs npm -y


2. Atualize o npm e o Node.js para versões recentes (Node.js 16+ recomendado):
sudo npm install -g npm
node --version  # Deve ser 16+ (ex.: v18.19.0)
npm --version   # Deve ser 7+ ou 8+ (ex.: 10.2.3)


- Se o Node.js for antigo, atualize com n:
sudo apt install curl -y
curl -L https://raw.githubusercontent.com/tj/n/master/bin/n | bash
sudo n latest



3. Instale as dependências do package.json:
npm install


- Se der erro, use:
sudo npm install


- Ou instale localmente:
npm install --no-bin-links


4. Verifique as dependências:
ls node_modules
cat package-lock.json

- Deve listar electron e python-shell.

---

### 5. Rode o Back-end (Python/Flask)
- Objetivo: Iniciar o servidor Flask em http://127.0.0.1:8000.

1. Abra um terminal e navegue:
cd /home/euumarcin/Área\ de\ Trabalho/securelink


2. Se usar virtualenv, ative:
source venv/bin/activate



3. Rode o back-end:
python3 backend.py


- O output deve ser:
Serving Flask app 'backend'
Debug mode: off WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
Running on http://127.0.0.1:8000 Press CTRL+C to quit

- Deixe rodando (não feche).

---

### 6. Rode o Front-end (Electron)
- Objetivo: Iniciar a interface gráfica com npm start.

1. Abra um segundo terminal (mantendo o backend.py rodando).
2. Navegue:
cd /home/euumarcin/Área\ de\ Trabalho/securelink


3. Se usar virtualenv, ative (opcional, só pro back-end):
source venv/bin/activate

t
4. Execute o front-end:
npm start


- Se der erro:
  - Verifique o package.json (código abaixo se necessário).
  - Reinstale:
npm install


- Se der npm: command not found, instale:
sudo apt install npm -y


- Se der Error: Cannot find module, reinstale:
npm install electron python-shell
npm start


- Se der EACCES, use:
sudo npm start



5. Uma janela Electron abrirá. Teste:
- Digite uma mensagem (ex.: "Olá, teste seguro") ou clique "Carregar Arquivo".
- Insira um PIN (ex.: "1234").
- Escolha o tempo (30 minutos).
- Clique "Criar Link Seguro" — veja o link clicável ("http://127.0.0.1:8000/link/XXXXXX").
- Clique no link (abre no navegador), insira o PIN pra acessar.
- Cancele com "Cancelar Link".
- Clique "Gerar Relatório PDF" pra salvar em /home/euumarcin/Desktop/securelink_report.pdf.
- Clique "Ajuda" pra ver o manual.

---

### 7. Verifique os Relatórios
- Abra o Explorer em /home/euumarcin/Desktop:
- Confirme securelink_logs.json e securelink_report.pdf.
- Se der erro de permissão, ajuste:
sudo chmod 777 /home/euumarcin/Desktop


---

### 8. Resolva Erros Comuns
- Se o link não abrir:
- Certifique que o backend.py está rodando na porta 8000 (http://127.0.0.1:8000).
- Verifique se a porta 8000 está livre:
sudo netstat -tuln | grep 8000


- Se ocupada, ajuste backend.py para porta 8080:
```python
app.run(host='127.0.0.1', port=8080, debug=False, use_reloader=False)
E mude os links em main.js e index.html para "http://127.0.0.1:8080/link/XXXXXX".

