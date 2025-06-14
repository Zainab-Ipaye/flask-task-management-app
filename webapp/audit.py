from webapp import db
from webapp.models import ActivityLog
from flask_login import current_user


def log_activity(action_desc):
    if current_user.is_authenticated:
        log = ActivityLog(user_id=current_user.id, action=action_desc)
        db.session.add(log)
        db.session.commit()


