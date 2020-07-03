import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

import charts as ch
import data_handler as dh

national_data = dh.get_national_data()
latest_national_data = dh.get_latest_national_data()


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


# Return page content
def get_contents():
    return html.Div([
		html.Br(className="my-2"),
		dbc.Jumbotron(
			[
				html.H1("Situação em Portugal", className="display-3"),
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
    ])
