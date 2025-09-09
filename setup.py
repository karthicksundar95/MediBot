from steuptools import find_packages, setup

with open("./requirements.txt", r) as f:
    requirements = f.read().splitlines()

setup(
    name = "Doctor bot",
    version = "0.0.0.1",
    author = "Karthick Sundar",
    author_email = "karthicksundar@gmail.com",
    packages = find_packages(), # auto detects all subfolders in this project which has __init__.py and treats them as package
    install_requires = requirements# to install your package what are all the dependencies to be installed prior
)   