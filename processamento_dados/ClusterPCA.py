
# First import library
import pyrealsense2 as rs
# Import Numpy for easy array manipulation
import numpy as np
# Import os.path for file path manipulation
import os.path

import matplotlib.pyplot as plt

import open3d as o3d

from sympy import python

# ler nuvem de pontos
point_cloud = o3d.io.read_point_cloud("C:/Users/mhmon/ovos-pv/sem_pano/14.ply")
# o3d.visualization.draw_geometries([point_cloud])
inicial = 996



# formação dos clusters
with o3d.utility.VerbosityContextManager(
        o3d.utility.VerbosityLevel.Debug) as cm:
    labels = np.array(
        point_cloud.cluster_dbscan(eps=0.01, min_points=10, print_progress=True))

# quantidade de clusters
max_label = labels.max()
print(f"point cloud has {max_label + 1} clusters")

# Obter a quantidade de pontos por cluster
cluster_sizes = [np.sum(labels == i) for i in range(max_label + 1)]
print(cluster_sizes)

# filtrar nuvem de pontos por tamanho do cluster
# min_cluster_size = 1100
# max_cluster_size = 5200
min_cluster_size = 3000
max_cluster_size = 9100
filtered_clusters = [i for i in range(max_label + 1) if cluster_sizes[i] > min_cluster_size and cluster_sizes[i] < max_cluster_size]

# armazena valores que estao presentes ao mesmo tempo em labels e filtered_clusters
filtered_points = np.isin(labels, filtered_clusters)
# gera nuvem de pontos 
filtered_pcd = point_cloud.select_by_index(np.where(filtered_points)[0])

#obter labels que restaram após filtragem
filtered_labels = labels[filtered_points]  
max_filtered_label = filtered_labels.max()

# Obter a quantidade de pontos por cluster

new_cluster_sizes = [np.sum(filtered_labels == i) for i in range(max_filtered_label + 1)]
print(new_cluster_sizes)
print(f"point cloud has {max_filtered_label + 1} clusters")


# # Usar um mapa de cores para os clusters filtrados
colors = plt.get_cmap("tab20")(filtered_labels / (max_filtered_label if max_filtered_label > 0 else 1))
colors[filtered_labels <= 0] = 0  # Colore o ruído de preto (se houver)

# Atribuir as cores à nuvem de pontos filtrada
filtered_pcd.colors = o3d.utility.Vector3dVector(colors[:, :3])


# Visualizar a nuvem de pontos filtrada sem o ruído
o3d.visualization.draw_geometries([filtered_pcd])

# separar os labels de cada cluster (ovo)
unique_labels = np.unique(filtered_labels)





from sklearn.decomposition import PCA

# Função para calcular a excentricidade do cluster usando PCA
def calcular_excentricidade(pcd):
    pontos = np.asarray(pcd.points)
    pca = PCA(n_components=3)
    pca.fit(pontos)
    # Excentricidade é a razão entre os comprimentos do maior e menor eixo
    excentricidade = pca.explained_variance_ratio_[0] / pca.explained_variance_ratio_[-1]
    return excentricidade

# Filtrar clusters com base na excentricidade
new_filtered_clusters = []
limite_excentricidade =  16 # ajustável conforme os testes

for label in unique_labels:
    if label < 0:
        continue
    cluster_indices = np.where(filtered_labels == label)[0]
    cluster_pcd = filtered_pcd.select_by_index(cluster_indices)
    
    # Calcular excentricidade
    excentricidade = calcular_excentricidade(cluster_pcd)
    print(excentricidade)
    
    # Clusters com excentricidade baixa são mantidos
    if excentricidade < limite_excentricidade:
        new_filtered_clusters.append(label)

# Visualizar os clusters filtrados

#valor do primeiro ovo da bandeija
cont = 0
nome = inicial
if new_filtered_clusters.__len__() == 15:
    for label in new_filtered_clusters:
        cont+=1
        cluster_indices = np.where(filtered_labels == label)[0]
        cluster_pcd = filtered_pcd.select_by_index(cluster_indices)
        # o3d.visualization.draw_geometries([cluster_pcd])
        o3d.io.write_point_cloud(f"C:/Users/mhmon/ovos-pv/ovonovo/ovo{nome}.ply" , cluster_pcd)
        print(nome)
        # if cont ==2 or cont ==6 or cont ==11:
        #     nome = nome + 4

        if cont % 5 != 0:
            nome = nome + 3
        else: 
            nome = inicial + 1
            inicial +=1
            
elif new_filtered_clusters.__len__() == 5:
    for label in new_filtered_clusters:
        cont+=1
        cluster_indices = np.where(filtered_labels == label)[0]
        cluster_pcd = filtered_pcd.select_by_index(cluster_indices)
        o3d.visualization.draw_geometries([cluster_pcd])
        
        o3d.io.write_point_cloud(f"C:/Users/mhmon/ovos-pv/ovonovo/ovo{nome}.ply", cluster_pcd)
        print(nome)
        if cont % 2 != 0: nome = nome + 3
        else: 
            nome = inicial + 1
            inicial += 1
    
else: 
    print(new_filtered_clusters.__len__())
    for label in new_filtered_clusters:
        cluster_indices = np.where(filtered_labels == label)[0]
        cluster_pcd = filtered_pcd.select_by_index(cluster_indices)
        o3d.visualization.draw_geometries([cluster_pcd])
        
    
