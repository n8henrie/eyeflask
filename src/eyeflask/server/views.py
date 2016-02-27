# -*- coding: utf-8 -*-
""""eyeflask.py
https://code.google.com/archive/p/sceye-fi/wikis/UploadProtocol.wiki
"""

from flask import current_app, request, render_template, abort
import defusedxml.ElementTree as etree
from werkzeug import secure_filename
import os.path
from . import server
import tarfile
import os
import uuid
from .crypto import create_credential, make_digest


def allowed_file(filename):
    """Returns `True` if file extension is `.tar`"""
    return '.' in filename and filename.rsplit('.', 1)[1] in ['tar']


def make_snonce():
    """Returns a unique 32 character string"""
    return str(uuid.uuid4()).replace('-', '')


@server.route("/api/soap/eyefilm/v1", methods=['POST'])
def start_session():
    upload_key = current_app.config.get('UPLOAD_KEY')

    if request.headers.get('SOAPAction') == '"urn:StartSession"':
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

    elif request.headers.get('SOAPAction') == '"urn:GetPhotoStatus"':
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

    elif request.headers.get('SOAPAction') == '"urn:MarkLastPhotoInRoll"':
        root = etree.fromstring(request.data)

        # Unused, here for future reference
        # macaddress = root.find(".//macaddress").text
        # mergedelta = root.find(".//mergedelta").text

        return render_template("mark_last.xml")


@server.route("/api/soap/eyefilm/v1/upload", methods=['POST'])
def upload_photo():
    current_app.logger.debug(request.form.get("SOAPENVELOPE"))
    root = etree.fromstring(request.form.get("SOAPENVELOPE"))

    filename = root.find(".//filename").text

    # macaddress = root.find(".//macaddress").text
    # fileid = root.find(".//fileid").text
    # filesize = root.find(".//filesize").text
    # filesignature = root.find(".//filesignature").text
    # encryption = root.find(".//encryption").text
    # flags = root.find(".//flags").text

    integrity_digest = request.form.get("INTEGRITYDIGEST")
    current_app.logger.debug(integrity_digest)

    upfile = request.files.get("FILENAME")

    if upfile and allowed_file(upfile.filename):
        upload_key = current_app.config.get('UPLOAD_KEY')
        true_digest = make_digest(upfile, upload_key)

        if integrity_digest == true_digest:
            upload_dir = current_app.config['UPLOAD_FOLDER']
            filename = secure_filename(upfile.filename)
            filepath = os.path.join(upload_dir, filename)

            upfile.seek(0)
            upfile.save(filepath)

            # Eye-Fi sets the image file's a/c/m times to some wonky date from
            # 2010 -- fix by setting them to the tarfile's creation time.
            # Unfortunately this will be the upload time and not the scan time,
            # but it's the best I can do at the moment.
            creation_time = os.stat(filepath).st_ctime

            with tarfile.open(filepath) as archive:
                if len(archive.getmembers()) == 1:
                    img_file = archive.getmembers()[0]
                    img_file.mtime = creation_time
                    archive.extract(img_file, path=upload_dir)

            # Delete `.tar` file after extracting the image
            os.remove(filepath)

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
