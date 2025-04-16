Sonoff-Scanner-GPR2

Sonoff-Scanner-GPR2 é uma aplicação web desenvolvida em Python que permite gerir e monitorizar dispositivos Sonoff na rede local. Através de uma interface simples, é possível visualizar os dispositivos activos, aceder a informações detalhadas e realizar acções administrativas.

Funcionalidades
	•	Detecção de dispositivos Sonoff na rede local.
	•	Interface web intuitiva para visualização e gestão dos dispositivos.
	•	Autenticação de utilizadores para um acesso seguro.
	•	Base de dados SQLite para armazenamento de informações dos dispositivos.

Pré-requisitos
	•	Python 3.6 ou superior
	•	Pip (gestor de pacotes do Python)

Instalação
	1.	Clonar o repositório:

git clone https://github.com/casousavng/Sonoff-Scanner-GPR2.git
cd Sonoff-Scanner-GPR2


	2.	Instalar as dependências:

pip install -r requirements.txt


	3.	Executar a aplicação:

python sonoff_scan.py


	4.	Aceder à interface web:
Abre o navegador e acede a http://localhost:5000.

Estrutura do Projecto
	•	sonoff_scan.py: Script principal que inicia a aplicação.
	•	templates/: Directório que contém os ficheiros HTML da interface.
	•	static/: Directório para ficheiros estáticos (CSS, JavaScript, imagens).
	•	sonoff.db: Base de dados SQLite com informações dos dispositivos.

Contribuições

As contribuições são bem-vindas! Se quiseres ajudar a melhorar este projecto:
	1.	Faz um fork do repositório.
	2.	Cria uma nova branch com a tua funcionalidade: git checkout -b a-minha-funcionalidade.
	3.	Faz commit das tuas alterações: git commit -m 'Adicionada nova funcionalidade'.
	4.	Faz push para a branch: git push origin a-minha-funcionalidade.
	5.	Abre um Pull Request.

Licença

Este projecto está licenciado sob a Licença MIT. Consulta o ficheiro LICENSE para mais informações.
