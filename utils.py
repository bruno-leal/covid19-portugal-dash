import os
from enum import Enum


# local paths
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

MAIN_FILE_LOCAL_PATH = os.path.join(ROOT_DIR, '..', 'covid19-portugal-data/time_series_covid19_portugal.xlsx')
MUNICIPALITIES_FILE_LOCAL_PATH = os.path.join(ROOT_DIR, '..', 'covid19-portugal-data/time_series_covid19_portugal_confirmados_concelhos.xlsx')
MUNICIPALITIES_METADATA_FILE_LOCAL_PATH = os.path.join(ROOT_DIR, '..', 'covid19-portugal-data/portugal_municipalities.xlsx')
MUNICIPALITIES_GEOJSON_LIMITS_FILE_LOCAL_PATH = 'file:///' + os.path.join(ROOT_DIR, '..', 'covid19-portugal-data/portugal_municipalities.geojson')
MUNICIPALITIES_GEOJSON_CENTROIDS_FILE_LOCAL_PATH = 'file:///' + os.path.join(ROOT_DIR, '..', 'covid19-portugal-data/portugal_municipalities_points.geojson')

# github paths
MAIN_FILE_GITHUB_PATH = 'https://github.com/bruno-leal/covid19-portugal-data/blob/master/time_series_covid19_portugal.xlsx?raw=true'
MUNICIPALITIES_FILE_GITHUB_PATH = 'https://github.com/bruno-leal/covid19-portugal-data/blob/master/time_series_covid19_portugal_confirmados_concelhos.xlsx?raw=true'
MUNICIPALITIES_METADATA_FILE_GITHUB_PATH = 'https://github.com/bruno-leal/covid19-portugal-data/blob/master/portugal_municipalities.xlsx?raw=true'
MUNICIPALITIES_GEOJSON_LIMITS_FILE_GITHUB_PATH = 'https://github.com/bruno-leal/covid19-portugal-data/raw/master/portugal_municipalities.geojson'
MUNICIPALITIES_GEOJSON_CENTROIDS_FILE_GITHUB_PATH = 'https://github.com/bruno-leal/covid19-portugal-data/raw/master/portugal_municipalities_points.geojson'


class Source(Enum):
	LOCAL = 1
	GITHUB = 2

class GeoJSONType(Enum):
	LIMITS = 1
	CENTROIDS = 2


def get_main_file_path(source):
	return MAIN_FILE_LOCAL_PATH if source == Source.LOCAL else MAIN_FILE_GITHUB_PATH

def get_municipalities_file_path(source):
	return MUNICIPALITIES_FILE_LOCAL_PATH if source == Source.LOCAL else MUNICIPALITIES_FILE_GITHUB_PATH

def get_municipalities_metadata_file_path(source):
	return MUNICIPALITIES_METADATA_FILE_LOCAL_PATH if source == Source.LOCAL else MUNICIPALITIES_METADATA_FILE_GITHUB_PATH

def get_municipalities_geojson_limits_file_path(source):
	return MUNICIPALITIES_GEOJSON_LIMITS_FILE_LOCAL_PATH if source == Source.LOCAL else MUNICIPALITIES_GEOJSON_LIMITS_FILE_GITHUB_PATH

def get_municipalities_geojson_centroids_file_path(source):
	return MUNICIPALITIES_GEOJSON_CENTROIDS_FILE_LOCAL_PATH if source == Source.LOCAL else MUNICIPALITIES_GEOJSON_CENTROIDS_FILE_GITHUB_PATH

def get_municipalities_geojson_file_path(source, layer_type):
	return get_municipalities_geojson_limits_file_path(source) if layer_type == GeoJSONType.LIMITS else get_municipalities_geojson_centroids_file_path(source)
