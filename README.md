# EyeFlask

[![Build Status](https://travis-ci.org/n8henrie/eyeflask.svg?branch=master)](https://travis-ci.org/n8henrie/eyeflask)

Simple [Flask](http://flask.pocoo.org)-based Python3 EyeFi server

- Documentation: [eyeflask.readthedocs.org](https://eyeflask.readthedocs.org)

## Introduction

I use an Eye-Fi SD card in my portable scanner. Unfortunately, it used to
upload directly to Evernote, but no longer supports uploading directly to any
service that suits my needs. Additionally, they don't provide a Linux version
of their server software.

EyeFlask is a simple Flask-based Eye-Fi server written for Python >= 3.4. The
Eye-Fi card can connect to it and will upload images to the folder specified in
the config. EyeFlask attempts to verify the file integrity using the same
security protocols used by Eye-Fi Server.

## Dependencies

- Python >= 3.4
- See `requirements.txt`

## Quickstart

1. `pip3 install eyeflask`
1. Copy `eyeflask/extras/eyeflask-sample.cfg` to `eyeflask.cfg`, modify
   with your values, and put it in [your instance
   folder](http://flask.pocoo.org/docs/0.10/config/#instance-folders)
1. Run: `eyeflask` (or `venv/bin/python -m eyeflask.cli`)
1. Scan some stuff, see if it ends up in your uploads folder

### Development Setup

1. Clone the repo: `git clone https://github.com/n8henrie/eyeflask && cd
   eyeflask`
1. Make a virtualenv: `python3 -m venv venv`
1. Make an instance folder: `mkdir -p instance`
1. Copy the config sample: `cp eyeflask/extras/eyeflask-sample.cfg
   instance/eyeflask.cfg`
1. Edit the config to include your upload directory and upload_key (see below):
   `vim instance/eyeflask.cfg`
1. Install with dev dependencies: `venv/bin/pip install .[dev]`
1. Run: `eyeflask` (or `venv/bin/python -m eyeflask.cli`)
1. Scan some stuff, see if it ends up in your uploads folder

## Extras

EyeFlask will help get the images uploaded and extracted to your server (e.g. a
Raspberry Pi in my case), but what do to from there? If you're running Raspbian
Jessie (and using systemd), I've included in the `extras` folder a few files
that may be of interested.

- `upload_scans.service` will run a given script when called (e.g. `sudo
  systemctl start upload_scans.service`)
- `upload_scans.timer` is an example [systemd timer
  unit](https://www.freedesktop.org/software/systemd/man/systemd.timer.html)
  that will call `upload_scans.service` every 10 minutes
- `upload_scans.path` is an example [systemd path
  unit](https://www.freedesktop.org/software/systemd/man/systemd.path.html)
  that will call `upload_scans.service` every time a file changes in a watched
  directory

Put together, this makes it *really* easy to put together a script to [upload
new scans to a Dropbox
folder](https://gist.github.com/n8henrie/1e8ab5bcf1a3af2c20de) whenever a new
one is added, or whatever command you'd like to run on all your scans.

I've also included `eyeflask/extras/eyeflask.service`, which is a sample
[systemd service
file](https://www.freedesktop.org/software/systemd/man/systemd.service.html) to
run EyeFlask at startup and restart it on errors.

## Acknowledgements

Much of the code for EyeFlask came from or was inspired by the following
projects / links. Many thanks to the authors for their work! If I've forgotten
anyone, let me know.

- <https://github.com/tachang/EyeFiServer>
- <https://github.com/dgrant/eyefiserver2>
- <https://code.google.com/archive/p/sceye-fi/wikis/UploadProtocol.wiki>
- <https://launchpad.net/eyefi>
- <https://code.google.com/archive/p/eyefiserver/>
- <https://github.com/BrentSouza/WP7EyeFiConnector>


## Troubleshooting / FAQ

### Where do I find my upload key?

You'll need a supported platform (OS X or Windows) with `Eye-Fi
Center.app` installed, and need to have uploaded photos to that computer at
least once. This ensures everything is working, and generates the
`Settings.xml` file, from which you need to copy the upload key into
`eyeflask.cfg`.

- OS X: `~/Library/Eye-Fi/Settings.xml`
- Windows 7: `C:\Users\[user]\AppData\Roaming\Eye-Fi\Settings.xml`
  ([source](http://support.photosmithapp.com/knowledgebase/articles/116903-why-do-i-see-multiple-eye-fi-card-upload-keys-ho))
- Windows XP: `C:\Documents and Settings\[user]\Application
  Data\Eye-Fi\Settings.xml`
  ([source](http://support.photosmithapp.com/knowledgebase/articles/116903-why-do-i-see-multiple-eye-fi-card-upload-keys-ho))

### Is it okay to be running this with the built-in Flask server?

It's not perfect, but it seems to work okay for me and my single Eye-Fi card
setup. You'd probably be better off running it behind
[gunicorn](http://gunicorn.org) or a gunicorn / nginx setup, but I'm running it
behind Flask alone for simplicity and because I haven't had any issues so far.

If you want to give it a go with gunicorn / nginx, I've included an *extremely*
simplified nginx configuration file: `eyeflask/extras/nginx.conf`. After
installing `gunicorn` into your virtualenv, hopefully you'll be able to get it
running behind nginx without much trouble with something like:

```
venv/bin/pip install gunicorn
venv/bin/gunicorn 'eyeflask:create_app("instance/eyeflask.cfg")'
```

For debugging you can also use the flags `--log-file=- --log-level=debug`.

NB: I do **not** plan on providing support for nginx / gunicorn setups, as I
don't know enough about it to be particularly helpful. I just verified that it
seemed to work. (Just FYI, Gunicorn *without* nginx did **not** seem to work
unless I used one of the async workers, kept getting timeouts.)

### Why am I getting repeat or unreliable file uploads on my Raspberry Pi?

I'm not sure. I was getting *excellent* reliability when running EyeFlask on my
Macbook Air and *very* poor reliability on my Raspberry Pi B+ with EyeFlask
0.1.0. It seemed like the file would be uploaded exctracted without issue, but
the EyeFi card kept sending the same file over and over, leading me to believe
that the confirmation response wasn't getting received every time. I thought it
might have something to do with slow response times, so I did a little code
optimization with 0.1.1 which seems to have helped. I also gave up and put
EyeFlask behind a gunicorn / nginx setup, and between the two of these changes
I have much better upload reliability.
