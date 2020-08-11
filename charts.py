import datetime
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

import utils


class Utils:

	def get_label_by_variable(variable):
		switcher={
			"confirmed": "casos confirmados",
			"confirmed_per_thousand": "casos confirmados por 1000 habitantes",
			"new_confirmed": "novos casos confirmados (último relatório)",
			"new_confirmed_avg_7": "novos casos confirmados (média móvel a 7 dias)",
			"new_confirmed_per": "% de variação diária (face ao relatório anterior)",
			"new_confirmed_per_avg_7": "% de variação diária (média móvel a 7 dias)"
		}

		return switcher.get(variable, "")


	def get_number_format_by_variable(variable):
		switcher={
			"confirmed": "{:.0f}",
			"confirmed_per_thousand": "{:.2f}",
			"new_confirmed": "{:.0f}",
			"new_confirmed_avg_7": "{:.1f}",
			"new_confirmed_per": "{:.2f}",
			"new_confirmed_per_avg_7": "{:.2f}"
		}

		return switcher.get(variable, "")


class NationalCharts:

	def new_confirmed_evolution(national_data):
		df = national_data.filter(['date', 'new_confirmed', 'new_confirmed_avg_7'])

		fig = go.Figure()
		fig.add_trace(go.Bar(x=df.date, y=df.new_confirmed, name="Valor diário", marker_color="lightblue"))
		fig.add_trace(go.Scatter(x=df.date, y=df.new_confirmed_avg_7, mode="lines", name="Média móvel (a 7 dias)", line=dict(color="darkblue", width=2)))

		fig.update_layout(
			title="Evolução do número de novos casos confirmados",
			xaxis_title="Data",
			yaxis_title="Casos",
			template="plotly_white"
		)
		fig.update_layout(
			legend=dict(
				x=0,
				y=1,
				traceorder="normal",
				font=dict(
					family="sans-serif",
					size=12,
					color="black"
				),
				bgcolor="White",
				bordercolor="LightGray",
				borderwidth=2
			)
		)

		return fig


	def new_dead_evolution(national_data):
		df = national_data.filter(['date', 'new_dead', 'new_dead_avg_7'])

		fig = go.Figure()
		fig.add_trace(go.Bar(x=df.date, y=df.new_dead, name="Valor diário", marker_color="lightblue"))
		fig.add_trace(go.Scatter(x=df.date, y=df.new_dead_avg_7, mode="lines", name="Média móvel (a 7 dias)", line=dict(color="darkblue", width=2)))

		fig.update_layout(
			title="Evolução do número de novos óbitos",
			xaxis_title="Data",
			yaxis_title="Óbitos",
			template="plotly_white"
		)
		fig.update_layout(
			legend=dict(
				x=0,
				y=1,
				traceorder="normal",
				font=dict(
					family="sans-serif",
					size=12,
					color="black"
				),
				bgcolor="White",
				bordercolor="LightGray",
				borderwidth=2
			)
		)

		return fig


	def new_tested_evolution(national_data):
		df = national_data.filter(['date', 'new_confirmed', 'new_unconfirmed'])
		df = df.assign(date_fmt=df.date.dt.strftime("%B %d"))

		fig = go.Figure()
		fig.add_trace(go.Bar(x = df.date, y = df.new_unconfirmed, name = 'Novos Infirmados', marker_color='lightgreen'))
		fig.add_trace(go.Bar(x = df.date, y = df.new_confirmed, name = 'Novos Confirmados', marker_color='lightcoral'))

		fig.update_layout(
			barmode='stack',
			title="Novos Testados",
			xaxis_title="Data",
			yaxis_title="Casos",
			template="plotly_white"
		)

		return fig


	def active_closed_evolution(national_data):
		df = national_data.filter(['date', 'active', 'closed'])
		# df = df.assign(date_fmt=df.date.dt.strftime("%B %d"))

		fig = go.Figure()
		fig.add_trace(go.Scatter(x=national_data.date, y=national_data.active, name='Casos activos', line=dict(color="darkblue", width=2)))
		fig.add_trace(go.Scatter(x=national_data.date, y=national_data.closed, name='Casos fechados', line=dict(color="black", width=2)))
		fig.add_trace(go.Bar(x=national_data.date, y=national_data.dead, name='Óbitos', marker_color='red'))
		fig.add_trace(go.Bar(x=national_data.date, y=national_data.recovered, name='Recuperados', marker_color='green'))
		# fig.add_trace(go.Bar(x = df.date, y = df.new_unconfirmed, name = 'Novos Infirmados', marker_color='lightgreen'))
		# fig.add_trace(go.Bar(x = df.date, y = df.new_confirmed, name = 'Novos Confirmados', marker_color='lightcoral'))

		fig.update_layout(
			barmode='stack',
			title="Casos activos vs. Casos fechados (óbitos ou recuperados)",
			xaxis_title="Data",
			yaxis_title="Casos",
			template="plotly_white"
		)

		return fig


	def outcome_evolution(national_data):
		df = national_data.filter(['date', 'recovered', 'dead', 'hospitalized_infirmary', 'hospitalized_icu', 'domiciliary_recovery'])
		df = df.assign(date_fmt=df.date.dt.strftime("%B %d"))

		fig = go.Figure()
		fig.add_trace(go.Scatter(x = df.date, y = df.recovered, mode = 'lines', name = 'Recuperados', line=dict(color="#006600", width=4), visible = 'legendonly'))
		fig.add_trace(go.Scatter(x = df.date, y = df.dead, mode = 'lines', name = 'Óbitos', line=dict(color="#ff0000", width=4), visible = 'legendonly'))
		fig.add_trace(go.Scatter(x = df.date, y = df.hospitalized_infirmary, mode = 'lines', name = 'Internados em enfermaria', line=dict(color="#ff9966", width=2, dash='dot')))
		fig.add_trace(go.Scatter(x = df.date, y = df.hospitalized_icu, mode = 'lines', name = 'Internados em UCI', line=dict(color="#ff3333", width=2, dash='dot')))
		fig.add_trace(go.Scatter(x = df.date, y = df.domiciliary_recovery, mode = 'lines', name = 'Recuperação domiciliária', line=dict(color="#3399ff", width=2, dash='dot'), visible = 'legendonly'))

		fig.update_layout(
			title="Recuperados, Óbitos e Internados",
			xaxis_title="Data",
			yaxis_title="Casos",
			template="plotly_white"
		)

		return fig
	

	def recovery_evolution(national_data):
		fig = go.Figure()

		reference_date = national_data.query("hospitalized_icu > 0").date.min() # first day with records of cases in icu
		df = national_data.query('date >= @reference_date')

		fig.add_trace(go.Scatter(
			x=df.date,
			y=df.hospitalized_icu,
			mode='lines',
			name='Internados em UCI',
			line=dict(width=0.5, color='#e65c00'),
			hoveron='points+fills', # select where hover is active
			stackgroup='group', # define stack group
			groupnorm='percent' # sets the normalization for the sum of the stackgroup
		))
		fig.add_trace(go.Scatter(
			x=df.date,
			y=df.hospitalized_infirmary,
			mode='lines',
			name='Internados em enfermaria',
			line=dict(width=0.5, color='#ffbb33'),
			hoveron='points+fills', # select where hover is active
			stackgroup='group'
		))
		fig.add_trace(go.Scatter(
			x=df.date,
			y=df.domiciliary_recovery,
			mode='lines',
			name='Recuperação domiciliária',
			line=dict(width=0.5, color='#4d88ff'),
			hoveron='points+fills', # select where hover is active
			stackgroup='group'
		))

		fig.update_layout(
			title='Evolução da situação dos casos confirmados',
			showlegend=True,
			xaxis_type='date',
			yaxis=dict(
				type='linear',
				range=[1, 100],
				ticksuffix='%')
		)

		return fig


	def confirmed_evolution(national_data, regional_data):
		df_regional = regional_data.filter(['date', 'region', 'confirmed'])
		df_national = national_data.filter(['date', 'region', 'confirmed'])
		df = pd.concat([df_national, df_regional])

		return px.line(
			df,
			x="date",
			y="confirmed",
			color="region",
			hover_name="region",
			labels=dict(
				confirmed="Casos Confirmados", region="Região", date = "Data"
			),
			title="Evolução dos Casos Confirmados, por região",
			template="plotly_white"
		)


class RegionalCharts:

	def confirmed_regional_proportion_evolution(national_data, regional_data):
		df = regional_data.filter(['date', 'region', 'confirmed', 'confirmed_per'])
		df = df.assign(date_fmt=df.date.dt.strftime("%B %d"))

		return px.bar(
			df,
			x="date",
			y="confirmed",
			color="region",
			hover_name="region",
			labels=dict(
				confirmed="Casos Confirmados", region="Região", date = "Data"
			),
			title="Evolução dos Casos Confirmados, por região",
			template="plotly_white"
		)


	def deaths_evolution(national_data, regional_data):
		df = regional_data.filter(['date', 'region', 'dead'])
		df = df.append(national_data.filter(['date', 'region', 'dead']))
		df = df.assign(date_fmt=df.date.dt.strftime("%B %d"))

		return px.line(
			df,
			x="date",
			y="dead",
			color="region",
			hover_name="region",
			labels=dict(
				dead="Óbitos", region="Região", date = "Data"
			),
			title="Evolução dos Óbitos, por região",
			template="plotly_white"
		)


	def deaths_regional_proportion_evolution(national_data, regional_data):
		df = regional_data.filter(['date', 'region', 'dead', 'dead_per'])
		df = df.assign(date_fmt=df.date.dt.strftime("%B %d"))

		return px.bar(
			df,
			x="date",
			y="dead",
			color="region",
			hover_name="region",
			labels=dict(
				dead="Óbitos", region="Região", date = "Data"
			),
			title="Evolução dos Óbitos, por região",
			template="plotly_white"
		)


	def confirmed_deaths_comparison_evolution(regional_data):
		reference_date = regional_data.query("dead > 0").date.min() # first day with records of deaths
		df = regional_data.query("date > @reference_date").filter(['date', 'region', 'confirmed', 'dead', 'lethality_rate'])
		df.lethality_rate = round(df.lethality_rate * 100, 2)
		df = df.assign(date_fmt = df.date.dt.strftime("%B %d"))

		return px.scatter(
			df,
			x = "confirmed",
			y = "dead",
			color = "region",
			size="lethality_rate",
			hover_name="region",
			animation_frame="date_fmt",
			animation_group = "region",
			range_x = [0, df.confirmed.max() * 1.1],
			range_y=[0, df.dead.max() * 1.1],
			labels = dict(
				confirmed = "Casos Confirmados", dead = "Óbitos", region = "Região", date_fmt = "Data", lethality_rate = "Taxa de Letalidade (%)"
			),
			title="Evolução de Casos Confirmados, Óbitos e Taxa de Letalidade, por região",
			template="plotly_white"
		)


class LocalCharts:

	def new_confirmed_evolution_municipality(local_data, municipality):
		df = local_data.query('municipality == @municipality').filter(['date', 'new_confirmed', 'new_confirmed_avg_7'])

		fig = go.Figure()
		fig.add_trace(go.Bar(x=df.date, y=df.new_confirmed, name="Valor diário", marker_color="lightblue"))
		fig.add_trace(go.Scatter(x=df.date, y=df.new_confirmed_avg_7, mode="lines", name="Média móvel (a 7 dias)", line=dict(color="darkblue", width=2)))

		fig.update_layout(
			title="Evolução do número de novos casos confirmados em {}".format(municipality),
			xaxis_title="Data",
			yaxis_title="Casos",
			template="plotly_white"
		)
		fig.update_layout(
			legend=dict(
				x=0,
				y=1,
				traceorder="normal",
				font=dict(
					family="sans-serif",
					size=12,
					color="black"
				),
				bgcolor="White",
				bordercolor="LightGray",
				borderwidth=2
			)
		)

		return fig


	def municipalities_limits_map(latest_local_data, municipalities_geojson_layer, variable):
		label = Utils.get_label_by_variable(variable)
		number_format = Utils.get_number_format_by_variable(variable)

		# print("creating figure at: " + datetime.datetime.now().strftime("%H:%M:%S"))
		fig = go.Figure(
			go.Choroplethmapbox(
				geojson=municipalities_geojson_layer,
				featureidkey="properties.CCA_2",
				locations=latest_local_data.code,
				z=latest_local_data[variable],
				colorscale="OrRd",
				# zmin=0,
				# zmax=12,
				marker_line_width=0,
				# text=latest_local_data.apply(lambda row: f"{row['municipality']}:<br>{row[variable]:.0f} " + label, axis=1),
				text=latest_local_data.apply(
					lambda row:
					"{}:<br>{} {}".format(
						row["municipality"],
						number_format.format(row[variable]),
						label
					),
					axis=1
				),
				hoverinfo="text"
			)
		)
		fig.update_layout(mapbox_style="carto-positron", mapbox_zoom=4.5, mapbox_center = {"lat": 38.3317, "lon": -17.2836})
		fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
		# fig.update_layout(height=800)
		# print("created figure at: " + datetime.datetime.now().strftime("%H:%M:%S"))

		return fig


	def municipalities_centroids_map(latest_local_data, municipalities_geojson_layer, variable):
		df = municipalities_geojson_layer.merge(
			latest_local_data, left_on = ['CCA_2'], right_on = ['code'], how = 'left',
		)
		df = df.loc[df[variable] > 0]
		
		label = Utils.get_label_by_variable(variable)
		number_format = Utils.get_number_format_by_variable(variable)

		# print("creating figure at: " + datetime.datetime.now().strftime("%H:%M:%S"))
		fig = fig = px.scatter_mapbox(
			df,
			# mapbox_style='carto-positron',
			lat="centroid_lat",
			lon="centroid_lon",
			color=variable,
			size=variable,
			hover_name="municipality",
			# hover_data=[variable],
			hover_data={
				variable: True,
				"centroid_lat": False,
				"centroid_lon": False
			},
			labels={
				variable: label
			},
			color_continuous_scale=px.colors.sequential.solar,
			# size_min=5,
			# size_max=20,
			zoom=5,
			# center=dict(lat=38.3317, lon=-17.2836)
		)
		fig.update_layout(hovermode='closest')
		fig.update_layout(mapbox_style="carto-positron", mapbox_zoom=4.5, mapbox_center = {"lat": 38.3317, "lon": -17.2836})
		fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0}, height=600)
		# print("created figure at: " + datetime.datetime.now().strftime("%H:%M:%S"))

		return fig