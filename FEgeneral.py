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

def red_social(matriz_peso, red_social):
    
    ################### Redes #################################
    ## Cargar datos desde el archivo CSV
    ruta_csv = 'dataset.csv'
    df = pd.read_csv(ruta_csv, usecols=['Concepto_asociado','Red_Social'])
    
    # Separar red social y cambiar nombre de columna
    Red = df[df['Red_Social'] == red_social]
    Red.rename(columns={'Concepto_asociado':'Polaridades'}, inplace=True)
    
    #Valores existentes en Red y su cantidad de aparición
    valores = Red['Polaridades'].value_counts()
    
    #Mapear matriz preso usando valores
    matriz_peso['Apariciones'] = matriz_peso['Polaridades'].map(valores)
    
    #Eliminar las columnas que no presentan aparición
    matriz_peso = matriz_peso.dropna(subset = 'Apariciones')

    return matriz_peso
    