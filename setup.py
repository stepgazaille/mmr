from setuptools import setup, find_packages

setup(name='qbsum',
      version='0.1.1',
      description='A set of query-based summarization algorithms',
      author='Stephane Gazaille',
      author_email='stepgazaille@gmail.com',
      url='https://github.com/stepgazaille/qbsum',
      packages=find_packages(exclude=['tests']),
      zip_safe=True,
      install_requires=[
        'pandas>=0.23.4',
        'nltk>=3.4',
        'en_core_web_sm @ https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-2.1.0a0/en_core_web_sm-2.1.0a0.tar.gz'
        ]
      )
