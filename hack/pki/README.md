# Configure secure access to on-prem nodes

Initially on-prem Linux nodes are configured with local user Linux accounts - user names/passwords.

`configure-nodes.py` automates the hardening of users access to remote nodes:
1. Take the following input parameters:
    - user name 
    - user paassword provided by on-prem admin
    - user strong passwrd that will be replace the initially provided password.
    - path to public SSH key to configure SSH access using public keys.

2. SSHes to each node using user name and password
3. Changes the existing password to the new, strong password.
4. Configures PKI SSH access.

After this point, only PKI SSH access should be used. This is essential requirement for using Ansible playbooks.

# Configure python venv

Create the virtual env if it is missing.
```
$ python3 -m venv ./venv

$ . ./venv/bin/activate

(venv) $
(venv) $ pip install -r requirements.txt
...
(venv) $ pip install --upgrade pip
```

# Configure remote nodes.

At the moment this script should be run on newly provisioned VM nodes only 
to change the temp password and configure SSH PKI access. 

Future improvements will be added as needed.

```
$ . ./venv/bin/activate

(venv) $ ./configure-nodes.py \
--username dimitar \
--init-password <temp-password> \
--strong-password <my-strong-password>
```


