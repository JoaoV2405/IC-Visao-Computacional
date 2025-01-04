# Previsão da Qualidade da Casca de Ovos

## Sobre o Projeto 
Este repositório explora o uso de aprendizado profundo para prever a qualidade de cascas de ovos a partir de nuvens de pontos derivadas de capturas de profundidade. Utilizando arquiteturas como PointNet++, DGCNN e técnicas de normalização e data augmentation, o objetivo é desenvolver técnicas de VC para determinar propriedades de cascas de ovos a partir de nuvens de pontos.

## Etapas do Projeto

### 1. Coleta de Dados
Os dados foram capturados usando dispositivos de profundidade que geram arquivos no formato `.bag`. Cada arquivo representa informações tridimensionais dos ovos, que foram convertidas em nuvens de pontos.

Exemplo de nuvem de pontos:

<img src="https://github.com/user-attachments/assets/d060310c-14b2-41be-b2f3-db0a74128b66" width="400">


### 2. Processamento dos Dados

#### [Transformação](src/process_bag.py)
O processamento dos arquivos `.bag` inclui a leitura e conversão dos dados em imagens de profundidade e, posteriormente, em nuvens de pontos tridimensionais. Um exemplo prático deste processo está descrito no código principal. A transformação segue as etapas:

1. **Leitura do Arquivo de Profundidade:** O arquivo de entrada é lido usando a biblioteca `pyrealsense2`, que permite acessar os quadros de profundidade.
2. **Extração de Informações por Pixel:** Para cada pixel na imagem de profundidade, o valor de distância é obtido e limitado a um intervalo máximo de 3 metros para evitar ruídos.
3. **Conversão para Nuvem de Pontos:** Os dados de profundidade são normalizados, convertidos para milímetros e transformados em uma nuvem de pontos usando a biblioteca `open3d`.
4. **Segmentação de Planos:** Utilizando RANSAC, o pano de fundo é removido da nuvem de pontos, deixando apenas os pontos de interesse, nesse caso, os ovos

Exemplo de nuvem após transformação

<img src="https://github.com/user-attachments/assets/7fa551fb-7a81-4e5e-a080-1c6fc0ee22ba" width="400">

#### Filtragem e Armazenamento
Como a etapa de transfomação resulta em uma nuvem de pontos composta de resíduos, foi necessário aplicar uma etapa de filtragem para remover pontos indesejados. Para isso, primeiramente os pontos são agrupados em clusters baseados na densidade espacial utilizando a técnica DBSCAN, assim, cada cluster pode representar um ovo ou um ruído.

Após a formação de clusters, é realizada uma filtragem inicial eliminando clusters com base na sua quantidade de pontos, assim, caso o cluster seja maior ou menor que o limite de um intervalo pré-definido, ele é eliminado da nuvem de pontos geral.
Caso o número de clusters seja maior ou menor do que a quantidade desejada, é realizada outra filtragem. Utilizando o algoritmo PCA (Principal Component Analysis) é calculada a excentricidade de cada cluster. Clusters com formas mais uniformes, como ovos, geralmente têm uma excentricidade baixa, enquanto resíduos têm uma excentricidade significativamente maior.


Separação e Exportação dos Clusters:
Os clusters finais, após todas as etapas de filtragem, são salvos em arquivos .ply separados e nomeados de acordo com catálogos pré-estabelecidos.

Exemplo de nuvem de pontos após clusterização:

<img src="https://github.com/user-attachments/assets/9754e84e-0eb6-4ef4-8e02-d7d496bc7210" width="400">



### 3. Modelagem
Arquiteturas como PointNet++ e DGCNN foram utilizadas para treinar modelos capazes de prever as métricas de qualidade com base nas nuvens de pontos processadas. O código carrega nuvens de pontos em formato .ply e realiza a normalização para centralizar os dados na origem e escalá-los para uma esfera unitária. Essas operações garantem que todas as nuvens sejam tratadas de maneira uniforme, independentemente de suas dimensões ou localização original. 
Tanto as normalizações quanto processamento dos dados de entrada são feitas na classe de dataset customizada chamada Eggshell Dataset, ela vincula cada nuvem de pontos às suas respectivas medições armazenadas em arquivos CSV, os itens retornados são da classe Data do pytorch, cada um contendo os atributos 'pos' (coordenadas dos pontos) e y (métricas associadas).



### 4. Avaliação e Ajustes
As métricas MAE, MSE e R² foram empregadas para avaliar os modelos, normalizações nos dados e funções de perda foram realizados para mitigar problemas de overfitting e vieses. Além disso, gráficos de dispersão e histogramas de erro são plotados para melhor analisar o comportamento dos dados previstos.

### 5. Etapa atual
Foi observado um problema de overfitting em ambas arquiteturas de rede neural, ajustes em funções de perda e normalizações não resultaram em melhoras significativas. Está sendo estudado o desempenho dos modelos na previsão de um target ao invés de múltiplos. Além disso, os dados fornecidos para o estudo apresentam um certo desbalanceamento, o que pode estar causando esse vício nas previões, para mitigar esse problema, estão sendo estudados métodos de Data Augmentation.

## Tecnologias Utilizadas

- **Linguagem de Programação:** Python
- **Processamento de Nuvens de Pontos:** Open3D
- **Visualização e Manipulação de Dados:** NumPy, OpenCV, Matplotlib, Pandas, Scikit-Learn
- **Modelagem:** PyTorch, TensorFlow

## Referências

-  Qi, C. R., Yi, L., Su, H., & Guibas, L. J. (2017). PointNet++: Deep Hierarchical Feature Learning on Point Sets in a Metric Space.
-  Phan, A. V., Nguyen, M. L., Nguyen, Y., & Bui, L. (2018). DGCNN: A convolutional neural network over large-scale labeled graphs. Neural Networks
-  Chawla, N. V., et al. (2002). SMOTE: Synthetic Minority Over-sampling Technique.
-  Srivastava, N., Hinton, G., Krizhevsky, A., Sutskever, I., & Salakhutdinov, R. (2014). Dropout: A Simple Way to Prevent Neural Networks from Overfitting.

