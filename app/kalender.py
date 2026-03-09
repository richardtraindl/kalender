
from datetime import datetime, timedelta

from flask import Blueprint, flash, g, redirect, render_template, request, url_for
from werkzeug.exceptions import abort
from sqlalchemy import or_, and_
from flask_login import login_required
from app import app, db
from app.models import Termin


bp = Blueprint('kalender', __name__, url_prefix='/kalender')


AUTOREN = ["Ordi", "Elfi", "TP"]
jahre = [2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025, 2026, 2027, 2028, 2029, 2030, 2031, 2032, 2033, 2034, 2035]
monate = [["Jänner", 1], ["Februar", 2], ["März", 3], ["April", 4], ["Mai", 5], ["Juni", 6], ["Juli", 7], ["August", 8], ["September", 9], ["Oktober", 10], ["November", 11], ["Dezember", 12]]
wochentage = ["Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag", "Samstag", "Sonntag"]
wtage = ["Mo", "Di", "Mi", "Do", "Fr", "Sa", "So"]


# Ermittle von datum den Beginn der Kalenderwoche (Montag)
def gib_kwbeginn(datum):
    newdatum = datetime(year=datum.year, month=datum.month, day=datum.day, hour=0, minute=0, second=0, microsecond=0)
    add = newdatum.weekday() * -1
    return newdatum + timedelta(days=add)

def adjust_datum(datum, mode=None):
    if(mode == 'ymd'):
        # Tagesdatum ohne Stunden, etc.
        return datetime(year=datum.year, month=datum.month, day=datum.day, hour=0, minute=0, second=0, microsecond=0)
    else:
        # Default ohne Angabe von mode: Runde minute auf ganze Viertelstunden
        minute = (datum.minute // 15)  * 15
        return datetime(year=datum.year, month=datum.month, day=datum.day, hour=datum.hour, minute=minute, second=0, microsecond=0)

def lese_termine(kwbeginn):
    kwende = kwbeginn + timedelta(days=7)

    return db.session.query(Termin) \
            .filter(or_(and_(Termin.beginn < kwbeginn, Termin.ende > kwbeginn), and_(Termin.beginn >= kwbeginn, Termin.beginn < kwende))) \
            .order_by(Termin.beginn.asc()).all()


class ktermin:
    def __init__(self, termin, tag, stunde, viertel, dauer_viertel):
        self.termin = termin
        self.tag = tag
        self.stunde = stunde 
        self.viertel = viertel 
        self.dauer_viertel = dauer_viertel


def gib_ktermine(termine, kwbeginn):
    ktermine=[]

    for i in range(0, 7):

        dt = kwbeginn + timedelta(days=i)
        tag = int(dt.day)

        for termin in termine:

            if(termin.autor == 'TP'):
                if(termin.beginn.day == dt.day): # and termin.ende.day > dt.day
                    stunde = 21
                    viertel = 0
                    dauer_viertel = 1
                elif(termin.beginn.day < dt.day and termin.ende.day > dt.day):
                    stunde = 22
                    viertel = 0
                    dauer_viertel = 1
                elif(termin.ende.day == dt.day):
                    stunde = 23
                    viertel = 0
                    dauer_viertel = 1
                else:
                    continue
                    
                ktermine.append(ktermin(termin, tag, stunde, viertel, dauer_viertel))

            else:
                if(termin.beginn.hour < 7):
                    stunde = 7
                    viertel = 0
                else:
                    stunde = int(termin.beginn.hour)
                    viertel = int(termin.beginn.minute) // 15
                
                if(termin.beginn.day == dt.day):
                    if(termin.ende.day == dt.day):
                        # Ein Tagestermin
                        dauer_viertel = ((termin.ende.hour - stunde) * 4) + ((termin.ende.minute // 15) - viertel)
                    else:
                        # Beginn Mehrere-Tage Termin
                        dauer_viertel = ((24 - stunde) * 4) - viertel

                elif(termin.beginn.day < dt.day and termin.ende.day > dt.day):
                    # Zwischen Beginn und Ende Mehrere-Tage Termin
                    stunde = 7
                    viertel = 0
                    dauer_viertel = (17 * 4) # den vollen Kalender belegen
                    
                elif(termin.beginn.day < dt.day and termin.ende.day == dt.day):
                    # Ende Mehrere-Tage Termin
                    stunde = 7
                    viertel = 0
                    dauer_viertel = ((termin.ende.hour - stunde) * 4) + (termin.ende.minute // 15)

                else:
                    continue

                ktermine.append(ktermin(termin, tag, stunde, viertel, dauer_viertel))

    return ktermine


@bp.route('/', methods=('GET', 'POST'))
@bp.route('/index', methods=('GET', 'POST'))
@bp.route('/<kwbeginn>/index', methods=('GET', 'POST'))
@login_required
def index(kwbeginn=None):
    aktdatum = adjust_datum(datetime.now())

    if(kwbeginn):
        datum = datetime.strptime(kwbeginn, "%Y-%m-%d %H:%M:00") 
        kwbeginn = gib_kwbeginn(datum)
    else:
        kwbeginn = gib_kwbeginn(aktdatum)

    if(request.method == 'POST'):
        if(len(request.form['kjahr']) > 0 and len(request.form['kmonat']) > 0 and
           len(request.form['ktag']) > 0):
            try:
                kjahr = int(request.form['kjahr'])
                kmonat = int(request.form['kmonat'])
                ktag = int(request.form['ktag'])
                datum = datetime(year=kjahr, month=kmonat, day=ktag)
                kwbeginn = gib_kwbeginn(datum)
            except:
                flash("error")
                return render_template(template, aktdatum=adjust_datum(aktdatum, 'ymd'), 
                                        kwbeginn=kwbeginn, jahre=jahre, monate=monate, 
                                        wochentage=wochentage, wtage=wtage, page_title="Kalender")

        if(len(request.form['kwadjust']) > 0):
            try:
                adjust = int(request.form['kwadjust'])
            except:
                flash("error")
                return render_template("kalender/index.html", aktdatum=adjust_datum(aktdatum, 'ymd'), 
                                        kwbeginn=kwbeginn, jahre=jahre, monate=monate, 
                                        wochentage=wochentage, wtage=wtage, page_title="Kalender")

            kwbeginn += timedelta(weeks=adjust)

    termine = lese_termine(kwbeginn)
    ktermine = gib_ktermine(termine, kwbeginn)

    return render_template("kalender/index.html", ktermine=ktermine, aktdatum=adjust_datum(aktdatum, 'ymd'), kwbeginn=kwbeginn, jahre=jahre, monate=monate, wochentage=wochentage, wtage=wtage, page_title="Kalender")


@bp.route('/create', methods=('GET', 'POST'))
@bp.route('/<beginn>/create', methods=('GET', 'POST'))
@login_required
def create(beginn=None):
    aktdatum = adjust_datum(datetime.now())

    if(request.method == 'POST'):
        autor = request.form['autor']

        time_begin = request.form['time_begin']
        date_begin = request.form['date_begin']
        beginn = datetime.strptime(date_begin + " " + time_begin, "%Y-%m-%d %H:%M")

        time_end = request.form['time_end']
        date_end = request.form['date_end']
        ende = datetime.strptime(date_end + " " + time_end, "%Y-%m-%d %H:%M")

        thema = request.form['thema']

        error = None
        if(beginn >= ende):
          error = "Ende liegt vor oder auf Beginn."

        if(not thema):
          error = "Thema fehlt."

        if(error):
            flash(error)
            kwbeginn = gib_kwbeginn(beginn)
            return render_template('kalender/termin.html', termin=None, autoren=AUTOREN, aktdatum=aktdatum, 
                                    kwbeginn=kwbeginn, jahre=jahre, monate=monate, wochentage=wochentage, page_title="Termin")


        termin = Termin(autor=autor, beginn=beginn, ende=ende, thema=thema)
        db.session.add(termin)
        db.session.commit()

        return redirect(url_for('kalender.index', kwbeginn=gib_kwbeginn(termin.beginn), page_title="Kalender"))
    else:
        if(beginn):
            dtbeginn = datetime.strptime(beginn, "%Y-%m-%d %H:%M:00")
        else:
            dtbeginn = adjust_datum(datetime.now())
                
        ende = dtbeginn + timedelta(hours=0.5)
        thema = ""
        termin = Termin(autor="Gerold", beginn=dtbeginn, ende=ende, thema=thema)
        kwbeginn = gib_kwbeginn(dtbeginn)
        return render_template('kalender/termin.html', termin=termin, autoren=AUTOREN, aktdatum=aktdatum, 
                                kwbeginn=kwbeginn, jahre=jahre, monate=monate, wochentage=wochentage, page_title="Termin")


@bp.route('/<int:id>/edit', methods=('GET','POST'))
@login_required
def edit(id):
    aktdatum = adjust_datum(datetime.now())

    termin = db.session.query(Termin).get(id)

    if(request.method == 'POST'):
        termin.autor = request.form['autor']

        time_begin = request.form['time_begin']
        date_begin = request.form['date_begin']
        termin.beginn = datetime.strptime(date_begin + " " + time_begin, "%Y-%m-%d %H:%M")

        time_end = request.form['time_end']
        date_end = request.form['date_end']
        termin.ende = datetime.strptime(date_end + " " + time_end, "%Y-%m-%d %H:%M")

        termin.thema = request.form['thema']

        error = None
        if(termin.beginn >= termin.ende):
          error = "Ende liegt vor oder auf Beginn."

        if(not termin.thema):
          error = "Thema fehlt."
          
        if(error):
            flash(error)
            kwbeginn = gib_kwbeginn(termin.beginn)
            return render_template('kalender/termin.html', termin=termin, autoren=AUTOREN, 
                                    aktdatum=aktdatum, kwbeginn=kwbeginn, jahre=jahre, monate=monate, wochentage=wochentage, page_title="Termin")

        

        db.session.commit()

        return redirect(url_for('kalender.index', kwbeginn=gib_kwbeginn(termin.beginn)))
    else:
        kwbeginn = gib_kwbeginn(termin.beginn)
        return render_template("kalender/termin.html", termin=termin, autoren=AUTOREN, aktdatum=aktdatum, 
                                kwbeginn=kwbeginn, jahre=jahre, monate=monate, wochentage=wochentage, page_title="Termin")


@bp.route('/<int:id>/delete', methods=('GET',))
@login_required
def delete(id):
    try:
        termin = db.session.query(Termin).get(id)
        kwbeginn = gib_kwbeginn(termin.beginn)
        db.session.delete(termin)
        db.session.commit()
        return redirect(url_for('kalender.index', kwbeginn=kwbeginn, page_title="Kalender"))
    except:
        flash("error")
        return render_template("kalender/index.html", page_title="Kalender")

