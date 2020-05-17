import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output

from app import app, server
from views import national, regional, local
import data_handler as dh



app.layout = dbc.Container([
    dcc.Location(id='url', refresh=False),

	dbc.NavbarSimple(
		children=[
			dbc.NavItem(dbc.NavLink("Dados nacionais", href="/national")),
			dbc.NavItem(dbc.NavLink("Dados regionais", href="/regional")),
			dbc.NavItem(dbc.NavLink("Dados concelhios", href="/local"))
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
								" (última actualização: {})".format(dh.get_last_update()),
								"."
							]
						),
						width={"size": 6, "order": 1},
					),
					dbc.Col(
						html.P(
							[
								"Autor: ",
								html.A(children=["Bruno Leal"], href="https://github.com/bruno-leal/covid-19-data", target="_blank"),
							]
						),
						width={"size": 3, "order": "last", "offset": 3},
					)
				]
			)
		]
	)
])


@app.callback(Output('page-content', 'children'), [Input('url', 'pathname')])
def display_page(pathname):
	if (pathname == '/national'):
		return national.get_contents(last_n_days=60)
	elif (pathname == '/regional'):
		return regional.get_contents(last_n_days=60)
	elif (pathname == '/local'):
		return local.get_contents()
	else:
		return '404'


if __name__ == '__main__':
    app.run_server(debug=True)
