# Previsão da Qualidade da Casca de Ovos

## Sobre o Projeto 
Este repositório explora o uso de aprendizado profundo para prever a qualidade de cascas de ovos a partir de nuvens de pontos derivadas de capturas de profundidade. Utilizando arquiteturas como PointNet++, DGCNN e técnicas de normalização e data augmentation, o objetivo é desenvolver técnicas de VC para determinar propriedades de cascas de ovos a partir de nuvens de pontos.

## Etapas do Projeto

### 1. Coleta de Dados
Os dados foram capturados usando dispositivos de profundidade que geram arquivos no formato `.bag`. Cada arquivo representa informações tridimensionais dos ovos, que foram convertidas em nuvens de pontos.

### 2. Processamento dos Dados

#### [Transformação](src/process_bag.py)
O processamento dos arquivos `.bag` inclui a leitura e conversão dos dados em imagens de profundidade e, posteriormente, em nuvens de pontos tridimensionais. Um exemplo prático deste processo está descrito no código principal. A transformação segue as etapas:

1. **Leitura do Arquivo de Profundidade:** O arquivo de entrada é lido usando a biblioteca `pyrealsense2`, que permite acessar os quadros de profundidade.
2. **Extração de Informações por Pixel:** Para cada pixel na imagem de profundidade, o valor de distância é obtido e limitado a um intervalo máximo de 3 metros para evitar ruídos.
3. **Conversão para Nuvem de Pontos:** Os dados de profundidade são normalizados, convertidos para milímetros e transformados em uma nuvem de pontos usando a biblioteca `open3d`.
4. **Segmentação de Planos:** Utilizando RANSAC, o pano de fundo é removido da nuvem de pontos, deixando apenas os pontos de interesse, nesse caso, os ovos

Exemplo de nuvem pós transformação



--
#### [Normalização](src/process_bag.py)


### 3. Modelagem
Arquiteturas como PointNet++ foram utilizadas para treinar modelos capazes de prever as métricas de qualidade com base nas nuvens de pontos processadas.

### 4. Avaliação e Ajustes
As métricas MAE, MSE e R² foram empregadas para avaliar os modelos, e ajustes nos dados e funções de perda foram realizados para mitigar problemas de overfitting e vieses.

## Tecnologias Utilizadas

- **Linguagem de Programação:** Python
- **Processamento de Nuvens de Pontos:** Open3D
- **Visualização e Manipulação de Dados:** NumPy, OpenCV
- **Modelagem:** PyTorch, TensorFlow
- **Gerenciamento de Dados:** pyrealsense2

## Referências

- **PointNet++:** Qi, C. R., Yi, L., Su, H., & Guibas, L. J. (2017). PointNet++: Deep Hierarchical Feature Learning on Point Sets in a Metric Space.
- **Data Augmentation:** Chawla, N. V., et al. (2002). SMOTE: Synthetic Minority Over-sampling Technique.

## Como Executar

1. Clone o repositório:
   ```bash
   git clone <URL>
   ```
2. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```
3. Execute o script principal para processar os arquivos `.bag`:
   ```bash
   python process_bag.py --input <path_to_bag_file>
   ```
