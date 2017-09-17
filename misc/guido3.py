import binascii
import bitcoin
address = '3BSBPJyP7r6W7WBz74ghL6W3A1aB7F6SoF'
pk = 'b3a6b8c655d471f003be2d0ccf5766c48cc36cdf02110cfcf3920971571c02b5'
msg = 'Grazie mille per il bellissimo ed originale regalo di matrimonio!'

OP_RETURN = 106
OP_PUSHDATA1 = 76
inputs = [
    {
    'output': '5377427396f9ba7ca186bd7c82e42a599e19115e7b8818d1051fa153aab5f0f6:3',
    'value': 10000000
    }
]

outputs = [
    {'address': address, 'value': 10000000 - 29800},
    {'script': '6a4c41' + binascii.hexlify(msg.encode()).decode(),
     'value': 0
    }
]
tx = bitcoin.mktx(inputs, outputs)
tx = bitcoin.sign(tx, 0, pk)
print(tx)
print(len(tx) / 2000)

