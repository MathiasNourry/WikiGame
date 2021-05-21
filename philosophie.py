#!/usr/bin/python3
# -*- coding: utf-8 -*-

from flask import Flask, render_template, session, request, redirect, flash
from getpage import getPage
import logging


app = Flask(__name__)
# app.logger.disabled = True
# log = logging.getLogger('werkzeug')

app.secret_key = b"fgh6=12fgh}]65[#\|p"
score = 0

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/new-game', methods=['POST'])
def new_game():
    global score

    session['article'] = request.form['start']
    score = 0
    return redirect('/game')


@app.route('/game', methods=['GET'])
def game():
    global score

    session['title'], session['links'] = getPage(session['article'])

    # Begin page
    if score == 0:

        # Non-existent page
        if session['title'] is None:
            flash("La page de départ est inexistante !")
            return render_template('index.html')
        
        # Absence of related links
        elif len(session['links']) == 0:
            flash("La page de départ ne contient pas de liens connexes.")
            return render_template('index.html')

        # Begin with "Philosophie" page or related one
        elif session['article'] == 'Philosophie' or session['title'] == 'Philosophie':
            flash("La page que tu as testé mène droit vers la solution.\nUn peu de difficulté, cherche un autre point de départ !")
            return render_template('index.html')

        else:
            return render_template('game.html', score=score)

    # Other pages
    else:

        # "Philosophie" page found
        if session['title'] == 'Philosophie':
            flash(f"Victoire !\nTon score est de {score}.")
            return render_template('index.html')

        # Absence of related links
        elif len(session['links']) == 0:
            flash(f"Perdu !\nLa page \"{session['article']}\" était un cul de sac !")
            return render_template('index.html')

        else:
            return render_template('game.html', score=score)


@app.route('/move', methods=['POST'])
def move():
    global score

    # Continue the game
    if request.form['action'] == "validate":
        session['article'] = request.form['destination']

        # Manual POST command with article not present 
        # in links proposal
        if session['article'] not in session['links']:
            flash("Eh bien alors petit malin, on essaie de tricher ?\nCe jeu est peut-être trop dur pour toi ...")
            return redirect('/')
        
        else:
            score = int(request.form['score_data']) + 1
            return redirect('/game')

    # Leave the game
    else:
        flash("On n'est peut-être pas parti du bon pied tous les deux.\nNe baisse pas les bras, tes efforts finiront par payer !")
        return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)

