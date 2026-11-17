# ============================================================
# SISTEMA CRUD DE ALUNOS
# Python + Streamlit + SQLite
# ============================================================
#
# Este programa demonstra as quatro operações fundamentais
# de um CRUD:
#
# CREATE  - cadastrar um aluno
# READ    - consultar os alunos
# UPDATE  - alterar os dados de um aluno
# DELETE  - excluir um aluno
#
# A interface é desenvolvida com Streamlit e apresentada
# no navegador. O SQLite armazena os dados em um arquivo.
#
# Para executar:
#   pip install streamlit
#   streamlit run CRUD_Alunos.py
#
# ============================================================


# ============================================================
# 1. IMPORTAÇÃO DAS BIBLIOTECAS
# ============================================================

# sqlite3 permite criar e manipular bancos de dados SQLite.
import sqlite3

# streamlit é utilizado para construir a interface web.
import streamlit as st


# ============================================================
# 2. CONFIGURAÇÕES
# ============================================================

# Nome do arquivo do banco de dados.
# Se ele não existir, o SQLite o criará automaticamente.
NOME_BANCO = "alunos.db"

# Configura título, ícone e largura da página no navegador.
# Esta configuração deve ser um dos primeiros comandos Streamlit.
st.set_page_config(
    page_title="CRUD - Cadastro de Alunos",
    page_icon="🎓",
    layout="wide"
)


# ============================================================
# 3. BANCO DE DADOS
# ============================================================

def conectar_banco():
    """
    Estabelece uma conexão com o banco de dados SQLite.

    sqlite3.connect() abre o arquivo informado.
    Caso o arquivo ainda não exista, ele será criado.

    Retorna:
        Um objeto de conexão com o banco de dados.
    """
    return sqlite3.connect(NOME_BANCO)


def criar_tabela():
    """
    Cria a tabela alunos caso ela ainda não exista.

    CREATE TABLE IF NOT EXISTS evita um erro quando
    o programa é executado novamente e a tabela já existe.
    """

    conexao = conectar_banco()

    try:
        # cursor() cria o objeto utilizado para executar SQL.
        cursor = conexao.cursor()

        # CREATE TABLE cria a estrutura da tabela.
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS alunos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                cpf TEXT,
                email TEXT,
                curso TEXT,
                semestre INTEGER
            )
        """)

        # commit() confirma a criação/alteração no banco.
        conexao.commit()

    finally:
        # Fecha a conexão mesmo se ocorrer algum erro.
        conexao.close()


# ============================================================
# 4. OPERAÇÃO CREATE - INSERIR
# ============================================================

def inserir_aluno(nome, cpf, email, curso, semestre):
    """
    Insere um novo aluno no banco de dados.

    Os dados são recebidos como parâmetros da função.
    A interface Streamlit coleta os valores e os envia
    para esta função.
    """

    conexao = conectar_banco()

    try:
        cursor = conexao.cursor()

        # INSERT INTO insere um novo registro na tabela.
        #
        # Os sinais ? são parâmetros SQL.
        # Os valores são enviados separadamente, evitando
        # concatenar dados do usuário diretamente no SQL.
        cursor.execute("""
            INSERT INTO alunos
                (nome, cpf, email, curso, semestre)
            VALUES (?, ?, ?, ?, ?)
        """, (nome, cpf, email, curso, semestre))

        # Confirma a gravação no banco.
        conexao.commit()

        # lastrowid retorna o ID gerado automaticamente.
        return cursor.lastrowid

    finally:
        conexao.close()


# ============================================================
# 5. OPERAÇÃO READ - CONSULTAR
# ============================================================

def consultar_alunos():
    """
    Consulta todos os alunos cadastrados.

    SELECT recupera dados da tabela.
    ORDER BY nome organiza os resultados alfabeticamente.

    Retorna:
        Uma lista contendo os registros encontrados.
    """

    conexao = conectar_banco()

    try:
        cursor = conexao.cursor()

        cursor.execute("""
            SELECT id, nome, cpf, email, curso, semestre
            FROM alunos
            ORDER BY nome
        """)

        # fetchall() recupera todos os registros retornados.
        registros = cursor.fetchall()

        return registros

    finally:
        conexao.close()


def consultar_aluno_por_id(id_aluno):
    """
    Consulta um único aluno pelo seu ID.

    WHERE restringe a consulta ao registro informado.
    fetchone() retorna somente o primeiro resultado.
    """

    conexao = conectar_banco()

    try:
        cursor = conexao.cursor()

        cursor.execute("""
            SELECT id, nome, cpf, email, curso, semestre
            FROM alunos
            WHERE id = ?
        """, (id_aluno,))

        return cursor.fetchone()

    finally:
        conexao.close()


# ============================================================
# 6. OPERAÇÃO UPDATE - ALTERAR
# ============================================================

def alterar_aluno(id_aluno, nome, cpf, email, curso, semestre):
    """
    Atualiza os dados de um aluno existente.

    UPDATE modifica registros.
    SET define os novos valores.
    WHERE identifica qual registro será alterado.
    """

    conexao = conectar_banco()

    try:
        cursor = conexao.cursor()

        cursor.execute("""
            UPDATE alunos
            SET nome = ?,
                cpf = ?,
                email = ?,
                curso = ?,
                semestre = ?
            WHERE id = ?
        """, (nome, cpf, email, curso, semestre, id_aluno))

        # Confirma a alteração.
        conexao.commit()

        # rowcount informa quantos registros foram afetados.
        return cursor.rowcount

    finally:
        conexao.close()


# ============================================================
# 7. OPERAÇÃO DELETE - EXCLUIR
# ============================================================

def excluir_aluno(id_aluno):
    """
    Exclui um aluno pelo ID.

    DELETE FROM remove registros da tabela.
    WHERE define qual registro será excluído.
    """

    conexao = conectar_banco()

    try:
        cursor = conexao.cursor()

        cursor.execute("""
            DELETE FROM alunos
            WHERE id = ?
        """, (id_aluno,))

        # Confirma a exclusão.
        conexao.commit()

        # Informa quantos registros foram excluídos.
        return cursor.rowcount

    finally:
        conexao.close()


# ============================================================
# 8. FUNÇÕES AUXILIARES
# ============================================================

def validar_dados(nome, semestre_texto):
    """
    Valida os campos obrigatórios e converte o semestre.

    Retorna:
        (True, semestre_convertido, None) se estiver correto.
        (False, None, mensagem_de_erro) se houver problema.
    """

    # O nome é obrigatório.
    if not nome.strip():
        return False, None, "Informe o nome do aluno."

    # Se o semestre não foi informado, será armazenado como NULL.
    if semestre_texto.strip() == "":
        return True, None, None

    # Tenta converter o semestre para número inteiro.
    try:
        semestre = int(semestre_texto)

    except ValueError:
        return False, None, "O semestre deve ser um número inteiro."

    # Validação adicional: semestre deve ser positivo.
    if semestre <= 0:
        return False, None, "O semestre deve ser maior que zero."

    return True, semestre, None


def formatar_aluno(aluno):
    """
    Recebe um registro de aluno e monta um texto para
    apresentação na caixa de seleção do Streamlit.
    """

    id_aluno, nome, cpf, email, curso, semestre = aluno

    return f"{id_aluno} - {nome} | {curso or 'Curso não informado'}"


# ============================================================
# 9. INICIALIZAÇÃO DO BANCO DE DADOS
# ============================================================

# Garante que o banco e a tabela existam antes de utilizar
# as funções de cadastro, consulta, alteração e exclusão.
criar_tabela()


# ============================================================
# 10. CABEÇALHO DA APLICAÇÃO
# ============================================================

# st.title() apresenta o título principal da página.
st.title("🎓 Cadastro de Alunos")

# st.write() apresenta textos e outros elementos na página.
st.write("Exemplo de CRUD utilizando Python + Streamlit + SQLite.")

# st.divider() apresenta uma linha divisória.
st.divider()


# ============================================================
# 11. INDICADORES DO CADASTRO
# ============================================================

# Consulta os registros para calcular a quantidade de alunos.
alunos = consultar_alunos()

# st.columns() divide a área da página em colunas.
coluna1, coluna2 = st.columns(2)

# metric() apresenta um indicador numérico.
with coluna1:
    st.metric("Alunos cadastrados", len(alunos))

with coluna2:
    st.metric("Banco de dados", NOME_BANCO)


st.divider()


# ============================================================
# 12. ÁREA DE CADASTRO
# ============================================================

# st.subheader() apresenta um título secundário.
st.subheader("Cadastrar novo aluno")

# st.form() agrupa campos e permite enviar os valores
# em conjunto quando o usuário clica no botão de envio.
#
# clear_on_submit=True limpa os campos após o envio.
with st.form("form_cadastro", clear_on_submit=True):

    # Divide o formulário em duas colunas.
    col_nome, col_cpf = st.columns(2)

    # text_input() cria um campo de entrada de texto.
    with col_nome:
        nome_novo = st.text_input("Nome *")

    with col_cpf:
        cpf_novo = st.text_input("CPF")

    col_email, col_curso = st.columns(2)

    with col_email:
        email_novo = st.text_input("E-mail")

    with col_curso:
        curso_novo = st.text_input("Curso")

    semestre_novo = st.text_input(
        "Semestre",
        placeholder="Exemplo: 1, 2, 3..."
    )

    # form_submit_button() cria um botão que envia
    # os dados preenchidos no formulário.
    cadastrar = st.form_submit_button(
        "Salvar aluno",
        type="primary",
        use_container_width=True
    )


# O código abaixo é executado quando o formulário é enviado.
if cadastrar:

    # Valida o nome e converte o semestre.
    valido, semestre_convertido, erro = validar_dados(
        nome_novo,
        semestre_novo
    )

    if not valido:

        # st.error() apresenta uma mensagem de erro.
        st.error(erro)

    else:

        try:
            # Executa a operação CREATE.
            novo_id = inserir_aluno(
                nome_novo.strip(),
                cpf_novo.strip(),
                email_novo.strip(),
                curso_novo.strip(),
                semestre_convertido
            )

            # st.success() apresenta uma mensagem de sucesso.
            st.success(
                f"Aluno cadastrado com sucesso! ID: {novo_id}"
            )

            # rerun() executa novamente o programa Streamlit,
            # atualizando os dados apresentados na página.
            st.rerun()

        except sqlite3.Error as erro_banco:
            st.error(f"Erro ao cadastrar aluno: {erro_banco}")


st.divider()


# ============================================================
# 13. ÁREA DE ALTERAÇÃO E EXCLUSÃO
# ============================================================

st.subheader("Alterar ou excluir aluno")

# Consulta novamente os alunos existentes.
alunos = consultar_alunos()

if not alunos:

    # st.info() apresenta uma informação ao usuário.
    st.info("Ainda não existem alunos cadastrados.")

else:

    # Cria uma lista contendo os IDs dos alunos.
    ids_alunos = [aluno[0] for aluno in alunos]

    # Cria um dicionário para localizar rapidamente
    # os dados completos de cada aluno pelo ID.
    alunos_por_id = {
        aluno[0]: aluno for aluno in alunos
    }

    # selectbox() cria uma caixa de seleção.
    # O usuário escolhe qual aluno deseja alterar ou excluir.
    id_selecionado = st.selectbox(
        "Selecione um aluno",
        options=ids_alunos,
        format_func=lambda id_aluno: formatar_aluno(
            alunos_por_id[id_aluno]
        )
    )

    # Recupera os dados do aluno selecionado.
    aluno_selecionado = alunos_por_id[id_selecionado]

    # Separa os campos do registro.
    (
        id_atual,
        nome_atual,
        cpf_atual,
        email_atual,
        curso_atual,
        semestre_atual
    ) = aluno_selecionado

    # Apresenta o formulário de alteração.
    with st.form("form_alteracao"):

        st.write(f"**ID do aluno:** {id_atual}")

        col_nome_alt, col_cpf_alt = st.columns(2)

        with col_nome_alt:
            nome_alt = st.text_input(
                "Nome",
                value=nome_atual or "",
                key=f"nome_alt_{id_atual}"
            )

        with col_cpf_alt:
            cpf_alt = st.text_input(
                "CPF",
                value=cpf_atual or "",
                key=f"cpf_alt_{id_atual}"
            )

        col_email_alt, col_curso_alt = st.columns(2)

        with col_email_alt:
            email_alt = st.text_input(
                "E-mail",
                value=email_atual or "",
                key=f"email_alt_{id_atual}"
            )

        with col_curso_alt:
            curso_alt = st.text_input(
                "Curso",
                value=curso_atual or "",
                key=f"curso_alt_{id_atual}"
            )

        # Se o semestre estiver vazio no banco, apresenta
        # um campo de texto vazio.
        semestre_texto_atual = (
            str(semestre_atual)
            if semestre_atual is not None
            else ""
        )

        semestre_alt = st.text_input(
            "Semestre",
            value=semestre_texto_atual,
            key=f"semestre_alt_{id_atual}"
        )

        # Botão responsável por enviar os dados para alteração.
        alterar = st.form_submit_button(
            "Alterar cadastro",
            type="primary",
            use_container_width=True
        )

    # Executa a alteração somente após o envio do formulário.
    if alterar:

        valido, semestre_convertido, erro = validar_dados(
            nome_alt,
            semestre_alt
        )

        if not valido:

            st.error(erro)

        else:

            try:
                quantidade = alterar_aluno(
                    id_atual,
                    nome_alt.strip(),
                    cpf_alt.strip(),
                    email_alt.strip(),
                    curso_alt.strip(),
                    semestre_convertido
                )

                if quantidade > 0:
                    st.success("Aluno alterado com sucesso!")
                    st.rerun()

                else:
                    st.warning("Nenhum registro foi alterado.")

            except sqlite3.Error as erro_banco:
                st.error(f"Erro ao alterar aluno: {erro_banco}")


    # --------------------------------------------------------
    # EXCLUSÃO DO ALUNO
    # --------------------------------------------------------

    st.markdown("#### Excluir aluno")

    # checkbox() cria uma caixa de confirmação.
    # O usuário precisa marcá-la antes de excluir.
    confirmar_exclusao = st.checkbox(
        f"Confirmo que desejo excluir o aluno {nome_atual}.",
        key=f"confirmar_exclusao_{id_atual}"
    )

    # button() cria um botão de ação.
    excluir = st.button(
        "Excluir aluno selecionado",
        type="secondary",
        disabled=not confirmar_exclusao,
        use_container_width=True
    )

    if excluir:

        try:
            quantidade = excluir_aluno(id_atual)

            if quantidade > 0:
                st.success("Aluno excluído com sucesso!")
                st.rerun()

            else:
                st.warning("Aluno não encontrado.")

        except sqlite3.Error as erro_banco:
            st.error(f"Erro ao excluir aluno: {erro_banco}")


st.divider()


# ============================================================
# 14. OPERAÇÃO READ - LISTAGEM DOS ALUNOS
# ============================================================

st.subheader("Alunos cadastrados")

# Consulta os dados atualizados no banco.
alunos = consultar_alunos()

if alunos:

    # Cria uma lista de dicionários para apresentar
    # os registros em formato tabular.
    #
    # Cada dicionário representa uma linha.
    dados_tabela = []

    for aluno in alunos:

        dados_tabela.append({
            "ID": aluno[0],
            "Nome": aluno[1],
            "CPF": aluno[2],
            "E-mail": aluno[3],
            "Curso": aluno[4],
            "Semestre": aluno[5]
        })

    # st.dataframe() apresenta os dados em formato de tabela.
    #
    # use_container_width=True utiliza toda a largura disponível.
    # hide_index=True oculta o índice interno do DataFrame/tabela.
    st.dataframe(
        dados_tabela,
        use_container_width=True,
        hide_index=True
    )

else:

    st.info("Nenhum aluno cadastrado para apresentar.")


# ============================================================
# 15. RODAPÉ
# ============================================================

st.divider()

# caption() apresenta um texto de menor destaque.
st.caption(
    "Python + Streamlit + SQLite | Exemplo didático de CRUD"
)
