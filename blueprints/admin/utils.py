from extensions import db
from blueprints.why_choose_me.models import Reason  # import your model


def resort_order(): # Resorting after: 1) Adding a new FAQ; 2) Deleting a FAQ; 3) Changing sort_order position in the list
    reasons = Reason.query.order_by(Reason.sort_order, Reason.id).all()
    next_order = 1
    for reason in reasons:
        if reason.sort_order != next_order:
            reason.sort_order = next_order
        next_order += 1
    db.session.commit()