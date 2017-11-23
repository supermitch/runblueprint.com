Ansible Setup
=============

Ansible runs on Python 2.7 still 🙁

```bash
pyenv install 2.7.14
pyenv local 2.7.14
python -V  # ok?
virtualenv ansible_env
source ansible_env/bin/activate
which pip  # ok?
pip install ansible
ansible --version  # ok?
```
