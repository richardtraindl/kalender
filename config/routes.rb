Kalender::Application.routes.draw do


   match 'kalender', :to => 'termine#index', :as => 'kalender' 
   # kalender_path()

   resources :termine, :except => [:index, :show]
  
  # Note: This route will make all actions in every controller accessible via GET requests.
	match ':controller(/:action(/:id))(.:format)'
end
