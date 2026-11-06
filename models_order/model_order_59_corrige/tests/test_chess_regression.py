from evaluation_adapters.environments import ChessEnv

def test_uci_board_coordinate_consistency_and_mate_one():
    e=ChessEnv(fen="7k/5Q2/7K/8/8/8/8/8 w - - 0 1",max_plies=2)
    legal=e.legal_actions()
    assert "f7g7" in legal
    obs,reward,done,info=e.act("f7g7")
    assert done is True
    assert reward==1.0
    assert info["mate"] is True


def test_cannot_capture_king():
    e=ChessEnv(fen='6k1/5Q2/7K/8/8/8/8/8 w - - 0 1')
    assert not e._legal_move(e.board,e.turn,'f7g8')


def test_castling_state_update():
    from evaluation_adapters.environments import ChessEnv
    e=ChessEnv(fen="r3k2r/8/8/8/8/8/8/R3K2R w KQkq - 0 1")
    assert "e1g1" in e.legal_actions()
    e.act("e1g1")
    assert e.board[7][6]=='K' and e.board[7][5]=='R' and 'K' not in e.castle and 'Q' not in e.castle


def test_en_passant_state_update():
    from evaluation_adapters.environments import ChessEnv
    e=ChessEnv(fen="7k/8/8/3pP3/8/8/8/K7 w - d6 0 1")
    assert "e5d6" in e.legal_actions()
    e.act("e5d6")
    assert e.board[2][3]=='P' and e.board[3][3]=='.'


def test_promotion_action_is_legal_and_executed():
    from evaluation_adapters.environments import ChessEnv
    e=ChessEnv(fen="7k/4P3/8/8/8/8/8/4K2R w - - 0 1")
    assert "e7e8q" in e.legal_actions()
    e.act("e7e8q")
    assert e.board[0][4]=='Q'
