from setuptools import setup

setup(
    name='sos',
    version='0.0.1',
    entry_points={
        'console_scripts':[
            'sos=sos:main'
        ]
    }
)