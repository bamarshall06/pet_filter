from flask import Blueprint, render_template, request, url_for, redirect, flash
from app.db_connect import get_db
from app.functions import filter_pets

pets = Blueprint('pets', __name__)


@pets.route('/pet', methods=['GET', 'POST'])
def pet():
    db = get_db()
    cursor = db.cursor()

    # Fetch all pet types for the form (move this to ensure it is always available)
    cursor.execute('SELECT * FROM pet_type')
    all_pet_types = cursor.fetchall()

    all_pets = []

    # Handle POST request to filter pets
    if request.method == 'POST' and 'filter_pet_type_id' in request.form:
        filter_pet_type_id = request.form['filter_pet_type_id']
        all_pets = filter_pets(filter_pet_type_id)
    elif request.method == 'POST' and 'pet_name' in request.form:
        pet_name = request.form['pet_name']
        pet_type_id = request.form['pet_type_id']
        gender = request.form['gender']

        # Insert the new pet info into the database
        cursor.execute('INSERT INTO pet (pet_name, pet_type_id, gender) VALUES (%s, %s, %s)',
                       (pet_name, pet_type_id, gender))
        db.commit()
        return redirect(url_for('pets.pet'))
    else:
        cursor.execute('SELECT p.pet_id, p.pet_name, pt.pet_type_name, p.gender FROM pet p JOIN pet_type pt '
                       'ON p.pet_type_id = pt.pet_type_id')
        all_pets = cursor.fetchall()

    return render_template('pets.html', all_pets=all_pets, all_pet_types=all_pet_types)


@pets.route('/update_pet/<int:pet_id>', methods=['GET', 'POST'])
def update_pet(pet_id):
    db = get_db()
    cursor = db.cursor()

    if request.method == 'POST':
        # Update the pet's details
        pet_name = request.form['pet_name']
        pet_type_id = request.form['pet_type_id']
        gender = request.form['gender']

        cursor.execute('UPDATE pet SET pet_name = %s, pet_type_id = %s, gender = %s WHERE pet_id = %s',
                       (pet_name, pet_type_id, gender, pet_id))
        db.commit()

        return redirect(url_for('pets.pet'))

    # GET method: fetch pet's current data for pre-populating the form
    cursor.execute('SELECT * FROM pet WHERE pet_id = %s', (pet_id,))
    current_pet = cursor.fetchone()

    # Fetch all pet types for the form
    cursor.execute('SELECT * FROM pet_type')
    all_pet_types = cursor.fetchall()

    return render_template('update_pet.html', current_pet=current_pet, all_pet_types=all_pet_types)


@pets.route('/delete_pet/<int:pet_id>', methods=['POST'])
def delete_pet(pet_id):
    db = get_db()
    cursor = db.cursor()

    # Delete the pet
    cursor.execute('DELETE FROM pet WHERE pet_id = %s', (pet_id,))
    db.commit()
    return redirect(url_for('pets.pet'))
