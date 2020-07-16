import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import dash_table

import charts as ch
import data_handler as dh


latest_national_data = dh.get_latest_national_data()
latest_local_data = dh.get_latest_local_data()
last_update_date = dh.get_last_update_date()


def generate_confirmed_panel():
	confirmed = latest_national_data.confirmed
	new_confirmed = latest_national_data.new_confirmed
	color = ('red' if new_confirmed.item() > 0 else 'green')

	return html.Div(
		[
			html.H2("Casos Confirmados"),
			html.H3(confirmed),
			html.H4('%+d' % new_confirmed, style={'color': color})
		],
		style={
			'textAlign': 'center'
		}
	)

def generate_active_panel():
	active = latest_national_data.active
	new_active = latest_national_data.new_active
	color = ('red' if new_active.item() > 0 else 'green')

	return html.Div(
		[
			html.H2("Casos Activos"),
			html.H3(active),
			html.H4('%+d' % new_active, style={'color': color})
		],
		style={
			'textAlign': 'center'
		}
	)

def generate_recovered_panel():
	recovered = latest_national_data.recovered
	new_recovered = latest_national_data.new_recovered
	color = ('green' if new_recovered.item() > 0 else 'gray')

	return html.Div(
		[
			html.H2("Recuperados"),
			html.H3(recovered),
			html.H4('%+d' % new_recovered, style={'color': color})
		],
		style={
			'textAlign': 'center'
		}
	)

def generate_dead_panel():
	dead = latest_national_data.dead
	new_dead = latest_national_data.new_dead
	color = ('red' if new_dead.item() > 0 else 'green')

	return html.Div(
		[
			html.H2("Óbitos"),
			html.H3(dead),
			html.H4('%+d' % new_dead, style={'color': color})
		],
		style={
			'textAlign': 'center'
		}
	)

def generate_table_confirmed():
	df = latest_local_data.query(
		'confirmed > 0'
	).filter(
		['municipality', 'confirmed', 'confirmed_per_thousand', 'new_confirmed', 'new_confirmed_per', 'new_confirmed_avg_7', 'new_confirmed_per_avg_7']
	).sort_values(
		['confirmed'],
		ascending=False
	)

	return html.Div([
		html.Br(),
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
			# style_as_list_view=True,
			style_header={
				'backgroundColor': 'gray',
				'color': 'white',
				'fontWeight': 'bold',
				# 'border': '1px solid darkgray'
				# 'border': 'none'
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
    return html.Div([
		html.Br(className="my-2"),
		dbc.Jumbotron(
			[
				html.H1("Situação em Portugal", className="display-3"),
				html.H4("(em {})".format(last_update_date)),
				html.Br(className="my-2"),
				dbc.Row(
					[
						dbc.Col(
							generate_confirmed_panel(),
							width="12", md="6", lg="3",
							className="my-2"
						),
						dbc.Col(
							generate_active_panel(),
							width="12", md="6", lg="3",
							className="my-2"
						),
						dbc.Col(
							generate_recovered_panel(),
							width="12", md="6", lg="3",
							className="my-2"
						),
						dbc.Col(
							generate_dead_panel(),
							width="12", md="6", lg="3",
							className="my-2"
						)
					]
				)
			]
		),
		dbc.Card(
			dbc.CardBody(
				[
					html.H4("Concelhos com casos confirmados"),
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
