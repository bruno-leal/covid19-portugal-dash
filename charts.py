import pandas as pd
import datetime
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
import json

import utils


class ChartUtils:

	def calculate_chart_size(days):
		if days >= 30:
			return (20, 10)
		elif days >= 20:
			return (20, 8)
		elif days >= 10:
			return (12, 6)
		else:
			return (10, 5)


class StaticCharts:

	def confirmed_evolution(national_data, regional_data, last_n_days):
		plt.figure(figsize=ChartUtils.calculate_chart_size(last_n_days))

		sns.set(style="darkgrid")

		sns.set(rc={"lines.linewidth": 3})
		chart = sns.lineplot(
			x = 'date', y = 'confirmed', data = national_data
		)

		sns.set(rc={"lines.linewidth": 1})
		chart = sns.lineplot(
			x = 'date', y = 'confirmed', hue = 'region', data = regional_data, palette = sns.hls_palette(7, l = .4), legend = 'brief'
		)

		chart.set_title('Variação dos casos confirmados (por região)')
		chart.set_xlabel('Data')
		chart.set_ylabel('Casos confirmados')
		chart.legend(labels=['Total Nacional', 'Alentejo', 'Algarve', 'Açores', 'Centro', 'LVT', 'Madeira', 'Norte'])


	def deaths_evolution(national_data, regional_data, last_n_days):
		plt.figure(figsize=ChartUtils.calculate_chart_size(last_n_days))

		sns.set(style="darkgrid")

		sns.set(rc={"lines.linewidth": 3})
		chart = sns.lineplot(
			x = 'date', y = 'dead', data = national_data
		)

		sns.set(rc={"lines.linewidth": 1})
		chart = sns.lineplot(
			x = 'date', y = 'dead', hue = 'region', data = regional_data, palette = sns.hls_palette(7, l = .4), legend = 'brief'
		)

		chart.set_title('Variação dos óbitos (por região)')
		chart.set_xlabel('Data')
		chart.set_ylabel('Óbitos')
		chart.legend(labels=['Total Nacional', 'Alentejo', 'Algarve', 'Açores', 'Centro', 'LVT', 'Madeira', 'Norte'])


	def confirmed_deaths_comparison(regional_data):
		last_regional_data_date = regional_data.date.max().date()
		latest_regional_data = regional_data.query('date == @last_regional_data_date')
		latest_regional_data.lethality_rate = round(latest_regional_data.lethality_rate * 100, 2)

		plt.figure(figsize=(20,10))

		chart = sns.scatterplot(x = 'confirmed', y = 'dead', hue = 'region', size = 'lethality_rate', data = latest_regional_data, sizes = (10, 200), alpha = .8, legend = 'full')

		chart.set_title('Casos confirmados vs. Óbitos (por região)')
		chart.set_xlabel('Casos confirmados')
		chart.set_ylabel('Óbitos')


	def confirmed_deaths_comparison_evolution(regional_data, last_n_days):
		reference_date = regional_data.date.max() - datetime.timedelta(days = last_n_days)
		regional_reference_date = regional_data.query('date > @reference_date')
		regional_reference_date.lethality_rate = round(regional_reference_date.lethality_rate * 100, 2)

		plt.figure(figsize=(20,10))

		chart = sns.scatterplot(x = 'confirmed', y = 'dead', hue = 'region', size = 'lethality_rate', data = regional_reference_date, sizes = (10, 200), alpha = .8, legend = 'brief')

		chart.set_title('Evolução de Casos Confirmados vs. Óbitos, por região (nos últimos {n} dias)'.format(n = last_n_days))
		chart.set_xlabel('Casos Confirmados')
		chart.set_ylabel('Óbitos')


	def closed_active_evolution(data, last_n_days):
		reference_date = data.date.max() - datetime.timedelta(days = last_n_days)
		reference_date_total = data.query('date > @reference_date').query('region == "Total"')

		fig, ax = plt.subplots(figsize=ChartUtils.calculate_chart_size(last_n_days))
		ax.plot(reference_date_total.date, reference_date_total.closed, label = 'Casos Fechados')
		ax.plot(reference_date_total.date, reference_date_total.active, label = 'Casos Activos')

		plt.xlabel('Data')
		plt.ylabel('Casos')
		plt.grid(True)

		plt.title("Casos Fechados vs. Casos Activos (nos últimos {n} dias)".format(n = last_n_days))

		plt.legend()

		plt.show()


	def new_recovered_new_deaths_evolution(data, last_n_days):
		reference_date = data.date.max() - datetime.timedelta(days = last_n_days)
		reference_date_total = data.query('date > @reference_date').query('region == "Total"')

		fig, ax = plt.subplots(figsize=ChartUtils.calculate_chart_size(last_n_days))
		ax.plot(reference_date_total.date, reference_date_total.new_recovered, label = 'Novos Recuperados')
		ax.plot(reference_date_total.date, reference_date_total.new_dead, label = 'Novos Óbitos')

		plt.xlabel('Data')
		plt.ylabel('Casos')

		plt.title("Novos Recuperados vs. Novos Óbitos (nos últimos {n} dias)".format(n = last_n_days))

		plt.legend()

		plt.show()


	def outcome_evolution(data, last_n_days):
		reference_date = data.date.max() - datetime.timedelta(days = last_n_days)
		reference_date_total = data.query('date > @reference_date').query('region == "Total"')

		fig, ax = plt.subplots(figsize=ChartUtils.calculate_chart_size(last_n_days))
		ax.plot(reference_date_total.date, reference_date_total.recovered, linewidth = 2, label = 'Recuperados')
		ax.plot(reference_date_total.date, reference_date_total.dead, linewidth = 2, label = 'Óbitos')
		ax.plot(reference_date_total.date, reference_date_total.hospitalized_infirmary, linestyle = '--', label = 'Internados (em enfermaria)')
		ax.plot(reference_date_total.date, reference_date_total.hospitalized_icu, linestyle = '--', label = 'Internados (em UCI)')
		# ax.plot(reference_date_total.date, reference_date_total.domiciliary_recovery, label = 'Recuperação domiciliária')

		plt.xlabel('Data')
		plt.ylabel('Casos')
		plt.grid(True)

		plt.title("Recuperados vs. Óbitos vs. Internados (nos últimos {n} dias)".format(n = last_n_days))

		plt.legend()

		plt.show()


	def new_tested_evolution(data, last_n_days):
		reference_date = data.date.max() - datetime.timedelta(days = last_n_days)
		reference_date_total = data.query('date > @reference_date').query('region == "Total"').filter(['date', 'new_tested', 'new_confirmed', 'new_unconfirmed'])

		fig, ax = plt.subplots(figsize=ChartUtils.calculate_chart_size(last_n_days))
		ax.plot(reference_date_total.date, reference_date_total.new_tested, label = 'Novos Testados', color = 'black')
		ax.bar(reference_date_total.date, reference_date_total.new_unconfirmed, label = 'Novos Infirmados', color = 'lightgreen', edgecolor = 'white')
		ax.bar(reference_date_total.date, reference_date_total.new_confirmed, bottom = reference_date_total.new_unconfirmed, color = 'lightcoral', edgecolor = 'white', label = 'Novos Confirmados')

		plt.xlabel('Data')
		plt.ylabel('Casos')
		plt.grid(True)

		plt.title("Novos Testados (nos últimos {n} dias)".format(n = last_n_days))

		plt.legend()

		plt.show()


	def confirmed_variation_evolution(national_data, regional_data, last_n_days, regions):
		reference_date = national_data.date.max() - datetime.timedelta(days = last_n_days)

		national_reference_date = national_data.query('date > @reference_date').filter(['date', 'new_confirmed_per'])
		regional_reference_date = regional_data.query('date > @reference_date').query('region in @regions').filter(['date', 'region', 'new_confirmed_per'])

		fig, ax = plt.subplots(figsize=ChartUtils.calculate_chart_size(last_n_days))

		regional_reference_date_diff = pd.DataFrame()
		for region in regions:
			data_region = regional_reference_date.query('region == @region').reset_index()
			data_region = data_region.assign(new_confirmed_per_diff = data_region.new_confirmed_per.sub(national_reference_date.reset_index().new_confirmed_per))

			ax.plot(data_region.date, data_region.new_confirmed_per_diff, linestyle = ':', linewidth = 2, marker = 'o', markersize = 8, label = region) 

		plt.axhline(linewidth = 4, color = 'black')

		plt.xlabel('Data')
		plt.ylabel('Diferença face à média')
		plt.grid(True)

		plt.title("Diferença face à Taxa Nacional de Variação dos Casos Confirmados (nos últimos {n} dias)".format(n = last_n_days))

		plt.legend()

		plt.show()


	def confirmed_regional_proportion_evolution(data, last_n_days):
		reference_date = data.date.max() - datetime.timedelta(days = last_n_days)
		reference_date = data.query('date > @reference_date').filter(['date', 'region', 'confirmed_per'])
		data_norte = reference_date.query('region == "Norte"')
		data_centro = reference_date.query('region == "Centro"')
		data_lvt = reference_date.query('region == "LVT"')
		data_alentejo = reference_date.query('region == "Alentejo"')
		data_algarve = reference_date.query('region == "Algarve"')
		data_acores = reference_date.query('region == "Açores"')
		data_madeira = reference_date.query('region == "Madeira"')

		fig, ax = plt.subplots(figsize=ChartUtils.calculate_chart_size(last_n_days))
		
		ax.bar(data_norte.date, data_norte.confirmed_per, label = 'Norte', color = 'navy')
		ax.bar(data_centro.date, data_centro.confirmed_per, bottom = data_norte.confirmed_per, label = 'Centro', color = 'seagreen')
		ax.bar(data_lvt.date, data_lvt.confirmed_per, bottom = data_norte.confirmed_per + data_centro.confirmed_per, label = 'LVT', color = 'khaki')
		ax.bar(data_alentejo.date, data_alentejo.confirmed_per, bottom = data_norte.confirmed_per + data_centro.confirmed_per + data_lvt.confirmed_per, label = 'Alentejo', color = 'wheat')
		ax.bar(data_algarve.date, data_algarve.confirmed_per, bottom = data_norte.confirmed_per + data_centro.confirmed_per + data_lvt.confirmed_per + data_alentejo.confirmed_per, label = 'Algarve', color = 'goldenrod')
		ax.bar(data_acores.date, data_acores.confirmed_per, bottom = data_norte.confirmed_per + data_centro.confirmed_per + data_lvt.confirmed_per + data_alentejo.confirmed_per + data_algarve.confirmed_per, label = 'Açores', color = 'darkgreen')
		ax.bar(data_madeira.date, data_madeira.confirmed_per, bottom = data_norte.confirmed_per + data_centro.confirmed_per + data_lvt.confirmed_per + data_alentejo.confirmed_per + data_algarve.confirmed_per + data_acores.confirmed_per, label = 'Madeira', color = 'aquamarine')

		plt.xlabel('Data')
		plt.ylabel('Casos Confirmados')

		plt.title("Evolução da proporção de confirmados por região (nos últimos {n} dias)".format(n = last_n_days))

		plt.legend()

		plt.show()


	def deaths_regional_proportion_evolution(data, last_n_days):
		reference_date = data.date.max() - datetime.timedelta(days = last_n_days)
		reference_date = data.query('date > @reference_date').filter(['date', 'region', 'dead_per'])
		data_norte = reference_date.query('region == "Norte"')
		data_centro = reference_date.query('region == "Centro"')
		data_lvt = reference_date.query('region == "LVT"')
		data_alentejo = reference_date.query('region == "Alentejo"')
		data_algarve = reference_date.query('region == "Algarve"')
		data_acores = reference_date.query('region == "Açores"')
		data_madeira = reference_date.query('region == "Madeira"')

		fig, ax = plt.subplots(figsize=ChartUtils.calculate_chart_size(last_n_days))
		
		ax.bar(data_norte.date, data_norte.dead_per, label = 'Norte', color = 'navy')
		ax.bar(data_centro.date, data_centro.dead_per, bottom = data_norte.dead_per, label = 'Centro', color = 'seagreen')
		ax.bar(data_lvt.date, data_lvt.dead_per, bottom = data_norte.dead_per + data_centro.dead_per, label = 'LVT', color = 'khaki')
		ax.bar(data_alentejo.date, data_alentejo.dead_per, bottom = data_norte.dead_per + data_centro.dead_per + data_lvt.dead_per, label = 'Alentejo', color = 'wheat')
		ax.bar(data_algarve.date, data_algarve.dead_per, bottom = data_norte.dead_per + data_centro.dead_per + data_lvt.dead_per + data_alentejo.dead_per, label = 'Algarve', color = 'goldenrod')
		ax.bar(data_acores.date, data_acores.dead_per, bottom = data_norte.dead_per + data_centro.dead_per + data_lvt.dead_per + data_alentejo.dead_per + data_algarve.dead_per, label = 'Açores', color = 'darkgreen')
		ax.bar(data_madeira.date, data_madeira.dead_per, bottom = data_norte.dead_per + data_centro.dead_per + data_lvt.dead_per + data_alentejo.dead_per + data_algarve.dead_per + data_acores.dead_per, label = 'Madeira', color = 'aquamarine')

		plt.xlabel('Data')
		plt.ylabel('Óbitos')

		plt.title("Evolução da proporção de óbitos por região (nos últimos {n} dias)".format(n = last_n_days))

		plt.legend()

		plt.show()

class PlotlyCharts:

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


	def new_tested_evolution(national_data, last_n_days):
		reference_date = national_data.date.max() - datetime.timedelta(days=last_n_days)
		df = national_data.query("date > @reference_date").filter(['date', 'new_confirmed', 'new_unconfirmed'])
		df = df.assign(date_fmt=df.date.dt.strftime("%B %d"))

		fig = go.Figure()
		fig.add_trace(go.Bar(x = df.date, y = df.new_unconfirmed, name = 'Novos Infirmados', marker_color='lightgreen'))
		fig.add_trace(go.Bar(x = df.date, y = df.new_confirmed, name = 'Novos Confirmados', marker_color='lightcoral'))

		fig.update_layout(
			barmode='stack',
			title="Novos Testados (nos últimos {n} dias)".format(n=last_n_days),
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


	def outcome_evolution(national_data, last_n_days):
		reference_date = national_data.date.max() - datetime.timedelta(days=last_n_days)
		df = national_data.query("date > @reference_date").filter(['date', 'recovered', 'dead', 'hospitalized_infirmary', 'hospitalized_icu', 'domiciliary_recovery'])
		df = df.assign(date_fmt=df.date.dt.strftime("%B %d"))

		fig = go.Figure()
		fig.add_trace(go.Scatter(x = df.date, y = df.recovered, mode = 'lines', name = 'Recuperados', line=dict(color="#006600", width=4)))
		fig.add_trace(go.Scatter(x = df.date, y = df.dead, mode = 'lines', name = 'Óbitos', line=dict(color="#ff0000", width=4)))
		fig.add_trace(go.Scatter(x = df.date, y = df.hospitalized_infirmary, mode = 'lines', name = 'Internados em enfermaria', line=dict(color="#ff9966", width=2, dash='dot')))
		fig.add_trace(go.Scatter(x = df.date, y = df.hospitalized_icu, mode = 'lines', name = 'Internados em UCI', line=dict(color="#ff3333", width=2, dash='dot')))
		fig.add_trace(go.Scatter(x = df.date, y = df.domiciliary_recovery, mode = 'lines', name = 'Recuperação domiciliária', line=dict(color="#3399ff", width=2, dash='dot'), visible = 'legendonly'))

		fig.update_layout(
			title="Recuperados, Óbitos e Internados (nos últimos {n} dias)".format(n=last_n_days),
			xaxis_title="Data",
			yaxis_title="Casos",
			template="plotly_white"
		)

		return fig
	

	def recovery_evolution(national_data):
		fig = go.Figure()

		df = national_data.query('date >= "2020-03-14"') # first day with records of cases in icu

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


	def confirmed_evolution(national_data, regional_data, last_n_days):
		reference_date = regional_data.date.max() - datetime.timedelta(days=last_n_days)

		df_regional = regional_data.query("date > @reference_date").filter(['date', 'region', 'confirmed'])
		df_national = national_data.query("date > @reference_date").filter(['date', 'region', 'confirmed'])
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
			title="Evolução dos Casos Confirmados, por região (nos últimos {n} dias)".format(n=last_n_days),
			template="plotly_white"
		)


	def confirmed_regional_proportion_evolution(national_data, regional_data, last_n_days):
		reference_date = regional_data.date.max() - datetime.timedelta(days=last_n_days)
		df = regional_data.query("date > @reference_date").filter(['date', 'region', 'confirmed', 'confirmed_per'])
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
			title="Evolução dos Casos Confirmados, por região (nos últimos {n} dias)".format(n=last_n_days),
			template="plotly_white"
		)


	def deaths_evolution(national_data, regional_data, last_n_days):
		reference_date = regional_data.date.max() - datetime.timedelta(days=last_n_days)
		df = regional_data.query("date > @reference_date").filter(['date', 'region', 'dead'])
		df = df.append(national_data.query("date > @reference_date").filter(['date', 'region', 'dead']))
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
			title="Evolução dos Óbitos, por região (nos últimos {n} dias)".format(n=last_n_days),
			template="plotly_white"
		)


	def deaths_regional_proportion_evolution(national_data, regional_data, last_n_days):
		reference_date = regional_data.date.max() - datetime.timedelta(days=last_n_days)
		df = regional_data.query("date > @reference_date").filter(['date', 'region', 'dead', 'dead_per'])
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
			title="Evolução dos Óbitos, por região (nos últimos {n} dias)".format(n=last_n_days),
			template="plotly_white"
		)


	def confirmed_deaths_comparison_evolution(regional_data, last_n_days):
		reference_date = regional_data.date.max() - datetime.timedelta(days = last_n_days)
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
			title="Evolução de Casos Confirmados, Óbitos e Taxa de Letalidade, por região (nos últimos {n} dias)".format(n=last_n_days),
			template="plotly_white"
		)


	def new_confirmed_evolution_municipaliy(local_data, municipality):
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


	def confirmed_municipalities_map(local_data, last_n_days):
		local_data_most_recent_date = local_data.date.max().date()
		latest_local_data = local_data.query('date == @local_data_most_recent_date')

		with open(utils.GEOJSON_FILE_PATH, encoding='utf-8') as json_file:
			geojson_layer = json.load(json_file)

		# import plotly.express as px

		fig = px.choropleth(
			latest_local_data,
			geojson=geojson_layer,
			color="confirmed",
			locations="municipality",
			featureidkey="properties.NAME_2",
			# scope="europe",
			width=1024,
			height=768,
			# projection="stereographic"
		)
		fig.update_geos(fitbounds="locations")
		# fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

		# fig.show()

		return fig
