import os
from enum import Enum


# local paths
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

MAIN_FILE_LOCAL_PATH = os.path.join(ROOT_DIR, '..', 'covid19-portugal-data/time_series_covid19_portugal.xlsx')
MUNICIPALITIES_FILE_LOCAL_PATH = os.path.join(ROOT_DIR, '..', 'covid19-portugal-data/time_series_covid19_portugal_confirmados_concelhos.xlsx')
GEOJSON_FILE_LOCAL_PATH = os.path.join(ROOT_DIR, '..', 'covid19-portugal-data/concelhos.min.geojson') # source: https://dados.gov.pt/pt/datasets/concelhos-de-portugal/

# github paths
MAIN_FILE_GITHUB_PATH = 'https://github.com/bruno-leal/covid19-portugal-data/blob/master/time_series_covid19_portugal.xlsx?raw=true'
MUNICIPALITIES_FILE_GITHUB_PATH = 'https://github.com/bruno-leal/covid19-portugal-data/blob/master/time_series_covid19_portugal_confirmados_concelhos.xlsx?raw=true'


class Source(Enum):
	LOCAL = 1
	GITHUB = 2

def get_main_file_path(source):
	return MAIN_FILE_LOCAL_PATH if source == Source.LOCAL else MAIN_FILE_GITHUB_PATH

def get_municipalities_file_path(source):
	return MUNICIPALITIES_FILE_LOCAL_PATH if source == Source.LOCAL else MUNICIPALITIES_FILE_GITHUB_PATH