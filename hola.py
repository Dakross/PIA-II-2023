import pandas as pd
import matplotlib.pyplot as plt
from FEgeneral import migeneral, red_social
from flask import Flask, render_template, request, send_file
from graph import grafico_frecuencia, grafico_puntaje, wordcloud
from glosario import glosario_general,glosario_capital_emocional,glosario_capital_social,glosario_auto_regulacion,glosario_auto_reconocimiento,glosario_reconocimiento,glosario_regulacion_social

pd.options.mode.chained_assignment = None  # default='warn'

# Especifica la ruta de matriz peso y dataset
ruta_matriz_peso = 'Matriz_Pesos.xlsx'
ruta_dataset = 'dataset.csv'

# Lee el archivo Excel desde la fila 4 como encabezado y datos
matriz_peso = pd.read_excel(ruta_matriz_peso, header=4, index_col=0, usecols=range(20))

# Reemplaza NaN con 0 en las columnas del 1 al 18
matriz_peso.iloc[:, 1:19] = matriz_peso.iloc[:, 1:19].fillna(0)

# Lee solo la columna 'Concepto'
concepto = pd.read_csv(ruta_dataset, usecols=['Concepto_asociado'])

# Obtiene el top 10 de los valores más frecuentes en la columna 'Concepto'
top_conceptos = concepto['Concepto_asociado'].str.lower().value_counts()

nombres_columnas = 'Polaridades,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18'.split(',')
matriz_peso.columns = nombres_columnas

# Asigna el valor de apariciones de top_conceptos a matriz_peso como una nueva columna
matriz_peso['Apariciones'] = matriz_peso['Polaridades'].str.lower().map(lambda x: top_conceptos[x] if x in top_conceptos.index else 0)

# Resetea el índice y renumera de 1 a 281
matriz_peso = matriz_peso.reset_index(drop=True)
matriz_peso.index = matriz_peso.index + 1

df_threads = red_social(matriz_peso.copy(),'Threads')
df_twitter = red_social(matriz_peso.copy(),'Twitter')
df_reddit = red_social(matriz_peso.copy(),'Reddit')

# División del DataFrame
#Capital emocional
capital_emocional = matriz_peso[['Polaridades','1', '2', '3','4', '5', '6', '7', 'Apariciones']]
auto_reconocimiento = matriz_peso[['Polaridades','1', '2', '3', 'Apariciones']]
auto_regulacion = matriz_peso[['Polaridades','4', '5', '6', '7', 'Apariciones']]

#Capital social
capital_social = matriz_peso[['Polaridades','8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', 'Apariciones']]
reconocimiento = matriz_peso[['Polaridades','8', '9', '10', '11','Apariciones']]
regulacion_social= matriz_peso[['Polaridades','12', '13', '14', '15', '16', '17', '18', 'Apariciones']]

grafico_frecuencia(capital_emocional, 'static/grafico_capital_emocional.png')
grafico_frecuencia(auto_reconocimiento, 'static/grafico_auto_reconocimiento.png')
grafico_frecuencia(auto_regulacion, 'static/grafico_auto_regulacion.png')
grafico_frecuencia(capital_social, 'static/grafico_capital_social.png')
grafico_frecuencia(reconocimiento, 'static/grafico_reconocimiento.png')
grafico_frecuencia(regulacion_social, 'static/grafico_regulacion_social.png')

# Calcula la Ponderación (suma de todos los % de la fila) para las columnas del 1 al 7
#Capital emocional
capital_emocional['Ponderación'] = capital_emocional['1']+capital_emocional['2']+capital_emocional['3']+capital_emocional['4']+capital_emocional['5']+capital_emocional['6']+capital_emocional['7']
auto_reconocimiento['Ponderación'] = auto_reconocimiento['1']+auto_reconocimiento['2']+auto_reconocimiento['3']
auto_regulacion['Ponderación'] = auto_regulacion['4']+auto_regulacion['5']+auto_regulacion['6']+auto_regulacion['7']

# Convierte los valores de la columna '14' a numéricos
capital_social['14'] = pd.to_numeric(capital_social['14'], errors='coerce')

#Capital social
capital_social['Ponderación'] = capital_social['8']+capital_social['9']+capital_social['10']+capital_social['11']+capital_social['12']+capital_social['13']+capital_social['14']+capital_social['15']+capital_social['16']+capital_social['17']+capital_social['18']
reconocimiento['Ponderación'] = reconocimiento['8']+reconocimiento['9']+reconocimiento['10']+reconocimiento['11']
regulacion_social['Ponderación'] = regulacion_social['12']+regulacion_social['13']+regulacion_social['14']+regulacion_social['15']+regulacion_social['16']+regulacion_social['17']+regulacion_social['18']

# Calcula el Puntaje (ponderación * apariciones)
#Capital emocional
capital_emocional['Puntaje'] = capital_emocional['Ponderación'] * capital_emocional['Apariciones']
auto_reconocimiento['Puntaje'] = auto_reconocimiento['Ponderación'] * auto_reconocimiento['Apariciones']
auto_regulacion['Puntaje'] = auto_regulacion['Ponderación'] * auto_regulacion['Apariciones']

#Capital social
capital_social['Puntaje'] = capital_social['Ponderación'] * capital_social['Apariciones']
reconocimiento['Puntaje'] = reconocimiento['Ponderación'] * reconocimiento['Apariciones']
regulacion_social['Puntaje'] = regulacion_social['Ponderación'] * regulacion_social['Apariciones']


grafico_puntaje(capital_emocional, 'static/grafico_puntaje_capital_emocional.png')
grafico_puntaje(auto_reconocimiento, 'static/grafico_puntaje_auto_reconocimiento.png')
grafico_puntaje(auto_regulacion, 'static/grafico_puntaje_auto_regulacion.png')
grafico_puntaje(capital_social, 'static/grafico_puntaje_capital_social.png')
grafico_puntaje(reconocimiento, 'static/grafico_puntaje_reconocimiento.png')
grafico_puntaje(regulacion_social, 'static/grafico_puntaje_regulacion_social.png')

# Ordena el DataFrame por la columna 'Puntaje' de forma descendente
#Capital emocional
capital_emocional = capital_emocional.sort_values(by='Puntaje', ascending=False)
auto_reconocimiento = auto_reconocimiento.sort_values(by='Puntaje', ascending=False)
auto_regulacion = auto_regulacion.sort_values(by='Puntaje', ascending=False)

#Capital social
capital_social = capital_social.sort_values(by='Puntaje', ascending=False)
reconocimiento = reconocimiento.sort_values(by='Puntaje', ascending=False)
regulacion_social = regulacion_social.sort_values(by='Puntaje', ascending=False)

# Top 10 capital emocional y social
#Capital emocional
top_10_capital_emocional = capital_emocional.head(10)
top_10_auto_reconocimiento = auto_reconocimiento.head(10)
top_10_auto_regulacion = auto_regulacion.head(10)

#Capital social
top_10_capital_social = capital_social.head(10)
top_10_reconocimiento = reconocimiento.head(10)
top_10_regulacion_social = regulacion_social.head(10)

matriz_general = migeneral(matriz_peso.copy())
top_10_matriz_general = matriz_general.head(10)

wordcloud_matriz_general = wordcloud(matriz_general, 'wordcloud_matriz_general.png')
wordcloud_df_threads = wordcloud(df_threads, 'wordcloud_df_threads.png')
wordcloud_twitter = wordcloud(df_twitter, 'wordcloud_twitter.png')
wordcloud_reddit = wordcloud(df_reddit, 'wordcloud_reddit.png')


def index():
    return render_template('base.html',
                            glosario_general=glosario_general,
                            glosario_capital_emocional=glosario_capital_emocional,
                            glosario_auto_reconocimiento=glosario_auto_reconocimiento,
                            glosario_auto_regulacion=glosario_auto_regulacion,
                            glosario_capital_social=glosario_capital_social,
                            glosario_reconocimiento=glosario_reconocimiento,
                            glosario_regulacion_social=glosario_regulacion_social,

                            matriz_general= [matriz_general.to_html(classes='data', header='true')],
                            top_10_matriz_general = [top_10_matriz_general.to_html(classes='', header='true')],
                            
                            df_threads=[df_threads.to_html(classes='data', header='true')],
                            df_twitter=[df_twitter.to_html(classes='data', header='true')],
                            df_reddit=[df_reddit.to_html(classes='data', header='true')],

                            capital_emocional=[top_10_capital_emocional.to_html(classes='data', header="true")],
                            auto_reconocimiento=[top_10_auto_reconocimiento.to_html(classes='data', header="true")],
                            auto_regulacion=[top_10_auto_regulacion.to_html(classes='data', header="true")],
                            capital_social=[top_10_capital_social.to_html(classes='data', header="true")],
                            reconocimiento=[top_10_reconocimiento.to_html(classes='data', header="true")],
                            regulacion_social=[top_10_regulacion_social.to_html(classes='data', header="true")],

                            grafico_matriz_general='static/grafico_matriz_general.png',
                            grafico_puntaje_matriz_general='static/grafico_puntaje_matriz_general.png',
                            grafico_capital_emocional='static/grafico_capital_emocional.png',
                            grafico_auto_reconocimiento='static/grafico_auto_reconocimiento.png',
                            grafico_auto_regulacion='static/grafico_auto_regulacion.png',
                            grafico_capital_social='static/grafico_capital_social.png',
                            grafico_reconocimiento='static/grafico_reconocimiento.png',
                            grafico_regulacion_social='static/grafico_regulacion_social.png',
                            grafico_puntaje_capital_emocional='static/grafico_puntaje_capital_emocional.png',
                            grafico_puntaje_auto_reconocimiento='static/grafico_puntaje_auto_reconocimiento.png',
                            grafico_puntaje_auto_regulacion='static/grafico_puntaje_auto_regulacion.png',
                            grafico_puntaje_capital_social='static/grafico_puntaje_capital_social.png',
                            grafico_puntaje_reconocimiento='static/grafico_puntaje_reconocimiento.png',
                            grafico_puntaje_regulacion_social='static/grafico_puntaje_regulacion_social.png',
                            
                            wordcloud_matriz_general='static/wordcloud_matriz_general.png',
                            wordcloud_df_threads='static/wordcloud_df_threads.png',
                            wordcloud_df_twitter='static/wordcloud_twitter.png',
                            wordcloud_df_reddit='static/wordcloud_reddit.png'
                            )
