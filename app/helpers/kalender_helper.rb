# encoding: UTF-8

module KalenderHelper

  def berechneOstern(jahr)
		# Die Methode
		# Teile das Jahr, dessen Osterdatum berechnet werden soll, durch 19. 
		# Der Quotient interessiert uns nicht, aber der Divisionsrest kommt zur späteren Verwendung in das "Einmachglas" a.
		@a = jahr % 19
	
		# Teile das Jahr durch 100. 
		# Der Quotient kommt in Glas b, der Rest in Glas c.	
		@b = jahr / 100
		@c = jahr % 100
	
		# Teile den Inhalt von Einmachglas b durch 4. 
		# Lege den Quotienten in Glas d und den Rest in Glas e.
		@d = @b / 4
		@e = @b % 4
		
		# Addiere zum Inhalt von b die Zahl 8. Teile das Ergebnis durch 25. 
		# Lege den Quotienten in Glas f.
		@f = (@b + 8) / 25
		
		# Nimm den Inhalt von b, ziehe den Inhalt von f ab und addiere 1. Das Ergebnis teile durch 3. 
		# Lege den Quotienten in Glas g.
		@g = (@b - @f + 1) / 3
		
		# Jetzt wird's kompliziert: Nimm den Inhalt von a mal 19. Addiere dazu zuerst den Inhalt von b und dann die Zahl 15. 
		# Nun subtrahiere zuerst den Inhalt von d, dann noch den Inhalt von g. Das Resultat wird durch 30 geteilt. 
		# So lange gerechnet, und trotzdem werfen wir den Quotienten in den Biomüll! Uns interessiert nur der Rest, und der 
		# kommt in Glas h.
		@h = (@a * 19 + @b + 15 - @d - @g) % 30
		
		# Zur Entspannung was Leichtes: Teile den Inhalt von c durch 4, lege den Quotienten in i und den Rest in j.
		@i = @c / 4
		@j = @c % 4
		
		# Der allerkomplizierteste Schritt: Nimm den Inhalt von e und addiere den Inhalt von i. Verdoppele das Ergebnis. 
		# Addiere 32. Ziehe erst den Inhalt von h ab und dann noch den Inhalt von j. 
		# Teile das Resultat durch 7 und lege den Divisionsrest in Glas k.
		@k = ((@e + @i) * 2 + 32 - @h - @j) % 7
			
		# Nimm den Inhalt von k gleich wieder heraus und verdoppele die Zahl. Addiere den Inhalt von h. 
		# Multipliziere mit 11 und addiere den Inhalt von a. 
		# Teile durch 451 und lege den Quotienten in Glas l.
		@l = ((@k * 2 + @h) * 11 + @a) / 451
		
		# Fast geschafft! Nimm den Inhalt von h und addiere zuerst den Inhalt von k und dann die Zahl 114. 
		# Nun multipliziere den Inhalt von l mit 7 und ziehe diese Zahl von der Summe ab. 
		# Teile durch 31, lege den Quotienten in Glas m und den Rest in Glas n. 
		@m = ((@h + @k + 114) - (@l * 7)) / 31
		@n = ((@h + @k + 114) - (@l * 7)) % 31
		
		# Nun hast du im Einmachglas m den Monat liegen (3 = März und 4 = April). Den Inhalt von Glas n mußt du noch um 1 erhöhen, 
		# und schon hast du den Monatstag vom Ostersonntag des gewünschten Jahres!
		@n = @n + 1
		return Time.local(jahr,@m,@n,0,0,0)	
		 # return @m,@n
  end
  
	def gibFeiertag(tagesdatum)
		datum = Time.local(tagesdatum.year, tagesdatum.month, tagesdatum.day,0,0,0)
		if datum.month == 1 && datum.day == 1
			return true,"Neujahr"
		elsif datum.month == 5 && datum.day == 1
			return true,"Staatsfeiertag"
		elsif datum.month == 8 && datum.day == 15
			return true,"Mariae Himmelfahrt"
		elsif datum.month == 10 && datum.day == 26
			return true,"Staatsfeiertag"
		elsif datum.month == 11 && datum.day == 1
			return true,"Allerheiligen"
		elsif datum.month == 12 && datum.day == 8
			return true,"Mariae Empfängnis"
		elsif datum.month == 12 && datum.day == 25
			return true,"Christtag"
		elsif datum.month == 12 && datum.day == 26
			return true,"Stefanitag"
		end
		
		@ostern = berechneOstern(datum.year)
		if @ostern == datum
			return true,"Ostern"
		elsif @ostern + 1.day == datum
			return true,"Ostern"
		elsif @ostern + 39.days == datum
			return true,"Christi Himmelfahrt"
		elsif @ostern + 49.days == datum
			return true,"Pfingsten"
		elsif @ostern + 50.days == datum
			return true,"Pfingsten"
		elsif @ostern + 60.days == datum
			return true,"Fronleichnam"
		end
		
		return false,""
 end

 def calcKW(datum)
	@dt = Time.gm(datum.year, datum.month, datum.day)

	# Determine its Day of Week, D
	# Use that to move to the nearest Thursday (-3..+3 days)
	@dt += (4 - @dt.wday).days

	# Note the year of that date, Y
	# Obtain January 1 of that year
	@firstofyear = Time.gm(@dt.year, 1, 1)

	# Get the Ordinal Date of that Thursday, DDD of YYYY-DDD
	@diff = @dt.yday - @firstofyear.yday

	# Then W is 1 + (DDD-1) div 7
	(1 + @diff / 7).to_s
 end
	
end
