from setuptools import setup, find_packages

setup(
      name='sammobile-cli',
      version='0.0.1',
      description='CLI to download firmwares from Sammobile',
      author='Mehul Gupta',
      author_email='mehul.guptagm@gmail.com',
      packages=find_packages(),
      entry_points={
          'console_scripts': [
              'sammobile-cli = sammobile.cli:main',
          ]
      },
      url='https://github.com/therealssj/sammobile-cli',
      keywords=['sammobile', 'cli', 'command-line', 'python'],
      license='MIT',
      classifiers=[],
      install_requires=[
            'requests',
            'BeautifulSoup4',
            'tqdm',
            'robobrowser',
      ]
)
