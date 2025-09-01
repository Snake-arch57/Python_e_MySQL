import pymysql.cursors

# Função para abrir conexão com o banco de dados
def open_connection(db_name='Seu banco de dados'):
    try:
        connection = pymysql.connect(
            host='Seu host',
            user='Seu usuario',
            password='Sua senha',
            database=db_name,
            cursorclass=pymysql.cursors.DictCursor
        )
        return connection
    except pymysql.Error as e:
        print(f"Connection failed: {e}")
        return None

# Função para verificar se o banco existe
def database_exists(connection, db_name):
    try:
        with connection.cursor() as cursor:
            cursor.execute('SHOW DATABASES;')
            databases = [db['Database'] for db in cursor.fetchall()]
            return db_name in databases
    except pymysql.Error as e:
        print(f"Error checking databases: {e}")
        return False

# Loop principal
while True:
    print('----Funções----')
    print('1. List databases')
    print('2. Insert aluno')
    print('3. Insert books')
    print('4. inserir livro por titulo e email')
    print('5. Checar emprestimos pendentes por nome do aluno')
    print('6. Close SQL')
    print('---------------------')

    opcao = input('Type an option: ')
    connection = open_connection()

    if not connection:
        print("Failed to connect to database")
        continue

    if opcao == '1':
        try:
            with connection.cursor() as cursor:
                cursor.execute('SHOW DATABASES;')
                result = cursor.fetchall()
                print("Databases:", result)
        except pymysql.Error as e:
            print(f"Error executing query: {e}")
        finally:
            connection.close()

    elif opcao == "2":
        try:
            with connection.cursor() as cursor:
                sql = "INSERT INTO alunos (nome, email, data_nascimento) VALUES (%s, %s, %s)"
                nome = input("Digite o nome do aluno: ")
                email = input("Digite o email do aluno: ")
                data_nascimento = input("Digite a data de nascimento do aluno (AAAA-MM-DD): ")
                cursor.execute(sql, (nome, email, data_nascimento))
                connection.commit()
                print("Aluno cadastrado com sucesso!")
        except pymysql.Error as e:
            print(f"Erro ao cadastrar aluno: {e.args[0]} - {e.args[1]}")
            connection.rollback() # é usado em execpt para impedir inputs de dados incompletos
        finally:
            connection.close()

    elif opcao == "3":
        try:
            with connection.cursor() as cursor:
                sql = "INSERT INTO livros (titulo, autor, ano_publicacao) VALUES (%s, %s, %s)"
                titulo = input("Digite o título do livro: ")
                autor = input("Digite o autor do livro: ")
                ano_publicacao = input("Digite o ano de publicação do livro (AAAA): ")
                cursor.execute(sql, (titulo, autor, ano_publicacao))
                connection.commit()
                print("Livro cadastrado com sucesso!")
        except pymysql.Error as e:
            print(f"Erro ao cadastrar livro: {e.args[0]} - {e.args[1]}")
            connection.rollback()#Impede inputs de dados incompletos
        finally:
            connection.close()

    elif opcao == "4":
        try:
            with connection.cursor() as cursor:
                titulo = input("Digite o título do livro: ")
                email = input("Digite o email do aluno: ")
                sql = """
                    SELECT l.titulo, l.autor, l.ano_publicacao, a.nome, a.email
                    FROM livros l
                    JOIN alunos a ON a.email = %s
                    WHERE l.titulo = %s
                """
                cursor.execute(sql, (email, titulo))
                result = cursor.fetchone() #retorna a proxima linha da consulta, no caso o livro
                if result:
                    print("Registro encontrado:", result)
                else:
                    print("Nenhum registro encontrado para o título e email fornecidos.")
        except pymysql.Error as e:
            print(f"Erro ao buscar registro: {e.args[0]} - {e.args[1]}")
        finally:
            connection.close()

    elif opcao == "5":
        try:
            with connection.cursor() as cursor:
                nome = input("Digite o nome do aluno: ")
                sql = """
                    SELECT alunos.aluno_id, alunos.nome, livros.titulo, emprestimo_livros.data_emprestimo
                    FROM alunos
                    LEFT JOIN emprestimo_livros ON emprestimo_livros.aluno_id = alunos.aluno_id
                    LEFT JOIN livros ON livros.livro_id = emprestimo_livros.livro_id
                    WHERE alunos.nome = %s AND emprestimo_livros.data_devolucao IS NULL
                """
                cursor.execute(sql, (nome,))
                results = cursor.fetchall() #retorna todos as consultas do Banco de dados 
                if results:
                    print("Empréstimos pendentes:", results)
                else:
                    print("Nenhum empréstimo pendente encontrado para o aluno.")
        except pymysql.Error as e:
            print(f"Erro ao consultar empréstimos: {e.args[0]} - {e.args[1]}")
        finally:
            connection.close()

    elif opcao == '6':
        print("Closing...")
        break

    else:
        print("Function not found")

        connection.close()

