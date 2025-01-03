import tkinter as tk
from tkinter import filedialog, messagebox
from Stenography import *


class SteganographyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Steganography App")
        self.root.geometry("500x500")

        # Title
        self.title = tk.Label(root, text="Steganography Application", font=("Arial", 16))
        self.title.pack(pady=20)

        # Steganography options
        self.create_widgets()

    def create_widgets(self):
        # Text Steganography
        self.text_button = tk.Button(self.root, text="Text Steganography", command=self.text_steganography)
        self.text_button.pack(pady=10)

        # Image Steganography
        self.image_button = tk.Button(self.root, text="Image Steganography", command=self.image_steganography)
        self.image_button.pack(pady=10)

        # Audio Steganography
        self.audio_button = tk.Button(self.root, text="Audio Steganography", command=self.audio_steganography)
        self.audio_button.pack(pady=10)

        # Video Steganography
        self.video_button = tk.Button(self.root, text="Video Steganography", command=self.video_steganography)
        self.video_button.pack(pady=10)

    # Text Steganography
    def text_steganography(self):
        text_window = tk.Toplevel(self.root)
        text_window.title("Text Steganography")
        text_window.geometry("400x300")

        def encode_text():
            # Input message when encode button is pressed
            message = tk.simpledialog.askstring("Input", "Enter the message to encode:")
            cover_text = filedialog.askopenfilename(title="Select Cover Text File", filetypes=[("Text Files", "*.txt")])
            output_file = filedialog.asksaveasfilename(title="Save Stego Text File", filetypes=[("Text Files", "*.txt")])

            if message and cover_text and output_file:
                TextSteganography.txt_encode(message, cover_text, output_file)
                messagebox.showinfo("Success", "Text successfully encoded!")

        def decode_text():
            stego_text = filedialog.askopenfilename(title="Select Stego Text File", filetypes=[("Text Files", "*.txt")])
            if stego_text:
                message = TextSteganography.decode_txt_data(stego_text)
                messagebox.showinfo("Decoded Message", f"Decoded Message: {message}")

        tk.Button(text_window, text="Encode", command=encode_text).pack(pady=10)
        tk.Button(text_window, text="Decode", command=decode_text).pack(pady=10)

    # Image Steganography
    def image_steganography(self):
        image_window = tk.Toplevel(self.root)
        image_window.title("Image Steganography")
        image_window.geometry("400x300")

        def encode_image():
            # Input message when encode button is pressed
            message = tk.simpledialog.askstring("Input", "Enter the message to encode:")
            cover_image = filedialog.askopenfilename(title="Select Cover Image", filetypes=[("Image Files", "*.png *.jpg")])
            output_image = filedialog.asksaveasfilename(title="Save Stego Image", filetypes=[("Image Files", "*.png *.jpg")])

            if message and cover_image and output_image:
                ImageSteganography.encode_image(cover_image, message, output_image)
                messagebox.showinfo("Success", "Image successfully encoded!")

        def decode_image():
            stego_image = filedialog.askopenfilename(title="Select Stego Image", filetypes=[("Image Files", "*.png *.jpg")])
            if stego_image:
                message = ImageSteganography.decode_image(stego_image)
                messagebox.showinfo("Decoded Message", f"Decoded Message: {message}")

        tk.Button(image_window, text="Encode", command=encode_image).pack(pady=10)
        tk.Button(image_window, text="Decode", command=decode_image).pack(pady=10)

    # Audio Steganography
    def audio_steganography(self):
        audio_window = tk.Toplevel(self.root)
        audio_window.title("Audio Steganography")
        audio_window.geometry("400x300")

        def encode_audio():
            # Input message when encode button is pressed
            message = tk.simpledialog.askstring("Input", "Enter the message to encode:")
            cover_audio = filedialog.askopenfilename(title="Select Cover Audio", filetypes=[("WAV Files", "*.wav")])
            output_audio = filedialog.asksaveasfilename(title="Save Stego Audio", filetypes=[("WAV Files", "*.wav")])

            if message and cover_audio and output_audio:
                AudioSteganography.encode_audio(cover_audio, message, output_audio)
                messagebox.showinfo("Success", "Audio successfully encoded!")

        def decode_audio():
            stego_audio = filedialog.askopenfilename(title="Select Stego Audio", filetypes=[("WAV Files", "*.wav")])
            if stego_audio:
                message = AudioSteganography.decode_audio(stego_audio)
                messagebox.showinfo("Decoded Message", f"Decoded Message: {message}")

        tk.Button(audio_window, text="Encode", command=encode_audio).pack(pady=10)
        tk.Button(audio_window, text="Decode", command=decode_audio).pack(pady=10)

    # Video Steganography
    def video_steganography(self):
        video_window = tk.Toplevel(self.root)
        video_window.title("Video Steganography")
        video_window.geometry("400x300")

        def encode_video():
            # Input message and key when encode button is pressed
            message = tk.simpledialog.askstring("Input", "Enter the message to encode:")
            key = tk.simpledialog.askstring("Input", "Enter the encryption key:")
            cover_video = filedialog.askopenfilename(title="Select Cover Video", filetypes=[("Video Files", "*.mp4")])
            output_video = filedialog.asksaveasfilename(title="Save Stego Video", filetypes=[("Video Files", "*.mp4")])

            if message and cover_video and output_video:
                VideoSteganography().encode_video(cover_video, key, output_video)
                messagebox.showinfo("Success", "Video successfully encoded!")

        def decode_video():
            stego_video = filedialog.askopenfilename(title="Select Stego Video", filetypes=[("Video Files", "*.mp4")])
            key = tk.simpledialog.askstring("Input", "Enter the decryption key:")

            if stego_video and key:
                message = VideoSteganography().decode_video(stego_video, key)
                messagebox.showinfo("Decoded Message", f"Decoded Message: {message}")

        tk.Button(video_window, text="Encode", command=encode_video).pack(pady=10)
        tk.Button(video_window, text="Decode", command=decode_video).pack(pady=10)


if __name__ == "__main__":
    root = tk.Tk()
    app = SteganographyApp(root)
    root.mainloop()
