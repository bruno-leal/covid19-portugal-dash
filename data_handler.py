import data_manipulation as dm
import utils

print("LOADING DATA...")
data = dm.load_data(utils.Source.GITHUB)
print("DATA LOADED.")

def get_all_data():
	return data

def get_national_data():
	return data['national_data']
	
def get_regional_data():
	return data['regional_data']

def get_local_data():
	return data['local_data']


def get_last_update():
	return data['national_data'].date.max().date()