class Termin < ActiveRecord::Base

	def Termin.find_neu( wbeginn, wende )
			@termine = []

			termine_sql = Termin.find :all, :conditions => ['(beginn >= ? AND beginn <= ?) || (ende >= ? AND ende <= ?) || (beginn < ? AND ende > ?)', wbeginn, wende, wbeginn, wende, wbeginn, wende], :order => ('beginn ASC')
			
			0.upto(6) do |tag|

				termine_neu = []	
				termine_tp  = []
				
				termine_sql.each do |t|			
			  	if wbeginn.to_datetime.jd + tag >=	t.beginn.to_datetime.jd && wbeginn.to_datetime.jd + tag <= t.ende.to_datetime.jd 
		        if t.autor == "TP"
							termine_tp << t
						else
							termine_neu << t
						end
			  	end
				end

				termine_tp.reverse!
				
				@termine[tag] = termine_neu + termine_tp

			end # loop tag
			
			@termine # return
	end   

end
