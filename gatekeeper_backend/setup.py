from setuptools import find_packages, setup

setup(
    name="gatekeeper",
    version="0.1.0",
    description="gatekeeper",
    scripts=["manage.py"],
    package_dir={"": "."},
    packages=find_packages("src"),
    include_package_data=True,
    # classifiers=[
    #     'Environment :: Web Environment',
    #     'Framework :: Django',
    #     'License :: Other/Proprietary License',
    #     'Operating System :: Unix',
    #     'Private :: Do Not Upload',
    #     'Programming Language :: Python',
    # ],
)
