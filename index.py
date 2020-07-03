import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output

from app import app, server
from views import home, national, regional, local
import data_handler as dh



app.layout = dbc.Container(
	[
		dcc.Location(id='url', refresh=False),

		dbc.NavbarSimple(
			children=[
				dbc.NavItem(dbc.NavLink("Início", href="/")),
				dbc.DropdownMenu(
					children=[
						# dbc.DropdownMenuItem("Evolução", header=True),
						dbc.DropdownMenuItem("Dados nacionais", href="/national"),
						dbc.DropdownMenuItem("Dados regionais", href="/regional"),
						dbc.DropdownMenuItem("Dados concelhios", href="/local"),
					],
					nav=True,
					in_navbar=True,
					label="Evolução",
				)
			],
			dark=True,
			color="primary",
			className="p-2"
		),

		dbc.Spinner(children=[html.Div(id='page-content')], color="light"),

		html.Br(),
		html.Hr(),

		html.Footer(
			[
				dbc.Row(
					[
						dbc.Col(
							html.P(
								[
									"Fonte dos dados: ",
									html.A(children=["relatórios dários da DGS"], href="https://covid19.min-saude.pt/relatorio-de-situacao", target="_blank"),
									" (última actualização: {})".format(dh.get_last_update_date()),
									"."
								]
							),
							width={"size": 6, "order": 1},
						),
						dbc.Col(
							html.P(
								[
									"Autor: ",
									html.A(children=["Bruno Leal"], href="https://github.com/bruno-leal/covid19-portugal-dash", target="_blank"),
								]
							),
							width={"size": 3, "order": "last", "offset": 3},
						)
					]
				)
			]
		)
	],
	fluid=True
)


@app.callback(Output('page-content', 'children'), [Input('url', 'pathname')])
def display_page(pathname):
	if (pathname == "/"):
		return home.get_contents()
	elif (pathname == '/national'):
		return national.get_contents()
	elif (pathname == '/regional'):
		return regional.get_contents()
	elif (pathname == '/local'):
		return local.get_contents()
	else:
		return '404'


if __name__ == '__main__':
    app.run_server(debug=True)
