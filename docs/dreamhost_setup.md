Dreamhost Setup
===============

## SSH setup
```bash
cat ~/.ssh/id_rsa.pub | ssh <usernam>e@<server>.dreamhost.com "mkdir ~/.ssh; cat >> ~/.ssh/authorized_keys"
```

Add the following to `~/.ssh/config`:

```
Host *
  ServerAliveInterval 15
  ServerAliveCountMax 4
```
