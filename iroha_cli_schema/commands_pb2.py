# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: commands.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


import primitive_pb2 as primitive__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='commands.proto',
  package='iroha.protocol',
  syntax='proto3',
  serialized_pb=_b('\n\x0e\x63ommands.proto\x12\x0eiroha.protocol\x1a\x0fprimitive.proto\"`\n\x10\x41\x64\x64\x41ssetQuantity\x12\x12\n\naccount_id\x18\x01 \x01(\t\x12\x10\n\x08\x61sset_id\x18\x02 \x01(\t\x12&\n\x06\x61mount\x18\x03 \x01(\x0b\x32\x16.iroha.protocol.Amount\",\n\x07\x41\x64\x64Peer\x12\x0f\n\x07\x61\x64\x64ress\x18\x01 \x01(\t\x12\x10\n\x08peer_key\x18\x02 \x01(\x0c\"6\n\x0c\x41\x64\x64Signatory\x12\x12\n\naccount_id\x18\x01 \x01(\t\x12\x12\n\npublic_key\x18\x02 \x01(\x0c\"G\n\x0b\x43reateAsset\x12\x12\n\nasset_name\x18\x01 \x01(\t\x12\x11\n\tdomain_id\x18\x02 \x01(\t\x12\x11\n\tprecision\x18\x03 \x01(\r\"M\n\rCreateAccount\x12\x14\n\x0c\x61\x63\x63ount_name\x18\x01 \x01(\t\x12\x11\n\tdomain_id\x18\x02 \x01(\t\x12\x13\n\x0bmain_pubkey\x18\x03 \x01(\x0c\"#\n\x0c\x43reateDomain\x12\x13\n\x0b\x64omain_name\x18\x01 \x01(\t\"9\n\x0fRemoveSignatory\x12\x12\n\naccount_id\x18\x01 \x01(\t\x12\x12\n\npublic_key\x18\x02 \x01(\x0c\"]\n\x15SetAccountPermissions\x12\x12\n\naccount_id\x18\x01 \x01(\t\x12\x30\n\x0bpermissions\x18\x02 \x01(\x0b\x32\x1b.iroha.protocol.Permissions\"6\n\x10SetAccountQuorum\x12\x12\n\naccount_id\x18\x01 \x01(\t\x12\x0e\n\x06quorum\x18\x02 \x01(\r\"\x8f\x01\n\rTransferAsset\x12\x16\n\x0esrc_account_id\x18\x01 \x01(\t\x12\x17\n\x0f\x64\x65st_account_id\x18\x02 \x01(\t\x12\x10\n\x08\x61sset_id\x18\x03 \x01(\t\x12\x13\n\x0b\x64\x65scription\x18\x04 \x01(\t\x12&\n\x06\x61mount\x18\x05 \x01(\x0b\x32\x16.iroha.protocol.Amount\"3\n\nAppendRole\x12\x12\n\naccount_id\x18\x01 \x01(\t\x12\x11\n\trole_name\x18\x02 \x01(\t\"4\n\nCreateRole\x12\x11\n\trole_name\x18\x01 \x01(\t\x12\x13\n\x0bpermissions\x18\x02 \x03(\t\"\xad\x05\n\x07\x43ommand\x12>\n\x12\x61\x64\x64_asset_quantity\x18\x01 \x01(\x0b\x32 .iroha.protocol.AddAssetQuantityH\x00\x12+\n\x08\x61\x64\x64_peer\x18\x02 \x01(\x0b\x32\x17.iroha.protocol.AddPeerH\x00\x12\x35\n\radd_signatory\x18\x03 \x01(\x0b\x32\x1c.iroha.protocol.AddSignatoryH\x00\x12\x33\n\x0c\x63reate_asset\x18\x04 \x01(\x0b\x32\x1b.iroha.protocol.CreateAssetH\x00\x12\x37\n\x0e\x63reate_account\x18\x05 \x01(\x0b\x32\x1d.iroha.protocol.CreateAccountH\x00\x12\x35\n\rcreate_domain\x18\x06 \x01(\x0b\x32\x1c.iroha.protocol.CreateDomainH\x00\x12\x36\n\x0bremove_sign\x18\x07 \x01(\x0b\x32\x1f.iroha.protocol.RemoveSignatoryH\x00\x12?\n\x0eset_permission\x18\x08 \x01(\x0b\x32%.iroha.protocol.SetAccountPermissionsH\x00\x12\x36\n\nset_quorum\x18\t \x01(\x0b\x32 .iroha.protocol.SetAccountQuorumH\x00\x12\x37\n\x0etransfer_asset\x18\n \x01(\x0b\x32\x1d.iroha.protocol.TransferAssetH\x00\x12\x31\n\x0b\x61ppend_role\x18\x0b \x01(\x0b\x32\x1a.iroha.protocol.AppendRoleH\x00\x12\x31\n\x0b\x63reate_role\x18\x0c \x01(\x0b\x32\x1a.iroha.protocol.CreateRoleH\x00\x42\t\n\x07\x63ommandb\x06proto3')
  ,
  dependencies=[primitive__pb2.DESCRIPTOR,])




_ADDASSETQUANTITY = _descriptor.Descriptor(
  name='AddAssetQuantity',
  full_name='iroha.protocol.AddAssetQuantity',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='account_id', full_name='iroha.protocol.AddAssetQuantity.account_id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='asset_id', full_name='iroha.protocol.AddAssetQuantity.asset_id', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='amount', full_name='iroha.protocol.AddAssetQuantity.amount', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=51,
  serialized_end=147,
)


_ADDPEER = _descriptor.Descriptor(
  name='AddPeer',
  full_name='iroha.protocol.AddPeer',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='address', full_name='iroha.protocol.AddPeer.address', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='peer_key', full_name='iroha.protocol.AddPeer.peer_key', index=1,
      number=2, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=_b(""),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=149,
  serialized_end=193,
)


_ADDSIGNATORY = _descriptor.Descriptor(
  name='AddSignatory',
  full_name='iroha.protocol.AddSignatory',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='account_id', full_name='iroha.protocol.AddSignatory.account_id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='public_key', full_name='iroha.protocol.AddSignatory.public_key', index=1,
      number=2, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=_b(""),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=195,
  serialized_end=249,
)


_CREATEASSET = _descriptor.Descriptor(
  name='CreateAsset',
  full_name='iroha.protocol.CreateAsset',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='asset_name', full_name='iroha.protocol.CreateAsset.asset_name', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='domain_id', full_name='iroha.protocol.CreateAsset.domain_id', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='precision', full_name='iroha.protocol.CreateAsset.precision', index=2,
      number=3, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=251,
  serialized_end=322,
)


_CREATEACCOUNT = _descriptor.Descriptor(
  name='CreateAccount',
  full_name='iroha.protocol.CreateAccount',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='account_name', full_name='iroha.protocol.CreateAccount.account_name', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='domain_id', full_name='iroha.protocol.CreateAccount.domain_id', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='main_pubkey', full_name='iroha.protocol.CreateAccount.main_pubkey', index=2,
      number=3, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=_b(""),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=324,
  serialized_end=401,
)


_CREATEDOMAIN = _descriptor.Descriptor(
  name='CreateDomain',
  full_name='iroha.protocol.CreateDomain',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='domain_name', full_name='iroha.protocol.CreateDomain.domain_name', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=403,
  serialized_end=438,
)


_REMOVESIGNATORY = _descriptor.Descriptor(
  name='RemoveSignatory',
  full_name='iroha.protocol.RemoveSignatory',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='account_id', full_name='iroha.protocol.RemoveSignatory.account_id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='public_key', full_name='iroha.protocol.RemoveSignatory.public_key', index=1,
      number=2, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=_b(""),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=440,
  serialized_end=497,
)


_SETACCOUNTPERMISSIONS = _descriptor.Descriptor(
  name='SetAccountPermissions',
  full_name='iroha.protocol.SetAccountPermissions',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='account_id', full_name='iroha.protocol.SetAccountPermissions.account_id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='permissions', full_name='iroha.protocol.SetAccountPermissions.permissions', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=499,
  serialized_end=592,
)


_SETACCOUNTQUORUM = _descriptor.Descriptor(
  name='SetAccountQuorum',
  full_name='iroha.protocol.SetAccountQuorum',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='account_id', full_name='iroha.protocol.SetAccountQuorum.account_id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='quorum', full_name='iroha.protocol.SetAccountQuorum.quorum', index=1,
      number=2, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=594,
  serialized_end=648,
)


_TRANSFERASSET = _descriptor.Descriptor(
  name='TransferAsset',
  full_name='iroha.protocol.TransferAsset',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='src_account_id', full_name='iroha.protocol.TransferAsset.src_account_id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='dest_account_id', full_name='iroha.protocol.TransferAsset.dest_account_id', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='asset_id', full_name='iroha.protocol.TransferAsset.asset_id', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='description', full_name='iroha.protocol.TransferAsset.description', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='amount', full_name='iroha.protocol.TransferAsset.amount', index=4,
      number=5, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=651,
  serialized_end=794,
)


_APPENDROLE = _descriptor.Descriptor(
  name='AppendRole',
  full_name='iroha.protocol.AppendRole',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='account_id', full_name='iroha.protocol.AppendRole.account_id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='role_name', full_name='iroha.protocol.AppendRole.role_name', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=796,
  serialized_end=847,
)


_CREATEROLE = _descriptor.Descriptor(
  name='CreateRole',
  full_name='iroha.protocol.CreateRole',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='role_name', full_name='iroha.protocol.CreateRole.role_name', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='permissions', full_name='iroha.protocol.CreateRole.permissions', index=1,
      number=2, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=849,
  serialized_end=901,
)


_COMMAND = _descriptor.Descriptor(
  name='Command',
  full_name='iroha.protocol.Command',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='add_asset_quantity', full_name='iroha.protocol.Command.add_asset_quantity', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='add_peer', full_name='iroha.protocol.Command.add_peer', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='add_signatory', full_name='iroha.protocol.Command.add_signatory', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='create_asset', full_name='iroha.protocol.Command.create_asset', index=3,
      number=4, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='create_account', full_name='iroha.protocol.Command.create_account', index=4,
      number=5, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='create_domain', full_name='iroha.protocol.Command.create_domain', index=5,
      number=6, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='remove_sign', full_name='iroha.protocol.Command.remove_sign', index=6,
      number=7, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='set_permission', full_name='iroha.protocol.Command.set_permission', index=7,
      number=8, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='set_quorum', full_name='iroha.protocol.Command.set_quorum', index=8,
      number=9, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='transfer_asset', full_name='iroha.protocol.Command.transfer_asset', index=9,
      number=10, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='append_role', full_name='iroha.protocol.Command.append_role', index=10,
      number=11, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='create_role', full_name='iroha.protocol.Command.create_role', index=11,
      number=12, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
    _descriptor.OneofDescriptor(
      name='command', full_name='iroha.protocol.Command.command',
      index=0, containing_type=None, fields=[]),
  ],
  serialized_start=904,
  serialized_end=1589,
)

_ADDASSETQUANTITY.fields_by_name['amount'].message_type = primitive__pb2._AMOUNT
_SETACCOUNTPERMISSIONS.fields_by_name['permissions'].message_type = primitive__pb2._PERMISSIONS
_TRANSFERASSET.fields_by_name['amount'].message_type = primitive__pb2._AMOUNT
_COMMAND.fields_by_name['add_asset_quantity'].message_type = _ADDASSETQUANTITY
_COMMAND.fields_by_name['add_peer'].message_type = _ADDPEER
_COMMAND.fields_by_name['add_signatory'].message_type = _ADDSIGNATORY
_COMMAND.fields_by_name['create_asset'].message_type = _CREATEASSET
_COMMAND.fields_by_name['create_account'].message_type = _CREATEACCOUNT
_COMMAND.fields_by_name['create_domain'].message_type = _CREATEDOMAIN
_COMMAND.fields_by_name['remove_sign'].message_type = _REMOVESIGNATORY
_COMMAND.fields_by_name['set_permission'].message_type = _SETACCOUNTPERMISSIONS
_COMMAND.fields_by_name['set_quorum'].message_type = _SETACCOUNTQUORUM
_COMMAND.fields_by_name['transfer_asset'].message_type = _TRANSFERASSET
_COMMAND.fields_by_name['append_role'].message_type = _APPENDROLE
_COMMAND.fields_by_name['create_role'].message_type = _CREATEROLE
_COMMAND.oneofs_by_name['command'].fields.append(
  _COMMAND.fields_by_name['add_asset_quantity'])
_COMMAND.fields_by_name['add_asset_quantity'].containing_oneof = _COMMAND.oneofs_by_name['command']
_COMMAND.oneofs_by_name['command'].fields.append(
  _COMMAND.fields_by_name['add_peer'])
_COMMAND.fields_by_name['add_peer'].containing_oneof = _COMMAND.oneofs_by_name['command']
_COMMAND.oneofs_by_name['command'].fields.append(
  _COMMAND.fields_by_name['add_signatory'])
_COMMAND.fields_by_name['add_signatory'].containing_oneof = _COMMAND.oneofs_by_name['command']
_COMMAND.oneofs_by_name['command'].fields.append(
  _COMMAND.fields_by_name['create_asset'])
_COMMAND.fields_by_name['create_asset'].containing_oneof = _COMMAND.oneofs_by_name['command']
_COMMAND.oneofs_by_name['command'].fields.append(
  _COMMAND.fields_by_name['create_account'])
_COMMAND.fields_by_name['create_account'].containing_oneof = _COMMAND.oneofs_by_name['command']
_COMMAND.oneofs_by_name['command'].fields.append(
  _COMMAND.fields_by_name['create_domain'])
_COMMAND.fields_by_name['create_domain'].containing_oneof = _COMMAND.oneofs_by_name['command']
_COMMAND.oneofs_by_name['command'].fields.append(
  _COMMAND.fields_by_name['remove_sign'])
_COMMAND.fields_by_name['remove_sign'].containing_oneof = _COMMAND.oneofs_by_name['command']
_COMMAND.oneofs_by_name['command'].fields.append(
  _COMMAND.fields_by_name['set_permission'])
_COMMAND.fields_by_name['set_permission'].containing_oneof = _COMMAND.oneofs_by_name['command']
_COMMAND.oneofs_by_name['command'].fields.append(
  _COMMAND.fields_by_name['set_quorum'])
_COMMAND.fields_by_name['set_quorum'].containing_oneof = _COMMAND.oneofs_by_name['command']
_COMMAND.oneofs_by_name['command'].fields.append(
  _COMMAND.fields_by_name['transfer_asset'])
_COMMAND.fields_by_name['transfer_asset'].containing_oneof = _COMMAND.oneofs_by_name['command']
_COMMAND.oneofs_by_name['command'].fields.append(
  _COMMAND.fields_by_name['append_role'])
_COMMAND.fields_by_name['append_role'].containing_oneof = _COMMAND.oneofs_by_name['command']
_COMMAND.oneofs_by_name['command'].fields.append(
  _COMMAND.fields_by_name['create_role'])
_COMMAND.fields_by_name['create_role'].containing_oneof = _COMMAND.oneofs_by_name['command']
DESCRIPTOR.message_types_by_name['AddAssetQuantity'] = _ADDASSETQUANTITY
DESCRIPTOR.message_types_by_name['AddPeer'] = _ADDPEER
DESCRIPTOR.message_types_by_name['AddSignatory'] = _ADDSIGNATORY
DESCRIPTOR.message_types_by_name['CreateAsset'] = _CREATEASSET
DESCRIPTOR.message_types_by_name['CreateAccount'] = _CREATEACCOUNT
DESCRIPTOR.message_types_by_name['CreateDomain'] = _CREATEDOMAIN
DESCRIPTOR.message_types_by_name['RemoveSignatory'] = _REMOVESIGNATORY
DESCRIPTOR.message_types_by_name['SetAccountPermissions'] = _SETACCOUNTPERMISSIONS
DESCRIPTOR.message_types_by_name['SetAccountQuorum'] = _SETACCOUNTQUORUM
DESCRIPTOR.message_types_by_name['TransferAsset'] = _TRANSFERASSET
DESCRIPTOR.message_types_by_name['AppendRole'] = _APPENDROLE
DESCRIPTOR.message_types_by_name['CreateRole'] = _CREATEROLE
DESCRIPTOR.message_types_by_name['Command'] = _COMMAND
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

AddAssetQuantity = _reflection.GeneratedProtocolMessageType('AddAssetQuantity', (_message.Message,), dict(
  DESCRIPTOR = _ADDASSETQUANTITY,
  __module__ = 'commands_pb2'
  # @@protoc_insertion_point(class_scope:iroha.protocol.AddAssetQuantity)
  ))
_sym_db.RegisterMessage(AddAssetQuantity)

AddPeer = _reflection.GeneratedProtocolMessageType('AddPeer', (_message.Message,), dict(
  DESCRIPTOR = _ADDPEER,
  __module__ = 'commands_pb2'
  # @@protoc_insertion_point(class_scope:iroha.protocol.AddPeer)
  ))
_sym_db.RegisterMessage(AddPeer)

AddSignatory = _reflection.GeneratedProtocolMessageType('AddSignatory', (_message.Message,), dict(
  DESCRIPTOR = _ADDSIGNATORY,
  __module__ = 'commands_pb2'
  # @@protoc_insertion_point(class_scope:iroha.protocol.AddSignatory)
  ))
_sym_db.RegisterMessage(AddSignatory)

CreateAsset = _reflection.GeneratedProtocolMessageType('CreateAsset', (_message.Message,), dict(
  DESCRIPTOR = _CREATEASSET,
  __module__ = 'commands_pb2'
  # @@protoc_insertion_point(class_scope:iroha.protocol.CreateAsset)
  ))
_sym_db.RegisterMessage(CreateAsset)

CreateAccount = _reflection.GeneratedProtocolMessageType('CreateAccount', (_message.Message,), dict(
  DESCRIPTOR = _CREATEACCOUNT,
  __module__ = 'commands_pb2'
  # @@protoc_insertion_point(class_scope:iroha.protocol.CreateAccount)
  ))
_sym_db.RegisterMessage(CreateAccount)

CreateDomain = _reflection.GeneratedProtocolMessageType('CreateDomain', (_message.Message,), dict(
  DESCRIPTOR = _CREATEDOMAIN,
  __module__ = 'commands_pb2'
  # @@protoc_insertion_point(class_scope:iroha.protocol.CreateDomain)
  ))
_sym_db.RegisterMessage(CreateDomain)

RemoveSignatory = _reflection.GeneratedProtocolMessageType('RemoveSignatory', (_message.Message,), dict(
  DESCRIPTOR = _REMOVESIGNATORY,
  __module__ = 'commands_pb2'
  # @@protoc_insertion_point(class_scope:iroha.protocol.RemoveSignatory)
  ))
_sym_db.RegisterMessage(RemoveSignatory)

SetAccountPermissions = _reflection.GeneratedProtocolMessageType('SetAccountPermissions', (_message.Message,), dict(
  DESCRIPTOR = _SETACCOUNTPERMISSIONS,
  __module__ = 'commands_pb2'
  # @@protoc_insertion_point(class_scope:iroha.protocol.SetAccountPermissions)
  ))
_sym_db.RegisterMessage(SetAccountPermissions)

SetAccountQuorum = _reflection.GeneratedProtocolMessageType('SetAccountQuorum', (_message.Message,), dict(
  DESCRIPTOR = _SETACCOUNTQUORUM,
  __module__ = 'commands_pb2'
  # @@protoc_insertion_point(class_scope:iroha.protocol.SetAccountQuorum)
  ))
_sym_db.RegisterMessage(SetAccountQuorum)

TransferAsset = _reflection.GeneratedProtocolMessageType('TransferAsset', (_message.Message,), dict(
  DESCRIPTOR = _TRANSFERASSET,
  __module__ = 'commands_pb2'
  # @@protoc_insertion_point(class_scope:iroha.protocol.TransferAsset)
  ))
_sym_db.RegisterMessage(TransferAsset)

AppendRole = _reflection.GeneratedProtocolMessageType('AppendRole', (_message.Message,), dict(
  DESCRIPTOR = _APPENDROLE,
  __module__ = 'commands_pb2'
  # @@protoc_insertion_point(class_scope:iroha.protocol.AppendRole)
  ))
_sym_db.RegisterMessage(AppendRole)

CreateRole = _reflection.GeneratedProtocolMessageType('CreateRole', (_message.Message,), dict(
  DESCRIPTOR = _CREATEROLE,
  __module__ = 'commands_pb2'
  # @@protoc_insertion_point(class_scope:iroha.protocol.CreateRole)
  ))
_sym_db.RegisterMessage(CreateRole)

Command = _reflection.GeneratedProtocolMessageType('Command', (_message.Message,), dict(
  DESCRIPTOR = _COMMAND,
  __module__ = 'commands_pb2'
  # @@protoc_insertion_point(class_scope:iroha.protocol.Command)
  ))
_sym_db.RegisterMessage(Command)


try:
  # THESE ELEMENTS WILL BE DEPRECATED.
  # Please use the generated *_pb2_grpc.py files instead.
  import grpc
  from grpc.beta import implementations as beta_implementations
  from grpc.beta import interfaces as beta_interfaces
  from grpc.framework.common import cardinality
  from grpc.framework.interfaces.face import utilities as face_utilities
except ImportError:
  pass
# @@protoc_insertion_point(module_scope)