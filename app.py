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
    return redirect(url_for('get_creatures'))


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
        'location_name':request.form.get('location_name'),
        'creature_description': request.form.get('creature_description'),
        'due_date': request.form.get('due_date'),
        'is_urgent':request.form.get('is_urgent')
    })
    return redirect(url_for('get_creatures'))
    
"""   

@app.route('/delete_creature/<creature_id>')
def delete_creature(creature_id):
    mongo.db.creatures.remove({'_id': ObjectId(creature_id)})
    return redirect(url_for('get_creatures'))
    
@app.route('/get_locations')
def get_locations():
    return render_template('locations.html',
                           locations=mongo.db.locations.find())
                           
@app.route('/edit_location/<location_id>')
def edit_location(location_id):
    return render_template('editlocation.html',
                           location=mongo.db.locations.find_one(
                           {'_id': ObjectId(location_id)}))

@app.route('/update_location/<location_id>', methods=['POST'])
def update_location(location_id):
    mongo.db.locations.update(
        {'_id': ObjectId(location_id)},
        {'location_name': request.form.get('location_name')})
    return redirect(url_for('get_locations'))
    
@app.route('/delete_location/<location_id>')
def delete_location(location_id):
    mongo.db.locations.remove({'_id': ObjectId(location_id)})
    return redirect(url_for('get_locations'))
    
@app.route('/insert_location', methods=['POST'])
def insert_location():
    location_doc = {'location_name': request.form.get('location_name')}
    mongo.db.locations.insert_one(location_doc)
    return redirect(url_for('get_locations'))
    
"""

if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)