import pandas as pd
import matplotlib.pyplot as plt
from flask import Flask, render_template, request, send_file
from graph import grafico_frecuencia, grafico_puntaje

def migeneral(matriz_peso):
    print('hola mundo')

    matriz_peso['Ponderación'] = matriz_peso['1']+matriz_peso['2']+matriz_peso['3']+matriz_peso['4']+matriz_peso['5']+matriz_peso['6']+matriz_peso['7']+matriz_peso['8']+matriz_peso['9']+matriz_peso['10']+matriz_peso['11']+matriz_peso['12']+matriz_peso['13']+matriz_peso['14']+matriz_peso['15']+matriz_peso['16']+matriz_peso['17']+matriz_peso['18']
    matriz_peso['Puntaje'] = matriz_peso['Ponderación'] * matriz_peso['Apariciones']
    matriz_peso = matriz_peso.sort_values(by='Puntaje', ascending=False)

    grafico_frecuencia(matriz_peso, 'static/grafico_matriz_general.png')
    grafico_puntaje(matriz_peso, 'static/grafico_puntaje_matriz_general.png')

    return matriz_peso

def red_social(matriz_peso):
    ################### Threads #################################
    ## Cargar datos desde el archivo CSV
    ruta_csv = 'dataset.csv'
    df_csv = pd.read_csv(ruta_csv, usecols=['Red_Social'])

    # Combina las columnas de matriz_peso y df_csv
    df_threads = pd.concat([matriz_peso, df_csv], axis=1)
    
    # Filtra los datos solo para 'Threads'
    df_threads = df_threads[df_threads['Red_Social'] == 'Threads']

    # Resetea el índice y renumera de 1 a 281
    df_threads = df_threads.reset_index(drop=True)
    df_threads.index = df_threads.index + 1

    # Realiza la suma de columnas específicas
    df_threads['Ponderación'] = df_threads.iloc[:, 1:19].sum(axis=1)
    df_threads['Puntaje'] = df_threads['Ponderación'] * df_threads['Apariciones']
    
    # Ordena el DataFrame por 'Puntaje' de forma descendente
    df_threads = df_threads.sort_values(by='Puntaje', ascending=False)

    # Renombra la columna 'Red_Social' sin el guion bajo
    df_threads = df_threads.rename(columns={'Red_Social': 'Red Social'})

    return df_threads


    # ################### Twitter #################################
    # df_twitter = matriz_peso[matriz_peso['Red Social'] == 'twitter']
    # # Lee solo la columna 'Concepto'
    # concepto_twitter = pd.read_csv(df_twitter, usecols=['Concepto_asociado'])

    # # Obtiene el top 10 de los valores más frecuentes en la columna 'Concepto'
    # top_conceptos_twitter = concepto_twitter['Concepto_asociado'].str.lower().value_counts()
    
    # # Asigna el valor de apariciones de top_conceptos a matriz_peso como una nueva columna
    # df_twitter['Apariciones'] = df_twitter['Polaridades'].str.lower().map(lambda x: top_conceptos_twitter[x] if x in top_conceptos_twitter.index else 0)

    # # Resetea el índice y renumera de 1 a 281
    # df_twitter = df_twitter.reset_index(drop=True)
    # df_twitter.index = df_twitter.index + 1

    # df_threads['Ponderación'] = df_twitter['1']+df_twitter['2']+df_twitter['3']+df_twitter['4']+df_twitter['5']+df_twitter['6']+df_twitter['7']+df_twitter['8']+df_twitter['9']+df_twitter['10']+df_twitter['11']+df_twitter['12']+df_twitter['13']+df_twitter['14']+df_twitter['15']+df_twitter['16']+df_twitter['17']+df_twitter['18']
    # df_twitter['Puntaje'] = df_twitter['Ponderación'] * df_twitter['Apariciones']
    # df_twitter = df_twitter.sort_values(by='Puntaje', ascending=False)

    # top_10_df_twitter = df_twitter.head(10)


    # ################### Reddit #################################
    # df_reddit = matriz_peso[matriz_peso['Red Social'] == 'reddit']
    # # Lee solo la columna 'Concepto'
    # concepto_reddit = pd.read_csv(df_reddit, usecols=['Concepto_asociado'])

    # # Obtiene el top 10 de los valores más frecuentes en la columna 'Concepto'
    # top_conceptos_reddit = concepto_reddit['Concepto_asociado'].str.lower().value_counts()
    
    # # Asigna el valor de apariciones de top_conceptos a matriz_peso como una nueva columna
    # df_reddit['Apariciones'] = df_reddit['Polaridades'].str.lower().map(lambda x: top_conceptos_reddit[x] if x in top_conceptos_reddit.index else 0)

    # # Resetea el índice y renumera de 1 a 281
    # df_reddit = df_reddit.reset_index(drop=True)
    # df_reddit.index = df_reddit.index + 1

    # df_reddit['Ponderación'] = df_reddit['1']+df_reddit['2']+df_reddit['3']+df_reddit['4']+df_reddit['5']+df_reddit['6']+df_reddit['7']+df_reddit['8']+df_reddit['9']+df_reddit['10']+df_reddit['11']+df_reddit['12']+df_reddit['13']+df_reddit['14']+df_reddit['15']+df_reddit['16']+df_reddit['17']+df_reddit['18']
    # df_reddit['Puntaje'] = df_reddit['Ponderación'] * df_reddit['Apariciones']
    # df_reddit = df_reddit.sort_values(by='Puntaje', ascending=False)

    # top_10_df_reddit = df_reddit.head(10)
    