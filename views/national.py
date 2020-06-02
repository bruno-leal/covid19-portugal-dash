import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

import charts as ch
import data_handler as dh

national_data = dh.get_national_data()
regional_data = dh.get_regional_data()


def generate_chart_new_confirmed():
	return html.Div(children=[
		dcc.Graph(
			figure=ch.PlotlyCharts.new_confirmed_evolution(national_data)
		)
	])

def generate_chart_new_dead():
	return html.Div(children=[
		dcc.Graph(
			figure=ch.PlotlyCharts.new_dead_evolution(national_data)
		)
	])

def generate_chart_bar_tested():
	return html.Div(children=[
		dcc.Graph(
			figure=ch.PlotlyCharts.new_tested_evolution(national_data)
		)
	])

def generate_chart_active():
	return html.Div(children=[
		dcc.Graph(
			figure=ch.PlotlyCharts.active_closed_evolution(national_data)
		)
	])

def generate_chart_line_recovery():
	return html.Div(children=[
		dcc.Graph(
			figure=ch.PlotlyCharts.recovery_evolution(national_data)
		)
	])

def generate_chart_line_outcome():
	return html.Div(children=[
		dcc.Graph(
			figure=ch.PlotlyCharts.outcome_evolution(national_data)
		)
	])


# Return page content
def get_contents():
    return html.Div([
		dbc.Card(
			dbc.CardBody(
				[
					html.H4("Novos Confirmados"),
					generate_chart_new_confirmed()
				]
			),
			className="my-2"
		),
		dbc.Card(
			dbc.CardBody(
				[
					html.H4("Novos Óbitos"),
					generate_chart_new_dead()
				]
			),
			className="my-2"
		),
		dbc.Card(
			dbc.CardBody(
				[
					html.H4("Novos Testados"),
					generate_chart_bar_tested()
				]
			),
			className="my-2"
		),
		dbc.Card(
			dbc.CardBody(
				[
					html.H4("Evolução dos casos activos"),
					generate_chart_active()
				]
			),
			className="my-2"
		),
		dbc.Card(
			dbc.CardBody(
				[
					html.H4("Recuperados, Óbitos e Internados"),
					generate_chart_line_outcome()
				]
			),
			className="my-2"
		),
		dbc.Card(
			dbc.CardBody(
				[
					html.H4("Local de recuperação"),
					generate_chart_line_recovery()
				]
			),
			className="my-2"
		)
    ])
