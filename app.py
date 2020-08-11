import dash
import dash_bootstrap_components as dbc

FONT_AWESOME = "https://use.fontawesome.com/releases/v5.10.2/css/all.css"
external_stylesheets = [dbc.themes.FLATLY, FONT_AWESOME]
app = dash.Dash(
	__name__,
	title="COVID-19 em Portugal",
	update_title='A carregar...',
	external_stylesheets=external_stylesheets,
	suppress_callback_exceptions=True
)
server = app.server
