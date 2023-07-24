"""test_eyeflask.py
Basic tests for eyeflask"""

import defusedxml.ElementTree as etree

from eyeflask.server.crypto import create_credential, make_digest
from .mock_payloads import (start_session, get_photo_status,
                            mark_last_photo, upload_photo)


def test_create_credential(client):
    assert create_credential('1234', '2345', '3456') == \
            'd870deb305a764802e3692eaac87129e'


def test_make_digest(client):
    with open("tests/test.jpg.tar", "rb") as f:
        assert make_digest(f, "abcd") == "c5a1a3dc5bfbf1244b5ae140270dd6a9"


def test_get_fails(client):
    """Test that GET requests fail (endpoint is POST only)."""

    assert client.get("/api/soap/eyefilm/v1").status_code == 405


def test_startsession(client):
    global snonce
    ns = "{http://localhost/api/soap/eyefilm}"
    headers = {'SOAPAction': '"urn:StartSession"'}
    response = client.post("/api/soap/eyefilm/v1", headers=headers,
                           data=start_session)

    root = etree.fromstring(response.data)
    cred = root.find(".//{}credential".format(ns)).text
    snonce = root.find(".//{}snonce".format(ns)).text

    assert cred == "9e7553d8fd7e1e675cb6c8e0606bd9bd"
    assert response.status_code == 200


def test_photostatus(client):
    """Test the GetPhotoStatus SOAPAction.

    Generates `credential` from the test_config upload_key and macaddress and
    snonce obtained in in `test_startsession` above.
    """

    headers = {'SOAPAction': '"urn:GetPhotoStatus"'}

    credential = create_credential("0a1b2c3d4e5f", snonce, "abcd",
                                   from_eyefi=True)
    response = client.post("/api/soap/eyefilm/v1", headers=headers,
                           data=get_photo_status.format(credential=credential))
    assert response.status_code == 200


def test_uploadphoto(client, tmpdir):
    """Tests uploading of test file (test.jpg.tar, in tests folder)."""

    with open("tests/test.jpg.tar", "rb") as test_file:

        data = {
                "SOAPENVELOPE": upload_photo,
                "FILENAME": test_file,
                "INTEGRITYDIGEST": "c5a1a3dc5bfbf1244b5ae140270dd6a9"
                }

        config = client.application.config
        tmp_upload_dir = str(tmpdir / config['UPLOAD_FOLDER'])
        config['UPLOAD_FOLDER'] = tmp_upload_dir
        response = client.post("/api/soap/eyefilm/v1/upload", data=data,
                               content_type='multipart/form-data')
    assert response.status_code == 200


def test_marklast(client):
    headers = {'SOAPAction': '"urn:MarkLastPhotoInRoll"'}

    response = client.post("/api/soap/eyefilm/v1", headers=headers,
                           data=mark_last_photo)
    assert response.status_code == 200
