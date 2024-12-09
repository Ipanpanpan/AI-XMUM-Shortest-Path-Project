import customtkinter as ctk
import tkintermapview
import map_with_shortest
from map import Map
from data_loader import get_map
import utils
from PIL import Image, ImageTk

xmu = Map()
xmu = get_map()
ctk.set_appearance_mode("dark")  # Modes: "dark", "light", or "system"
ctk.set_default_color_theme("blue")  # Themes: "blue", "green", "dark-blue"

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.grid_rowconfigure(0, weight=1)  # Center content vertically
        self.grid_columnconfigure(0, weight=1)  # Center content horizontally

        self.title("Shortest Path App")
        self.geometry("900x600")

        # Create two frames
        self.frame1 = Screen1(self)
        self.frame2 = Screen2(self)
        self.frame3 = Screen3(self)

        # Show the first screen initially
        self.show_frame(self.frame1)

    def show_frame(self, frame):
        frame.tkraise()  # Bring the selected frame to the front


class Screen1(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        self.grid(row=0, column=0, sticky="nsew")  # Full screen
        self.show_bg(parent)

    def show_bg(self, parent):
        # Load and display background image
        self.bg_image = ctk.CTkImage(Image.open("main.png"), size=(900, 600))
        self.bg_label = ctk.CTkLabel(self, image=self.bg_image, text="")
        self.bg_label.pack(fill="both", expand=True)

        self.navigate_button1 = ctk.CTkButton(
            self, text="Click to verify your current location", command=lambda: parent.show_frame(parent.frame2)
        )
        self.navigate_button1.place(relx=0.5, rely=0.8, anchor="center")

class Screen2(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.current_coordinates = utils.get_curr_loc()  # Initial coordinates

        # Add the frame to the grid
        self.grid(row=0, column=0, sticky="nsew")  # Stretch to fill parent container

        # Create a frame for the left-side widgets
        left_frame = ctk.CTkFrame(self, width=300)  # Fixed width for the left frame
        left_frame.pack(side="left", fill="y", padx=10, pady=10)  # Left side of the window

        # Add widgets to the left frame
        label1 = ctk.CTkLabel(left_frame, text="Please Confirm Your\nCurrent Location", font=("Arial", 18))
        label1.pack(padx=20, pady=10)

        label2 = ctk.CTkLabel(left_frame,
                              text="Follow These Instructions:\n1. Hover over your preferred\n    current location\n2. Right-click on the map\n3. Click confirm location",
                              justify='left', font=("Arial", 15))
        label2.pack(padx=20, pady=10)

        label3 = ctk.CTkLabel(left_frame, text="\nCurrent Location", justify='left', font=("Arial", 18))
        label3.pack()

        # Variable for live-updating coordinates
        self.current_coords_var = ctk.StringVar()
        self.current_coords_var.set("Latitude: -\nLongitude: -")  # Initial placeholder text

        coords_label = ctk.CTkLabel(left_frame, textvariable=self.current_coords_var, font=("Arial", 15),
                                    justify='left')
        coords_label.pack(pady=5)

        # Back Button
        continue_button = ctk.CTkButton(left_frame, text="Click to Continue",
                                    command=lambda: parent.show_frame(parent.frame3))
        continue_button.pack(pady=(20, 5))

        # Create the map frame
        map_frame = ctk.CTkFrame(self)
        map_frame.pack(side="right", fill="both", expand=True)  # Aligns map frame to the right

        # Create the map widget inside the map frame
        self.map_widget = tkintermapview.TkinterMapView(map_frame, width=1400, height=600, corner_radius=0)
        self.map_widget.pack(fill="both", expand=True)  # Ensures the map fills its frame
        self.map_widget.set_position(2.8317, 101.7050)
        self.map_widget.set_zoom(18)

        # Variable to hold the current location marker
        self.current_marker = self.map_widget.set_marker(self.current_coordinates[0],self.current_coordinates[1], "Current Location")

        # Function to change the current location
        def change_current(coords):
            print("Change Current Location to:", coords)

            # Update coordinates text
            self.current_coords_var.set(f"Latitude: {coords[0]:.6f}\nLongitude: {coords[1]:.6f}")

            # Remove the previous marker if it exists
            if self.current_marker:
                self.current_marker.delete()

            # Set a new marker for the current location
            self.current_marker = self.map_widget.set_marker(coords[0], coords[1], text="New Current Location")

            # Update the stored coordinates
            self.current_coordinates = [coords[0], coords[1]]

        # Add right-click menu to the map
        self.map_widget.add_right_click_menu_command(label="Confirm Location", command=change_current, pass_coords=True)

class Screen3 (ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

    # Add the frame to the grid
        self.grid(row=0, column=0, sticky="nsew")  # Stretch to fill parent container
        self.show_bg2(parent)

    def show_bg2(self, parent):
        # Load and display background image
        self.bg_image = ctk.CTkImage(Image.open("bg_pic.png"), size=(900, 600))
        self.bg_label = ctk.CTkLabel(self, image=self.bg_image, text="")
        self.bg_label.place(relx=0.5, rely=0.5, anchor="center")

        important_locations = xmu.get_important_loc()
        important_label = sorted([loc.get_name() for loc in important_locations])
        # Create a dropdown menu (CTkOptionMenu)
        self.choices = ctk.CTkOptionMenu(self,
                                    values=important_label, width=200,
                                    font=('Times New Roman', 16), fg_color="black")

        # Set default value
        self.choices.set(important_label[0])
        self.choices.place(relx=0.5, rely=0.5, anchor="center")
        
        # Set dev tools
        new_frame = ctk.CTkFrame(self,fg_color="black",width=10)
        new_frame.place(relx=0.5, rely=0.56, anchor="center")

        text = ctk.CTkLabel(new_frame,  text="Custom Search", font=("Lato",12))
        text.pack(side="left", padx=(5,0))

        # Choosing search algorithms
        algo_choices = xmu.get_all_search_algorithm()
        def choose_algo():
            self.chosen_algo = ctk.CTkOptionMenu(self,
                                    values=algo_choices, width=30,
                                    font=('Lato', 16), fg_color="black")
            # Default
            self.chosen_algo.set(algo_choices[0])     
            self.chosen_algo.place(relx=0.5, rely=0.63, anchor="center")
    
            
        # Checkbox for the item
        def on_check():
            if checkbox.get() == 1:  # If the checkbox is selected
                choose_algo()
            else:
                self.chosen_algo.place_forget()

        checkbox = ctk.CTkCheckBox(new_frame, text="", command=on_check,width=40,hover=True)
        checkbox.pack(side="left", padx=11)

        def get_chosen_algo():
            if hasattr(self, 'chosen_algo') and self.chosen_algo:  # Check if it exists
                return self.chosen_algo.get()
            else:
                return 'a star'  # Or some default value if no selection is available


        # Add a button
        def button_action():
            to_location = self.choices.get()  # Get selected location from dropdown
            from_location = list(parent.frame2.current_coordinates)
            chosen_algorithm = get_chosen_algo()
            map_with_shortest.play(from_location,to_location,chosen_algorithm)

        button = ctk.CTkButton(self, text="Select Location", command=button_action, width=40,
                                fg_color="black",  # Button's primary color
                                hover_color="green",  # Button's color when hovered
                                text_color="white",  # Text color on the button
                                corner_radius=20
                                )
        button.place(relx=0.5, rely=0.70, anchor="center")

        # Back Button
        back_button = ctk.CTkButton(self, text="Back",
                                    command=lambda: parent.show_frame(parent.frame2))
        back_button.place(relx=0.82, rely=0.9, anchor="center")

if __name__ == "__main__":
    app = App()
    app.mainloop()
