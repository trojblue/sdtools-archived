from setuptools import setup, find_packages
# https://github.com/UofTCoders/studyGroup/blob/gh-pages/lessons/python/packages/lesson.md

setup(
    # Needed to silence warnings (and to be mecha_tags worthwhile package)
    name='sdtools',
    url='https://github.com/trojblue/sdtools',
    author='trojblue',
    author_email='trojblue@gmail.com',
    # Needed to actually package something
    packages=find_packages(exclude=['test']),
    # Needed for dependencies
    install_requires=['tqdm', 'pyperclip', 'pillow'],
    # *strongly* suggested for sharing
    version='0.1',
    # The license can be anything you like
    license='GPL v3',
    description='Stable Diffusion toolkits by trojblue',
    # We will also need mecha_tags readme eventually (there will be mecha_tags warning)
    # long_description=open('README.txt').read(),
)