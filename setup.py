from setuptools import setup, find_packages

setup(name='mmr',
      version='0.1.2',
      description='A naive implementation of MMR',
      author='Stephane Gazaille',
      author_email='stepgazaille@gmail.com',
      url='https://github.com/stepgazaille/mmr',
      packages=find_packages(exclude=['tests']),
      zip_safe=True,
      install_requires=[
        'pandas>=0.23.4',
        'nltk>=3.4',
        'en_core_web_sm @ https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-2.1.0/en_core_web_sm-2.1.0.tar.gz'
        ]
      )
