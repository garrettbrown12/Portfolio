from tkinter import dialog

import customtkinter as ctk
import database

#configure appearance
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("green")

class GameDeciderApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        #setup Database
        self.conn = database.initialize_db()

        #window config
        self.title("Orenth V1.2")
        self.geometry("400x450")

        #UI Elements
        self.label = ctk.CTkLabel(self, text="Orenth Main Menu", font=("Arial", 20))
        self.label.pack(pady=20)

        self.vibe_entry = ctk.CTkEntry(self, placeholder_text="Enter a vibe")
        self.vibe_entry.pack(pady=10)

        #buttons
        ctk.CTkButton(self, text="Get a Recommendation", command=self.get_rec).pack(pady=5)
        ctk.CTkButton(self, text="Add a New Game", command=self.add_game_ui).pack(pady=5)
        ctk.CTkButton(self, text="Get Your Most Played Game By Vibe", command=self.get_top_game).pack(pady=5)
        ctk.CTkButton(self, text="Fresh Start", command=self.confirm_reset, fg_color="red", hover_color="darkred").pack(pady=20)

        #making outputs appear in the gui
        self.result_display = ctk.CTkLabel(self, text="", font=("Arial", 14), text_color="yellow")
        self.result_display.pack(pady=20)

    def get_rec(self):
        vibe = self.vibe_entry.get()
        game = database.get_random_game_by_vibe(self.conn, vibe)
        if game:
            #simple dialogue
            self.result_display.configure(text=f"How about: {game}", text_color="green")
            database.update_game_stats(self.conn, game)
        else:
            self.result_display.configure(text="No Game Found.", text_color="red")

    def add_game_ui(self):
        #create top-level window
        add_window = ctk.CTkToplevel(self)
        add_window.title("Add New Game")
        add_window.geometry("300x250")
        #ensure window stays on top
        add_window.attributes("-topmost", True)

        #labels and entries
        ctk.CTkLabel(add_window, text="Game Name:").pack(pady=5)
        name_entry = ctk.CTkEntry(add_window)
        name_entry.pack(pady=5)

        ctk.CTkLabel(add_window, text="Vibe:").pack(pady=5)
        vibe_entry = ctk.CTkEntry(add_window)
        vibe_entry.pack(pady=5)

        #function to execute adding and closing
        def save_game():
            name = name_entry.get()
            vibe = vibe_entry.get()
            if name and vibe:
                database.add_new_game(self.conn, name, vibe)
                self.result_display.configure(text=f"Added {name} to {vibe}", text_color="green")
                add_window.destroy() #closes the popup

        ctk.CTkButton(add_window, text="Save Game", command=save_game).pack(pady=20)

    def get_top_game(self):
        vibe = self.vibe_entry.get()
        game = database.get_most_played_by_vibe(self.conn, vibe)
        self.result_display.configure(text=f"Most Played for {vibe}: {game}", text_color="white")

    def confirm_reset(self):
        #create a popup for confirmation
        dialog = ctk.CTkInputDialog(text="Type 'DELETE' to confirm a total reset:", title="Fresh Start")
        user_input = dialog.get_input()

        if user_input == "DELETE":
            database.reset_database(self.conn)
            self.result_display.configure(text="Reset Complete", text_color="orange")
        else:
            self.result_display.configure(text="Reset Cancelled", text_color="red")
if __name__ == "__main__":
    app = GameDeciderApp()
    app.mainloop()