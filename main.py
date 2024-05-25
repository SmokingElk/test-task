from flask import Flask, request, render_template, abort
from plots import create_counts_plot, create_scores_plot
from json import dumps
from gevent import sleep
from gevent.pywsgi import WSGIServer
import os
from process_data import (
	load_data, 
	create_stat_table, 
	form_tables_with_required_people, 
	calc_ranges_common, 
	reshape_counts_to_show, 
	DIR_CODES_COL, 
	COUNTS_REQUIRED_COL
)

DATA_PATH = "data"
OUT_PATH = "out"
HOST = "127.0.0.1"
PORT = 3000

app = Flask(__name__, static_folder="static", template_folder="static")
ui_server = WSGIServer((HOST, PORT), app, log=open(os.devnull, "w"))

source_data = load_data(DATA_PATH)
ranges = calc_ranges_common(source_data)


@app.route('/', methods=['GET'])
def root():
	return render_template(
		"index.html", 
		b_min=ranges["b_min"], 
		b_max=ranges["b_max"], 
		p_min=ranges["p_min"], 
		p_max=ranges["p_max"]
	)


@app.route('/table_counts', methods=['POST'])
def table_counts():
	try:
		params = request.get_json()

		# при необходимости можно принимать разные параметры фильтрации для разных направлений
		params_dict = {}
		ranges_dict = {}
		for i in source_data.keys():
			params_dict[i] = params
			ranges_dict[i] = ranges

		stat_table = create_stat_table(source_data, params_dict, ranges_dict)

		stat_table[[DIR_CODES_COL, COUNTS_REQUIRED_COL]].to_excel(f"{OUT_PATH}/common.xlsx")
		
		counts_save_path = "static/counts_spread.png"
		counts_to_show = reshape_counts_to_show(source_data, stat_table)

		create_counts_plot(counts_to_show, counts_save_path)

		score_save_path = "static/average_score_spread.png"

		create_scores_plot(stat_table, score_save_path)

		return dumps({"counts_spread": counts_save_path, "average_score_spread": score_save_path})
	
	except ValueError:
		return abort(400)


@app.route('/people_required_for_every_table', methods=['POST'])
def tables_with_people():
	try:
		params = request.get_json()

		# при необходимости можно принимать разные параметры фильтрации для разных направлений
		params_dict = {}
		ranges_dict = {}
		for i in source_data.keys():
			params_dict[i] = params
			ranges_dict[i] = ranges

		form_tables_with_required_people(source_data, params_dict, ranges_dict, OUT_PATH)

		return "ok"   

	except ValueError:
		return abort(400)


if __name__ == "__main__":
	print(f"UI is running on http://{HOST}:{PORT}")
	ui_server.start()

	while True:
		sleep(60)