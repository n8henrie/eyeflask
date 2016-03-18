# History

## 0.1.1 :: 20160318

- Use `array.array` instead of `struct.iter_unpack` for modest speed boost
- Rename `start_session` to `handle_SOAP` -- because that's what it does
- Extract the image from the tarfile data prior to writing to disk (eliminating
  the need to delete the tarfile afterwards)

## 0.1.0 :: 20160227

- Initial release to GitHub, PyPI
