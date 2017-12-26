# reversi
reversi game implemented on python
This is python implementation of the Reversi/Othello game.
You have simple rules if you chose classic mode: you can place
your disk only any through a continuous series of opponent's disks,
after them, you flip it and up your score. In extra mode both of players
have different count of common disks - strategic blocks. Their count is
limited, it depends on field size. (count of these disk == field size, for example, if filed size is 8*8
it could be only 8 extra disks on the field)
You can place extra disk by right mouse button click, after them, next player get move.
Both of players can't flip disks thought this extra.
If players haven't extra disks anymore u'll have a warning message, if u'll try to place extra disk.
Game overs when both of players can't make move.

if u want to run game you need:
1) pip3 install requirements.txt
2)python3 main.py
3)choose start parameters and play!
