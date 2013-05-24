# encoding: UTF-8

require 'pp'

class Time

   # Todo/FIX:  nach lib schieben

   def wday_de  
     self.wday == 0 ? 6  : self.wday - 1
	 end
end


class TermineController < ApplicationController
    
  AUTOREN = [ "Ordi", "Elfi", "TP" ]
	SEK_PRO_TAG = (60 * 60 * 24)
	SEK_PRO_STUNDE = (60 * 60)
		
  def index    
		@aktzeit = Time.new
		@aktdatum = Time.gm(@aktzeit.year, @aktzeit.month, @aktzeit.day, 0, 0, 0, 0)
		
		@maxkaldatum = Time.gm(2020, 12, 31, 0, 0, 0, 0)
		@minkaldatum = Time.gm(2009, 1, 1, 0, 0, 0, 0)
		@sek_pro_tag = SEK_PRO_TAG
		@sek_pro_stunde = SEK_PRO_STUNDE
	
		@wochentage = ["Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag", "Samstag", "Sonntag"]
	
		@monate = [["Jänner", "1"], ["Februar", "2"], ["März", "3"], ["April", "4"], ["Mai", "5"], ["Juni", "6"], ["Juli", "7"], ["August", "8"], ["September", "9"], ["Oktober", "10"], ["November", "11"], ["Dezember", "12"]]
		
		if @aktdatum.wday == 0
			@kaldatum = @aktdatum - 6 * SEK_PRO_TAG
		else
			@kaldatum = @aktdatum - (@aktdatum.wday - 1) * SEK_PRO_TAG
		end
		
		if !params[:Jahr].blank? && !params[:Monat].blank? && !params[:Tag].blank?
			@jahr = params[:Jahr]
			@monat = params[:Monat]
			@tag = params[:Tag]

			if @monat == 2 && @tag > 29
				@tag = 29
			end
			begin
				@kaldatum = Time.gm(@jahr, @monat, @tag, 0, 0, 0, 0)
				
				rescue ArgumentError
				@tag = @tag - 1
				@kaldatum = Time.gm(@jahr, @monat, @tag, 0, 0, 0, 0)
			end
			
			if @kaldatum.wday == 0
				@kaldatum = @kaldatum - 6 * SEK_PRO_TAG
			else
				@kaldatum = @kaldatum - (@kaldatum.wday - 1) * SEK_PRO_TAG
			end
		end

		if !params[:KWadjust].blank?
			@adjust = params[:KWadjust]
			if @adjust == "1"
				@kaldatum = @kaldatum + SEK_PRO_TAG * 7
			elsif @adjust == "-1"
				@kaldatum = @kaldatum - SEK_PRO_TAG * 7	
			end
		end
	
		@termine = Termin.find_neu( @kaldatum, (@kaldatum + 7 * SEK_PRO_TAG) )   
  end


  def new
		@termin				 = Termin.new
		@termin.beginn = Time.at(Integer(params[:beginn]))
		@termin.ende   = @termin.beginn + 15.minutes
  end


  def build_datetime_from_params( params, field_name )
    DateTime.new(      
      params["#{field_name.to_s}(1i)"].to_i,
      params["#{field_name.to_s}(2i)"].to_i,
      params["#{field_name.to_s}(3i)"].to_i,
      params["#{field_name.to_s}(4i)"].to_i,
      params["#{field_name.to_s}(5i)"].to_i
      )      
  end


  def create
		@termin 			 = Termin.new
	  @termin.autor  = params[:termin][:autor]
	  @termin.thema  = params[:termin][:thema]
		@termin.beginn = Time.gm(
												(params[:termin][:date_begin].to_s[6,4]).to_i,
												(params[:termin][:date_begin].to_s[3,2]).to_i,
												(params[:termin][:date_begin].to_s[0,2]).to_i, 
												(params[:termin][:time_begin].to_s[0,2]).to_i, 
												(params[:termin][:time_begin].to_s[3,2]).to_i,
												0, 0)
		@termin.ende = Time.gm(
												(params[:termin][:date_end].to_s[6,4]).to_i,
												(params[:termin][:date_end].to_s[3,2]).to_i,
												(params[:termin][:date_end].to_s[0,2]).to_i,
												(params[:termin][:time_end].to_s[0,2]).to_i,
												(params[:termin][:time_end].to_s[3,2]).to_i,
												0, 0)
	  
	  # @termin.beginn = build_datetime_from_params( params[:termin], "beginn" )
		# @termin.ende   = build_datetime_from_params( params[:termin], "ende" )

		if( @termin.beginn > @termin.ende )
		    flash[:error] = 'Ende liegt vor Beginn.'
      	render :action => "new", :beginn => @termin.beginn, :ende => @termin.ende
		elsif( @termin.thema.length == 0 )
		    flash[:error] = 'Eingabe für Thema fehlt.'
      	render :action => "new", :beginn => @termin.beginn, :ende => @termin.ende		
		else
	    if @termin.save
	        flash[:notice] = 'Termin erfolgreich gespeichert.'
	        redirect_to :action => "index", :Jahr => @termin.beginn.year, :Monat => @termin.beginn.month, :Tag => @termin.beginn.day
	    else
	        flash[:notice] = 'Fehler beim Speichern des Termins.'
	        render :action => "new"
	    end
	   end
  end


  def edit
  	@kaldatum = Time.gm(params[:kjahr].to_i, params[:kmonat].to_i, params[:ktag].to_i)
		@termin	= Termin.find(params[:id])
  end


  def update
    @termin = Termin.find(params[:id])
    @termin.autor = params[:termin][:autor]
    @termin.thema = params[:termin][:thema]
    # @termin.beginn = build_datetime_from_params( params[:termin], "beginn" )
		# @termin.ende   = build_datetime_from_params( params[:termin], "ende" )
		@termin.beginn = Time.gm(
												(params[:termin][:date_begin].to_s[6,4]).to_i,
												(params[:termin][:date_begin].to_s[3,2]).to_i,
												(params[:termin][:date_begin].to_s[0,2]).to_i, 
												(params[:termin][:time_begin].to_s[0,2]).to_i, 
												(params[:termin][:time_begin].to_s[3,2]).to_i,
												0, 0)
		@termin.ende = Time.gm(
												(params[:termin][:date_end].to_s[6,4]).to_i,
												(params[:termin][:date_end].to_s[3,2]).to_i,
												(params[:termin][:date_end].to_s[0,2]).to_i,
												(params[:termin][:time_end].to_s[0,2]).to_i,
												(params[:termin][:time_end].to_s[3,2]).to_i,
												0, 0)

		if( @termin.beginn > @termin.ende )
		    flash[:error] = 'Ende liegt Beginn.'
      	render :action => "edit", :id => @termin.id
		elsif( @termin.thema.length == 0 )
		    flash[:error] = 'Eingabe für Thema fehlt.'
      	render :action => "edit", :id => @termin.id
		else
		  	if @termin.update_attributes(:autor => @termin.autor, :thema => @termin.thema, :beginn => @termin.beginn, :ende => @termin.ende )
		        flash[:notice] = 'Termin erfolgreich geändert.'
		        redirect_to :action => "index", :Jahr => @termin.beginn.year, :Monat => @termin.beginn.month, :Tag => @termin.beginn.day
		    else
		      	flash[:notice] = 'Fehler beim Speichern des Termins.'
		        render :action => "edit"
		    end
	  end
  end


  def destroy
		@termin = Termin.find(params[:id])
		jahr = @termin.beginn.year
		monat = @termin.beginn.month
		tag = @termin.beginn.day

		if @termin.destroy
			flash[:notice] = 'Termin erfolgreich gelöscht.'
		else
			flash[:notice] = 'Fehler beim Löschen des Termins.'
		end
		redirect_to :action => "index", :Jahr => jahr, :Monat => monat, :Tag => tag
  end


end 
