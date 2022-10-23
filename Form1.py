from ._anvil_designer import Form1Template
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from ..Autocomplete import Autocomplete
from random import choice

class Form1(Form1Template):
  genre = "All"
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.type_games = anvil.server.call('gettype', app_files.action_json)
    self.winner = choice(self.type_games)
    self.options = action = anvil.server.call('getgames', app_files.action_json)
    self.count = 0
    self.row_count = 0
    self.logged_in = False
    self.username = ''
    self.repeating_panel_1.items = [{'text':' '}] * 2
    self.repeating_panel_1.set_event_handler('x-option_clicked',self.option_clicked)

    self.grid_panel_1.add_component(Label(text="Name", background='#696969', align="center", bold=True),row="MyRow", col_xs=0, width_xs=2)
    self.grid_panel_1.add_component(Label(text="Release", background='#696969', align="center", bold=True),row="MyRow", col_xs=2, width_xs=2)
    self.grid_panel_1.add_component(Label(text="Owned", background='#696969', align="center", bold=True),row="MyRow", col_xs=4, width_xs=2)
    self.grid_panel_1.add_component(Label(text="Rating", background='#696969', align="center", bold=True),row="MyRow", col_xs=6, width_xs=2)
    self.grid_panel_1.add_component(Label(text="Platforms", background='#696969', align="center", bold=True),row="MyRow", col_xs=8, width_xs=2)
    self.grid_panel_1.add_component(Label(text="Player", background='#696969', align="center", bold=True),row="MyRow", col_xs=10, width_xs=2)
    # Any code you write here will run when the form opens.

  def reset(self):
    self.grid_panel_2.clear()
  
  def drop_down_1_change(self, **event_args):
    """This method is called when an item is selected"""
    pass

  def get_data(self, name):
    for i in self.type_games:
      if name == i["Name"]:
        return i
    return None
    
  def text_box_1_pressed_enter(self, **event_args):
    """This method is called when the user presses Enter in this text box"""
    guess = self.text_box_1.text
    print(guess)
    #self.label_3.text = guess
    guess = self.get_data(guess)
    current_row = str(self.row_count)
    print(guess)
    win = (guess["Name"] == self.winner["Name"])
    if win:
      self.grid_panel_2.add_component(Label(text=guess["Name"], background='#014421', align="center", bold=True),row=current_row, col_xs=0, width_xs=2)
    else:
      self.grid_panel_2.add_component(Label(text=guess["Name"], background='#8B0000', align="center", bold=True),row=current_row, col_xs=0, width_xs=2)

    if guess["Release"] == self.winner["Release"]:
      self.grid_panel_2.add_component(Label(text=guess["Release"], background='#014421', align="center"),row=current_row, col_xs=2, width_xs=2)
    elif guess["Release"] < self.winner["Release"]:
      self.grid_panel_2.add_component(Label(text=str(guess["Release"])+ " \u21E7", background='#8B0000', align="center"),row=current_row, col_xs=2, width_xs=2)
    else:
      self.grid_panel_2.add_component(Label(text=str(guess["Release"]) + " \u21E9", background='#8B0000', align="center"),row=current_row, col_xs=2, width_xs=2)

    if guess["Owned"] == self.winner["Owned"]:
      self.grid_panel_2.add_component(Label(text=guess["Owned"], background='#014421', align="center"),row=current_row, col_xs=2, width_xs=2)
    elif guess["Owned"] < self.winner["Owned"]:
      self.grid_panel_2.add_component(Label(text=str(guess["Owned"])+ " \u21E7", background='#8B0000', align="center"),row=current_row, col_xs=2, width_xs=2)
    else:
      self.grid_panel_2.add_component(Label(text=str(guess["Owned"]) + " \u21E9", background='#8B0000', align="center"),row=current_row, col_xs=2, width_xs=2)

    if guess["Rating"] == self.winner["Rating"]:
      self.grid_panel_2.add_component(Label(text=guess["Rating"], background='#014421', align="center"),row=current_row, col_xs=2, width_xs=2)
    elif guess["Rating"] < self.winner["Rating"]:
      self.grid_panel_2.add_component(Label(text=str(guess["Rating"])+ " \u21E7", background='#8B0000', align="center"),row=current_row, col_xs=2, width_xs=2)
    else:
      self.grid_panel_2.add_component(Label(text=str(guess["Rating"]) + " \u21E9", background='#8B0000', align="center"),row=current_row, col_xs=2, width_xs=2)

    plat = ('\n').join(guess["Platforms"])
    
    
    if guess["Platforms"] == self.winner["Platforms"]:
      self.grid_panel_2.add_component(Label(text=plat, background='#014421', align="center"),row=current_row, col_xs=8, width_xs=2)
    elif any([i in self.winner["Platforms"] for i in guess["Platforms"]]):
      self.grid_panel_2.add_component(Label(text=plat, background='#FFBF00', align="center"),row=current_row, col_xs=8, width_xs=2)
    else:
      self.grid_panel_2.add_component(Label(text=plat, background='#8B0000', align="center"),row=current_row, col_xs=8, width_xs=2)

    string = ''
    if guess["Type"][0] and guess["Type"][1]:
      string = 'Singleplayer\nMultiplayer'
    elif guess["Type"][0]:
      string = 'Singleplayer'
    elif guess["Type"][1]:
      string = 'Multiplayer''
    else:
      string = 'None'
      
    if guess["Type"] == self.winner["Type"]:
      self.grid_panel_2.add_component(Label(text=string, background='#014421', align="center"),row=current_row, col_xs=10, width_xs=2)
    else:
      self.grid_panel_2.add_component(Label(text=string, background='#8B0000', align="center"),row=current_row, col_xs=10, width_xs=2)

    self.row_count += 1
    self.count += 1
    if win:
      statement = f"You Guessed Correctly :)"
      if self.logged_in:
        row = app_tables.users.get(email=self.username)
        row.update(Score=row['Score']+1)
        statement = f"You Guessed Correctly :)\nWin: {row['Score']}"
      n = Notification(statement, timeout=10)
      n.show()
      self.reset()
      self.count = 0
    if self.count >= 7 and not win:
      n = Notification(f'You ran out of tries :(\nAnswer is: {self.winner["Name"]}', timeout=10)
      n.show()
      self.reset()
      self.count = 0
      

  def Login_click(self, **event_args):
    """This method is called when the button is clicked"""
    user = anvil.users.login_with_form() 
    self.username = user['email']
    if user['Score'] == None:
      user.update(Score=0)
    alert("Logged In")
    self.logged_in = True
    self.Logout.visible = True
    self.Login.text = self.username[:self.username.index('@')]
    #self.Login.enabled = False
    pass

  def text_box_1_change(self, **event_args):
    """This method is called when the text in this text box is edited"""
    new_options = []
    for option in self.options:
      if option.lower().startswith(self.text_box_1.text.lower()):
        new_options.append({'text':option})
    # truncate to 7 max
    new_options = new_options[:2]
    # ensure a full 7 options
    if len(new_options) < 2:
      new_options+=( [{'text':' '}] * (2-len(new_options)))
    self.repeating_panel_1.items = new_options

  def button_18_click(self, **event_args):
    """This method is called when the button is clicked"""
    if anvil.users.get_user() == None:
      alert("Already Logged Out")
    else:
      anvil.users.logout()
      alert("Logged Out")
      self.Login.text = "Login"
     #self.Login.enabled = True
      
    pass

  def Help_Button_mouse_down(self, x, y, button, **event_args):
    """This method is called when a mouse button is pressed on this component"""
    alert(content="Enter in a name of a game and get hints as to what the game actually is.",
               title=f"Tutorial",
               large=True)
    pass

  def button_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    genre = "Action"
    self.text_box_1.placeholder = "Enter in a Guess for " + genre + " Games"
    self.options = anvil.server.call('getgames', app_files.action_json)

  def option_clicked(self,option,**event_args):
    if option == ' ':
      return
    self.text_box_1.text = option
    self.repeating_panel_1.items = []
    
  def all_click(self, **event_args):
    genre = "All"
    self.text_box_1.placeholder = "Enter in a Guess for " + genre + " Games"
    #self.options = anvil.server.call('getgames', app_files.action_json)
   
  def action_click(self, **event_args):
    genre = "Action"
    self.text_box_1.placeholder = "Enter in a Guess for " + genre + " Games"
    self.type_games = anvil.server.call('gettype', app_files.action_json)
    self.winner = choice(self.type_games)
    self.options = anvil.server.call('getgames', app_files.action_json)
    self.reset()
    self.count = 0

  def adventure_click(self, **event_args):
    genre = "Adventure"
    self.text_box_1.placeholder = "Enter in a Guess for " + genre + " Games"
    self.type_games = anvil.server.call('gettype', app_files.adventure_json)
    self.winner = choice(self.type_games)
    self.options = anvil.server.call('getgames', app_files.adventure_json)
    self.reset()
    self.count = 0
    
  def arcade_click(self, **event_args):
    genre = "Arcade"
    self.text_box_1.placeholder = "Enter in a Guess for " + genre + " Games"
    self.type_games = anvil.server.call('gettype', app_files.arcade_json)
    self.winner = choice(self.type_games)
    self.options = anvil.server.call('getgames', app_files.arcade_json)
    self.reset()
    self.count = 0
    
  def card_click(self, **event_args):
    genre = "Card"
    self.text_box_1.placeholder = "Enter in a Guess for " + genre + " Games"
    self.type_games = anvil.server.call('gettype', app_files.card_json)
    self.winner = choice(self.type_games)
    self.options = anvil.server.call('getgames', app_files.card_json)
    self.reset()
    self.count = 0
    
  def fighting_click(self, **event_args):
    genre = "Fighting"
    self.text_box_1.placeholder = "Enter in a Guess for " + genre + " Games"
    self.type_games = anvil.server.call('gettype', app_files.fighting_json)
    self.winner = choice(self.type_games)
    self.options = anvil.server.call('getgames', app_files.fighting_json)
    self.reset()
    self.count = 0
    
  def indie_click(self, **event_args):
    genre = "Indie"
    self.text_box_1.placeholder = "Enter in a Guess for " + genre + " Games"
    self.type_games = anvil.server.call('gettype', app_files.indie_json)
    self.winner = choice(self.type_games)
    self.options = anvil.server.call('getgames', app_files.indie_json)
    self.reset()
    self.count = 0
    
  def mmo_click(self, **event_args):
    genre = "MMO"
    self.text_box_1.placeholder = "Enter in a Guess for " + genre + " Games"
    self.type_games = anvil.server.call('gettype', app_files.massively_multiplayer_json)
    self.winner = choice(self.type_games)
    self.options = anvil.server.call('getgames', app_files.massively_multiplayer_json)
    self.reset()
    self.count = 0
    
  def platformer_click(self, **event_args):
    genre = "Platformer"
    self.text_box_1.placeholder = "Enter in a Guess for " + genre + " Games"
    self.type_games = anvil.server.call('gettype', app_files.platformer_json)
    self.winner = choice(self.type_games)
    self.options = anvil.server.call('getgames', app_files.platformer_json)
    self.reset()
    self.count = 0
    
  def puzzle_click(self, **event_args):
    genre = "Puzzle"
    self.text_box_1.placeholder = "Enter in a Guess for " + genre + " Games"
    self.type_games = anvil.server.call('gettype', app_files.puzzle_json)
    self.winner = choice(self.type_games)
    self.options = anvil.server.call('getgames', app_files.puzzle_json)
    self.reset()
    self.count = 0
    
  def racing_click(self, **event_args):
    genre = "Racing"
    self.text_box_1.placeholder = "Enter in a Guess for " + genre + " Games"
    self.type_games = anvil.server.call('gettype', app_files.racing_json)
    self.winner = choice(self.type_games)
    self.options = anvil.server.call('getgames', app_files.racing_json)
    self.reset()
    self.count = 0
    
  def shooter_click(self, **event_args):
    genre = "Shooter"
    self.text_box_1.placeholder = "Enter in a Guess for " + genre + " Games"
    self.type_games = anvil.server.call('gettype', app_files.shooter_json)
    self.winner = choice(self.type_games)
    self.options = anvil.server.call('getgames', app_files.shooter_json)
    self.reset()
    self.count = 0
    
  def rpg_click(self, **event_args):
    genre = "RPG"
    self.text_box_1.placeholder = "Enter in a Guess for " + genre + " Games"
    self.type_games = anvil.server.call('gettype', app_files.rpg_json)
    self.winner = choice(self.type_games)
    self.options = anvil.server.call('getgames', app_files.rpg_json)
    self.reset()
    self.count = 0
    
  def simulation_click(self, **event_args):
    genre = "Simulation"
    self.text_box_1.placeholder = "Enter in a Guess for " + genre + " Games"
    self.type_games = anvil.server.call('gettype', app_files.simulation_json)
    self.winner = choice(self.type_games)
    self.options = anvil.server.call('getgames', app_files.simulation_json)
    self.reset()
    self.count = 0
    
  def sports_click(self, **event_args):
    genre = "Sports"
    self.text_box_1.placeholder = "Enter in a Guess for " + genre + " Games"
    self.type_games = anvil.server.call('gettype', app_files.sports_json)
    self.winner = choice(self.type_games)
    self.options = anvil.server.call('getgames', app_files.sports_json)
    self.reset()
    self.count = 0
    
  def strategy_click(self, **event_args):
    genre = "Strategy"
    self.text_box_1.placeholder = "Enter in a Guess for " + genre + " Games"
    self.type_games = anvil.server.call('gettype', app_files.strategy_json)
    self.winner = choice(self.type_games)
    self.options = anvil.server.call('getgames', app_files.strategy_json)
    self.reset()
    self.count = 0
  def label_1_show(self, **event_args):
    """This method is called when the Label is shown on the screen"""
    pass
  
  def label_1_hide(self, **event_args):
    """This method is called when the Label is removed from the screen"""
    pass

  def Login_hide(self, **event_args):
    """This method is called when the Button is removed from the screen"""
    pass

  def grid_panel_1_show(self, **event_args):
    pass
