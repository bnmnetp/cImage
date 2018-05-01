from setuptools import setup

#with open('requirements.txt', 'r') as fh:
#    dependencies = [l.strip() for l in fh]

setup(
    name='cs20-image',
    description='Image manipulation library for media computation education',
    version='1.5.4',
    py_modules = ['image'],
    author = 'Brad Miller and Dan Schellenberg',
    author_email = 'schellenberg@gmail.com',
    install_requires= ['Pillow>=2.9.0'],
    include_package_data = False,
    license='GPL',
    url = 'https://github.com/schellenberg/cImage',
    keywords = ['image', 'education'], # arbitrary keywords
    classifiers=('Development Status :: 5 - Production/Stable',
                   'Environment :: Console',
                   'Intended Audience :: Education',
                   'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
                   'Operating System :: MacOS',
                   'Operating System :: Unix',
                   'Programming Language :: Python',
                   'Programming Language :: Python :: 3.4',
                   'Topic :: Education'),
    long_description=open('README.rst').read(),
)
