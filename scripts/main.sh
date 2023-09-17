#!/bin/bash
# Definindo o interpretador de script como bash

# Este script lança a classe QueryOptimizer com o agente Java JoularJX
# Deve ser executado nesta pasta

trap 'rm -f joularJX-*.csv ; exit' INT
# Configura um tratamento de sinal (INT) para remover arquivos CSV do JoularJX em caso de interrupção e, em seguida, sai do script.

source <(grep = ../var.ini)
# Lê e carrega variáveis do arquivo var.ini encontrado no diretório superior como variáveis de ambiente.

CLASS=greendb.QueryOptimizer
# Define a classe Java que será executada como CLASS.

if [ $# -lt 1 ]; then
  # Verifica se o número de argumentos passados é menor que 1
  echo 1>&2 "usage: bash $0 <number of iterations>"
  # Exibe uma mensagem de uso no STDERR (1>&2) se o número de argumentos for insuficiente.
  exit 2
fi

# Atribui o primeiro argumento (número de iterações) a nb_iterations e desloca os argumentos para a esquerda.
nb_iterations=$1
shift

now=$(date +%y.%m.%d-%Hh%Mm%Ss)
# Obtém a data e hora atual no formato especificado e armazena em now.

mkdir -p results/$now
mkdir -p graphs
# Cria diretórios para armazenar resultados e gráficos com base na data e hora atual.

for i in $(seq 1 $nb_iterations); do
    # Loop para realizar a iteração do programa Java várias vezes

    # Linha de comando para executar o programa Java com o agente JoularJX
    java -javaagent:$joularJX_jar -cp $CLASSPATH:$connector_jar $CLASS

    # Especifica os nomes dos arquivos do JoularJX a serem coletados
    total_energy="joularJX-*-methods-energy.csv"
    total_filtered_energy="joularJX-*-methods-energy-filtered.csv"
    power="joularJX-*-methods-power.csv"
    power_filtered="joularJX-*-methods-filtered-power.csv"

    # Define caminhos para mover os arquivos do JoularJX
    filtered_csv="./results/"$now"/"$i"_"$now"_joularJX-methods-energy-filtered.csv"
    graph="./graphs/"$now"_methods-consumption.png"

    # Move os arquivos do JoularJX para os diretórios especificados (move o do método filtrado no config.properties)
    mv $total_filtered_energy $filtered_csv
    echo "JoularJX csv moved to $filtered_csv"

    # Remove os arquivos de potência
    rm -f $power
    rm -f $power_filtered
    rm -f $total_energy
done

# Criação do gráfico a partir dos dados coletados
echo "Creation of the graph..."
python3 jx_plot.py "results/"$now $graph

# Exibe o gráfico usando o visualizador de imagens "eog"
eog $graph

