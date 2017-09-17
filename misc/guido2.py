import bitcoin
import hashlib
auguri = 'A Mirko e Rossana i nostri più sinceri auguri, felici di vivere questo giorno con voi!'
for x in range(0, 20170729):
  auguri = hashlib.sha256(auguri.encode()).hexdigest()

print(auguri)
print(bitcoin.privtoaddr(auguri))
