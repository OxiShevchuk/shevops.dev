from flask import render_template, request, redirect, url_for, jsonify
from sqlalchemy import func
from blueprints.why_choose_me.models import Reason
from blueprints.services.models import Service
from extensions import db
from . import admin_bp
from .utils import resort_order
from flask_login import login_required, current_user
from blueprints.auth.utils import load_user
import html

@admin_bp.route('/')
@login_required
def dashboard():
    services = Service.query.all()
    reasons = Reason.query.order_by(Reason.sort_order, Reason.id).all()
    return render_template('admin/dashboard.html', services=services, reasons=reasons, user=current_user)


@admin_bp.route('/why-choose-me')
@login_required
def why_choose_me():
    reasons = Reason.query.order_by(Reason.sort_order, Reason.id).all()
    print(reasons)
    return render_template('admin/why-choose-me.html', reasons=reasons, user=current_user)

@admin_bp.route('/services')
@login_required
def services():
    services = Service.query.all()
    return render_template('admin/services.html', services=services, user=current_user)


@admin_bp.route('/addservice', methods=['POST'])
@login_required
def add_service():
    icon = html.escape(request.form['icon'])
    name = html.escape(request.form['name'])
    desc = html.escape(request.form['desc'])
    new_service = Service(icon=icon, name=name, description=desc)
    db.session.add(new_service)
    db.session.commit()
    return redirect(url_for('admin.dashboard'))


@admin_bp.route('/editservice/<int:id>', methods=['POST'])
@login_required
def edit_service(id):
    service = Service.query.get_or_404(id)
    service.icon = html.escape(request.form['icon'])
    service.name = html.escape(request.form['name'])
    service.description = html.escape(request.form['desc'])
    db.session.commit()
    return redirect(url_for('admin.dashboard'))


@admin_bp.route('/deleteservice/<int:id>', methods=['POST'])
@login_required
def delete_service(id):
    service = Service.query.get_or_404(id)
    db.session.delete(service)
    db.session.commit()
    return redirect(url_for('admin.dashboard'))


@admin_bp.route('/addwhychooseme', methods=['POST'])
@login_required
def add_why_choose_me():
    title = html.escape(request.form['title'])
    desc = html.escape(request.form['desc'])
    new_whychooseme = Reason(sort_order=None, title=title, description=desc)
    db.session.add(new_whychooseme)
    db.session.commit()
    resort_order() # Resorting after: 1) Adding a new FAQ; 2) Deleting a FAQ; 3) Changing orders
    return redirect(url_for('admin.dashboard') + "#why-choose-me")


@admin_bp.route('/editwhychooseme/<int:id>', methods=['POST'])
@login_required
def edit_why_choose_me(id):
    reason = Reason.query.get_or_404(id)
    reason.title = html.escape(request.form['title'])
    reason.description = html.escape(request.form['desc'])
    db.session.commit()
    return redirect(url_for('admin.dashboard') + "#why-choose-me")


@admin_bp.route('/deletewhychooseme/<int:id>', methods=['POST'])
@login_required
def delete_why_choose_me(id):
    reason = Reason.query.get_or_404(id)
    db.session.delete(reason)
    db.session.commit()
    resort_order() # Resorting after: 1) Adding a new FAQ; 2) Deleting a FAQ; 3) Changing sort_order position in the list
    return redirect(url_for('admin.dashboard') + "#why-choose-me")


@admin_bp.route('/reorderwhychooseme', methods=['POST'])
@login_required
def reorder_faq():
    data = request.get_json()
    reason_id = data.get('id')
    direction = data.get('direction')
    # Get current row
    current = db.session.query(Reason).with_for_update().filter(Reason.id==reason_id).one()
    
    resort_order() # Resorting after: 1) Adding a new FAQ; 2) Deleting a FAQ; 3) Changing sort_order position in the list
    # return jsonify({"success": True})

    # Get the current faq
    reason = Reason.query.get(reason_id)
    
    # If there is no such id
    if not reason: 
        db.session.rollback()
        return jsonify({"error": "Reason not found"}), 404 
    
    # If the admin is trying to move the first row up, or the last one down
    reason_len = db.session.query(Reason).count()
    if (current.sort_order == 1 and direction == "up") or (current.sort_order == reason_len and direction == "down"):
        db.session.rollback()
        return jsonify({"error": "Cannot move further"}), 404
    
    if direction == 'up':
        neighbor = db.session.query(Reason).with_for_update().filter(Reason.sort_order==current.sort_order - 1).one()
    elif direction == 'down':
        neighbor = db.session.query(Reason).with_for_update().filter(Reason.sort_order==current.sort_order + 1).one()
    else:
        db.session.rollback()
        return jsonify({"error": "Invalid direction"}), 400
    
    current.sort_order, neighbor.sort_order = neighbor.sort_order, current.sort_order
    db.session.commit()
    return jsonify({"success": True}) 
