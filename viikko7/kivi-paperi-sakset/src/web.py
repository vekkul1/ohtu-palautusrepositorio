from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from src.tuomari import Tuomari
from src.tekoaly import Tekoaly
from src.tekoaly_parannettu import TekoalyParannettu

app = FastAPI()

app.mount("/static", StaticFiles(directory="src/static"), name="static")
templates = Jinja2Templates(directory="src/web_templates")

# simple in-memory game state (single session)
_tuomari = Tuomari()
_tekoaly = Tekoaly()
_tekoaly_par = TekoalyParannettu(10)
_last_player = None
_last_ai = None
_last_mode = "basic"
_last_round_winner = None


@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    global _last_round_winner
    winner = _tuomari.voittaja()
    winner_label = None
    if winner == 'eka':
        winner_label = 'Ensimmäinen pelaaja'
    elif winner == 'toka':
        winner_label = 'Toinen pelaaja'
    # show one-time round flash then clear it
    flash = _last_round_winner
    _last_round_winner = None

    return templates.TemplateResponse("index.html", {
        "request": request,
        "tuomari": _tuomari,
        "last_player": _last_player,
        "last_ai": _last_ai,
        "mode": _last_mode,
        "winner": winner_label,
        "round_flash": flash,
    })


@app.post("/play", response_class=HTMLResponse)
def play(request: Request, move: str | None = Form(None), move1: str | None = Form(None), move2: str | None = Form(None), mode: str = Form("basic")):
    global _tuomari, _tekoaly, _tekoaly_par, _last_player, _last_ai, _last_mode, _last_round_winner

    # If game already finished, just render with winner
    if _tuomari.onko_peli_loppu():
        winner = _tuomari.voittaja()
        winner_label = None
        if winner == 'eka':
            winner_label = 'Ensimmäinen pelaaja'
        elif winner == 'toka':
            winner_label = 'Toinen pelaaja'
        return templates.TemplateResponse("index.html", {
            "request": request,
            "tuomari": _tuomari,
            "last_player": _last_player,
            "last_ai": _last_ai,
            "mode": _last_mode,
            "winner": winner_label,
        })

    # Two-player mode: use move1 and move2
    if mode == "pvp":
        player = move1
        opponent = move2
        print("DEBUG: received PvP post:", player, opponent, "mode:", mode)
        if player is None or opponent is None:
            # missing fields; re-render without change
            return templates.TemplateResponse("index.html", {
                "request": request,
                "tuomari": _tuomari,
                "last_player": _last_player,
                "last_ai": _last_ai,
                "mode": _last_mode,
            })

        _tuomari.kirjaa_siirto(player, opponent)
        # determine round winner for flash
        res = _tuomari.tulos(player, opponent)
        if res == 'eka':
            _last_round_winner = 'Ensimmäinen pelaaja voitti kierroksen!'
        elif res == 'toka':
            _last_round_winner = 'Toinen pelaaja voitti kierroksen!'
        else:
            _last_round_winner = 'Tasapeli!'
        # include the flash in the immediate response but clear for subsequent requests
        flash_local = _last_round_winner
        _last_round_winner = None
        _last_player = player
        _last_ai = opponent
        _last_mode = mode
        winner = _tuomari.voittaja()
        winner_label = None
        if winner == 'eka':
            winner_label = 'Ensimmäinen pelaaja'
        elif winner == 'toka':
            winner_label = 'Toinen pelaaja'

        return templates.TemplateResponse("index.html", {
            "request": request,
            "tuomari": _tuomari,
            "last_player": _last_player,
            "last_ai": _last_ai,
            "mode": _last_mode,
            "winner": winner_label,
            "round_flash": flash_local,
        })

    # Single-player modes (basic or improved)
    player = move
    ai_move = "k"

    if mode == "basic":
        ai_move = _tekoaly.anna_siirto()
    else:
        ai_move = _tekoaly_par.anna_siirto()

    # update enhanced AI memory with player's last move
    try:
        if player is not None:
            _tekoaly_par.aseta_siirto(player)
    except Exception:
        pass

    _tuomari.kirjaa_siirto(player, ai_move)
    # determine round winner for flash
    res = _tuomari.tulos(player, ai_move)
    if res == 'eka':
        _last_round_winner = 'Sinä voitit kierroksen!'
    elif res == 'toka':
        _last_round_winner = 'Tietokone voitti kierroksen!'
    else:
        _last_round_winner = 'Tasapeli!'
    flash_local = _last_round_winner
    _last_round_winner = None

    _last_player = player
    _last_ai = ai_move
    _last_mode = mode

    winner = _tuomari.voittaja()
    winner_label = None
    if winner == 'eka':
        winner_label = 'Ensimmäinen pelaaja'
    elif winner == 'toka':
        winner_label = 'Toinen pelaaja'

    return templates.TemplateResponse("index.html", {
        "request": request,
        "tuomari": _tuomari,
        "last_player": _last_player,
        "last_ai": _last_ai,
        "mode": _last_mode,
        "winner": winner_label,
        "round_flash": flash_local,
    })


@app.get("/reset")
def reset():
    global _tuomari, _tekoaly, _tekoaly_par, _last_player, _last_ai, _last_mode
    _tuomari = Tuomari()
    _tekoaly = Tekoaly()
    _tekoaly_par = TekoalyParannettu(10)
    _last_player = None
    _last_ai = None
    _last_mode = "basic"
    return RedirectResponse(url="/", status_code=302)
