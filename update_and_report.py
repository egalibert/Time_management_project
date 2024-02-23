from report_handler import all_rows, write_to_file, get_average_hours_per_day_per_consultant
from report_uploader import export_data
from input_handler import validate_input
from extra_table_creation import extra_table_main
from flask import Flask, request

app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
	return {"index": True}

# When /report is used  fetches data using all_rows(), validates it, updates the file and exports it to blob container.
@app.route('/report', methods=['GET'])
def post_working_hours():
	data = all_rows()
	# print(data)

	# Validate and process input data and updates the second table before writing to file
	if validate_input(data):
		extra_table_main()
		write_to_file(data)
		export_data()
		return {"message": "Data successfully inserted into the database"}
	else:
		return {"error": "Invalid input data"}, 400
	
if __name__ == '__main__':
	app.run(debug=True)