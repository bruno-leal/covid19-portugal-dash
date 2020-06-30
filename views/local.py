import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import dash_table
import json

from app import app
import charts as ch
import data_handler as dh

local_data = dh.get_local_data()


def generate_chart_bar_new_confirmed_municipality(municipality):
	return html.Div(children=[
		dcc.Graph(
			figure=ch.PlotlyCharts.new_confirmed_evolution_municipaliy(local_data, municipality)
		)
	])

def generate_table_confirmed():
	max_date = local_data.date.max().date()
	df = local_data.query(
		'date == @max_date'
	).query(
		'confirmed > 0'
	).filter(
		['municipality', 'confirmed', 'confirmed_per_thousand', 'new_confirmed', 'new_confirmed_per', 'new_confirmed_avg_7', 'new_confirmed_per_avg_7']
	).sort_values(
		['confirmed'],
		ascending=False
	)

	return html.Div([
		dash_table.DataTable(
			id='datatable-interactivity',
			columns=[
				{"name": ["", "Concelho"], "id": "municipality"},
				{"name": ["", "Casos confirmados"], "id": "confirmed"},
				{"name": ["", "Casos confirmados p/ mil habitantes"], "id": "confirmed_per_thousand"},
				{"name": ["Novos confirmados (último relatório)", "#"], "id": "new_confirmed"},
				{"name": ["Novos confirmados (último relatório)", "%"], "id": "new_confirmed_per"},
				{"name": ["Novos confirmados (média móvel a 7 dias)", "#"], "id": "new_confirmed_avg_7"},
				{"name": ["Novos confirmados (média móvel a 7 dias)", "%"], "id": "new_confirmed_per_avg_7"},
			],
			data=df.to_dict('records'),
			merge_duplicate_headers=True,
			filter_action="native",
			sort_action="native",
			page_action="native",
			page_size= 10,
			style_as_list_view=True,
			style_header={
				'backgroundColor': 'white',
				'fontWeight': 'bold',
				'border': 'none'
			},
			style_cell={
				'fontFamily': 'Open Sans',
                'textAlign': 'center',
                'height': '40px',
				# 'padding': '2px 5px',
				'maxWidth': '100px',
				'whiteSpace': 'normal'
			},
			style_cell_conditional=[
				{
					'if': {'column_id': 'municipality'},
					'width': '25%',
				}
			],
			style_data_conditional=[
				{
					'if': {'column_id': 'municipality'},
					'textAlign': 'left'
				}
			]
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
		),
		dbc.Card(
			dbc.CardBody(
				[
					html.H4("Lista dos concelhos com casos confirmados"),
					html.I(className="fas fa-question-circle fa-lg", id="tooltip-target"),
					dbc.Tooltip(
						"Ao clicar nos botões de ordenação de cada coluna poderá ordenar a tabela por esse dado específico. "
						"Pode também filtrar a informação pretendida. "
						"Os filtros dos campos numéricos permitem pesquisas do género '>400' ou '<=100'.",
						target="tooltip-target"
					),
					generate_table_confirmed(),
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

