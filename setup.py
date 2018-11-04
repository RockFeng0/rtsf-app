#! python3
# -*- encoding: utf-8 -*-
'''
Current module: setup

Rough version history:
v1.0    Original version to use

********************************************************************
    @AUTHOR:  Administrator-Bruce Luo(罗科峰)
    MAIL:     luokefeng@163.com
    RCS:      setup,  v1.0 2018年9月18日
    FROM:   2018年9月18日
********************************************************************
======================================================================

Provide a function for the automation test

'''



from appuidriver import __about__
import os, io, sys
from shutil import rmtree
from setuptools import setup, find_packages, Command

here = os.path.abspath(os.path.dirname(__file__))

with io.open("README.md", encoding='utf-8') as f:
    long_description = f.read()

class UploadCommand(Command):
    """ Build and publish this package.
        Support setup.py upload. Copied from requests_html.
    """

    user_options = []

    @staticmethod
    def status(s):
        """Prints things in green color."""
        print("\033[0;32m{0}\033[0m".format(s))

    def initialize_options(self):
        """ override
        """
        pass

    def finalize_options(self):
        """ override
        """
        pass

    def run(self):
        try:
            self.status('Removing previous builds…')
            rmtree(os.path.join(here, 'dist'))
        except OSError:
            pass

        self.status('Building Source and Wheel (universal) distribution…')
        os.system('{0} setup.py sdist bdist_wheel --universal'.format(sys.executable))

        self.status('Uploading the package to PyPi via Twine…')
        os.system('twine upload dist/*')

        self.status('Publishing git tags…')
        os.system('git tag v{0}'.format(__about__.__version__))
        os.system('git push --tags')

        sys.exit()
        
install_requires = [
    "Appium-Python-Client",
    "requests",
    "rtsf",
    "rtsf-web",
]

# dependency_links=[
# "git+https://github.com/RockFeng0/rtsf.git#egg=rtsf-0",
# "git+https://github.com/RockFeng0/rtsf-web.git#egg=rtsf-web-0",
# ]

setup(
        name = __about__.__title__,
        version=__about__.__version__,
        description=__about__.__short_desc__,
        long_description=long_description,
        long_description_content_type='text/markdown',
        author=__about__.__autor__,
        author_email=__about__.__author_email__,
        url=__about__.HOME_PAGE,
        license=__about__.__license__,
        python_requires='>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, <4',
        packages=find_packages(exclude=()),        
        keywords='test android ui',
        install_requires=install_requires,
#         dependency_links=dependency_links,
        extras_require={},
        entry_points={
            'console_scripts': [
                'aldriver=appuidriver.cli:local_main_run', # one appium server <--> only one android device  
                'ardriver=appuidriver.cli:remote_main_run', # appium nodes <--> android devices          
                'appserver=appuidriver.cli:appium_main_run', # appium server, appium node for grid mode
                'ainfo=appuidriver.cli:tools_main_run', # devices info or apk info
            ]
        },
        # $ setup.py upload support.
        cmdclass={
            'upload': UploadCommand
        }
    )
