# brownie compiles, dumps to file, gets abi/bytecode, spins up local ganache
# need private key and account

from brownie import accounts 


def deploy_simple_storage():
  account = accounts[0]
  print(account)
  


def main(): 
  deploy_simple_storage()

