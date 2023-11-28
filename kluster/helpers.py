import os
from typing import List

from flask_mail import Message

from kluster import db, mail
from cloudinary.uploader import upload
from kluster.models.users import Users
from kluster.models.medication import Medication


def convert_pic_to_link(picture) -> str:
    r = upload(picture, use_filename=True)
    return r.get("url")


def query_one_filtered(table, **kwargs):
    """_summary_

    Args:
        table (_type_): _description_

    Returns:
        _type_: _description_
    """
    return db.session.execute(
        db.select(table).filter_by(**kwargs)
    ).scalar_one_or_none()


# get all items from table based on filter
# args:table=model_class **kwargs=filters
def query_all_filtered(table, **kwargs):
    """_summary_

    Args:
        table (_type_): _description_

    Returns:
        _type_: _description_
    """
    return (
        db.session.execute(db.select(table).filter_by(**kwargs))
        .scalars()
        .all()
    )


# get first one item from table no filter
def query_one(table):
    """_summary_

    Args:
        table (_type_): _description_

    Returns:
        _type_: _description_
    """
    return db.session.execute(db.select(table)).scalar_one_or_none()


# get all items on table no filter
def query_all(table):
    """_summary_

    Args:
        table (_type_): _description_

    Returns:
        _type_: _description_
    """
    return db.session.execute(db.select(table)).scalars().all()


# get all items from table no filter paginated
def query_paginated(table, page):
    """_summary_

    Args:
        table (_type_): _description_
        page (_type_): _description_

    Returns:
        _type_: _description_
    """
    return db.paginate(
        db.select(table).order_by(table.date_created.desc()),
        per_page=15,
        page=page,
        error_out=False,
    )


# get all items from table based on filtered paginated
def query_paginate_filtered(table, page, **kwargs):
    """_summary_

    Args:
        table (_type_): _description_
        page (_type_): _description_

    Returns:
        _type_: _description_
    """
    return db.paginate(
        db.select(table)
        .filter_by(**kwargs)
        .order_by(table.date_created.desc()),
        per_page=15,
        page=page,
        error_out=False,
    )


def mail_composer(
        patient_name: str,
        medication_name: str,
        dosage: str,
        scheduled_time: str,
        recipient: str,
        subject: str = "Medication Alert!",
):
    msg = Message(subject,
                  sender=os.environ.get("MAIL_USERNAME"),
                  recipients=[recipient])

    mail_template_path = "/Users/firelord.py/Documents/python code/klusterthon/kluster/mail_template.html"

    with open(mail_template_path, 'r', encoding='utf-8') as template_file:
        template_content = template_file.read()

    template_content = template_content.replace('[Patient\'s Name]', patient_name)
    template_content = template_content.replace('[Medication Name]', medication_name)
    template_content = template_content.replace('[Dosage]', dosage)
    template_content = template_content.replace('[Scheduled Time]', scheduled_time)

    msg.body = template_content
    msg.html = template_content

    mail.send(msg)


def mail_compose(
        subject: str = "Medication Alert!",
        *args,
        **kwargs
):


    msg = Message(subject,
                  sender=os.environ.get("MAIL_USERNAME"),
                  recipients=[recipient])

    mail_template_path = "/Users/firelord.py/Documents/python code/klusterthon/kluster/mail_template.html"

    with open(mail_template_path, 'r', encoding='utf-8') as template_file:
        template_content = template_file.read()

    template_content = template_content.replace('[Patient\'s Name]', patient_name)
    template_content = template_content.replace('[Medication Name]', medication_name)
    template_content = template_content.replace('[Dosage]', dosage)
    template_content = template_content.replace('[Scheduled Time]', scheduled_time)

    msg.body = template_content
    msg.html = template_content

    mail.send(msg)
