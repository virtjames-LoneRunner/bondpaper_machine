import customtkinter as ct
from datetime import datetime, timedelta

# Modes: "System" (standard), "Dark", "Light"
ct.set_appearance_mode("Dark")
# Themes: "blue" (standard), "green", "dark-blue"
ct.set_default_color_theme("blue")


class App(ct.CTk):

    button_colors = {"active": "#AEAE00", "normal": "blue"}

    system = None
    coin_slot = None

    def __init__(self, system):
        super().__init__()
        self.system = system

    # Overridable Custom Methods
    add_amount_button_event = None

    # Constants
    FRAME_WIDTH = 100
    SIDEBAR_FRAME_WIDTH = 70
    BUTTON_WIDTH = 150
    BUTTON_HEIGHT = 30
    BUTTON_FONT_SIZE = 20
    BUTTON_PADX=10
    BUTTON_PADY=10

    # Variables
    paper_sizes = []
    paper_size_buttons = {} 
    amount_given_var = 0
    selected_paper = ""

    # Display variables
    views = ["main_frame", "select_paper_frame", "quantity_frame", "done_frame"]
    display_index = 0
    active_view = 'main_frame'

    # Utility variables
    is_running = False
    end_time = None

    def customInit(self):
        # configure window
        self.title("Automated Bondpaper Selling Machine")
        # self.geometry("500x300")
        self.attributes("-fullscreen", True)  # Make the window fullscreen

        # configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure((0, 1, 2), weight=1)


        # Add buttons for the first time
        self._init_buttons()

        # Add the display for the first time
        self._initialize_display_for_start()

    # Initialize buttons at start
    def _init_buttons(self):
        # create sidebar frame with widgets
        self.sidebar_frame = ct.CTkFrame(
            self, width=self.SIDEBAR_FRAME_WIDTH, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(
            4, minsize=20)  # reserve space for padding

        self.sidebar_button_1 = ct.CTkButton(
            self.sidebar_frame,
            text="Start Transaction",
            command=lambda: self.change_active_view("main_frame"),
            width=self.BUTTON_WIDTH,
            height=self.BUTTON_WIDTH,
            fg_color="#453ad6",
            font=ct.CTkFont(size=self.BUTTON_FONT_SIZE))
        self.sidebar_button_1.grid(row=1, column=0, padx=self.BUTTON_PADX, pady=self.BUTTON_PADY)

        self.sidebar_button_2 = ct.CTkButton(
            self.sidebar_frame,
            text="Select Paper",
            state="disabled",
            command=lambda: self.change_active_view("select_paper_frame"),
            width=self.BUTTON_WIDTH,
            height=self.BUTTON_WIDTH,
            font=ct.CTkFont(size=self.BUTTON_FONT_SIZE))
        self.sidebar_button_2.grid(row=2, column=0, padx=self.BUTTON_PADX, pady=self.BUTTON_PADY)

        self.sidebar_button_3 = ct.CTkButton(
            self.sidebar_frame,
            text="Quantity",
            state="disabled",
            command=lambda: self.change_active_view("quantity_frame"),
            width=self.BUTTON_WIDTH,
            height=self.BUTTON_WIDTH,
            font=ct.CTkFont(size=self.BUTTON_FONT_SIZE))
        self.sidebar_button_3.grid(row=3, column=0, padx=self.BUTTON_PADX, pady=self.BUTTON_PADY)

        self.sidebar_button_4 = ct.CTkButton(
            self.sidebar_frame,
            text="Done",
            state="disabled",
            command=lambda: self.change_active_view("done_frame"),
            width=self.BUTTON_WIDTH,
            height=self.BUTTON_WIDTH,
            font=ct.CTkFont(size=self.BUTTON_FONT_SIZE))
        self.sidebar_button_4.grid(row=4, column=0, padx=self.BUTTON_PADX, pady=self.BUTTON_PADY)

    # Initialize first display
    def _initialize_display_for_start(self):
        # Select Paper Frame
        self.select_paper_frame = ct.CTkFrame(
            self, width=self.FRAME_WIDTH, fg_color=("gray75", "gray25"))
        self.select_paper_frame.grid_rowconfigure(
            3, minsize=20)  # reserve space for padding
        self.select_paper_label = ct.CTkLabel(self.select_paper_frame, text="Select Paper", anchor="w", font=ct.CTkFont(size=self.BUTTON_FONT_SIZE))
        self.select_paper_label.pack(padx=20, pady=(50, 0))
        self.paper_buttons_frame = ct.CTkFrame(self.select_paper_frame, fg_color=("gray75", "gray25"))
        for i, paper_size in enumerate(self.paper_sizes):
            self.paper_size_buttons[paper_size] = ct.CTkButton(
                self.paper_buttons_frame,
                text=paper_size,
                width=self.BUTTON_WIDTH,
                height=self.BUTTON_WIDTH,
                font=ct.CTkFont(size=self.BUTTON_FONT_SIZE))
            self.paper_size_buttons[paper_size].grid(row=0, column=i, padx=20, pady=(50, 0))
        self.paper_buttons_frame.pack(padx=20, pady=(50, 0))
        # Select Paper Frame

        # Quantity Frame
        self.quantity_frame = ct.CTkFrame(
            self, width=self.FRAME_WIDTH, fg_color=("gray75", "gray25"))
        self.quantity_frame.grid_rowconfigure(
            3, minsize=20)  # reserve space for padding
        self.quantity_label = ct.CTkLabel(self.quantity_frame, text="Set Quantity", anchor="w", font=ct.CTkFont(size=self.BUTTON_FONT_SIZE))
        self.quantity_label.pack(padx=20, pady=(50, 0))
        # Quantity Frame

        # Done Frame
        self.done_frame = ct.CTkFrame(
            self, width=self.FRAME_WIDTH, fg_color=("gray75", "gray25"))
        self.done_frame.grid_rowconfigure(
            3, minsize=20)  # reserve space for padding
        self.done_label = ct.CTkLabel(self.done_frame, text="Done", anchor="w", font=ct.CTkFont(size=self.BUTTON_FONT_SIZE))
        self.done_label.pack(padx=20, pady=(50, 0))

        self.countdown_label = ct.CTkLabel(self.done_frame, text="00:00:00", anchor="w", font=ct.CTkFont(size=self.BUTTON_FONT_SIZE))
        self.countdown_label.pack(padx=20, pady=(50, 0))
        self.done_button = ct.CTkButton(self.done_frame, text="Another Transaction")
        # Done Frame

        # Main Frame
        self.main_frame = ct.CTkFrame(
            self, width=self.FRAME_WIDTH, fg_color=("gray75", "gray25"))
        self.main_frame.grid(row=0, column=1, rowspan=3, sticky="news")
        self.main_frame.grid_rowconfigure(
            3, minsize=20)  # reserve space for padding
        self.main_label = ct.CTkLabel(self.main_frame, text="Start Transaction", anchor="w", font=ct.CTkFont(size=self.BUTTON_FONT_SIZE))
        self.main_label.pack(padx=20, pady=(50, 0))
        self.amount_frame = ct.CTkFrame(self.main_frame, fg_color=("gray75", "gray25")) 
        self.amount_frame.pack(padx=20, pady=(50, 0))
        self.amount_given_var = ct.IntVar(value=0)
        self.currency_symbol_label = ct.CTkLabel(self.amount_frame, text="₱", anchor="w", font=ct.CTkFont(size=100))
        self.currency_symbol_label.grid(row=0, column=0, padx=20, pady=(50, 50))
        self.display_amount_label = ct.CTkLabel(self.amount_frame, textvariable=self.amount_given_var, anchor="w", font=ct.CTkFont(size=100))
        self.display_amount_label.grid(row=0, column=1, padx=20, pady=(50, 50))
        # Main Frame

        # Global Buttons
        self.buttons_frame = ct.CTkFrame(self, fg_color=("gray75", "gray25"))
        self.prev_button = ct.CTkButton(
            self.buttons_frame,
            text="Back",
            command=self._display_back,
            width=self.BUTTON_WIDTH,
            height=self.BUTTON_HEIGHT,
            fg_color="gray75",
            text_color="#453ad6",
            font=ct.CTkFont(size=self.BUTTON_FONT_SIZE))
        self.prev_button.grid(row=0, column=0, padx=20, pady=10)
        self.next_button = ct.CTkButton(
            self.buttons_frame,
            text="Next",
            command=self._display_next,
            width=self.BUTTON_WIDTH,
            height=self.BUTTON_HEIGHT,
            fg_color="gray75",
            text_color="#453ad6",
            font=ct.CTkFont(size=self.BUTTON_FONT_SIZE))
        self.next_button.grid(row=0, column=1, padx=20, pady=10)
        self.buttons_frame.grid(row=2, column=1, rowspan=3, sticky="e")
        # Global Buttons
    
    # Restart display after transaction 
    def _refresh_display(self):
        self.select_paper_frame.grid_forget()
        self.main_frame.grid(row=0, column=1, rowspan=3, sticky="news")
    
    # Built-in methods
    def change_appearance_mode(self, new_appearance_mode):
        ct.set_appearance_mode(new_appearance_mode)

    def reset(self):
        self.amount_given_var = 0
        self.selected_paper = ""

        self.display_index = 0
        self._change_active_view_by_index(self.display_index)

        self.next_button.configure(state="normal")
        self.sidebar_button_1.configure(fg_color="#453ad6", state="normal")
        self.sidebar_button_2.configure(fg_color="#1f6aa5", state="disabled")
        self.sidebar_button_3.configure(fg_color="#1f6aa5", state="disabled")
        self.sidebar_button_4.configure(fg_color="#1f6aa5", state="disabled")

    def change_active_view(self, view):
        self.active_view = view
        if view == "main_frame":
            self.main_frame.grid(row=0, column=1, rowspan=3, sticky="news")
            self.select_paper_frame.grid_forget()
            self.quantity_frame.grid_forget()
            self.done_frame.grid_forget()
            self.prev_button.configure(state="disabled")
            self.sidebar_button_1.configure(fg_color="#453ad6")
            self.sidebar_button_2.configure(fg_color="#1f6aa5")
            self.sidebar_button_3.configure(fg_color="#1f6aa5")
            self.sidebar_button_4.configure(fg_color="#1f6aa5")
        elif view == "select_paper_frame":
            self.main_frame.grid_forget()
            self.select_paper_frame.grid(row=0, column=1, rowspan=3, sticky="news")
            self.quantity_frame.grid_forget()
            self.done_frame.grid_forget()
            self.prev_button.configure(state="normal")
            self.sidebar_button_1.configure(fg_color="#1f6aa5")
            self.sidebar_button_2.configure(fg_color="#453ad6", state="normal")
            self.sidebar_button_3.configure(fg_color="#1f6aa5")
            self.sidebar_button_4.configure(fg_color="#1f6aa5")
        elif view == "quantity_frame":
            self.main_frame.grid_forget()
            self.select_paper_frame.grid_forget()
            self.quantity_frame.grid(row=0, column=1, rowspan=3, sticky="news")
            self.done_frame.grid_forget()
            self.sidebar_button_1.configure(fg_color="#1f6aa5")
            self.sidebar_button_2.configure(fg_color="#1f6aa5")
            self.sidebar_button_3.configure(fg_color="#453ad6", state="normal")
            self.sidebar_button_4.configure(fg_color="#1f6aa5")
        elif view == "done_frame":
            self.main_frame.grid_forget()
            self.select_paper_frame.grid_forget()
            self.quantity_frame.grid_forget()
            self.done_frame.grid(row=0, column=1, rowspan=3, sticky="news")
            self.sidebar_button_1.configure(fg_color="#1f6aa5", state="disabled")
            self.sidebar_button_2.configure(fg_color="#1f6aa5", state="disabled")
            self.sidebar_button_3.configure(fg_color="#1f6aa5", state="disabled")
            self.sidebar_button_4.configure(fg_color="#453ad6", state="disabled")

            self.prev_button.configure(state="disabled")

            self.start_stop()


    def _change_active_view_by_index(self, index):
        self.change_active_view(self.views[index])
    
    def _display_back(self):
        if self.display_index == 0:
            return
        self.display_index -= 1
        self._change_active_view_by_index(self.display_index)

    def _display_next(self):
        if self.display_index == len(self.views) - 1:
            return
        self.display_index += 1
        self._change_active_view_by_index(self.display_index)   
    
    def start_stop(self):
        if not self.is_running:
            # Get end time
            self.end_time = datetime.now() + timedelta(seconds=4)  # Example: 10 seconds countdown
            self.is_running = True
            self.update_countdown()
        else:
            self.is_running = False

    def update_countdown(self):
        if self.is_running:
            now = datetime.now()
            time_left = self.end_time - now
            if time_left > timedelta(0):
                # Format time remaining
                minutes, seconds = divmod(time_left.seconds, 60)
                hours, minutes = divmod(minutes, 60)
                # time_str = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
                time_str = f"Please wait {seconds:02d} seconds"
                self.countdown_label.configure(text=time_str)
                self.after(1000, self.update_countdown)  # Update every second
            else:
                self.is_running = False
                self.reset()
                self.countdown_label.configure(text="00:00:00")