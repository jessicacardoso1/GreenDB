package greendb;
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;


public class QueryOptimizer {

    public static void main(String[] args) {
    	teste();
    	System.exit(0);       
    }
    
    public static int teste() {
		// Configurações da conexão
        String url = "jdbc:mysql://localhost:3306/datasus";
        String user = "root";
        String password = "Dev@Jessic4";

        try {
            // Carrega o driver JDBC
            Class.forName("com.mysql.cj.jdbc.Driver");
            
            // Estabelece a conexão com o banco de dados
            Connection connection = DriverManager.getConnection(url, user, password);
            
            // Verifica se a conexão foi bem-sucedida
            if (connection != null) {
                System.out.println("Conexão bem-sucedida!");
                
                Statement statement = connection.createStatement();
                
                String consultaSQL = "SELECT * FROM internamentos_ba 10"; // Substitua pela consulta desejada

                // Executa a consulta SQL e obtém o resultado
                ResultSet resultSet = statement.executeQuery(consultaSQL);

                for(int i = 0; i < 1000000; i++) {           
                	while (resultSet.next()) {
                        // Aqui você pode acessar os dados da tabela "internamentos"
                        // Exemplo: int id = resultSet.getInt("ID");
                            String nome = resultSet.getString("ESPEC");
                            nome = i + nome; 
                         //   System.out.println(nome);		
                        // Faça o que desejar com os dados aqui
                    } 
                }
                               
                connection.close();
            }
        } catch (ClassNotFoundException e) {
            System.out.println("Driver JDBC não encontrado.");
        } catch (SQLException e) {
            System.out.println("Erro ao conectar ao banco de dados: " + e.getMessage());
        }
        return 0;
	}
	
}
