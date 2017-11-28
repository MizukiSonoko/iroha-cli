Getting Started
=====================

What's required Iroha-cli?
------------------------------

| iroha-ya-cli running on Python🐍  
| In now, only Python3.5

Simple Install 
------------------------------

Cli is hosted by pypi.
`pypi/iroha-ya-cli <https://pypi.python.org/pypi/iroha-ya-cli>`_

.. image:: https://badge.fury.io/py/iroha-ya-cli.svg
    :target: https://badge.fury.io/py/iroha-ya-cli

so you can install using this command.
  
.. code-block:: shell

   pip install iroha-ya-cli

or 

.. code-block:: shell

   git clone -b v1.2.5 https://github.com/MizukiSonoko/iroha-cli.git
   cd iroha-cli
   python setup.py install
   
This is `release list <https://github.com/MizukiSonoko/iroha-cli/releases>`_ . 

Generate key pair and config
------------------------------

You should create keypair and config.
| **KeyPair is very important.If you lost keypair, You willn't be able to access Iroha ledger**
| **注意！KeyPairはアカウントと紐付いており紛失するとIrohaに対しへアクセス(Transaction/Query)ができなくなります**

.. code-block:: shell

   iroha-ya-cli keygen  --account_name mizuki --make_conf yes
   
* account_name KeyPairに紐付くAccountの名前です。この名前のKeyが生成されます。名前はCreateAccount等のコマンドを実行しない限り、Irohaとは関係ないので変更しても問題ありません。

.. code-block:: shell

   root@9a7f3f24d416:/# ls -htl
   total 76K
   -rw-r--r--   1 root root  122 Nov 28 01:33 config.yml
   -rw-r--r--   1 root root   88 Nov 28 01:33 mizuki.pri
   -rw-r--r--   1 root root   44 Nov 28 01:33 mizuki.pub

**Testのため、Permissionを644にしていますが、推奨されません。600にしてください

Common Error
------------------------------

chino

