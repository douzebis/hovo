# Hovo
A demonstrator for parsing Google docs and Google partner issues

## Installation

(Tested with python@3.11)

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
pip install --upgrade selenium
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

- Google docs API are powerful and permit reading from- and writing to- a Google
  document.
  - It is a robust and foolproof approach
  - It enables processing a document that is also shared by human users
  - Proceeding so allows to view the document as a database that has a
    convenient interface with humane user. This database can be used as source
    or truth, and backends can be developed to produce indicators and various
    operational views.
- structural elements: beware of "silent" elements that still consume one
  position - e.g., `pageBreak`
- batch-updating the document: intelligent backwards sorting first
- OIDC authentication: Flask and OAuthLib do a good job. Flask listens to
  localhost:port for the redirect from the OP so that the integration is
  seamless. This is perfect for OIDC-aware APIs
- For Google Partner IssueTracker unfortunately, no API is provided. We have to
  pretend we are a user accessing via a browser.
  - Use selenium to authenticate and retrieve the necessary cookies (this
    process also nicely handles the FIDO2 second factor).
  - The freshness of saved cookies can be verified on application startup so as
    not to bother the user unless required
  - Buganizer "private API" and bug format had to be (partially) reversed
    engineered
  - Using appropriate GET method, it is possible to read the bug fields
  - BeautifulSoup and py2js are extremely helpful libraries
  - Using appropriate POST method, it is also possible to write fields back to
    Buganizer
  - This however requires the x-xsrf-token header. It is to be found embedded in
    the blob returned by the GET method
- Google docs API is powerful, but has some limitations. For example it is not
  possible to retrieve information about comments.
- For retrieving comments, one way is to use the Google drive API. However there
  are still some limitations. In particular it is not possible to retrieve the
  information about comment assignees
- To retrieve information about comment assignees, one possible way is as
  follows
  - Use the Google drive API to convert the document to HTML format and export
    it as a zip 
  - Process the HTML using BeautifulSoup: the comments appear as "footnotes".
    The footnotes include information about the comment assignee (if any).
- With all the above we can use the Google doc as
  - the source of truth
  - a pivot format that synchronizes human users and buganizer
  - a global summary of activities that can help the management
  - a producer of various backend indicators and charts that can help the teams
    and the management

## To do

- Produce maturity indicator as markdown
- Produce assignee tracker as markdown
- Produce dependency graph
- Produce Gantt chart
- Publish indicators on internal website
- In the charts, color the nodes according to leadership
- Fix `hovo row n --remove` so that it does not panic if row is out of range
- Add a `hovo row n --add label` option
