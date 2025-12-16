from fastapi.testclient import TestClient
import sys, pathlib, importlib
# ensure project root is on sys.path so `src` package can be imported
sys.path.insert(0, str(pathlib.Path('.').resolve()))
web = importlib.import_module('src.web')


client = TestClient(web.app)


def test_index_page_served():
    r = client.get('/')
    assert r.status_code == 200
    assert 'Kivi Paperi Sakset' in r.text


def test_single_player_play_basic():
    # play rock vs basic AI
    r = client.post('/play', data={'move': 'k', 'mode': 'basic'})
    assert r.status_code == 200
    assert 'Pistelasku' in r.text
    assert 'Sinä:' in r.text or 'Viimeisin siirto' in r.text


def test_two_player_play():
    # play PvP where player1=k, player2=s (player1 should win)
    r = client.post('/play', data={'move1': 'k', 'move2': 's', 'mode': 'pvp'})
    assert r.status_code == 200
    assert 'Pelaaja 1' in r.text
    assert 'Pelaaja 2' in r.text


def test_pvp_buttons_rendered():
    r = client.get('/')
    # p1-choices is present (the two-step PvP UI)
    assert 'id="p1-choices"' in r.text
    assert 'Pelaaja 1 valitsee' in r.text


def test_game_ends_after_five():
    # reset first
    client.get('/reset')
    # give player1 five wins against player2
    for i in range(5):
        r = client.post('/play', data={'move1': 'k', 'move2': 's', 'mode': 'pvp'})
        assert r.status_code == 200

    r = client.get('/')
    assert 'Voittaja' in r.text


def test_internal_score_after_five_rounds():
    # diagnostic: ensure web._tuomari internal state reaches 5 points for player1
    client.get('/reset')
    for i in range(5):
        r = client.post('/play', data={'move1': 'k', 'move2': 's', 'mode': 'pvp'})
        assert r.status_code == 200

    import importlib, pathlib, sys
    sys.path.insert(0, str(pathlib.Path('.').resolve()))
    web = importlib.import_module('src.web')
    assert web._tuomari.ekan_pisteet == 5


def test_trace_increments_per_round():
    client.get('/reset')
    import importlib, pathlib, sys
    sys.path.insert(0, str(pathlib.Path('.').resolve()))
    web = importlib.import_module('src.web')
    for expected in range(1, 6):
        r = client.post('/play', data={'move1': 'k', 'move2': 's', 'mode': 'pvp'})
        assert r.status_code == 200
        # debug prints to inspect response and internal score
        print('round', expected, 'response contains Voittaja?', 'Voittaja' in r.text, 'score:', web._tuomari.ekan_pisteet)
        print('tuomari voittaja():', web._tuomari.voittaja())
        print('snippet:', r.text[r.text.find('<main'):r.text.find('</main>')+7])
        assert web._tuomari.ekan_pisteet == expected


def test_round_flash_appears_then_clears():
    client.get('/reset')
    # one round PvP where player1 wins
    r = client.post('/play', data={'move1': 'k', 'move2': 's', 'mode': 'pvp'})
    assert r.status_code == 200
    # the response to the POST should include the flash
    assert 'voitti kierroksen' in r.text or 'Tasapeli' in r.text
    # subsequent GET should not have the flash (it was cleared)
    r2 = client.get('/')
    assert 'voitti kierroksen' not in r2.text
