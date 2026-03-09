

from datetime import date, timedelta


def berechne_ostern(jahr):
    # Die Methode
    # Teile das Jahr, dessen Osterdatum berechnet werden soll, durch 19. 
    # Der Quotient interessiert uns nicht, aber der Divisionsrest kommt zur 
    # späteren Verwendung in das "Einmachglas" a.
    a = jahr % 19

    # Teile das Jahr durch 100. 
    # Der Quotient kommt in Glas b, der Rest in Glas c.	
    b = jahr // 100
    c = jahr % 100

    # Teile den Inhalt von Einmachglas b durch 4. 
    # Lege den Quotienten in Glas d und den Rest in Glas e.
    d = b // 4
    e = b % 4

    # Addiere zum Inhalt von b die Zahl 8. Teile das Ergebnis durch 25. 
    # Lege den Quotienten in Glas f.
    f = (b + 8) // 25

    # Nimm den Inhalt von b, ziehe den Inhalt von f ab und addiere 1. 
    # Das Ergebnis teile durch 3. Lege den Quotienten in Glas g.
    g = (b - f + 1) // 3

    # Nimm den Inhalt von a mal 19. 
    # Addiere dazu zuerst den Inhalt von b und dann die Zahl 15. 
    # Nun subtrahiere zuerst den Inhalt von d, dann noch den Inhalt von g. 
    # Das Resultat wird durch 30 geteilt. 
    # Uns interessiert nur der Rest, und der kommt in Glas h.
    h = (a * 19 + b + 15 - d - g) % 30

    # Teile den Inhalt von c durch 4, lege den Quotienten in i und den Rest in j.
    i = c // 4
    j = c % 4

    # Nimm den Inhalt von e und addiere den Inhalt von i. Verdoppele das Ergebnis. 
    # Addiere 32. Ziehe erst den Inhalt von h ab und dann noch den Inhalt von j. 
    # Teile das Resultat durch 7 und lege den Divisionsrest in Glas k.
    k = ((e + i) * 2 + 32 - h - j) % 7

    # Nimm den Inhalt von k gleich wieder heraus und verdoppele die Zahl. 
    # Addiere den Inhalt von h. 
    # Multipliziere mit 11 und addiere den Inhalt von a. 
    # Teile durch 451 und lege den Quotienten in Glas l.
    l = ((k * 2 + h) * 11 + a) // 451

    # Nimm den Inhalt von h und addiere zuerst den Inhalt von k und dann die Zahl 114. 
    # Nun multipliziere den Inhalt von l mit 7 und ziehe diese Zahl von der Summe ab. 
    # Teile durch 31, lege den Quotienten in Glas m und den Rest in Glas n. 
    m = (h + k + 114 - l * 7) // 31
    n = (h + k + 114 - l * 7) % 31

    # Nun hast du im Einmachglas m den Monat liegen (3 = März und 4 = April). 
    # Den Inhalt von Glas n mußt du noch um 1 erhöhen, 
    # und schon hast du den Monatstag vom Ostersonntag des gewünschten Jahres!
    n += 1

    return date(jahr, m, n)


def gib_feiertag(tagesdatum):
    datum = date(tagesdatum.year, tagesdatum.month, tagesdatum.day)
    if(datum.month == 1 and datum.day == 1):
        return "Neujahr"
    elif(datum.month == 5 and datum.day == 1):
        return "Staatsfeiertag"
    elif(datum.month == 8 and datum.day == 15):
        return "Mariae Himmelfahrt"
    elif(datum.month == 10 and datum.day == 26):
        return "Staatsfeiertag"
    elif(datum.month == 11 and datum.day == 1):
        return "Allerheiligen"
    elif(datum.month == 12 and datum.day == 8):
        return "Mariae Empfängnis"
    elif(datum.month == 12 and datum.day == 25):
        return "Christtag"
    elif(datum.month == 12 and datum.day == 26):
        return "Stefanitag"
    
    ostern = berechne_ostern(datum.year)
    if(ostern == datum):
        return "Ostern"
    elif(ostern + timedelta(days=1) == datum):
        return "Ostern"
    elif(ostern + timedelta(days=39) == datum):
        return "Christi Himmelfahrt"
    elif(ostern + timedelta(days=49) == datum):
        return "Pfingsten"
    elif(ostern + timedelta(days=50) == datum):
        return "Pfingsten"
    elif(ostern + timedelta(days=60) == datum):
        return "Fronleichnam"
    
    return ""

