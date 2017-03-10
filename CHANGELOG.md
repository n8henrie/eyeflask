# [Changelog](http://keepachangelog.com)

## 0.1.3 :: 20170310

- Add strftime based subfolders to config (see issue #2)
- Encourage use of virtualenv in the README
- Test docs creation in Travis
- Fix some flake8 compliants

## 0.1.2 :: 20170303

- Python 3.6 compatibility
- Stop using `src/` subdirectory
- Try to fix some Pandoc exceptions

## 0.1.1 :: 20160318

- Use `array.array` instead of `struct.iter_unpack` for modest speed boost
- Rename `start_session` to `handle_SOAP` -- because that's what it does
- Extract the image from the tarfile data prior to writing to disk (eliminating
  the need to delete the tarfile afterwards)

## 0.1.0 :: 20160227

- Initial release to GitHub, PyPI
