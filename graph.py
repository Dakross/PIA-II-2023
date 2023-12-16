import matplotlib.pyplot as plt
from wordcloud import WordCloud

def grafico_frecuencia(data, filename):
    # Ordenar el DataFrame por 'Apariciones' en orden descendente
    top_10_conceptos = data.sort_values(by='Apariciones', ascending=False).head(10)

    # Crear el gráfico de barras con 'Polaridades' en el eje x y 'Apariciones' en el eje y
    ax = top_10_conceptos.plot(kind='bar', x='Polaridades', y='Apariciones', color='royalblue')
    plt.title('Top 10 Conceptos Más Frecuentes')
    plt.xlabel('Concepto')
    plt.ylabel('Frecuencia')

    # Añadir etiquetas a cada barra con un solo decimal, dentro de la columna
    for p in ax.patches:
        height = int(p.get_height())
        width = p.get_width()
        x, y = p.get_x(), p.get_y()
        ax.annotate(f'{height}', (x + width / 2, min(y + height, 1300)),
                    ha='center', va='center', xytext=(0, 10), textcoords='offset points')

    # Ajustar el diseño para asegurar que las etiquetas no se corten
    plt.ylim(0, 1300)
    plt.tight_layout()

    # Guardar la figura en un archivo
    plt.savefig(filename)
    plt.switch_backend('agg')
    plt.close()


def grafico_puntaje(data, filename):
    # Ordenar el DataFrame por 'Apariciones' en orden descendente
    top_10_conceptos = data.sort_values(by='Puntaje', ascending=False).head(10)

    # Crear una figura más grande antes de trazar el gráfico
    plt.figure(figsize=(10, 6))  # Ajusta el tamaño según tus necesidades

    # Crear el gráfico de barras con 'Polaridades' en el eje x y 'Apariciones' en el eje y
    ax = top_10_conceptos.plot(kind='bar', x='Polaridades', y='Puntaje', color='forestgreen')
    plt.title('Top 10 Conceptos Con Mayor Puntaje')
    plt.xlabel('Concepto')
    plt.ylabel('Frecuencia')

    # Añadir etiquetas a cada barra con un solo decimal, dentro de la columna
    for p in ax.patches:
        height = p.get_height()
        width = p.get_width()
        x, y = p.get_x(), p.get_y()
        ax.annotate(f'{height:.1f}', (x + width / 2, min(y + height, 1250)),
                    ha='center', va='center', xytext=(0, 10), textcoords='offset points')

    # Ajustar el diseño para asegurar que las etiquetas no se corten
    plt.ylim(0, 1250)
    plt.tight_layout()

    # Guardar la figura en un archivo
    plt.savefig(filename)
    plt.switch_backend('agg')
    plt.close()

def wordcloud(data, filename):
    # Capitalizar la primera letra de cada palabra
    data['Polaridades'] = data['Polaridades'].apply(lambda x: ' '.join(word.capitalize() for word in x.split()))

    # Ordenar el DataFrame por la columna "Apariciones" de mayor a menor
    data = data.sort_values(by='Apariciones', ascending=False)

    words = ' '.join(data['Polaridades'].astype(str))

    wc = WordCloud(background_color="white").generate(words)

    # Guardar la figura en un archivo
    wc.to_file(f"static/{filename}")