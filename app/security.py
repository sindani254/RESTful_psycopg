from werkzeug.security import safe_str_cmp
from user import User


def authenticate(username, password):
    user = User.find_by_username(username)
    if user and safe_str_cmp(user.password, password):
        return user


def identity(payload):
    user_id = payload['identity']
    return User.find_by_id(user_id)


conn = connect_db()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    try:
        query = "SELECT * FROM parcels ORDER BY id"
        cursor.execute(query)
    except Exception:
        return jsonify({'error': "error fetching parcels"})

    result = cursor.fetchall()
    conn.close()

    if result:
        parcels = [dict(id=row[0], name=row[1], qty=row[2], price=row[3]) for row in result]
        return jsonify({'parcels': parcels})
    else:
        return jsonify({'msg': "no items were found"})
