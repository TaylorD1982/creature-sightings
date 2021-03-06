import os
from flask import Flask, render_template, redirect, request, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

app = Flask(__name__)
app.config["MONGO_DBNAME"] = 'creature_sightings'
app.config["MONGO_URI"] = 'mongodb+srv://root:Sweden123@myfirstcluster-8eedf.mongodb.net/creature_sightings?retryWrites=true&w=majority'

mongo = PyMongo(app)

@app.route('/')

@app.route('/get_creatures')
def get_creatures():
    return render_template("creatures.html", 
                           creatures=mongo.db.creatures.find())

@app.route('/add_creature')
def add_creature():
    return render_template('addcreature.html',
                           locations=mongo.db.locations.find())
                           
@app.route('/creatures_list')
def creature():
    return render_template('creatures_list.html',
                           locations=mongo.db.locations.find())
                           
@app.route('/location')
def location():
    return render_template('location.html')
                           
@app.route('/statistics')
def statistics():
    return render_template('statistics.html',
                           creatures=mongo.db.creatures.find())

@app.route('/insert_creature', methods=['POST'])
def insert_creature():
    creatures =  mongo.db.creatures
    creatures.insert_one(request.form.to_dict())
    return redirect(url_for('statistics'))


@app.route('/edit_creature/<creature_id>')
def edit_creature(creature_id):
    the_creature =  mongo.db.creatures.find_one({"_id": ObjectId(creature_id)})
    all_locations =  mongo.db.locations.find()
    return render_template('editcreature.html', creature=the_creature,
                           locations=all_locations)


@app.route('/update_creature/<creature_id>', methods=["POST"])
def update_creature(creature_id):
    creatures = mongo.db.creatures
    creatures.update( {'_id': ObjectId(creature_id)},
    {
        'creature_name':request.form.get('creature_name'),
        'location':request.form.get('location'),
        'comment': request.form.get('comment'),
        'date': request.form.get('date'),
        'time':request.form.get('time')
    })
    return redirect(url_for('statistics'))
  

@app.route('/delete_creature/<creature_id>')
def delete_creature(creature_id):
    mongo.db.creatures.remove({'_id': ObjectId(creature_id)})
    return redirect(url_for('statistics'))

if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)