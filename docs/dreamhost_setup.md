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

## Git setup

```bash
git config --global user.name "John Doe"
git config --global user.email johndoe@example.com
git config --global core.editor "vim"
git config --global push.default simple
# ?? git config --global pull.rebase true
```
