APP_NAME = 'simplegallery'
PACKAGE_NAME = 'django-%s' % APP_NAME
DESCRIPTION = 'django image gallery app'
PROJECT_URL = 'http://github.com/divio/%s/' % PACKAGE_NAME

INSTALL_REQUIRES = [
    'django (<1.2.5)',
    'mptt (<0.4)',
    'django_cms',
    'django_filer',
    'django_multilingual_ng',
    'django_tinymce',
] # e.g 'django (>1.1.0)'

EXTRA_REQUIRES={
    'South':  ["south"],
}


AUTHOR="Stefan Foulis"

EXTRA_CLASSIFIERS = [
]


# DO NOT EDIT ANYTHING DOWN HERE... this should be common to all django app packages
from setuptools import setup, find_packages
import os

version = __import__(APP_NAME).__version__

classifiers = [
    'Environment :: Web Environment',
    'Framework :: Django',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: BSD License',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    'Topic :: Software Development',
    'Topic :: Software Development :: Libraries :: Application Frameworks',
]
if not 'a' in version and not 'b' in version: classifiers.append('Development Status :: 5 - Production/Stable')
elif 'a' in version: classifiers.append('Development Status :: 3 - Alpha')
elif 'b' in version: classifiers.append('Development Status :: 4 - Beta')

for c in EXTRA_CLASSIFIERS:
    if not c in classifiers:
        classifiers.append(c)

media_files = []
for dir in ['%s/media' % APP_NAME,'%s/templates' % APP_NAME]:
    for dirpath, dirnames, filenames in os.walk(dir):
        media_files.append([dirpath, [os.path.join(dirpath, f) for f in filenames]])
#media_files.append('README.rst')
#media_files.append('HISTORY')
# build the MANIFEST.in file
"""
open(os.path.join(os.path.dirname(__file__), 'MANIFEST.in'), 'w').write('''include README.rst
include HISTORY
recursive-include %s/media *
recursive-include %s/templates *
''')
"""
    


def read(fname):
    # read the contents of a text file
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    author=AUTHOR,
    name=PACKAGE_NAME,
    version=version,
    url=PROJECT_URL,
    description=DESCRIPTION,
    long_description=read('README.rst') + '\n\n\n' + read('HISTORY'),
    platforms=['OS Independent'],
    classifiers=classifiers,
    requires=INSTALL_REQUIRES,
    extras_require=EXTRA_REQUIRES,
    packages=find_packages(),
    package_dir={
        APP_NAME: APP_NAME,
    },
    data_files = media_files,
    zip_safe = False
)
