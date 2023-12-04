import plotly.express as px
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import os
import plotly.io as pio


# Hier kann entweder ein Liniendiagramm erzeugt werden (entweder Position[dauer] oder Strom[mA]
def showlineplot(y_axes,dataframes_list,title):
    # Liniendiagramme für jede DataFrame in der Liste erstellen und anzeigen
    for i, df in enumerate(dataframes_list):
        # Erstellen Sie ein Liniendiagramm mit den entsprechenden x- und y-Spalten aus dem DataFrame
        fig = px.line(df, x='Time[s]', y=y_axes, title=title + f'_{i+1}')


        # Hier werden weitere Anpassungen am Diagramm vorgenommen

        # Achsentitel hinzufügen
        fig.update_xaxes(title_text='Zeit [s]')
        fig.update_yaxes(title_text=y_axes)

        # Diagrammtitel ändern
        #fig.update_layout(title='Angepasstes Scatter-Plot')

        # Hinzufügen einer Legende
        fig.update_traces(marker=dict(size=10), selector=dict(mode='markers'))

        # Farbpalette ändern
        #fig.update_traces(marker=dict(color='red'), selector=dict(mode='markers'))

        # Diagrammgröße ändern
        #fig.update_layout(width=800, height=400)

        # Hinzufügen von Gitterlinien
        fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='lightgray')
        fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='lightgray')

        # Diagramm anzeigen
        fig.show()


# Hier wird ein Liniendiagramm mit Strom und Position angezeigt
def showbothlineplot(dataframes_list,title):

    fig_list = []

    # Liniendiagramme für jede DataFrame in der Liste erstellen und anzeigen
    for i, df in enumerate(dataframes_list):
        # Subplots erstellen
        fig = make_subplots(specs=[[{"secondary_y": True}]])  # "secondary_y" ermöglicht eine zweite y-Achse

        # Liniendiagramm zur ersten y-Achse hinzufügen
        fig.add_trace(go.Scatter(x=df['Time[s]'], y=df['Strom[mA]'], mode='lines', name='Stromstärke[mA]'))

        # Liniendiagramm zur zweiten y-Achse hinzufügen
        fig.add_trace(go.Scatter(x=df['Time[s]'], y=df['Position[dauer]'], mode='lines', name='Position[dauer]'), secondary_y=True)

        # Layout anpassen
        fig.update_layout(title=title + f'_{i}',
                          xaxis_title='Time [s]',
                          yaxis_title='Stromstärke [mA]',
                          yaxis2_title='Position [dauer]')

        # Diagramm anzeigen
        #fig.show()

        # Liste hinzufügen
        fig_list.append(fig)

    return fig_list



