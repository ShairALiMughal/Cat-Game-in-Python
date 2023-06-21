import tkinter as tk
from PIL import Image, ImageTk
import random

# Constants
CANVAS_WIDTH = 800
CANVAS_HEIGHT = 600
CAT_CORE_DEPLETION_RATE = 1
MONEY_INCREASE_RATE = 1
MAX_CATS = 5

class Cat:
    def __init__(self, canvas):
        self.canvas = canvas
        self.x = random.randint(50, CANVAS_WIDTH-50)
        self.y = random.randint(50, CANVAS_HEIGHT-50)
        self.happiness = 100
        self.hydration = 100
        self.energy = 100
        # Generate a new random cat image number between 1 and 4
        cat_image_number = random.randint(1, 4)

        # Load cat image
        cat_image = Image.open(f"cat_image{cat_image_number}.png")
        # Load cat image
        cat_image = cat_image.resize((50, 50), Image.ANTIALIAS)
        self.image = ImageTk.PhotoImage(cat_image)

        # Display cat image on canvas
        self.image_obj = canvas.create_image(self.x, self.y, image=self.image)

        # Create text labels for cat attributes
        self.happiness_text = canvas.create_text(self.x, self.y+30, text=f"Happiness: {self.happiness}")
        self.hydration_text = canvas.create_text(self.x, self.y+45, text=f"Hydration: {self.hydration}")
        self.energy_text = canvas.create_text(self.x, self.y+60, text=f"Energy: {self.energy}")

    def update_cores(self):
        self.happiness -= CAT_CORE_DEPLETION_RATE
        self.hydration -= CAT_CORE_DEPLETION_RATE
        self.energy -= CAT_CORE_DEPLETION_RATE

    def is_depleted(self):
        return self.happiness <= 0 or self.hydration <= 0 or self.energy <= 0

class Game:
    def __init__(self, root):
        self.root = root
        self.canvas = tk.Canvas(root, width=CANVAS_WIDTH, height=CANVAS_HEIGHT)
        self.canvas.pack()

        self.cats = []
        self.money = 0

        # Create buttons
        self.buy_button = tk.Button(root, text="Buy Item", command=self.buy_item)
        self.buy_button.pack()

        # Start the game loop
        self.game_loop()

    def game_loop(self):
        # Update cat cores
        for cat in self.cats:
            cat.update_cores()
            if cat.is_depleted():
                self.canvas.delete(cat.image_obj)
                self.canvas.delete(cat.happiness_text)
                self.canvas.delete(cat.hydration_text)
                self.canvas.delete(cat.energy_text)
                self.cats.remove(cat)
            else:
                self.canvas.itemconfigure(cat.happiness_text, text=f"Happiness: {cat.happiness}")
                self.canvas.itemconfigure(cat.hydration_text, text=f"Hydration: {cat.hydration}")
                self.canvas.itemconfigure(cat.energy_text, text=f"Energy: {cat.energy}")

        # Increase player's money
        self.money += MONEY_INCREASE_RATE

        # Update GUI
        self.canvas.delete("money")
        self.canvas.create_text(10, 10, anchor="nw", text="Money: $"+str(self.money), tag="money")
        # Create new cats if the number of cats is less than the maximum
        if len(self.cats) < MAX_CATS:
            self.cats.append(Cat(self.canvas))

        # Remove old cats if the number of cats exceeds the maximum
        while len(self.cats) == MAX_CATS:

            cat = self.cats.pop(0)
            self.canvas.delete(cat.image_obj)
            self.canvas.delete(cat.happiness_text)
            self.canvas.delete(cat.hydration_text)
            self.canvas.delete(cat.energy_text)

        # Schedule the next iteration of the game loop

        
        self.root.after(1000, self.game_loop)

    def buy_item(self):
        if self.money >= 10:
            self.money -= 10
            # Handle the item purchase logic here
            print("Item purchased!")
    def buy_item(self):
        if self.money >= 10:
            self.money -= 10
            # Perform the item purchase action here
            print("Item purchased!")
        else:
            print("Insufficient funds!")

if __name__ == "__main__":
    root = tk.Tk()
    game = Game(root)
    root.mainloop()
