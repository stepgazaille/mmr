from setuptools import setup, find_packages

setup(name='qbsum',
      version='0.1.0',
      description='A set of query-based summarization algorithms',
      author='Stephane Gazaille',
      author_email='stephane.gazaille@croesus.com',
      url='https://github.com/stepgazaille/qbsum',
      packages=find_packages(exclude=['tests']),
      zip_safe=True,
      dependency_links = [
        'git+https://github.com/stepgazaille/pythonrouge.git#egg=pythonrouge'
        ],
      install_requires=[
        'pandas>=0.23.4',
        'spacy>=2.0.16',
        'pythonrouge'
        ]
      )
