import json
from flask import Flask, render_template, request, redirect, flash, url_for
from datetime import datetime


def loadClubs():
    with open("clubs.json") as c:
        listOfClubs = json.load(c)["clubs"]
        return listOfClubs


def loadCompetitions():
    with open("competitions.json") as comps:
        listOfCompetitions = json.load(comps)["competitions"]
        return listOfCompetitions


app = Flask(__name__)
app.secret_key = "something_special"

competitions = loadCompetitions()
clubs = loadClubs()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/showSummary", methods=["POST"])
def showSummary():
    club = next((club for club in clubs if club["email"] == request.form["email"]), None)
    if club is None:
        flash("Sorry, that email wasn't found.")
        return redirect(url_for("index"))
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return render_template("welcome.html", club=club, competitions=competitions, current_time=current_time)


@app.route("/book/<competition>/<club>")
def book(competition, club):
    foundClub = next((c for c in clubs if c["name"] == club), None)
    foundCompetition = next((c for c in competitions if c["name"] == competition), None)
    if foundClub and foundCompetition:
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if foundCompetition["date"] > current_time:
            return render_template("booking.html", club=foundClub, competition=foundCompetition)
        else:
            flash("This competition is in the past and cannot be booked.")
    else:
        flash("Something went wrong-please try again.")
    return render_template("welcome.html", club=foundClub, competitions=competitions, current_time=current_time)


@app.route("/purchasePlaces", methods=["POST"])
def purchasePlaces():
    competition = next((c for c in competitions if c["name"] == request.form["competition"]), None)
    club = next((c for c in clubs if c["name"] == request.form["club"]), None)
    placesRequired = int(request.form["places"])

    if competition and club:
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if competition["date"] > current_time:
            if placesRequired > 12:
                flash("You cannot book more than 12 places.")
            else:
                points_required = placesRequired
                club_points = int(club["points"])
                competition_places = int(competition["numberOfPlaces"])

                if "bookings" not in competition:
                    competition["bookings"] = {}

                if club["name"] not in competition["bookings"]:
                    competition["bookings"][club["name"]] = 0

                total_booked_places = competition["bookings"][club["name"]] + placesRequired

                if total_booked_places > 12:
                    flash("You cannot book more than 12 places in total for this competition.")
                elif points_required > club_points:
                    flash("Not enough points to complete the booking.")
                else:
                    competition["numberOfPlaces"] = competition_places - placesRequired
                    club["points"] = club_points - points_required
                    competition["bookings"][club["name"]] = total_booked_places
                    flash("Great-booking complete!")
        else:
            flash("This competition is in the past and cannot be booked.")
    else:
        flash("Something went wrong-please try again.")

    return render_template("welcome.html", club=club, competitions=competitions, current_time=current_time)


# TODO: Add route for points display


@app.route("/logout")
def logout():
    return redirect(url_for("index"))
