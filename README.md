Claro! Com base no código fornecido e no repositório Sonoff-Scanner-GPR2, aqui está um ficheiro README.md em português de Portugal, adequado para o teu projeto:

⸻



# 🔌 Sonoff Scanner GPR2

**Sonoff Scanner GPR2** é uma aplicação web desenvolvida em Flask que permite detetar, controlar e gerir dispositivos Sonoff com firmware Tasmota na tua rede local. A aplicação oferece funcionalidades como scan de rede, controlo de dispositivos, gestão de nomes e bloqueio de IPs através de `iptables`.

## 🚀 Funcionalidades

- **Deteção de dispositivos Sonoff**: Realiza scans na rede local para identificar dispositivos Sonoff ativos.
- **Controlo de dispositivos**: Liga ou desliga dispositivos diretamente através da interface web.
- **Gestão de nomes**: Permite renomear dispositivos para uma identificação mais fácil.
- **Bloqueio de IPs**: Bloqueia ou desbloqueia o acesso de dispositivos à rede utilizando `iptables`.
- **Autenticação**: Acesso à área de administração protegido por login.

## 🛠️ Requisitos

- Python 3.8 ou superior
- `nmap` instalado no sistema (utilizado para o scan de rede)
- Permissões de `sudo` para gerir regras de `iptables`

## 📦 Instalação

1. **Clonar o repositório:**

   git clone https://github.com/casousavng/Sonoff-Scanner-GPR2.git
   cd Sonoff-Scanner-GPR2
   

	2.	Criar e ativar um ambiente virtual (opcional mas recomendado):

python -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate


	3.	Instalar as dependências:

pip install -r requirements.txt


	4.	Configurar variáveis de ambiente:
Criar um ficheiro .env na raiz do projeto com o seguinte conteúdo:

USERNAME=teu_utilizador
PASSWORD=sua_senha_segura


	5.	Executar a aplicação:

python app.py

A aplicação estará disponível em http://localhost:7500.

🖥️ Utilização
	•	Página principal: Acede a http://localhost:7500 para visualizar os dispositivos detetados.
	•	Administração: Acede a http://localhost:7500/admin e autentica-te para gerir dispositivos.
	•	Scan de rede: Utiliza a opção “Scan” na interface para procurar novos dispositivos Sonoff.
	•	Controlo de dispositivos: Liga ou desliga dispositivos diretamente na interface.
	•	Gestão de nomes: Renomeia dispositivos para uma identificação mais fácil.
	•	Bloqueio de IPs: Bloqueia ou desbloqueia o acesso de dispositivos à rede.

🗂️ Estrutura do Projeto

Sonoff-Scanner-GPR2/
├── app.py             # Código principal da aplicação Flask
├── sonoff.db          # Base de dados SQLite (criada automaticamente)
├── templates/         # Ficheiros HTML para a interface web
│   ├── index.html
│   └── admin.html
├── static/            # Ficheiros estáticos (CSS, JS, imagens)
├── .env               # Ficheiro de variáveis de ambiente
├── requirements.txt   # Lista de dependências Python
└── README.md          # Este ficheiro

⚠️ Notas
	•	Permissões de sudo: Algumas funcionalidades, como o bloqueio de IPs, requerem permissões de sudo. Certifica-te de que o utilizador que executa a aplicação tem as permissões necessárias.
	•	Segurança: Protege o ficheiro .env e evita expor as credenciais em ambientes públicos.
	•	Compatibilidade: Esta aplicação foi testada com dispositivos Sonoff que utilizam o firmware Tasmota.

📄 Licença

Este projeto está licenciado sob a MIT License.

🤝 Contribuições

Contribuições são bem-vindas! Sente-te à vontade para abrir issues ou pull requests no repositório.

⸻



---

### 📄 requirements.txt

Com base nas bibliotecas utilizadas no código fornecido, aqui está o conteúdo do ficheiro `requirements.txt`:

```txt
Flask
requests
python-dotenv

Certifica-te de que o nmap está instalado no sistema, pois é utilizado para o scan de rede. No Ubuntu, podes instalá-lo com:

sudo apt-get install nmap

Se precisares de mais alguma coisa ou tiveres dúvidas, estou aqui para ajudar!
