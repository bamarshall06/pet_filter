from app.db_connect import get_db

# Updated filter function in functions.py
def filter_pets(pet_type_id):
    db = get_db()
    cursor = db.cursor()

    # SQL query to filter pets by pet type, including pet type details
    query = ('SELECT p.pet_id, p.pet_name, pt.pet_type_name, p.gender FROM pet p '
             'JOIN pet_type pt ON p.pet_type_id = pt.pet_type_id '
             'WHERE p.pet_type_id = %s')
    cursor.execute(query, (pet_type_id,))
    pets = cursor.fetchall()

    return pets