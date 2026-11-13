# makefun-tiny-chess-engine

Tiny Chess engine for the make.fun tiny-chess-01 bounty ($500).

A compact Python chess engine in a single `main.py` (lzma-packed from `src.py`):
0x88 board, PVS + transposition table + quiescence, null-move pruning + LMR,
killer/history ordering, PeSTO tapered eval (middlegame tables), fixed node
budget per move (deterministic, no clock), no model calls.

`src.py` is the readable source; `main.py` is produced by
`makefun compress src.py --out main.py`.
