from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException
import json
from datetime import datetime

rpc_user='quaker_quorum'
rpc_password='franklin_fought_for_continental_cash'
rpc_ip='3.134.159.30'
rpc_port='8332'

rpc_connection = AuthServiceProxy("http://%s:%s@%s:%s"%(rpc_user, rpc_password, rpc_ip, rpc_port))

###################################

class TXO:
    def __init__(self, tx_hash, n, amount, owner, time ):
        self.tx_hash = tx_hash 
        self.n = n
        self.amount = amount
        self.owner = owner
        self.time = time
        self.inputs = []

    def __str__(self, level=0):
        ret = "\t"*level+repr(self.tx_hash)+"\n"
        for tx in self.inputs:
            ret += tx.__str__(level+1)
        return ret

    def to_json(self):
        fields = ['tx_hash','n','amount','owner']
        json_dict = { field: self.__dict__[field] for field in fields }
        json_dict.update( {'time': datetime.timestamp(self.time) } )
        if len(self.inputs) > 0:
            for txo in self.inputs:
                json_dict.update( {'inputs': json.loads(txo.to_json()) } )
        return json.dumps(json_dict, sort_keys=True, indent=4)

    @classmethod
    def from_tx_hash(cls,tx_hash,n=0):
        tx_dict = rpc_connection.getrawtransaction(tx_hash, True)
        
        return TXO(tx_dict['hash'], tx_dict['vout'][n]['n'], tx_dict['vout'][n]['value'] * (10**8), tx_dict['vout'][n]['scriptPubKey']['addresses'][0], datetime.fromtimestamp(tx_dict['time']))

#     def get_inputs(self,d=1):
#         tx_dict = rpc_connection.getrawtransaction(self.tx_hash, True)
#         self.inputs = tx_dict['vin']
#         last_round = tx_dict['vin']
        
#         for _ in range(d - 1):
#             curr_round = []
#             for inp in last_round:
#                 vins = rpc_connection.getrawtransaction(self.tx_hash, True)['vin']
#                 curr_round.extend(vins)
#             self.inputs.extend(curr_round)
#             last_round = curr_round

