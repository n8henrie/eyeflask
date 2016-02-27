"""mock_payloads.py
Payloads for eyeflask tests.
"""

start_session = """<?xml version="1.0" encoding="UTF-8"?><SOAP-ENV:Envelope
xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/"
xmlns:ns1="EyeFi/SOAP/EyeFilm"><SOAP-ENV:Body><ns1:StartSession>
<macaddress>0a1b2c3d4e5f</macaddress>
<cnonce>0123456789101112abcdefabcdefabcd</cnonce>
<transfermode>0</transfermode>
<transfermodetimestamp>1455199402</transfermodetimestamp></ns1:StartSession>
</SOAP-ENV:Body></SOAP-ENV:Envelope>"""

get_photo_status = """<?xml version="1.0" encoding="UTF-8"?><SOAP-ENV:Envelope
xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/"
xmlns:ns1="EyeFi/SOAP/EyeFilm"><SOAP-ENV:Body><ns1:GetPhotoStatus>
<credential>{credential}</credential>
<macaddress>0a1b2c3d4e5f</macaddress><filename>fake.jpg.tar</filename>
<filesize>1269760</filesize>
<filesignature>12345</filesignature>
<flags>4</flags></ns1:GetPhotoStatus></SOAP-ENV:Body></SOAP-ENV:Envelope>"""

upload_photo = """<?xml version="1.0" encoding="UTF-8"?><SOAP-ENV:Envelope
xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/"
xmlns:ns1="EyeFi/SOAP/EyeFilm"><SOAP-ENV:Body><ns1:UploadPhoto>
<fileid>1</fileid><macaddress>0a1b2c3d4e5f</macaddress>
<filename>test.jpg.tar</filename><filesize>57344</filesize>
<filesignature>3531000078f3020000000000e8cf0200</filesignature>
<encryption>none</encryption><flags>4</flags></ns1:UploadPhoto>
</SOAP-ENV:Body></SOAP-ENV:Envelope>"""

mark_last_photo = """<?xml version="1.0" encoding="UTF-8"?><SOAP-ENV:Envelope
xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/"
xmlns:ns1="EyeFi/SOAP/EyeFilm"><SOAP-ENV:Body><ns1:MarkLastPhotoInRoll>
<macaddress>0a1b2c3d4e5f</macaddress><mergedelta>0</mergedelta>
</ns1:MarkLastPhotoInRoll></SOAP-ENV:Body></SOAP-ENV:Envelope>"""
