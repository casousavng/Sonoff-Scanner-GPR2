# 🔌 Sonoff Scanner GPR2

**Sonoff Scanner GPR2** é uma aplicação web desenvolvida em Flask que permite detetar e controlar dispositivos Sonoff com firmware Tasmota na rede local. Através de uma interface simples, é possível identificar dispositivos na rede, controlá-los, renomeá-los e até bloquear o seu acesso com regras de iptables.

---

## 📋 Funcionalidades

- Deteta automaticamente dispositivos Sonoff com firmware Tasmota na rede local.
- Permite ligar e desligar dispositivos remotamente via interface web.
- intervace PWA para "instalacao" em dispositicos Android e iOS.
- Gestão de nomes personalizados para fácil identificação.
- Bloqueio e desbloqueio de IPs de dispositivos através de iptables.
- Área de administração protegida por autenticação.
- Persistência de dados com SQLite.
- Scan de rede com `nmap`.

---

## 🚀 Instalação

### 1. Clonar o repositório

```bash
git clone https://github.com/casousavng/Sonoff-Scanner-GPR2.git
cd Sonoff-Scanner-GPR2
```

### 2. Criar ambiente virtual (opcional mas recomendado)

```bash
python3 -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate
```

### 3. Instalar dependências

```bash
pip install -r requirements.txt
```

### 4. Instalar nmap (necessário para scan de rede)

```bash
sudo apt install nmap
```

### 5. Configurar variáveis de ambiente

Cria um ficheiro `.env` com o seguinte conteúdo:

```
USERNAME=teu_utilizador
PASSWORD=tua_senha_segura
```

### 6. Executar a aplicação

```bash
python sonoff_scan.py
```

Acede à aplicação em: [http://localhost:7500](http://localhost:7500)

---

## 🖥️ Utilização

- Acede ao endereço principal para ver os dispositivos detetados.
- Liga/desliga dispositivos diretamente através da interface.
- Acede à página `/admin` para gerir nomes, bloquear/desbloquear IPs e atualizar dispositivos.
- Usa o botão "Scan" para procurar dispositivos Sonoff ativos.
- A autenticação é necessária para aceder à página de administração.

---

## 📂 Estrutura do Projeto

```
Sonoff-Scanner-GPR2/
├── app.py               # Código principal da aplicação Flask
├── sonoff.db            # Base de dados SQLite gerada automaticamente
├── templates/           # Páginas HTML (Jinja2)
│   ├── index.html
│   └── admin.html
├── static/              # Assets estáticos (JS, CSS, imagens)
├── .env                 # Variáveis de ambiente (não incluído no repositório)
├── requirements.txt     # Dependências Python
└── README.md            # Este ficheiro
```

---

## 🔐 Segurança

- Apenas utilizadores autenticados podem aceder à interface de administração.
- As credenciais são definidas através de variáveis de ambiente (`.env`).
- Para bloquear IPs, é necessário que o utilizador que executa o app tenha permissões de `sudo`.

---

## 📦 requirements.txt

Conteúdo recomendado para o ficheiro `requirements.txt`:

```
Flask
requests
python-dotenv
```

---

## ⚠️ Notas Importantes

- O script utiliza `sudo` para executar comandos `iptables`, por isso, o utilizador deve ter permissões adequadas.
- nao correr o script Python com sudo pois nao deteta os dispositivos pelo nmap.
- Verifica se `nmap` está corretamente instalado e acessível via terminal.
- Dispositivos Sonoff devem estar com firmware **Tasmota** para serem compatíveis com os comandos utilizados.

---

## 📜 Licença

Distribuído sob a licença MIT. Consulta o ficheiro `LICENSE` para mais informações.

---

## 🤝 Contribuições

Contribuições são bem-vindas! Podes abrir uma issue ou submeter um pull request diretamente neste repositório.

---

Desenvolvido com ❤️ por [@casousavng](https://github.com/casousavng)
