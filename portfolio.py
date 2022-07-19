import csv
import os
from flask import Flask, render_template, request, redirect

app = Flask(__name__)


def get_datafile_path(data_file):
    """
    Return the path of provided database file in web server.
    """
    return os.path.join(app.root_path, 'data', data_file)


def is_new_file(file_path):
    """
    Check if file is a new file. Either not existing or with zero size.
    """
    return not os.path.exists(file_path) or not os.path.getsize(file_path)


def save_to_csv(data):
    """
    Save submitted data to the CSV file.
    """
    csv_file = get_datafile_path('database.csv')
    is_new = is_new_file(csv_file)
    with open(csv_file, 'a', newline='') as f:
        field_names = data.keys()
        # For variety use '|' as field delimiter
        writer = csv.DictWriter(f, fieldnames=field_names,
                                delimiter='|',
                                quoting=csv.QUOTE_MINIMAL)
        if is_new:
            writer.writeheader()
        writer.writerow(data)


def save_to_txt(data):
    """
    Save submitted data to the tab delimited text file.
    """
    txt_file = get_datafile_path('database.txt')
    is_new = is_new_file(txt_file)

    def write_row(row):
        file.write('{}\n'.format('\t'.join(row)))

    with open(txt_file, 'a', newline='') as file:
        if is_new:
            write_row(data.keys())
        write_row(data.values())


@app.route("/")
def route_main():
    """
    Default website root handler
    """
    return render_template('index.html')


@app.route("/<string:page_name>")
def page_about(page_name):
    """
    Page name handler for any page
    """
    return render_template(page_name)


@app.route('/submit_form', methods=['GET', 'POST'])
def submit_form():
    """
    # Contact form submit handler
    """
    # Grab submitted form data
    if request.method == 'POST':
        # It is possible to read specific form fields one by one
        """
        name = request.form['name']
        email = request.form['email']
        subject = request.form['subject']
        message = request.form['message']
        """
        # However more efficient way is to read all submitted fields into a dictionary
        data = request.form.to_dict()
        # Save submitted data. For variety - to both CSV and text files
        save_to_csv(data)
        save_to_txt(data)
        # Redirect to submit affirmation page
        return redirect('thank_you.html')
    else:
        return 'Something went wrong. Try again.'
