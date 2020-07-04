import dash
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import dash_table

from app import app
import charts as ch
import data_handler as dh


latest_local_data = dh.get_latest_local_data()
municipalities_geojson_layer = dh.get_municipalities_geojson_layer()


def generate_map(variable):
	return html.Div(children=[
			dcc.Graph(
				figure=ch.LocalCharts.municipalities_map(latest_local_data, municipalities_geojson_layer, variable)
			)
		])


# Return page content
def get_contents():
	return html.Div([
		dbc.Card(
			dbc.CardBody(
				[
					html.H4("Consulta de dados por município"),
					html.P("Indique a informação que pretende consultar no campo abaixo."),
					dbc.Select(
						id="select-map-type",
						options=[
                            {'label': 'Total de casos confirmados', 'value': 'confirmed'},
                            {'label': 'N.º de casos confirmados por 100 habitantes', 'value': 'confirmed_per_thousand'},
                            {'label': 'Novos casos confirmados (último relatório)', 'value': 'new_confirmed'},
                            {'label': 'Novos casos confirmados (média móvel a 7 dias)', 'value': 'new_confirmed_avg_7'},
                            {'label': 'Variação percentual de novos casos confirmados (último relatório)', 'value': 'new_confirmed_per'},
                            {'label': 'Variação percentual de novos casos confirmados (média móvel a 7 dias)', 'value': 'new_confirmed_per_avg_7'}
						],
                        className="my-2"
					),
					html.Small("(O carregamento do mapa poderá demorar alguns segundos.)"),
					html.Div(id='panel-map', className="my-2"),
				]
			),
			className="my-2"
		)
    ])


@app.callback(
    Output(component_id='panel-map', component_property='children'),
    [Input(component_id='select-map-type', component_property='value')]
)
def update_map(input_value):
	if (input_value):
		return html.Div([
			generate_map(input_value)
		])
	else:
		return ""

