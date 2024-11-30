import customtkinter as ctk
import tkintermapview
import map_with_shortest
from map import Map
from data_loader import get_map
import utils

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

        # Show the first screen initially
        self.show_frame(self.frame1)

    def show_frame(self, frame):
        frame.tkraise()  # Bring the selected frame to the front


class Screen1(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        # Add the frame to the grid
        self.grid(row=0, column=0, sticky="nsew")  # Stretch to fill parent container

        # Left frame
        left_frame = ctk.CTkFrame(self, width=600) 
        left_frame.pack(side="left", fill="both", expand=True)

        # UI elements for Screen 1
        label = ctk.CTkLabel(left_frame, text="Welcome to \nXMUM Shortest Path!", font=("Comic Sans", 35))
        label.pack(pady=(200, 5),padx=50)

        # To verify current location
        verify = ctk.CTkButton(left_frame, text="Click to verify your current location", width=250,
                                command=lambda: parent.show_frame(parent.frame2))
        verify.pack(pady=15)

        # To select location
        desc = ctk.CTkLabel(left_frame,
                            text="Why take the LONG way when you can take the RIGHT way? \n Let us guide you, shortcut style!;)",
                            font=("Comic Sans", 15))
        desc.pack(pady=(15, 5))

        # Right frame
        right_frame = ctk.CTkFrame(self, width=350)
        right_frame.pack(side="right", fill="both", expand=True)


        # To select location
        question = ctk.CTkLabel(right_frame, text="> Where are you heading to?", font=("Lato", 30))
        question.pack(pady=(200, 5))

        important_locations = xmu.get_important_loc()
        important_label = sorted([loc.get_name() for loc in important_locations])
        # Create a dropdown menu (CTkOptionMenu)
        self.choices = ctk.CTkOptionMenu(right_frame,
                                    values=important_label, width=200,
                                    font=('Times New Roman', 16), fg_color="black")

        # Set default value
        self.choices.set(important_label[0])
        self.choices.pack(pady=(15, 0))

        # Add a button
        def button_action():
            to_location = self.choices.get()  # Get selected location from dropdown
            from_location = list(parent.frame2.current_coordinates) 
            map_with_shortest.play(from_location,to_location)

        button = ctk.CTkButton(right_frame, text="Select Location", command=button_action, width=20,
                                fg_color="black",  # Button's primary color
                                hover_color="green",  # Button's color when hovered
                                text_color="white",  # Text color on the button
                                )
        button.pack(pady=(15, 0))

        # Set dev tools
        new_frame = ctk.CTkFrame(right_frame,fg_color="black")
        new_frame.pack(pady=18,padx=135, fill="both")

        text = ctk.CTkLabel(new_frame,  text="Dev Tools", font=("Lato",12))
        text.pack(side="left", padx=(15,0))

        # Choosing search algorithms
        algo_choices = xmu.get_all_search_algorithm()
        def choose_algo():
            self.chosen_algo = ctk.CTkOptionMenu(right_frame,
                                    values=algo_choices, width=30,
                                    font=('Lato', 16), fg_color="black")
            # Default
            self.chosen_algo.set(algo_choices[0])     
            self.chosen_algo.pack(pady= 0)

        # Checkbox for the item
        def on_check():
            if checkbox.get() == 1:  # If the checkbox is selected
                choose_algo()
            else:
                self.chosen_algo.pack_forget()

        checkbox = ctk.CTkCheckBox(new_frame, text="", command=on_check)
        checkbox.pack(side="right", padx=(90,0))

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
        back_button = ctk.CTkButton(left_frame, text="Back",
                                    command=lambda: parent.show_frame(parent.frame1))
        back_button.pack(pady=(20, 5))

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


if __name__ == "__main__":
    app = App()
    app.mainloop()
