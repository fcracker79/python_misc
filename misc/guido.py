import binascii
import bitcoin
address = '3BSBPJyP7r6W7WBz74ghL6W3A1aB7F6SoF'
pk = 'b3a6b8c655d471f003be2d0ccf5766c48cc36cdf02110cfcf3920971571c02b5'
msg = 'Grazie mille per il bellissimo ed originale regalo di matrimonio!'

OP_RETURN = 106
OP_PUSHDATA1 = 76

script = [OP_RETURN, OP_PUSHDATA1, len(msg)] + [int(x) for x in msg.encode()]
print(script)
print([':02x'.format(x) for x in [OP_RETURN, OP_PUSHDATA1, len(msg)] + [int(x) for x in msg.encode()]])
print(['{:02x}'.format(x) for x in [OP_RETURN, OP_PUSHDATA1, len(msg)]] + [binascii.hexlify(msg.encode()).decode()])
print(bitcoin.serialize_script(['{:02x}'.format(x) for x in [OP_RETURN, OP_PUSHDATA1, len(msg)]] + [binascii.hexlify(msg.encode())]))
