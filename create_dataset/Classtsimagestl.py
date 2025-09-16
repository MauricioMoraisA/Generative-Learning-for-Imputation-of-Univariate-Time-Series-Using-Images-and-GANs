# import sys 
# sys.path.append(r'C:\Users\USER\Documents\UCRLD2014')
# from Timeserie2image import TimeSeriesImageConverter
# #%%
# import pandas as pd
# import numpy as np
# import os 
# from glob import glob


# def replace_severe_outliers_with_mean(df, severe_multiplier=2.5, regular_multiplier=1.5):
#     """
#     Identifica outliers severos e regulares em cada coluna de um DataFrame utilizando o intervalo interquartílico (IQR)
#     e substitui os outliers severos pela média da coluna.

#     :param df: DataFrame pandas onde os outliers serão identificados e substituídos.
#     :param severe_multiplier: Multiplicador para identificar outliers severos (default é 4.0).
#     :param regular_multiplier: Multiplicador para identificar outliers regulares (default é 2.9).
#     :return: DataFrame com outliers severos substituídos pela média.
#     """
    
#     df_cleaned = df.copy()  # Cria uma cópia do DataFrame para não modificar o original
    
#     for column in df.columns:
#         if pd.api.types.is_numeric_dtype(df[column]):  # Verifica se a coluna é numérica
#             # Calcula Q1 (1º quartil), Q3 (3º quartil) e IQR
#             Q1 = df[column].quantile(0.25)
#             Q3 = df[column].quantile(0.75)
#             IQR = Q3 - Q1

#             # Define os limites para identificar outliers regulares e severos
#             lower_bound_regular = Q1 - regular_multiplier * IQR
#             upper_bound_regular = Q3 + regular_multiplier * IQR
#             lower_bound_severe = Q1 - severe_multiplier * IQR
#             upper_bound_severe = Q3 + severe_multiplier * IQR

#             # Identifica outliers regulares e severos
#             severe_outliers = (df[column] < lower_bound_severe) | (df[column] > upper_bound_severe)
            
#             # Substitui os outliers severos pela média da coluna
#             mean_value = df[column].mean()
#             df_cleaned.loc[severe_outliers, column] = mean_value

#     return df_cleaned

# def inserir_dados_faltantes(df, taxa_faltantes):
#     """
#     Insere uma taxa específica de valores faltosos (NaN) em uma coluna de um DataFrame.
    
#     Args:
#     df (pandas.DataFrame): O DataFrame que contém os dados.
#     coluna (str): O nome da coluna onde os NaN devem ser inseridos.
#     taxa_faltantes (float): A taxa de dados faltosos a ser inserida (valor entre 0 e 1).
    
#     Returns:
#     pandas.DataFrame: O DataFrame com os dados faltosos inseridos.
#     """
    
#     # Determinar o número de valores a serem substituídos por NaN
#     n_faltantes = int(taxa_faltantes * df.shape[0])
    
#     # Selecionar índices aleatórios para inserir NaN
#     indices_faltantes = np.random.choice(df.shape[0], n_faltantes, replace=False)
#     # Inserir NaN nos índices selecionados
#     df.iloc[indices_faltantes,:] = np.nan
    
#     return df ,indices_faltantes




# # Definir os parâmetros
# taxas_faltosos = [10, 20, 30,40]
# padrao = '*.csv'
# phat_base = 'C:/Users/USER/Documents/UCRLD2014/datasets/'

# bases= ['input', 'label']
# # Percorrer os subdiretórios em busca dos datasets
# for base in bases:
#     for root, dirs, files in os.walk(phat_base):
#         print(f'Explorando o diretório: {root}')
#         for dir in dirs:
#             phat = os.path.join(root, dir)
#             print(f'Processando o subdiretório: {phat}')
    
#             # Verificar e criar diretórios para cada taxa
#             for taxa in taxas_faltosos:
#                 path_image_taxa = os.path.join('C:/Users/USER/Documents/UCRLD2014/',base, str(taxa), dir)
#                 print(f'Diretório de destino: {path_image_taxa}')
    
#                 if not os.path.exists(path_image_taxa):
#                     os.makedirs(path_image_taxa)
#                     print(f'Diretório criado: {path_image_taxa}')
#                 else:
#                     print(f'Diretório já existe: {path_image_taxa}')
    
#                 # Percorrer os datasets
#                 lista = glob(f'{phat}/{padrao}')
#                 print(f'Arquivos encontrados: {lista}')
    
#                 for i in lista:
#                     print(f'Processando o arquivo: {i}')
                    
#                     df = pd.read_csv(i, index_col=0, parse_dates=True)
#                     # df= replace_severe_outliers_with_mean(df)
#                     if base == 'input':
#                         df, indices_faltantes = inserir_dados_faltantes(df, taxa/100)
#                         df.iloc[indices_faltantes,:] = np.nanmean(df.to_numpy())
#                     converter = TimeSeriesImageConverter(df, shape=(32, 32), image_dim=3)
#                     imagens = converter.get_images
#                     c = 0
    
#                     for image in imagens:
#                         if len(image) > 0:
#                             print(f'Gerando imagem {c} para o arquivo {i}')
#                             # Salvar a imagem concatenada
#                             save_path = os.path.join(path_image_taxa, os.path.basename(i).replace('.csv', f'_{c}.npy'))
#                             np.save(save_path,image)

                            

#                             print(f'Imagem salva em: {save_path}')
#                             c += 1
#                 print(f'Processamento do diretório {dir} concluído.')
                        


import sys 
sys.path.append(r'C:\Users\USER\Documents\UCRLD2014')
from Timeserie2image import TimeSeriesImageConverter
import pandas as pd
import numpy as np
import os 
from glob import glob

# def replace_severe_outliers_with_mean(df, severe_multiplier=2.5, regular_multiplier=1.5):
#     df_cleaned = df.copy()
    
#     for column in df.columns:
#         if pd.api.types.is_numeric_dtype(df[column]):  
#             Q1 = df[column].quantile(0.25)
#             Q3 = df[column].quantile(0.75)
#             IQR = Q3 - Q1

#             lower_bound_severe = Q1 - severe_multiplier * IQR
#             upper_bound_severe = Q3 + severe_multiplier * IQR

#             severe_outliers = (df[column] < lower_bound_severe) | (df[column] > upper_bound_severe)
            
#             mean_value = df[column].mean()
#             df_cleaned.loc[severe_outliers, column] = mean_value

#     return df_cleaned

# def inserir_dados_faltantes(df, taxa_faltantes):
#     n_faltantes = int(taxa_faltantes * df.shape[0])
#     indices_faltantes = np.random.choice(df.shape[0], n_faltantes, replace=False)

#     df.iloc[indices_faltantes, :] = np.nan
#     return df, indices_faltantes

# Definir os parâmetros



def replace_severe_outliers_with_mean_rolling(df, window_size=30, severe_multiplier=2.0):
    """
    Identifica outliers severos usando IQR em janelas deslizantes e substitui esses outliers pela média local da janela.
    
    :param df: DataFrame pandas (só colunas numéricas serão processadas)
    :param window_size: tamanho da janela deslizante (default=30)
    :param severe_multiplier: multiplicador do IQR para definir limites de outliers severos (default=2.5)
    :return: DataFrame limpo, com outliers severos substituídos
    """
    df_cleaned = df.copy()

    for column in df.columns:
        if pd.api.types.is_numeric_dtype(df[column]):
            series = df[column]
            cleaned_series = series.copy()

            for start in range(0, len(series), window_size):
                end = start + window_size
                window = series[start:end]

                if len(window) == 0:
                    continue

                Q1 = window.quantile(0.25)
                Q3 = window.quantile(0.75)
                IQR = Q3 - Q1

                lower_bound = Q1 - severe_multiplier * IQR
                upper_bound = Q3 + severe_multiplier * IQR

                mean_value = window.mean()

                # identifica índices de outliers severos na janela
                severe_outliers_idx = window[(window < lower_bound) | (window > upper_bound)].index

                # substitui por média local
                cleaned_series.loc[severe_outliers_idx] = mean_value

            df_cleaned[column] = cleaned_series

    return df_cleaned

taxas_faltosos = [10,20,30,40]
padrao = '*.csv'
phat_base = 'C:/Users/USER/Documents/UCRLD2014/datasets/'
bases = ['input', 'label']

# Processamento dos arquivos
for base in bases:
    for root, dirs, files in os.walk(phat_base):
        for dir in dirs:
            phat = os.path.join(root, dir)

            # Criar diretórios para imagens e índices
            for taxa in taxas_faltosos:
                path_image_taxa = os.path.join('C:/Users/USER/Documents/UCRLD2014/', base, str(taxa), dir)
                path_index_taxa = os.path.join('C:/Users/USER/Documents/UCRLD2014/', "index", str(taxa), dir)

                os.makedirs(path_image_taxa, exist_ok=True)
                os.makedirs(path_index_taxa, exist_ok=True)

                lista = glob(f'{phat}/{padrao}')
                for i in lista:
                    df = pd.read_csv(i, index_col=0, parse_dates=True)
                    df = replace_severe_outliers_with_mean_rolling(df)

                    # if base == 'input':
                    #     df, indices_faltantes = inserir_dados_faltantes(df, taxa/100)
                    #     df = df.apply(lambda col: col.fillna(col.mean()), axis=0)
                    if base == 'input':
                         converter = TimeSeriesImageConverter(df, shape=(32, 32), image_dim=3,taxa=taxa/100, input=True)
                    if not base == 'input':
                         converter = TimeSeriesImageConverter(df, shape=(32, 32), image_dim=3,taxa=taxa/100, input=False)
                    imagens, indices_faltantes = converter.get_images
                    c = 0

                    for image, indices in zip(imagens,indices_faltantes):
                        if len(image) > 0:
                            # Salvar a imagem com os 3 canais
                           
                            save_image_path = os.path.join(path_image_taxa, os.path.basename(i).replace('.csv', f'_{c}.npy'))
                            np.save(save_image_path, image)

                            # Salvar os índices dos valores faltantes
                            save_index_path = os.path.join(path_index_taxa, os.path.basename(i).replace('.csv', f'_{c}.npy'))
                        
                            if base == 'input':
                          
                                np.save(save_index_path, indices)

                            # print(f'Índices salvos em: {save_index_path}')
                            c += 1
            print(f'Processamento do diretório {dir} concluído.')