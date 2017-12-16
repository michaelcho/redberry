import os
import functools
from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask.ext.login import current_user

REDBERRY_ROOT = os.path.dirname(os.path.realpath(__file__))

cms = Blueprint('redberry', __name__, template_folder='templates', static_folder='static/redberry')
cms.config = {}


##############
# Jinja Filters
###############
@cms.app_template_filter()
def pretty_date(dttm):
    return dttm.strftime("%m/%d")

@cms.app_template_filter()
def date(dttm):
    return dttm.strftime('%Y-%m-%d')


########
# Config
########
# Automatically called once when the Blueprint is registered on the app.
@cms.record_once
def init_redberry(state):
    config = state.app.config.get("redberry.config")

    if config is None:
        raise Exception("Redberry expects you to provide a dict in the redberry.config setting for your app")

    if 'db' not in config:
        raise Exception("Redberry expects you to provide an SQLAlchemy object in redberry.config['db']")

    cms.config['db'] = config['db']

    from redberry.utils.logger import init_logger
    init_logger()

    from redberry.models.migrate import RedMigrator
    migrator = RedMigrator()
    migrator.do_migration()
    migrator.initialize_samples()


def admin_login_required(method):
    def is_admin(user):
        if isinstance(user.is_admin, bool):
            return user.is_admin
        else:
            return user.is_admin()

    @functools.wraps(method)
    def wrapper(*args, **kwargs):
        if not current_user.is_authenticated:
            flash("This section is for logged in users only.", 'warning')
            return redirect(url_for('redberry.home'))

        if not hasattr(current_user, 'is_admin'):
            flash("Redberry expects your user instance to implement an `is_admin` boolean attribute "
                  "or an `is_admin()` method.", 'warning')
            return redirect(url_for('redberry.home'))

        if not is_admin(current_user):
            flash("This section is for admin users only.", 'warning')
            return redirect(url_for('redberry.home'))

        return method(*args, **kwargs)

    return wrapper


############
# CMS ROUTES
############
@cms.route('/')
@cms.route('.amp/', endpoint='home_amp')
def home():
    from redberry.models import RedPost
    posts = RedPost.all_published()
    return render_redberry('redberry/index.html', posts=posts)


@cms.route('/<slug>')
@cms.route('/<slug>.amp', endpoint='show_post_amp')
def show_post(slug):
    from redberry.models import RedPost
    post = RedPost.query.filter_by(slug=slug).first()
    if not post:
        flash("Post not found!", 'danger')
        return redirect(url_for('redberry.home'))

    return render_redberry('redberry/post.html', post=post)


@cms.route('/category/<category_slug>')
@cms.route('/category/<category_slug>.amp', endpoint='show_category_amp')
def show_category(category_slug):
    from redberry.models import RedCategory
    category = RedCategory.query.filter_by(slug=category_slug).first()
    if not category:
        flash("Category not found!", 'danger')
        return redirect(url_for('redberry.home'))
    return render_redberry('redberry/category.html', category=category)


@cms.route('/sitemap')
def build_sitemap():
    from redberry.models import RedPost, RedCategory
    from apesmit import Sitemap
    sm = Sitemap(changefreq='weekly')

    for post in RedPost.all_published():
        sm.add(url_for('redberry.show_post', slug=post.slug, _external=True), lastmod=post.updated_at.date())

    for category in RedCategory.query.all():
        sm.add(url_for('redberry.show_category', category_slug=category.slug, _external=True), lastmod=category.updated_at.date())

    with open(os.path.join(REDBERRY_ROOT, 'static', 'redberry', 'sitemap.xml'), 'w') as f:
        sm.write(f)

    flash("Sitemap created.", 'success')
    return redirect(url_for('redberry.home'))


##############
# ADMIN ROUTES
##############
@cms.route('/admin', methods=['GET'], defaults={'model_name': 'category'})
@cms.route('/admin/<string:model_name>', methods=['GET'])
@admin_login_required
def admin(model_name):
    from redberry.models import RedCategory, RedPost

    if model_name == 'category':
        objects = RedCategory.query.all()

    elif model_name == 'post':
        objects = RedPost.query.all()

    return render_template('redberry/admin/index.html', objects=objects, model_name=model_name)


@cms.route('/admin/<string:model_name>/new', methods=['GET', 'POST'])
@admin_login_required
def new_record(model_name):
    from redberry.models import RedCategory, RedPost
    from redberry.forms import CategoryForm, PostForm

    if model_name == 'category':
        form = CategoryForm()
        new_record = RedCategory()

    elif model_name == 'post':
        form = PostForm()
        new_record = RedPost()

        # Convert category ids into objects for saving in the relationship.
        if form.categories.data:
            form.categories.data = RedCategory.query.filter(RedCategory.id.in_(form.categories.data)).all()
            form.categories.choices = [(c, c.title) for c in RedCategory.sorted()]
        else:
            form.categories.choices = [(c.id, c.title) for c in RedCategory.sorted()]

    if form.validate_on_submit():
        form.populate_obj(new_record)

        cms.config['db'].session.add(new_record)
        cms.config['db'].session.flush()

        build_sitemap()

        flash("Saved %s %s" % (model_name, new_record.id), 'success')
        return redirect(url_for('redberry.admin', model_name=model_name))

    return render_template('redberry/admin/form.html', form=form, model_name=model_name)


@cms.route('/admin/<string:model_name>/<string:slug>', methods=['GET', 'POST'])
@admin_login_required
def edit_record(model_name, slug):
    from redberry.models import RedCategory, RedPost
    from redberry.forms import CategoryForm, PostForm

    if model_name == 'category':
        record = RedCategory.query.filter_by(slug=slug).first()
        form = CategoryForm(obj=record)

    elif model_name == 'post':
        record = RedPost.query.filter_by(slug=slug).first()
        form = PostForm(obj=record)

        # Convert category ids into objects for saving in the relationship.
        form.categories.choices = [(c.id, c.title) for c in RedCategory.sorted()]
        if record.categories and request.method == 'GET':
            form.categories.data = [c.id for c in record.categories]

    if not record:
        flash("%s not found!" % model_name.title(), 'danger')
        return redirect(url_for('redberry.admin'))

    if form.validate_on_submit():

        if model_name == 'post' and form.categories.data:
            form.categories.data = RedCategory.query.filter(RedCategory.id.in_(form.categories.data)).all()

        form.populate_obj(record)
        cms.config['db'].session.flush()
        build_sitemap()
        flash("Saved %s %s" % (model_name, record.id), 'success')
        return redirect(url_for('redberry.admin', model_name=model_name))

    elif request.values.get('_method') == 'DELETE':
        record.delete()
        build_sitemap()
        flash("Deleted %s" % model_name, 'success')
        return redirect(url_for('redberry.admin', model_name=model_name))

    return render_template('redberry/admin/form.html', form=form, object=record, model_name=model_name)


##############
# ADMIN ROUTES
##############
def render_redberry(template_name, **kwargs):

    # For Accelerated Mobile Pages (AMP, ref: https://www.ampproject.org) use templates with a .amp suffix
    if '.amp' in request.path:
        kwargs['render_amp'] = True

    return render_template(template_name, **kwargs)
