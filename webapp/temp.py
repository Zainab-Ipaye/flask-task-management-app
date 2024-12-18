from werkzeug.security import generate_password_hash
from webapp import db
from webapp.models import User

# Retrieve all users from the database
users = User.query.all()

# Loop through each user and hash their password
for user in users:
    if not user.password.startswith('pbkdf2:sha256'):  # Only hash passwords that aren't already hashed
        hashed_password = generate_password_hash(user.password)
        user.password = hashed_password
        db.session.commit()

print("Passwords have been updated and hashed successfully.")
