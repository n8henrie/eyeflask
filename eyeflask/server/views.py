# -*- coding: utf-8 -*-
""""eyeflask.py
https://code.google.com/archive/p/sceye-fi/wikis/UploadProtocol.wiki
"""

import pathlib
import tarfile
import time
import uuid
from datetime import datetime

import defusedxml.ElementTree as etree
from flask import current_app, request, render_template, abort

from . import server
from .crypto import create_credential, make_digest


def make_path(upload_dir):
    return pathlib.Path(datetime.strftime(datetime.now(), upload_dir))


def allowed_file(filename):
    """Returns `True` if file extension is `.tar`"""
    return '.' in filename and filename.rsplit('.', 1)[1] in ['tar']


def make_snonce():
    """Returns a unique 32 character string"""
    return str(uuid.uuid4()).replace('-', '')


@server.route("/api/soap/eyefilm/v1", methods=['POST'])
def handle_SOAP():
    upload_key = current_app.config.get('UPLOAD_KEY')

    soapaction = request.headers.get('SOAPAction')
    current_app.logger.debug("Received SOAPAction: {}".format(soapaction))

    if soapaction == '"urn:StartSession"':
        root = etree.fromstring(request.data)

        transfermode = root.find(".//transfermode").text
        transfermodetimestamp = root.find(".//transfermodetimestamp").text

        cnonce = root.find(".//cnonce").text
        macaddress = root.find(".//macaddress").text
        credential = create_credential(macaddress, cnonce, upload_key)

        # EyeFi card doesn't accept cookies, so set a global var instead
        global snonce
        snonce = make_snonce()

        return render_template('start_session.xml', transfermode=transfermode,
                               transfermodetimestamp=transfermodetimestamp,
                               credential=credential, snonce=snonce)

    elif soapaction == '"urn:GetPhotoStatus"':
        root = etree.fromstring(request.data)

        macaddress = root.find(".//macaddress").text
        credential = root.find(".//credential").text

        # Unused, here for future reference
        # filename = root.find(".//filename").text
        # filesize = root.find(".//filesize").text
        # filesignature = root.find(".//filesignature").text
        # flags = root.find(".//flags").text

        expected_cred = create_credential(macaddress, snonce, upload_key,
                                          from_eyefi=True)
        current_app.logger.debug("Credential: {}\n"
                                 "Expected:   {}".format(credential,
                                                         expected_cred))

        if credential == expected_cred:
            return render_template('get_photo_status.xml', fileid=1, offset=0)
        else:
            return abort(403)

    elif soapaction == '"urn:MarkLastPhotoInRoll"':
        root = etree.fromstring(request.data)

        # Unused, here for future reference
        # macaddress = root.find(".//macaddress").text
        # mergedelta = root.find(".//mergedelta").text

        return render_template("mark_last.xml")


@server.route("/api/soap/eyefilm/v1/upload", methods=['POST'])
def upload_photo():
    root = etree.fromstring(request.form.get("SOAPENVELOPE"))

    filename = root.find(".//filename").text
    current_app.logger.debug("Got upload request for: {}".format(filename))

    # macaddress = root.find(".//macaddress").text
    # fileid = root.find(".//fileid").text
    # filesize = root.find(".//filesize").text
    # filesignature = root.find(".//filesignature").text
    # encryption = root.find(".//encryption").text
    # flags = root.find(".//flags").text

    integrity_digest = request.form.get("INTEGRITYDIGEST")
    current_app.logger.debug("Received INTEGRITYDIGEST: "
                             "{}".format(integrity_digest))

    upfile = request.files.get("FILENAME")

    if upfile and allowed_file(upfile.filename):
        upload_key = current_app.config.get('UPLOAD_KEY')
        true_digest = make_digest(upfile, upload_key)
        current_app.logger.debug("Calculated integritydigest: "
                                 "{}".format(true_digest))

        if integrity_digest == true_digest:
            upload_dir = current_app.config['UPLOAD_FOLDER']
            upload_path = make_path(upload_dir)

            try:
                upload_path.mkdir(mode=0o755, parents=True, exist_ok=True)

            # Workaround for Python 3.4
            except TypeError:
                try:
                    upload_path.mkdir(mode=0o755, parents=True)
                except FileExistsError:
                    pass

            upfile.seek(0)

            with tarfile.open(fileobj=upfile) as archive:
                if len(archive.getmembers()) == 1:
                    img_file = archive.getmembers()[0]

                    # Eye-Fi sets the image file's a/c/m times to some wonky
                    # date from 2010 -- fix by setting them to the current
                    # time. Tried using the tarfile's creation time and it was
                    # just the upload time, which is no better). Would ideally
                    # find a way to set it to the time it was scanned, in case
                    # that happened significantly prior to connecting to
                    # EyeFlask.
                    img_file.mtime = time.time()

                    archive.extract(img_file, path=str(upload_path))

                    return render_template("upload_photo.xml", success="true")

    # If you got here, either `INTEGRITYDIGEST` was wrong, the file wasn't
    # received, or it had an illegal filename.
    abort(403)


@server.errorhandler(403)
def unauthorized(e):
    return "Unauthorized", 403


@server.errorhandler(404)
def page_not_found(e):
    return "Page not found!", 404
