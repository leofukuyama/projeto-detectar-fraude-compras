# Sistema de Controle de Compras

Um sistema completo com tela de login para adicionar compras no banco de dados e flagar via algoritmo de machine learning compras que podem ser fraudulentas.

## 📌 Visão Geral

O sistema oferece:
- Autenticação de usuários
- Cadastro de arquivos csv

## 🛠️ Tecnologias Utilizadas

- **Frontend**: Streamlit
- **Backend**: Python
- **Banco de Dados**: MySQL via AWS
- **Autenticação**: Bcrypt para hash de senhas
- **Estilos**: CSS personalizado

## 🔐 Funcionalidades de Autenticação

- Login seguro com verificação de credenciais
- Alteração de senha

## 📊 Módulos Principais

1. **Cadastros**
   - Registros de compras

2. **Algoritmo Machine Learning**
   - Flag para detecção de fraude

## 🚀 Como Executar

1. Clone o repositório:
```bash
git clone https://github.com/leofukuyama/projeto-detectar-fraude-compras
```
Instale as dependências:

```bash
pip install -r requirements.txt
```
Execute o aplicativo:

```bash
streamlit run main.py
```

📦 Estrutura de Arquivos:
<pre>
├── main.py               # Executável 
├── assets/
│   └── style.css         # Estilos personalizados
└── machine_learning/
    └── algoritmo_ml.py   # Estilos personalizados
             
</pre>

📝 Licença
Este projeto está licenciado sob a licença MIT - veja o arquivo LICENSE para detalhes.

✉️ Contato
Para dúvidas ou sugestões, entre em contato com o desenvolvedor.