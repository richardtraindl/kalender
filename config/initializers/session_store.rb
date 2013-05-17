# Be sure to restart your server when you modify this file.

# Your secret key for verifying cookie session data integrity.
# If you change this key, all old sessions will become invalid!
# Make sure the secret is at least 30 characters and all random, 
# no regular words or you'll be exposed to dictionary attacks.
ActionController::Base.session = {
  :key         => '_kalender_session',
  :secret      => '76983b302811fa9bc4b2697d8b2bf97dd10baff2a4c7fce5aa1749588aad350c82bd45dfc9b6d68b8b3f95fbdd03cba40fade5f2fd348e70156a0d64b7a96283'
}

# Use the database for sessions instead of the cookie-based default,
# which shouldn't be used to store highly confidential information
# (create the session table with "rake db:sessions:create")
# ActionController::Base.session_store = :active_record_store
