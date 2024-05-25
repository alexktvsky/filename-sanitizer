# filename-sanitizer

A Python application to sanitize files on disk by replaceing unwanted characters and replacing them with characters that are allowed in filenames across different operating systems (ASCII-alphanumeric (a-z A-Z 0-9), hyphens, underscores and periods).

Key Features:
- Transliteration to ASCII
- Customizable replacement rules
- Recursive directory processing
- Protection against overwriting files with the same names


## Usage

Sanitize the specified file:

```
filename-sanitizer <path/to/file>
```

Recursively sanitize files in the specified directory and all its subdirectories:

```
filename-sanitizer -r <path/to/dir>
```

Sanitize the filename using the provided rules:

```
filename-sanitizer --replacements ",-> end " <path/to/file>
```

Note that filenames may contain mixed case (a-z A-Z) so if you require lowercase then run with flag `-l`.

You can also specify the character to be used as a separator using the `-s` flag.


## License

Released under a ([MIT](LICENSE)) license.
