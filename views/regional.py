import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import datetime

import charts as ch
import data_handler as dh

national_data = dh.get_national_data()
regional_data = dh.get_regional_data()


def generate_chart_stack_confirmed_region(last_n_days):
	return html.Div(children=[
		dcc.Graph(
			figure=ch.PlotlyCharts.confirmed_regional_proportion_evolution(national_data, regional_data, last_n_days)
		)
	])

def generate_chart_stack_dead_region(last_n_days):
	return html.Div(children=[
		dcc.Graph(
			figure=ch.PlotlyCharts.deaths_regional_proportion_evolution(national_data, regional_data, last_n_days)
		)
	])

def generate_chart_confirmed_dead_por_region(last_n_days):
	return html.Div(children=[
		dcc.Graph(
			figure=ch.PlotlyCharts.confirmed_deaths_comparison_evolution(regional_data, last_n_days)
		)
	])


# Return page content
def get_contents(last_n_days):
    return html.Div([
		dbc.Card(
			dbc.CardBody(
				[
					html.H4("Evolução dos Casos Confirmados por região"),
					generate_chart_stack_confirmed_region(last_n_days)
				]
			),
			className="my-2"
		),
		dbc.Card(
			dbc.CardBody(
				[
					html.H4("Evolução dos Óbitos por região"),
					generate_chart_stack_dead_region(last_n_days)
				]
			),
			className="my-2"
		),
		dbc.Card(
			dbc.CardBody(
				[
					html.H4("Evolução de Casos Confirmados vs. Óbitos, por região"),
					generate_chart_confirmed_dead_por_region(last_n_days)
				]
			),
			className="my-2"
		)
    ])
