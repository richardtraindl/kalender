class Termin < ActiveRecord::Migration
  def self.up
		create_table :termine do |t|
			t.string		:autor, :limit => 30
			t.datetime	:beginn, :null => false
			t.datetime	:ende, :null => false
	    t.string		:thema, :limit => 50, :null => false
    end
  end

  def self.down
		drop_table :termine
  end
end
 