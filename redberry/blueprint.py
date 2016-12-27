import functools
from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask.ext.login import current_user

cms = Blueprint('redberry', __name__, template_folder='templates', static_folder='static/redberry')
cms.config = {}


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
    @functools.wraps(method)
    def wrapper(*args, **kwargs):
        if not current_user.is_authenticated:
            flash("This section is for logged in users only.", 'warning')
            return redirect(url_for('redberry.home'))

        if not hasattr(current_user, 'is_admin'):
            flash("Redberry expects your user instance to implement an `is_admin()` method.", 'warning')
            return redirect(url_for('redberry.home'))

        if not current_user.is_admin():
            flash("This section is for admin users only.", 'warning')
            return redirect(url_for('redberry.home'))

        return method(*args, **kwargs)

    return wrapper


@cms.app_template_filter()
def pretty_date(dttm):
    return dttm.strftime("%m/%d")


############
# CMS ROUTES
############
@cms.route('/')
@cms.route('/page/<int:page>')
def home(page=1):
    from redberry.models import RedPost
    posts = RedPost.all_published()
    return render_template('redberry/index.html', posts=posts)


@cms.route('/<slug>')
def show_post(slug):
    from redberry.models import RedPost
    post = RedPost.query.filter_by(slug=slug).first()
    if not post:
        flash("Post not found!", 'danger')
        return redirect(url_for('redberry.home'))
    return render_template('redberry/post.html', post=post)


@cms.route('/category/<category_slug>')
def show_category(category_slug):
    from redberry.models import RedCategory
    category = RedCategory.query.filter_by(slug=category_slug).first()
    if not category:
        flash("Category not found!", 'danger')
        return redirect(url_for('redberry.home'))
    return render_template('redberry/category.html', category=category)


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
        if form.categories.data:
            form.categories.data = RedCategory.query.filter(RedCategory.id.in_(form.categories.data)).all()
            form.categories.choices = [(c, c.title) for c in RedCategory.sorted()]
        else:
            form.categories.choices = [(c.id, c.title) for c in RedCategory.sorted()]

    if not record:
        flash("%s not found!" % model_name.title(), 'danger')
        return redirect(url_for('redberry.admin'))

    if form.validate_on_submit():
        form.populate_obj(record)
        cms.config['db'].session.flush()
        flash("Saved %s %s" % (model_name, record.id), 'success')
        return redirect(url_for('redberry.admin', model_name=model_name))

    elif request.values.get('_method') == 'DELETE':
        record.delete()
        flash("Deleted %s" % model_name, 'success')
        return redirect(url_for('redberry.admin', model_name=model_name))

    return render_template('redberry/admin/form.html', form=form, object=record, model_name=model_name)