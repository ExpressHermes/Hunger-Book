from flask import Flask, render_template, url_for, flash, redirect, request
from final import Restaurant
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = '4574ff4bc5204581bbcc7c773927a734'

def calc(max_Price, people, min_Price, cuisine, locality):
    ansh = Restaurant(max_Price, people, min_Price, cuisine, locality)
    Restaurant.rest(ansh)
    ans = ansh.rest_list
    ans = ans.to_dict()
    res = [value for value in ans.values()]
    return res


@app.route("/")
@app.route("/home", methods=['GET', 'POST'])
def home():
    return render_template('home.html')


@app.route("/search", methods=['GET', 'POST'])
def search():
    if request.args:
        people = int(request.args.get('people'))
        min_Price = int(request.args.get('min_Price'))
        max_Price = int(request.args.get('max_Price'))
        cuisine = request.args.get('cuisine')
        locality = request.args.get('locality')
        res = calc(max_Price, people, min_Price, [cuisine], [locality])
        return render_template('search.html', title='Search', restaurants=res)
    else:
        return redirect(url_for('home'))

@app.route("/errorP")
def errorP():
    return '<h1>Error</h1>'


if __name__ == '__main__':
    app.run(debug=True)
