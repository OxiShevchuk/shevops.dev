from flask import render_template, request, redirect, url_for, jsonify
from sqlalchemy import func
from blueprints.faq.models import Faq
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
    faqs = Faq.query.order_by(Faq.sort_order, Faq.fid).all()
    return render_template('admin/dashboard.html', services=services, faqs=faqs, user=current_user)


@admin_bp.route('/faqs')
@login_required
def faqs():
    faqs = Faq.query.order_by(Faq.sort_order, Faq.fid).all()
    return render_template('admin/faq.html', faqs=faqs, user=current_user)

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


@admin_bp.route('/addfaq', methods=['POST'])
@login_required
def add_faq():
    title = html.escape(request.form['title'])
    desc = html.escape(request.form['desc'])
    new_faq = Faq(sort_order=None, title=title, description=desc)
    db.session.add(new_faq)
    db.session.commit()
    resort_order() # Resorting after: 1) Adding a new FAQ; 2) Deleting a FAQ; 3) Changing orders
    return redirect(url_for('admin.dashboard') + "#faq")


@admin_bp.route('/editfaq/<int:id>', methods=['POST'])
@login_required
def edit_faq(id):
    faq = Faq.query.get_or_404(id)
    faq.title = html.escape(request.form['title'])
    faq.description = html.escape(request.form['desc'])
    db.session.commit()
    return redirect(url_for('admin.dashboard') + "#faq")


@admin_bp.route('/deletefaq/<int:id>', methods=['POST'])
@login_required
def delete_faq(id):
    faq = Faq.query.get_or_404(id)
    db.session.delete(faq)
    db.session.commit()
    resort_order() # Resorting after: 1) Adding a new FAQ; 2) Deleting a FAQ; 3) Changing sort_order position in the list
    return redirect(url_for('admin.dashboard') + "#faq")


@admin_bp.route('/reorderfaq', methods=['POST'])
@login_required
def reorder_faq():
    data = request.get_json()
    faq_id = data.get('id')
    direction = data.get('direction')
    # Get current row
    current = db.session.query(Faq).with_for_update().filter(Faq.fid==faq_id).one()
    
    resort_order() # Resorting after: 1) Adding a new FAQ; 2) Deleting a FAQ; 3) Changing sort_order position in the list
    # return jsonify({"success": True})

    # Get the current faq
    faq = Faq.query.get(faq_id)
    
    # If there is no such id
    if not faq: 
        db.session.rollback()
        return jsonify({"error": "Faq not found"}), 404 
    
    # If the admin is trying to move the first row up, or the last one down
    faq_len = db.session.query(Faq).count()
    if (current.sort_order == 1 and direction == "up") or (current.sort_order == faq_len and direction == "down"):
        db.session.rollback()
        return jsonify({"error": "Cannot move further"}), 404
    
    if direction == 'up':
        neighbor = db.session.query(Faq).with_for_update().filter(Faq.sort_order==current.sort_order - 1).one()
    elif direction == 'down':
        neighbor = db.session.query(Faq).with_for_update().filter(Faq.sort_order==current.sort_order + 1).one()
    else:
        db.session.rollback()
        return jsonify({"error": "Invalid direction"}), 400
    
    current.sort_order, neighbor.sort_order = neighbor.sort_order, current.sort_order
    db.session.commit()
    return jsonify({"success": True}) 
