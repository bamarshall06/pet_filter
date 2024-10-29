from flask import Blueprint, render_template, request, url_for, redirect, flash
from app.db_connect import get_db

pet_types = Blueprint('pet_types', __name__)

@pet_types.route('/pet_type', methods=['GET', 'POST'])
def pet_type():
    db = get_db()
    cursor = db.cursor()

    # Handle POST request to add a new pet type
    if request.method == 'POST':
        pet_type_name = request.form['pet_type_name']

        # Insert the new pet type into the database
        cursor.execute('INSERT INTO pet_type (pet_type_name) VALUES (%s)', (pet_type_name,))
        db.commit()
        return redirect(url_for('pet_types.pet_type'))

    # Handle GET request to display all pet types
    cursor.execute('SELECT * FROM pet_type')
    all_pet_types = cursor.fetchall()
    return render_template('pet_types.html', all_pet_types=all_pet_types)

@pet_types.route('/update_pet_type/<int:pet_type_id>', methods=['GET', 'POST'])
def update_pet_type(pet_type_id):
    db = get_db()
    cursor = db.cursor()

    if request.method == 'POST':
        # Update the pet type's details
        pet_type_name = request.form['pet_type_name']

        cursor.execute('UPDATE pet_type SET pet_type_name = %s WHERE pet_type_id = %s',
                       (pet_type_name, pet_type_id))
        db.commit()

        return redirect(url_for('pet_types.pet_type'))

    # GET method: fetch pet type's current data for pre-populating the form
    cursor.execute('SELECT * FROM pet_type WHERE pet_type_id = %s', (pet_type_id,))
    current_pet_type = cursor.fetchone()
    return render_template('update_pet_type.html', current_pet_type=current_pet_type)

@pet_types.route('/delete_pet_type/<int:pet_type_id>', methods=['POST'])
def delete_pet_type(pet_type_id):
    db = get_db()
    cursor = db.cursor()

    # Delete the pet type
    cursor.execute('DELETE FROM pet_type WHERE pet_type_id = %s', (pet_type_id,))
    db.commit()
    return redirect(url_for('pet_types.pet_type'))
