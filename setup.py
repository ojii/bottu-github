from distutils.core import setup

setup(
    name='bottu-github',
    version='0.1',
    py_modules=['bottu_github'],
    url='',
    license='BSD',
    author='Jonas Obrist',
    author_email='ojiidotch@gmail.com',
    description='',
    install_requires=[
        'pyOpenSSL',
        'bottu',
    ],
    entry_points = {
        'bottu.plugins': [
            'github = bottu_github:register'
        ],
    }
)
