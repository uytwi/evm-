from web3 import Web3,Account
from web3.middleware import geth_poa_middleware
import time




class EvmClass(object):

    def __init__(self,rpc,private_key,to_address,hash_list):
        #rpc信息
        self.rpc = rpc 
        #接受地址
        self.to_address = to_address 
        self.hash_list = hash_list
        #你自己的私钥
        self.private_key= private_key
        self.lim=1 #打多少张 10u大概1000张,最好准备6u
        # 连接到rpc节点
        self.w3 = Web3(Web3.HTTPProvider(self.rpc))
        # w3.middleware_onion.inject(geth_poa_middleware, layer=0) #添加poa扩展字段
        self.from_address = Account.from_key(self.private_key).address
        self.chain_id = self.w3.eth.chain_id
        print('网络链接：',self.w3.is_connected())
        print('chain_id', self.chain_id )

    def gas_(self):
        gas_price = self.w3.eth.gas_price
        # 将燃气价格从Wei转换为Gwei
        gas_price_gwei = self.w3.from_wei(gas_price, 'Gwei')
        print("实时gas",gas_price_gwei)
        return gas_price
    #判断网络链接
    def to_wgei(self,gas_price_Gwei):
        gas_price_wei = self.w3.to_wei(gas_price_Gwei, 'Gwei')
        return gas_price_wei

    def main(self,_hash,lim = 1):
        if self.w3.is_connected() ==True:
            #获取当前noce
            nonce= self.w3.eth.get_transaction_count(self.from_address)
            # 获取当前燃气价格
            gas_price = self.w3.eth.gas_price
            # gas_price = to_wgei(10)
            # 将燃气价格从Wei转换为Gwei
            gas_price_gwei = self.w3.from_wei(gas_price, 'Gwei')
            value = self.w3.to_wei(0, 'ether')
            print("当前nonce:",nonce,"当前gas:",gas_price_gwei,'发送地址:',self.from_address)

            data_hex = _hash

            print("data_hex ",data_hex)

            # 批量发送交易
            for i in range(self.lim):
                transaction = {
                    'from': self.from_address,  # from：发送地址
                    'to': to_address,  # to：接收地址
                    'value':value,  # value：发送的以太币数量（整数）。这是以太币的数量，以Wei为单位。1 Ether等于10^18 Wei。
                    'nonce': nonce,  # nonce：发送地址的交易计数（整数）。它用于确保交易的唯一性。
                    'gas':25000,  # gas：指定用于交易的燃气数量（整数）。燃气用于执行交易的计算和存储操作。
                    'gasPrice': gas_price,  # gasPrice：燃气价格（整数）。以Wei为单位的燃气单价，用于计算交易的燃气费用。
                    'data': data_hex,  # 要添加到 Input Data 的自定义数据
                    'chainId': self.chain_id  # 区块链id
                }
                # print(transaction)
                # print(transaction)
                # 2.签名交易
                signed = self.w3.eth.account.sign_transaction(transaction, private_key)
                try:
                    # 3.广播交易
                    tx_hash = self.w3.eth.send_raw_transaction(signed.rawTransaction)
                    print("Hash:", tx_hash.hex(),'noce:',nonce)
                except Exception as e:
                    print('交易发生错误',e,'交易data：',data_hex)
                nonce+=1

    def runc(self):
        hash_count = len(self.hash_list)
        # print(hash_count,self.hash_list)
        for _hash in self.hash_list:
            print(_hash,hash_count)

        

#拆分数量 防止 none 过大 导致无法广播,100次拆分一次
# none_nums = 1

hash_list = ['。。。。。。。'] #哈希列表
rpc = "https://bsc.drpc.org"#prc
to_address = '。。。。。' #目标地址
private_key = '。。。。。' # 你自己的私钥

EvmClass(rpc,private_key = private_key,to_address = to_address,hash_list = hash_list).runc()

