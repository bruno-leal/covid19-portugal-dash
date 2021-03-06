import data_manipulation as dm
import utils


print("LOADING DATA...")
data = dm.load_data(utils.Source.GITHUB)
# municipalities_limits_geojson_layer = dm.load_municipalites_geojson(utils.Source.LOCAL, utils.GeoJSONType.LIMITS) # Loading time is about 30 times slower than the centroids map
municipalities_centroids_geojson_layer = dm.load_municipalites_geojson(utils.Source.GITHUB, utils.GeoJSONType.CENTROIDS)
print("DATA LOADED.")


def get_all_data():
	return data

def get_national_data():
	return data['national_data']
	
def get_regional_data():
	return data['regional_data']

def get_local_data():
	return data['local_data']


def get_last_update_date():
	return data['national_data'].date.max().date()

def get_latest_national_data():
	latest_date = get_last_update_date()
	return data['national_data'].query('date == @latest_date')

def get_latest_local_data():
	latest_date = get_last_update_date()
	return data['local_data'].query('date == @latest_date')


def get_municipalities_geojson_layer(layer_type):
	return municipalities_limits_geojson_layer if layer_type == utils.GeoJSONType.LIMITS else municipalities_centroids_geojson_layer