import numpy as np
import os
import statistics
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.offsetbox import AnchoredText
import sys

if __name__ == '__main__':
    # Verifica se o script está sendo executado como programa principal

    if len(sys.argv) < 2:
        # Verifica se pelo menos dois argumentos foram fornecidos na linha de comando
        print("usage : python3 jx_plot.py <csv folder path> <graph to create path>")
        exit(1)

    data_list = []
    files_list = []

    for root, _, files in os.walk(sys.argv[1]):
        # Percorre recursivamente a pasta especificada na linha de comando para encontrar arquivos CSV
        for name in files:
            files_list.append(os.path.join(root, name))

    for j in range(len(files_list)):
        data_list.append(pd.read_csv(files_list[j], header=None))
    
    data = pd.concat(data_list)
    # Lê todos os arquivos CSV encontrados e concatena os dados em um único DataFrame

    graph_name = sys.argv[2]
    # Obtém o nome do arquivo de gráfico a ser criado a partir da linha de comando

    data[0] = data[0].str.rsplit(r".", n=1, expand=True)[1]
    # Processa os dados: divide os nomes dos métodos para manter apenas a parte "name"

    methods = np.unique(data[0])
    sum_variance_energy = 0
    sum_energy = 0
    mean_energies = []
    std_energies = []

    plt.figure()
    axes = plt.gca()
    # Inicializa o ambiente para criar o gráfico usando o matplotlib

    for method in methods:
        # Loop através dos métodos únicos encontrados nos dados
        sub_data_method = data[data[0].__eq__(method)]
        mean_energy = np.mean(sub_data_method[1])
        mean_energies.append(mean_energy)
        std_energies.append(np.std(sub_data_method[1]))

        sum_energy += mean_energy
        sum_variance_energy += np.var(sub_data_method[1])
        # Calcula a média e o desvio padrão das energias para cada método

    sorted_list = [(y,x,z) for x,y,z in sorted(zip(mean_energies, methods, std_energies))]
    methods = [x[0] for x in sorted_list]
    mean_energies = [x[1] for x in sorted_list]
    std_energies = [x[2] for x in sorted_list]
    # Ordena os métodos com base na média de energia em ordem crescente

    bars = axes.barh(methods, mean_energies, xerr = std_energies)
    axes.bar_label(bars, fmt='  %.2f', label_type='center')
    axes.bar_label(bars, labels=["    ± {0:.2f}".format(x) for x in std_energies] , label_type='edge')
    # Cria um gráfico de barras horizontais com médias de energia e barras de erro

    mean_total_consumption = str(round(sum_energy, 2))
    std_total_consumption = str(round(np.sqrt(sum_variance_energy), 2))

    at = AnchoredText(
        "Total = " + mean_total_consumption + " ± " + std_total_consumption + " J", prop=dict(size=10), frameon=True, loc='center left',
        bbox_to_anchor=(0., 1.),
        bbox_transform=axes.transAxes,
    )
    at.patch.set_boxstyle("round,pad=0.,rounding_size=0.2")
    axes.add_artist(at)
    # Adiciona um texto ancorado ao gráfico que mostra o consumo total de energia calculado

    if graph_name.count("/") == 3:
        axes.set_xlabel("Energy consumption for the " + graph_name.split("/")[2] + " (J)")
    else:
        axes.set_xlabel("Energy consumption (J)")
    # Define os rótulos do gráfico

    plt.grid(True)
    plt.savefig(graph_name, bbox_inches='tight')
    # Salva o gráfico como um arquivo

    print("Graph created at " + graph_name)

