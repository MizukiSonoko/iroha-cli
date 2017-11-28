Generate KeyPair / Configure
=====================

Irohaでは全ての処理に電子署名を必要とします。なのでIrohaを扱う上で一番最初に行うべきことは自分自身の鍵を持つことです。

コマンドは
.. code-block:: shell

   iroha-ya-cli keygen  --account_name mizuki --make_conf yes
   
です。もし詳細が知りたい場合は ``-h`` で見ることが出来ます　　　　

.. code-block:: shell 

   root@9a7f3f24d416:/# iroha-ya-cli keygen -h　　
   usage: iroha-ya-cli keygen [-h] [--make_conf MAKE_CONF] --account_name ACCOUNT_NAME [--config CONFIG]

   optional arguments:
  　　-h, --help            show this help message and exit
  　　--make_conf MAKE_CONF
                        generate conf.yml
  　　--account_name ACCOUNT_NAME
                        target's account name
  　　--config CONFIG       config.yml's path

生成物として、 ``config.yml`` ``mizuki.pri`` ``mizuki.pri`` の 3つがカレントディレクトリに生成されます。

.. code-block:: shell 

  　　root@9a7f3f24d416:/# ls -l
  　　total 76K
  　　-rw-r--r--   1 root root  122 Nov 28 01:33 config.yml
  　　-rw-r--r--   1 root root   88 Nov 28 01:33 mizuki.pri
  　　-rw-r--r--   1 root root   44 Nov 28 01:33 mizuki.pub
    
* mizuki.pri 秘密鍵です。秘密にしてください。内容は ``Base64`` でエンコードされています。

.. code-block::  

   yFvujNuiOrhO2CHmEaDn6L9QXF7ecvRja/nWCt1fmlKrTdZ07WWjOQksD0zjPu36uh15NPH4JVG13kfS+yHCsw==

* mizuki.pub 公開鍵です。内容は ``Base64`` でエンコードされています。

.. code-block::  

   O2qV3gXeDL0TAoq/yyjVTbbeZ1L+IW1hzCeIW7OJP5s=
 
* config.yml　設定ファイルです。

.. code-block::

   account:
      name: mizuki
      privateKeyPath: mizuki.pri
      publicKeyPath: mizuki.pub
   peer:
      address: localhost
      port: 50051
      
- ``account`` はCliを実行する人の情報です。Pathはconfigからの相対パスか絶対パスで指定します。
- ``peer`` は Transaction/Queryを投げる先の情報です。

