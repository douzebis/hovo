from setuptools import setup
from setuptools import find_packages

setup(
    name='hovo',
    version='0.1.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'beautifulsoup4',
        'click',
        'google-api-python-client',
        'google-auth-httplib2',
        'google-auth-oauthlib',
        'oauth2client',
        'js2py',
    ],
    entry_points={
        'console_scripts': [
            'hovo=hovo.cli:cli',
        ],
    },
)
