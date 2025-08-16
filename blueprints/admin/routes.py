from flask import render_template, request, redirect, url_for
from blueprints.services.models import Service
from sqlalchemy import func
from blueprints.faq.models import Faq
from extensions import db
from . import admin_bp
import html

@admin_bp.route('/')
def dashboard():
    services = Service.query.all()
    faqs = Faq.query.all()
    return render_template('admin/dashboard.html', services=services, faqs=faqs)


@admin_bp.route('/addservice', methods=['POST'])
def add_service():
    icon = html.escape(request.form['icon'])
    name = html.escape(request.form['name'])
    desc = html.escape(request.form['desc'])
    new_service = Service(icon=icon, name=name, description=desc)
    db.session.add(new_service)
    db.session.commit()
    return redirect(url_for('admin.dashboard'))


@admin_bp.route('/editservice/<int:id>', methods=['POST'])
def edit_service(id):
    service = Service.query.get_or_404(id)
    service.icon = html.escape(request.form['icon'])
    service.name = html.escape(request.form['name'])
    service.description = html.escape(request.form['desc'])
    db.session.commit()
    return redirect(url_for('admin.dashboard'))


@admin_bp.route('/deleteservice/<int:id>', methods=['POST'])
def delete_service(id):
    service = Service.query.get_or_404(id)
    db.session.delete(service)
    db.session.commit()
    return redirect(url_for('admin.dashboard'))



@admin_bp.route('/addfaq', methods=['POST'])
def add_faq():
    max_order = db.session.query(func.max(Faq.order)).scalar()
    if max_order is None:
        order = 1
    else:
        order = int(max_order) + 1
    print(max_order)
    title = html.escape(request.form['title'])
    desc = html.escape(request.form['desc'])
    new_faq = Faq(order=order, title=title, description=desc)
    db.session.add(new_faq)
    db.session.commit()
    return redirect(url_for('admin.dashboard'))