Welcome to Iroha-Cli !🗻
=====================

What's Iroha-cli?
--------
iroha-ya-cli は Irohaの台帳を変更、内容確認をquery / tx を使い行うもの
iroha-ya-cli is that send tx / query to Iroha and read / write ledger data

Who uses Iroha-cli?
--------

User who wants to access Iroha ledger. **Not support user who wants to provision or manage Iroha network**  
いろは台帳にアクセスする(Tx/Query)人を主に対象とする。台帳を管理する人は現状、対象としない
  
What Iroha-cli has function?
--------
Generally iroha-ya-cli has two parts.
CLIは以下の2つを基本機能として持つ

* send transaction to iroha for writing data / Transactionをいろはに署名付きで投げ、台帳にデータを追加、更新を行う
* send query to iroha for getting data / Queryをいろはに署名付きで投げ、台帳のデータを取得する
　　
In addition, supports this　　
それに加え以下の機能を持つ　　

* generate keypair,config / 秘密鍵、構成ファイルの作成 
　　
Contents
--------

.. toctree::
   :maxdepth: 2
   :caption: Getting Started🛫 / はじめに🛫

   environments
   getting_started
   samples

.. toctree::
   :maxdepth: 2
   :caption: Tutorials✈️ / チュートリアル✈️

   generate_key_pair_configure
   send_transaction
   send_query

.. toctree::
   :maxdepth: 2
   :caption: Explain of Command,Query / Command,Query等の詳細
   
   transaction
   query
   built_in

.. toctree::
   :maxdepth: 2
   :caption: Extension🛠 / 独自カスタム🛠

   add_new_command
   add_new_query
