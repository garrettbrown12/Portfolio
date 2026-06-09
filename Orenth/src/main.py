from src.database import initialize_db, get_random_game_by_vibe, update_game_stats, add_new_game, \
    get_most_played_by_vibe


def main():
    conn = initialize_db()

    while True:
        print("\n--- Game Decider Menu ---")
        print("1. Get a recommendation")
        print("2. Add a new game")
        print("3. Get most played game by vibe")
        print("4. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            vibe = input("What's the vibe? ")
            while True:
                game = get_random_game_by_vibe(conn, vibe)
                if not game:
                    print("\nGame not found for that vibe, try adding one to it!")
                    break
                decision = input(f"How about {game}? (y/n/exit): ")
                if decision.lower() == "y":
                    update_game_stats(conn, game)
                    print(f"Great Choice! Have fun playing!")
                    break
                elif decision.lower() == "exit":
                    break
                else:
                    print("Searching for another game...")

        elif choice == "2":
            name = input("Enter Game Name: ")
            vibe = input("Enter Game Vibe: ")
            add_new_game(conn, name, vibe)
            print(f"Added {name} to the database!")

        elif choice == "3":
            vibe = input("Whats the vibe? ")
            game = get_most_played_by_vibe(conn, vibe)
            if game:
                print(f"Most played game for '{vibe}' is: {game}")
            else:
                print(f"No stats found for the vibe: {vibe}")

        elif choice == "4":
            print("Goodbye!")
            break
    conn.close()

if __name__ == "__main__":
    main()
