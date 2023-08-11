import unittest
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import filedialog
import numpy as np
import threading

class LoginWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Login")

        # Set the initial window size
        self.root.geometry("400x400")  # Adjusted height to accommodate the rectangles

        # Set the background color of the login window
        self.root.configure(bg="#55a630")  # Green background color

        # Create a rectangle shape for the login form
        login_frame = tk.Frame(root, bg="#ffffff", width=350, height=200)
        login_frame.pack(pady=20)
        login_frame.pack_propagate(False)

        # Add the application title outside the login form
        title_label = tk.Label(root, text="Voting Cryptography", font=("Helvetica", 16, "bold"), bg="#55a630", fg="#ffffff")
        title_label.pack(fill="x", pady=(10, 0))

        # Font settings
        font = ("Helvetica", 12)

        self.username_label = tk.Label(login_frame, text="Username:", bg="#ffffff", font=font)
        self.username_label.pack(anchor="w", padx=10, pady=(20, 0))  # Position the label

        self.username_entry = tk.Entry(login_frame, font=font)
        self.username_entry.pack(fill="x", padx=10, pady=5)  # Position the entry

        self.password_label = tk.Label(login_frame, text="Password:", bg="#ffffff", font=font)
        self.password_label.pack(anchor="w", padx=10)  # Position the label

        self.password_entry = tk.Entry(login_frame, show="*", font=font)
        self.password_entry.pack(fill="x", padx=10, pady=(0, 20))  # Position the entry

        self.login_button = tk.Button(login_frame, text="Login", command=self.login, bg="#55a630", fg="white", font=font)
        self.login_button.pack(pady=(0, 10))  # Position the button

        # Create two rectangles at the bottom
        self.rectangle1 = tk.Label(root, bg="#a0c8e0", height=2)
        self.rectangle1.pack(fill="x", side="bottom")

        self.rectangle2 = tk.Label(root, bg="#a0c8e0", height=2)
        self.rectangle2.pack(fill="x", side="bottom")

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        # Perform authentication (add your authentication logic here)
        if username == "admin" and password == "password":
            self.root.withdraw()  # Hide the login window
            self.open_main_window()
        else:
            tk.messagebox.showerror("Login Failed", "Invalid username or password")

    def open_main_window(self):
        main_window = tk.Toplevel(self.root)
        app = VisualCryptographyApp(main_window)
        main_window.configure(bg="#a0c8e0")  # Light blue background color

class VisualCryptographyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Visual Cryptography App")

        self.selected_image = None
        self.share1_image = None
        self.share2_image = None
        self.combine_image = None
        self.combined_image = None

        self.image_label = tk.Label(root)
        self.image_label.pack()

        self.select_button = tk.Button(root, text="Select Image", command=self.select_image)
        self.select_button.pack()

        self.generate_button = tk.Button(root, text="Generate Shares", command=self.generate_shares)
        self.generate_button.pack()

        self.save_button = tk.Button(root, text="Save Shares", command=self.save_shares)
        self.save_button.pack()

        self.combine_label = tk.Label(root, text="Combine Shares", font=("Helvetica", 14), bg="#a0c8e0")
        self.combine_label.pack()

        self.combine_button = tk.Button(root, text="Select Image for Combining", command=self.select_combine_image)
        self.combine_button.pack()

        self.combine_shares_button = tk.Button(root, text="Combine Shares", command=self.combine_shares)
        self.combine_shares_button.pack()

        self.update_image_display(Image.new("RGB", (200, 200)))  # Default image for display size

    def select_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png *.jpg *.jpeg *.bmp")])
        if file_path:
            self.selected_image = Image.open(file_path)
            self.update_image_display(self.selected_image)

    def generate_shares(self):
        if self.selected_image is not None:
            secret_array = np.array(self.selected_image)
            share1, share2 = self.generate_shares_helper(secret_array)

            self.share1_image = Image.fromarray(share1.astype('uint8') * 255)
            self.share2_image = Image.fromarray(share2.astype('uint8') * 255)

            self.combined_image = None

            self.update_image_display(self.share1_image)

    def generate_shares_helper(self, secret_array):
        share1 = np.random.randint(0, 2, secret_array.shape)
        share2 = secret_array ^ share1
        return share1, share2

    def save_shares(self):
        if self.share1_image is not None and self.share2_image is not None:
            share1_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
            if share1_path:
                self.share1_image.save(share1_path)

            share2_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
            if share2_path:
                self.share2_image.save(share2_path)

    def select_combine_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png *.jpg *.jpeg *.bmp")])
        if file_path:
            self.combine_image = Image.open(file_path)
            self.update_image_display(self.combine_image)

    def combine_shares(self):
        if self.combine_image is not None and self.share1_image is not None and self.share2_image is not None:
            combine_array = np.array(self.combine_image)
            share1_array = np.array(self.share1_image)
            share2_array = np.array(self.share2_image)
            combined_array = (share1_array & combine_array) | (share2_array & ~combine_array)

            self.combined_image = Image.fromarray(combined_array.astype('uint8') * 255)
            self.update_image_display(self.combined_image)

    def update_image_display(self, new_image):
        new_image.thumbnail((400, 400))  # Resize the image for proper display
        new_image_tk = ImageTk.PhotoImage(new_image)
        self.image_label.config(image=new_image_tk)
        self.image_label.image = new_image_tk

class TestVisualCryptographyApp(unittest.TestCase):
    def setUp(self):
        self.root = tk.Tk()
        self.app = VisualCryptographyApp(self.root)

    def test_select_image(self):
        self.app.select_image()
        self.assertIsNotNone(self.app.selected_image)

    def test_generate_shares(self):
        self.app.selected_image = Image.new("RGB", (200, 200))  # Create a dummy image for testing
        self.app.generate_shares()
        self.assertIsNotNone(self.app.share1_image)
        self.assertIsNotNone(self.app.share2_image)

    def test_combine_shares(self):
        self.app.selected_image = Image.new("RGB", (200, 200))  # Create a dummy image for testing
        self.app.generate_shares()
        self.app.combine_image = Image.new("RGB", (200, 200))   # Create a dummy combine image for testing
        self.app.combine_shares()
        self.assertIsNotNone(self.app.combined_image)

def run_tests():
    unittest.TextTestRunner().run(unittest.TestLoader().loadTestsFromTestCase(TestVisualCryptographyApp))

def run_gui():
    login_root = tk.Tk()
    login_app = LoginWindow(login_root)
    login_root.mainloop()

if __name__ == "__main__":
    gui_thread = threading.Thread(target=run_gui)
    gui_thread.start()

    # Run tests after GUI thread starts
    run_tests()

    # Join the GUI thread to wait for it to finish before exiting
    gui_thread.join()