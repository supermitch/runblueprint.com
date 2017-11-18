Dreamhost Setup
===============

## SSH key setup
```bash
cat ~/.ssh/id_rsa.pub | ssh <usernam>e@<server>.dreamhost.com "mkdir ~/.ssh; cat >> ~/.ssh/authorized_keys"
```
