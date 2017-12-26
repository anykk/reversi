# Reversi
<p>Reversi game implemented on python</p>
<h3></h3>
This is python implementation of the Reversi/Othello game.
You have simple rules if you chose classic mode: you can place
your disk only any through a continuous series of opponent's disks,
after them, you flip it and up your score. In extra mode both of players
have different count of common disks - strategic blocks. Their count is
limited, it depends on field size. (count of these disk == field size, for example, if filed size is 8*8
it could be only 8 extra disks on the field)
You can place extra disk by right mouse button click only in empty places but without your possible moves that underlyied by yellow
, after them, next player get move.Both of players can't flip disks thought this extra.
If players haven't extra disks anymore u'll have a warning message, if u'll try to place extra disk.
Game overs when both of players can't make move.

if u want to run game you need:
<li>1) pip3 install requirements.txt</li>
<li>2)python3 main.py</li>
<li>3)choose start parameters and play!</li>
