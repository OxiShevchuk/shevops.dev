from extensions import db
from blueprints.faq.models import Faq  # import your model


def resort_order(): # Resorting after: 1) Adding a new FAQ; 2) Deleting a FAQ; 3) Changing sort_order position in the list
    faqs = Faq.query.order_by(Faq.sort_order, Faq.fid).all()
    next_order = 1
    for faq in faqs:
        if faq.sort_order != next_order:
            faq.sort_order = next_order
        next_order += 1
    db.session.commit()