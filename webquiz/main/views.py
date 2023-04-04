from flask import Blueprint, redirect, render_template, url_for
from flask_login import login_required, current_user

main = Blueprint('main', __name__, template_folder='templates')

@main.route('/home')
@login_required
def home():
    if current_user.is_admin():
        return redirect(url_for('admin.home'))
    return render_template('home.html', user=current_user)
