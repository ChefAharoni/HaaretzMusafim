from setuptools import setup, find_packages

setup(
    name='HaaretzMusafim',
    version='0.1.0',  # Update the version as per your release
    author='ChefAharoni',
    author_email='ChefAharoni@proton.me',
    description='Archive of Musafim (magazines) of the Israeli Haaretz newspaper',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/ChefAharoni/HaaretzMusafim',
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.11',
    ],
    keywords='haaretz, newspaper, archive, israel, magazines',
    install_requires=[
        'beautifulsoup4==4.12.2',
        'blinker==1.7.0',
        'certifi==2023.11.17',
        'charset-normalizer==3.3.2',
        'click==8.1.7',
        'dotenv==0.0.5',
        'Flask==3.0.0',
        'gitdb==4.0.11',
        'GitPython==3.1.40',
        'idna==3.6',
        'itsdangerous==2.1.2',
        'Jinja2==3.1.2',
        'lxml==5.0.0',
        'MarkupSafe==2.1.3',
        'python-dotenv==1.0.0',
        'requests==2.31.0',
        'smmap==5.0.1',
        'soupsieve==2.5',
        'urllib3==2.1.0',
        'Werkzeug==3.0.1'
    ],
    python_requires='>=3.6',  # Adjust as per your project's Python version requirements
    entry_points={
        'console_scripts': [
        ],
    },
)
