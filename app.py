import os
from flask import Flask, render_template, url_for, redirect, request
from final import Restaurant

app = Flask(__name__)
env_config = os.getenv('APP_SETTINGS', 'config.ProductionConfig')
app.config.from_object(env_config)

def get_restaurants(max_Price, people, min_Price, cuisine, locality):
    ansh = Restaurant(max_Price, people, min_Price, cuisine, locality)
    Restaurant.rest(ansh)
    ans = ansh.rest_list
    ans = ans.to_dict()
    res = [value for value in ans.values()]
    return res


@app.route("/")
@app.route("/home", methods=['GET', 'POST'])
def home():
    return render_template('base.html')


@app.route("/search", methods=['GET', 'POST'])
def search():
    if request.args:
        people = int(request.args.get('guests'))
        min_Price = int(request.args.get('minBudget'))
        max_Price = int(request.args.get('maxBudget'))
        cuisine = request.args.get('cuisine')
        locality = request.args.get('locality')
        # to input values into html form
        input = {
            'guests': people,
            'minBudget': min_Price,
            'maxBudget': max_Price,
            'cuisine': cuisine,
            'locality': locality
        }
        restaurants = get_restaurants(max_Price, people, min_Price, [cuisine], [locality])
        return render_template('search.html', restaurants=restaurants, input=input )
    else:
        return redirect(url_for('home'))


if __name__ == '__main__':
    app.run()
