from setuptools import setup

setup(
    name='Data Analytics Toolkit',
    version='1.0',
    long_description=__doc__,
    packages=['DataAnalyticsToolkit'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'Flask~=1.1.2',
        'Flask-Login~=0.5.0',
        'Flask-SQLAlchemy~=2.4.1',
        'pybigquery~=0.4.15',
        'pymysql~=0.9.3',
        'oauthlib~=3.1.0',
        'requests~=2.23.0',
        'pyOpenSSL~=19.1.0',
        'google-cloud-bigquery~=1.25.0',
        'google-cloud-storage~=1.29.0'
    ]
)
