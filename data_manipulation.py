import pandas as pd
import datetime

import utils


#################################################################################
#   FUNCTION read_and_clean_main_data                                           #
#   - Reads and cleans data from the main file, containing national and 		#
# 		regional values.                                 						#
#################################################################################

def read_and_clean_main_data(source):
	print('Reading values from main file...')

	# read data
	raw_data = pd.read_excel(utils.get_main_file_path(source))

	# rename columns
	data = raw_data.rename(
		columns = {
			'Data (de fecho dos dados)': 'date',
			'Região': 'region',
			'Casos suspeitos': 'suspected',
			'Casos confirmados': 'confirmed',
			'Casos infirmados': 'unconfirmed',
			'Aguardam resultado laboratorial': 'pending_analysis',
			'Casos recuperados': 'recovered',
			'Óbitos': 'dead',
			'Casos internados': 'hospitalized',
			'Casos internados em UCI': 'hospitalized_icu',
			'Contactos em vigilância': 'vigilance'
		}
	)

	# change date format
	data = data.assign(
		data = pd.to_datetime(data.date)
	)

	# divide data into national (total) and regional
	national_data = data.query('region == "Total"')
	regional_data = data.query('region not in ["Total", "Estrangeiro"]')

	# clean unnecessary (empty) data from regional data frame
	regional_data = regional_data.drop(
		columns=['suspected', 'unconfirmed', 'pending_analysis', 'recovered', 'hospitalized', 'hospitalized_icu', 'vigilance']
	)

	print ('Done.')

	# return cleaned data
	return {
		'national_data': national_data,
		'regional_data': regional_data
	}


#################################################################################
#   FUNCTION read_and_clean_local_data											#
#   - Reads and cleans data from the file containing data at the local	 		#
# 		(municipalities) level.                            						#
#################################################################################

def read_and_clean_local_data(source):
	print('Reading values from municipalities file...')

	# read data
	raw_data = pd.read_excel(
		utils.get_municipalities_file_path(source),
		dtype={'codigo': str}  # keep leading zeros
	)

	# remove unnecessary columns
	data = raw_data.drop(columns=['distrito_ra'])

	# rename columns
	data = data.rename(
		columns={
			'codigo': 'code',
			'concelho': 'municipality',
			'data': 'date'
		}
	)

	# transform data into tidy format
	data = data.melt(
		id_vars=['code','municipality'],
		var_name='date',
		value_name='confirmed'
	)

	# change date format
	data = data.assign(
		date=pd.to_datetime(data.date, format='%Y/%m/%d')
	)

	# sort data
	data = data.sort_values(
		['code', 'date']
	).reset_index()

	print ('Done.')

	# return cleaned data
	return data


#################################################################################
#   FUNCTION read_and_clean_data												#
#   - Main function, that calls 'read_and_clean_main_data' and					#
# 		 'read_and_clean_local_data' to get all data at once.					#
#################################################################################

def read_and_clean_data(source):
	main_data = read_and_clean_main_data(source)
	local_data = read_and_clean_local_data(source)

	return {
		'national_data': main_data['national_data'],
		'regional_data': main_data['regional_data'],
		'local_data': local_data
	}


#################################################################################
#   FUNCTION boost_national_data												#
#   - Calculates new composed variables for the national dataframe.				#
#################################################################################

def boost_national_data(data):
	new_data = data.assign(closed=data.recovered + data.dead)
	new_data = new_data.assign(active=new_data.confirmed - new_data.closed)

	new_data = new_data.assign(new_suspected=new_data.groupby(['region']).suspected.diff())
	new_data = new_data.assign(new_confirmed=new_data.groupby(['region']).confirmed.diff())
	new_data = new_data.assign(new_unconfirmed=new_data.groupby(['region']).unconfirmed.diff())
	new_data = new_data.assign(new_tested=new_data.new_confirmed + new_data.new_unconfirmed)
	new_data = new_data.assign(new_recovered=new_data.groupby(['region']).recovered.diff())
	new_data = new_data.assign(new_dead=new_data.groupby(['region']).dead.diff())

	new_data = new_data.assign(new_suspected_per=new_data.groupby(['region']).suspected.pct_change())
	new_data = new_data.assign(new_confirmed_per=new_data.groupby(['region']).confirmed.pct_change())
	new_data = new_data.assign(new_unconfirmed_per=new_data.groupby(['region']).unconfirmed.pct_change())
	# new_data = new_data.assign(new_tested_per = new_data.new_confirmed + new_data.new_unconfirmed)
	new_data = new_data.assign(new_recovered_per=new_data.groupby(['region']).recovered.pct_change())
	new_data = new_data.assign(new_dead_per=new_data.groupby(['region']).dead.pct_change())

	new_data = new_data.assign(hospitalized_infirmary=new_data.hospitalized - new_data.hospitalized_icu)
	new_data = new_data.assign(domiciliary_recovery=new_data.confirmed - new_data.recovered - new_data.dead - new_data.hospitalized)

	new_data = new_data.assign(lethality_rate=new_data.dead / new_data.confirmed)
	new_data = new_data.assign(recovery_rate=new_data.recovered / new_data.confirmed)
	new_data = new_data.assign(hospitalization_rate=new_data.hospitalized / new_data.confirmed)
	new_data = new_data.assign(hospitalization_icu_rate=new_data.hospitalized_icu / new_data.confirmed)

	new_data = new_data.assign(new_confirmed_avg_7=new_data.new_confirmed.rolling(7).mean())
	new_data = new_data.assign(new_confirmed_per_avg_7=new_data.new_confirmed_per.rolling(7).mean())

	new_data = new_data.assign(new_dead_avg_7=new_data.new_dead.rolling(7).mean())
	new_data = new_data.assign(new_dead_per_avg_7=new_data.new_dead_per.rolling(7).mean())

	return new_data


#################################################################################
#   FUNCTION boost_regional_data												#
#   - Calculates new composed variables for the regional dataframe.				#
#################################################################################

def boost_regional_data(regional_data, national_data):
	# Variables calculated directly from the data frame
	new_regional_data = regional_data.assign(new_confirmed = regional_data.groupby(['region']).confirmed.diff())
	new_regional_data = new_regional_data.assign(new_dead = new_regional_data.groupby(['region']).dead.diff())

	new_regional_data = new_regional_data.assign(new_confirmed_per = new_regional_data.groupby(['region']).confirmed.pct_change())
	new_regional_data = new_regional_data.assign(new_dead_per = new_regional_data.groupby(['region']).dead.pct_change())

	new_regional_data = new_regional_data.assign(lethality_rate = new_regional_data.dead / new_regional_data.confirmed)

	# Variables calculated by comparison with national data
	data_norte = new_regional_data.query('region == "Norte"').reset_index()
	data_norte = data_norte.assign(confirmed_per = data_norte.confirmed.divide(national_data.reset_index().confirmed))
	data_norte = data_norte.assign(dead_per = data_norte.dead.divide(national_data.reset_index().dead))

	data_centro = new_regional_data.query('region == "Centro"').reset_index()
	data_centro = data_centro.assign(confirmed_per = data_centro.confirmed.divide(national_data.reset_index().confirmed))
	data_centro = data_centro.assign(dead_per = data_centro.dead.divide(national_data.reset_index().dead))

	data_lvt = new_regional_data.query('region == "LVT"').reset_index()
	data_lvt = data_lvt.assign(confirmed_per = data_lvt.confirmed.divide(national_data.reset_index().confirmed))
	data_lvt = data_lvt.assign(dead_per = data_lvt.dead.divide(national_data.reset_index().dead))

	data_alentejo = new_regional_data.query('region == "Alentejo"').reset_index()
	data_alentejo = data_alentejo.assign(confirmed_per = data_alentejo.confirmed.divide(national_data.reset_index().confirmed))
	data_alentejo = data_alentejo.assign(dead_per = data_alentejo.dead.divide(national_data.reset_index().dead))

	data_algarve = new_regional_data.query('region == "Algarve"').reset_index()
	data_algarve = data_algarve.assign(confirmed_per = data_algarve.confirmed.divide(national_data.reset_index().confirmed))
	data_algarve = data_algarve.assign(dead_per = data_algarve.dead.divide(national_data.reset_index().dead))

	data_acores = new_regional_data.query('region == "Açores"').reset_index()
	data_acores = data_acores.assign(confirmed_per = data_acores.confirmed.divide(national_data.reset_index().confirmed))
	data_acores = data_acores.assign(dead_per = data_acores.dead.divide(national_data.reset_index().dead))

	data_madeira = new_regional_data.query('region == "Madeira"').reset_index()
	data_madeira = data_madeira.assign(confirmed_per = data_madeira.confirmed.divide(national_data.reset_index().confirmed))
	data_madeira = data_madeira.assign(dead_per = data_madeira.dead.divide(national_data.reset_index().dead))

	new_regional_data = pd.concat([data_norte, data_centro, data_lvt, data_alentejo, data_algarve, data_acores, data_madeira])
	new_regional_data = new_regional_data.sort_values(['data', 'region'])

	return new_regional_data


#################################################################################
#   FUNCTION boost_local_data													#
#   - Calculates new composed variables for the local (municipalities)			#
# 		dataframe.																#
#################################################################################

def boost_local_data(local_data):
	new_local_data = local_data.assign(new_confirmed = local_data.groupby(['municipality']).confirmed.diff())
	new_local_data = new_local_data.assign(
		new_confirmed_per = round(
			new_local_data.groupby(['municipality']).confirmed.pct_change() * 100
			, 2
		)
	)

	new_local_data = new_local_data.assign(new_confirmed_avg_7=round(new_local_data.new_confirmed.rolling(7).mean(), 2))
	new_local_data = new_local_data.assign(new_confirmed_per_avg_7=round(new_local_data.new_confirmed_per.rolling(7).mean(), 2))

	return new_local_data


#################################################################################
#   FUNCTION get_all_data														#
#   - Loads all info and boosts the obtained data.								#
#################################################################################

def load_data(source):
	data = read_and_clean_data(source)

	national_data = data['national_data']
	regional_data = data['regional_data']
	local_data = data['local_data']

	national_data = boost_national_data(national_data)
	regional_data = boost_regional_data(regional_data, national_data)
	local_data = boost_local_data(local_data)

	return {
		'national_data': national_data,
		'regional_data': regional_data,
		'local_data': local_data
	}
