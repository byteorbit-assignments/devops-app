from setuptools import setup, find_packages

setup(
    name='devops-app',
    description='',
    author='Byte Orbit',
    author_email='assignments@byteorbit.com',
    url='http://byteorbit.com/',
    use_scm_version=True,  # Version from hg or git
    setup_requires=['setuptools_scm'],
    package_dir={'': 'src'},
    packages=find_packages('src'),
    include_package_data=True,
    zip_safe=False,
)
