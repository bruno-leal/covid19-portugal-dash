import dash
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import dash_table

from app import app
import charts as ch
import data_handler as dh


local_data = dh.get_local_data()


def generate_chart_bar_new_confirmed_municipality(municipality):
	return html.Div(children=[
		dcc.Graph(
			figure=ch.LocalCharts.new_confirmed_evolution_municipality(local_data, municipality)
		)
	])


# Return page content
def get_contents():
	municipalities = local_data.filter(['municipality']).drop_duplicates().sort_values(['municipality'])['municipality'].tolist()

	return html.Div([
		dbc.Card(
			dbc.CardBody(
				[
					html.H4("Dados por concelho"),
					html.P("Para consultar informação específica de um concelho, utilize o campo abaixo."),
					dbc.Select(
						id="select-municipality",
						options=[
                            {'label': i, 'value': i} for i in municipalities
						],
                        className="my-2"
					),
					html.Div(id='panel-municipality-info', className="my-2")
				]
			),
			className="my-2"
		)
    ])


@app.callback(
    Output(component_id='panel-municipality-info', component_property='children'),
    [Input(component_id='select-municipality', component_property='value')]
)
def update_municipality_info(input_value):
	if (input_value):
		max_date = local_data.date.max().date()
		df = local_data.query('date == @max_date').sort_values(['confirmed'], ascending=False).reset_index()
		row = df.loc[df['municipality']==input_value]
		index = df.index[df['municipality']==input_value][0]
		# confirmed = round(row.confirmed.round().values[0])
		# confirmed = df.at[index, 'confirmed']

		return html.Div([
			html.P('Com um total de {0} casos, o concelho de {1} é actualmente o {2}.º concelho com mais casos confirmados.'.format(
					"%.0f" % row.confirmed.values[0],
					input_value,
                    index + 1 # 0-based index
				),
			),
			html.P('Na última actualização apresentou {0} novos casos, correspondendo a uma variação percentual de {1}%.'.format(
					"%.0f" % row.new_confirmed.values[0],
					"%.1f" % row.new_confirmed_per.values[0]
				)
			),
			html.P('A média móvel a 7 dias é de {0} novos casos, o que corresponde a um valor percentual médio de {1}%.'.format(
					"%.0f" % row.new_confirmed_avg_7.values[0],
					"%.1f" % row.new_confirmed_per_avg_7.values[0]
				)
			),
			generate_chart_bar_new_confirmed_municipality(input_value)
		])
	else:
		return ""

