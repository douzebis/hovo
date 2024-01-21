# Hovo
A demonstrator for parsing Google docs and Google partner issues

## Installation

(Tested with python@3.12)

```bash
python3.11 -m venv venv
. venv/bin/activate
pip install --upgrade pip
pip install --upgrade beautifulsoup4
pip install --upgrade click
pip install --upgrade google-api-python-client
pip install --upgrade google-auth-httplib2
pip install --upgrade google-auth-oauthlib
pip install --upgrade js2py
pip install --upgrade oauth2client
pip install --editable .
```

## Usage

```shell
hovo --doc-id DOC_ID --checks
```

```shell
hovo --doc-id DOC_ID --row ROW_NO --add-row
```

```shell
hovo --doc-id DOC_ID --row ROW_NO --remove-row
```

```shell
hovo --doc-id DOC_ID --row ROW_NO --label-row LABEL
```

```shell
hovo --doc-id DOC_ID --import-google
```

```shell
hovo --doc-id DOC_ID --process
```


## Tips
