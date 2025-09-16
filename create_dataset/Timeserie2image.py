import re
import pandas as pd
import numpy as np
from colorama import Fore, Style
from pandas.tseries import offsets
from pandas.tseries.frequencies import to_offset
import os
from statsmodels.tsa.seasonal import STL

class TimeSeriesImageConverter:
    def __init__(self, df, shape=(32, 32), image_dim=1,taxa=0.1, input=False):
        self.df = df
        self.shape = shape
        self.image_dim = image_dim
        self.RED = Fore.RED
        self.RESET = Style.RESET_ALL
        self.taxa = taxa
        self.get_freq()
        self.input = input
     
        

    def print_error(self, message):
        print(self.RED + 'Erro: ' + message + self.RESET)

    @property
    def findSampleFreq(self):
        diferencas = self.df.index.to_series().diff()
        freq = diferencas.mode()[0]
        if not isinstance(freq, offsets.DateOffset):
            freq = to_offset(freq)
        return freq.rule_code.upper()

    def get_freq(self):
        try:
            if self.df[~self.df.index.duplicated(keep='first')].shape[0] < self.df.shape[0]:
                self.print_error('A série possui Datetime duplicado')
            inferred_freq = pd.infer_freq(self.df.index)
            if inferred_freq is None:
                freq_ = self.findSampleFreq
                freq_ = self.get_nearest_standard_freq(freq_)
                date_rng = pd.date_range(start=self.df.index[0], periods=self.df.shape[0], freq=freq_)
                self.df = pd.DataFrame(self.df.values, index=date_rng)
                inferred_freq = pd.infer_freq(self.df.index)
                
            n , letra = self.separate_l_n(inferred_freq) 
            if letra in ['N', 'U', 'L', 'S', 'T', 'min','MIN']:#caso a frequencia não seja aceita pelo stl reamostrar index
                freq_ = self.findSampleFreq
                freq_ = self.get_nearest_standard_freq(freq_)
                date_rng = pd.date_range(start=self.df.index[0], periods=self.df.shape[0], freq=freq_)
                self.df = pd.DataFrame(self.df.values, index=date_rng)
            
            return inferred_freq
        except Exception as e:
            self.print_error('Erro ao determinar frequência temporal: ' + str(e))
            self.print_error('Frequência média encontrada: ' + str(self.df.index.to_series().diff().mean()))

    def separate_l_n(self, string):
        letters = re.findall(r'[a-zA-Z]+', string)
        numbers = re.findall(r'\d+', string)
        try:
            return int(numbers[0]), letters[0]
        except:
            return 0, letters[0]
        
    
    
    def get_nearest_standard_freq(self, freq):
        if freq in ("A", "Y") or freq.startswith(("A-", "AS-", "Y-", "YS-", "YE-")):
            return 'A'
        elif freq == "Q" or freq.startswith(("Q-", "QS", "QE")):
            return 'Q'
        elif freq == "M" or freq.startswith(("M-", "MS", "ME")):
            return 'M'
        elif freq == "W" or freq.startswith("W-"):
            return 'W'
        elif freq == "D":
            return 'D'
        elif freq == "B":
            return 'B'
        elif freq == "H" or freq == "h":
            return 'h'
        elif freq == "T" or freq.startswith("min") or freq == "MIN" :
            return 'h'
        elif freq == "S":
            return 'h'
        else:
            raise ValueError(f"Error: Frequência {freq} desconhecida")

    def get_components(self):
        freq = pd.infer_freq(self.df.index)
        seasonal_period = 13
        if 'D' in freq:
            seasonal_period = 7  # Sazonalidade semanal para dados diários
        stl = STL(self.df, seasonal=seasonal_period)
        res = stl.fit()
        return pd.concat([res.trend, res.seasonal, res.resid], axis=1)

    @property
    def ts_delta(self):
        try:
            aliases_convert = {'H': 24, 'h': 24,'D': 30, 'W': 7, 'M': 12, 'MS': 12, 'Q': 4, 'B': 2,
                               'Y': 1, 'YS': 1, "A-": 1, "AS-": 1, "Y-": 1, "YS-": 1, "YE-": 1}
            n, freq = self.separate_l_n(pd.infer_freq(self.df.index))
            if freq in aliases_convert:
                return aliases_convert[freq] // n if n > 0 else aliases_convert[freq]
        except:
            self.print_error('Frequência {} desconhecida'.format(self.get_freq()))

    def inserir_dados_faltantes(self):
        n_faltantes = int(self.taxa * self.df.shape[0])  # Número de dados faltantes
        indices_faltantes = np.random.choice(self.df.shape[0], n_faltantes, replace=False)  # Escolhe os índices faltantes
        
        # Inserir NaN nos dados faltantes
        self.df.iloc[indices_faltantes, :] = np.nan

        # Preenche NaNs com a média de cada coluna
        self.df = self.df.apply(lambda col: col.fillna(col.mean()), axis=0)

        # Criando um vetor one-hot de tamanho igual ao número de linhas do DataFrame
        one_hot_vector = np.zeros(self.df.shape[0])
        one_hot_vector[indices_faltantes] = 1  # Marca os índices faltantes como 1
        
        return one_hot_vector  # Retorna o vetor one-hot dos dados faltantes
    
    # @property
    # def get_windows(self):
        
    #     indices =None
    #     if self.input:
    #         indices = self.inserir_dados_faltantes()
    #     new_data = self.get_components()
        
    #     try:
    #         lista_values = []
    #         lista_indices = []
    #         ds  = self.ts_delta
    #         if (self.shape[1] % ds) != 0:  new_window = (self.shape[1]//ds)*ds +ds
    #         if (self.shape[1] % ds) == 0:  new_window = self.shape[1]
            
    #         if new_data.shape[0]//new_window < (new_data.shape[0]-(new_window -self.shape[1]))//self.shape[1]:
    #             new_data = new_data.iloc[new_window -self.shape[1]:,:]
    #             self.df = new_data
    #             new_window = self.shape[1]

    #             if self.input:
    #                indices = indices[new_window -self.shape[1]:]
           
    #         temp = []  # Inicializa temp aqui fora do loop
    #         temp2 = []
    #         for i in range(0, new_data.__len__(), new_window):
    #             # Adiciona a sublista à lista de valores se tiver o tamanho correto
    #             temp.append(new_data.iloc[i:i+new_window,:].iloc[:self.shape[1],:].to_numpy())
    #             if self.input :
    #                 temp2.append(indices[i:i+new_window,:])

    #             if len(temp) == self.shape[0]:
                 
    #                 lista_values.append(temp)
    #                 lista_indices.append(np.concatenate(temp2))
    #                 temp = []  # Reinicia temp para uma nova sublista  
    #                 temp2 = []
            
    #         return lista_values, indices
        
    #     except Exception as e:
    #         self.print_error('Error: ' + str(e) + ' in get_window')

    @property
    def get_windows(self):
        indices = []
        if self.input:
            indices = self.inserir_dados_faltantes()  # Indices originais dos dados faltantes
            

        new_data = self.get_components()  # Obter os dados processados

        try:
            lista_values = []  # Lista para armazenar as imagens processadas
            lista_indices = []  # Lista para armazenar os índices dos dados faltantes

            ds = self.ts_delta  # Frequência dos dados
            if (self.shape[1] % ds) != 0:
                new_window = (self.shape[1] // ds) * ds + ds
            if (self.shape[1] % ds) == 0:
                new_window = self.shape[1]

            # Verifica se é necessário fazer o corte (ajuste dos dados)
            if new_data.shape[0] // new_window < (new_data.shape[0] - (new_window - self.shape[1])) // self.shape[1]:
                # Armazenar o comprimento original de new_data
                original_len = new_data.shape[0]
                
                # Faz o corte de new_data
                new_data = new_data.iloc[new_window - self.shape[1]:, :]
                self.df = new_data  # Atualiza o dataframe com o corte
                new_window = self.shape[1]
                

                if self.input:
                   indices = indices[new_window - self.shape[1]:]

            temp = []  # Inicializa a lista para armazenar as imagens por janela
            temp2 = []  # Para armazenar os índices dos dados faltantes por janela

            # Agora, percorre os dados em janelas
            for i in range(0, new_data.__len__(), new_window):
                # Cria a janela de dados
                temp.append(new_data.iloc[i:i + new_window, :].iloc[:self.shape[1], :].to_numpy())

                if self.input:
                    # Para cada janela, ajusta os índices (se existirem)
                    temp2.append(indices[i:i + new_window])

                # Quando a janela está completa, armazena os resultados
                if len(temp) == self.shape[0]:
                    lista_values.append(temp)
                    if self.input:
                        lista_indices.append(np.concatenate(temp2))  # Concatena os índices de dados faltantes dentro da janela
                        if np.concatenate(temp2).shape[0]<0:
                            print(f'Erro {indices.shape}{np.concatenate(temp2).shape}')
                    temp = []  # Reinicia a lista de imagens
                    temp2 = []  # Reinicia a lista de índices
            
            return lista_values, lista_indices  # Retorna as imagens e seus índices de dados faltantes

        except Exception as e:
            self.print_error('Error: ' + str(e) + ' in get_window')


    def image_construct(self, im):
        image = [ ]
        temp = []
        for c1 in im:
            for c2 in c1:
                temp.append(c2.reshape(1, 3))
            if len(temp) ==32:
                image.append(temp)
                temp = []
        image= np.stack(image, axis=0)
        # image = np.squeeze(image, axis=2)
        return image
    
    @property
    def get_images(self):
        pre_image, indeces = self.get_windows
        imagens = []
        for i in pre_image:
            imagens.append(self.image_construct(i))

        if len(indeces)==0:
            indeces = [ [] for _ in range(len(imagens))]

        return imagens, indeces

       