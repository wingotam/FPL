import os
from flask import Flask, render_template, request
from get_score import get_score

get_score_ = get_score()
app = Flask(__name__)

@app.route('/')
def index():
    selected_entry = request.args.get('selected_entry', None)
    data = get_score_.get_data()
    if selected_entry is None:
        selected_entry = [item['entry_name'] for item in data]
    return render_template('index.html', data=data, selected_entry=selected_entry)

if __name__ == '__main__':
    app.run(debug=True)