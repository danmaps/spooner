[![PyPI version](https://badge.fury.io/py/spooner.svg)](https://pypi.org/project/spooner/)
[![codecov](https://codecov.io/gh/danmaps/spooner/branch/master/graph/badge.svg)](https://codecov.io/gh/danmaps/spooner)
[![Build Status](https://dev.azure.com/dannybmcvey0582/spooner/_apis/build/status/danmaps.spooner?branchName=master)](https://dev.azure.com/dannybmcvey0582/spooner/_build/latest?definitionId=1&branchName=master)
# spooner

Generates [spoonerisms](https://en.wikipedia.org/wiki/Spoonerism) based on sounds in words.

```
input: three cheers for our dear old queen
['cheers', 'for'] -> [['fears'], ['chore']]
three fears chore our dear old queen
['cheers', 'queen'] -> [['queers'], ['cheane']]
three queers for our dear old cheane
['for', 'dear'] -> [["d'or", 'doar', 'doerr', 'dohr', 'door', 'dore', 'dorr'], ['fear', 'fier']]
three cheers dohr our fier old queen
['for', 'old'] -> [['oar', 'ohr', 'or', 'ore', 'orr'], ['fold']]
three cheers orr our dear fold queen
['dear', 'queen'] -> [['queer'], ['dean', 'deane', 'deen']]
three cheers for our queer old deane

input: I've got hope in my soul
['got', 'my'] -> [['mott', 'motte'], ['gae', 'guy', 'ngai', 'ngai']]
I've motte hope in ngai soul
['hope', 'my'] -> [['mope'], ['heye', 'hi', 'high', 'hy']]
I've got mope in heye soul
['hope', 'soul'] -> [['soap', 'sope'], ['hoel', 'hoell', 'hoelle', 'hohl', 'hole', 'whole']]
I've got soap in my hohl
['my', 'soul'] -> [['cy', 'psi', 'sai', 'sai', 'sigh', 'sy'], ['mohl', 'mole']]
I've got hope in psi mohl

input: you missed my history lecture
['missed', 'history'] -> [['hissed'], ['mystery']]
you hissed my mystery lecture
['my', 'history'] -> [['heye', 'hi', 'high', 'hy'], ['mystery']]
you missed high mystery lecture

input: a blushing crow
['blushing', 'crow'] -> [['crushing'], ['bleau', 'blow', 'blowe']]
a crushing blow

input: There’s nothing like a good spoonerism to tickle your funny bone
['like', 'to'] -> [['teich', 'tike', 'tyke'], ['leu', 'lew', 'lieu', 'lieu', 'loo', 'lou', 'louw', 'loux', 'lu', 'lue']]
There’s nothing teich a good spoonerism leu tickle your funny bone
['like', 'funny'] -> [['fike', 'fyke'], ['lunney', 'lunny']]
There’s nothing fyke a good spoonerism to tickle your lunny bone
['like', 'bone'] -> [['bike'], ['loan', 'lone']]
There’s nothing bike a good spoonerism to tickle your funny lone
['to', 'your'] -> [['ewe', 'u', 'u.', 'uwe', 'yew', 'yoo', 'you', 'yu', 'yue'], ['tor', 'tore', 'torr', 'torre']]
There’s nothing like a good spoonerism yue tickle tore funny bone
['to', 'funny'] -> [['foo', 'fu', 'phu'], ['tunney', 'tunny']]
There’s nothing like a good spoonerism phu tickle your tunny bone
['to', 'bone'] -> [['beu', 'boo'], ['tone']]
There’s nothing like a good spoonerism boo tickle your funny tone
['tickle', 'funny'] -> [['fickel', 'fickle'], ['tunney', 'tunny']]
There’s nothing like a good spoonerism to fickle your tunny bone
['tickle', 'bone'] -> [['bickel', 'bickell', 'bickle'], ['tone']]
There’s nothing like a good spoonerism to bickle your funny tone
['funny', 'bone'] -> [['bunney', 'bunnie', 'bunny'], ['fone', 'phone']]
There’s nothing like a good spoonerism to tickle your bunnie fone

input: Is the dean busy
['dean', 'busy'] -> [['bean', 'beane', 'beene', 'bein', 'beine', 'biehn', 'bien'], ['dizzy']]
Is the bean dizzy

input: jelly beans
['jelly', 'beans'] -> [['beli', 'belli', 'belly'], ['genes', 'jeanes', 'jeans']]
belly jeanes

input: trail snacks
['trail', 'snacks'] -> [['snail'], ['tracks', 'trax']]
snail trax

input: call box
['call', 'box'] -> [['ball', 'bawl'], ['cocks', 'cox', 'coxe']]
ball cox

input: Far out in the uncharted backwaters of the unfashionable end of the western spiral arm of the Galaxy lies a small unregarded yellow sun
['out', 'lies'] -> [['lout'], ['ais', 'ayes', 'eis', 'eyes', "eyes'", 'i.s', 'ise']]
Far lout in the uncharted backwaters of the unfashionable end of the western spiral arm of the Galaxy eis a small unregarded yellow sun
['of', 'lies'] -> [['love'], ['ais', 'ayes', 'eis', 'eyes', "eyes'", 'i.s', 'ise']]
Far out in the uncharted backwaters love the unfashionable end love the western spiral arm love the Galaxy ayes a small unregarded yellow sun
['end', 'lies'] -> [['lend'], ['ais', 'ayes', 'eis', 'eyes', "eyes'", 'i.s', 'ise']]
Far out in the uncharted backwaters of the unfashionable lend of the western spiral arm of the Galaxy eyes a small unregarded yellow sun
['end', 'sun'] -> [['send'], ['un']]
Far out in the uncharted backwaters of the unfashionable send of the western spiral arm of the Galaxy lies a small unregarded yellow un
['of', 'lies'] -> [['love'], ['ais', 'ayes', 'eis', 'eyes', "eyes'", 'i.s', 'ise']]
Far out in the uncharted backwaters love the unfashionable end love the western spiral arm love the Galaxy ais a small unregarded yellow sun
['of', 'lies'] -> [['love'], ['ais', 'ayes', 'eis', 'eyes', "eyes'", 'i.s', 'ise']]
Far out in the uncharted backwaters love the unfashionable end love the western spiral arm love the Galaxy eis a small unregarded yellow sun
['lies', 'sun'] -> [['sighs', 'size'], ['luhn', 'lun', 'lunn']]
Far out in the uncharted backwaters of the unfashionable end of the western spiral arm of the Galaxy size a small unregarded yellow lun
['yellow', 'sun'] -> [['celo'], ['youn', 'yun']]
Far out in the uncharted backwaters of the unfashionable end of the western spiral arm of the Galaxy lies a small unregarded celo youn
```
