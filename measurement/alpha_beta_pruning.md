# Alpha Beta Pruning

In the first run the nstep bot used the normal [minimax](https://en.wikipedia.org/wiki/Minimax) implementation.

In the second run it used the [alpha-beta-pruning](https://en.wikipedia.org/wiki/Alpha%E2%80%93beta_pruning) optimization.

```sh
 ╭─conrad@Bart in repo: connectfour on  main [!] via  v3.12.0 via  connectfour took 3s
 ╰─λ time python3 main.py -a1 random -a2 nstep -n 480
100%|██████████████████████████████████████████████████████████████| 480/480 [01:10<00:00,  6.76it/s]
Player 1 won 29 games (6.04%)
Player 2 won 451 games (93.96%)
Draws: 0

real	1m11,097s
user	27m41,338s
sys	0m0,241s

 ╭─conrad@Bart in repo: connectfour on  main [!] via  v3.12.0 via  connectfour took 1m11s
 ╰─λ time python3 main.py -a1 random -a2 nstep -n 480
100%|██████████████████████████████████████████████████████████████| 480/480 [00:34<00:00, 13.87it/s]
Player 1 won 35 games (7.29%)
Player 2 won 445 games (92.71%)
Draws: 0

real	0m34,746s
user	13m27,144s
sys	0m0,184s

 ╭─conrad@Bart in repo: connectfour on  main [!] via  v3.12.0 via  connectfour took 34s
 ╰─λ
```

<a href="https://github.com/chc0815/connectfour/blob/main/README.md">Back to README</a>
