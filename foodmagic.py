from flask import Flask, request, render_template  # Import flask libraries
import def_diabetic
import def_glutenfree
import def_keto
import def_cholesterol
import def_sodium
import def_vegan
import def_vegetarian

app = Flask(__name__, template_folder="templates")


@app.route('/')
def hello_world():  # put application's code here
    return render_template('form_index.html')


@app.route('/classify', methods=['POST', 'GET'])
def classify_type():
    try:
        if request.method == 'POST':
            text = request.form['text']

            diet_types = request.form['diet_types']

            if diet_types == "diabetic":
                prediction = def_diabetic.get_similar_diabetic(text)
            elif diet_types == "gluten_free":
                prediction = def_glutenfree.get_similar_glutenfree(text)
            elif diet_types == "ketogenic":
                prediction = def_keto.get_similar_keto(text)
            elif diet_types == "vegetarian":
                prediction = def_vegetarian.get_similar_vegetarian(text)
            elif diet_types == "vegan":
                prediction = def_vegan.get_similar_vegan(text)
            elif diet_types == "low_sodium":
                prediction = def_sodium.get_similar_lowsodium(text)
            elif diet_types == "low_cholesterol":
                prediction = def_cholesterol.get_similar_lowcholesterol(text)

            headings = ('Food Name', 'Ingredients', 'Recipe', 'Cooking Time', 'Nutrition')
            data = tuple(prediction.values)
            print(data)

            return render_template('result_rec.html', headings=headings, data=data)

        else:
            render_template('result_rec.html')
    except:
        return 'Oops! This food is not in the recipes. Please go back.'


# Run the Flask server
if __name__ == '__main__':
    app.run(debug=True)
