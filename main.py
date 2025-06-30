import tkinter as tk
from PIL import Image, ImageTk
import os
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# ------------ Setup Window ------------
root = tk.Tk()
root.title("Our Rorschach Test: An invitation to the Mindpool")
root.geometry("700x720")

image_paths = [f"images/{i}.png" for i in range(1, 11)]
images = []
current_index = 0
responses = []

# ------------ Clear Window Helper ------------
def clear_window():
    for widget in root.winfo_children():
        widget.destroy()

# ------------ First Page ------------
def first_page():
    clear_window()
    title_label = tk.Label(
        root,
        text="Our Rorschach Test: An invitation to the Mindpool",
        font=("Helvetica", 16, "bold"),
        wraplength=550,
        justify="center"
    )
    title_label.pack(pady=100)

    reflect_button = tk.Button(
        root,
        text="Reflect",
        font=("Helvetica", 12, "bold"),
        command=second_page
    )
    reflect_button.pack()

# ------------ Second Page ------------
def second_page():
    clear_window()

    # Add some space at the top
    tk.Label(root, text="", height=2).pack()

    description = (
        "Mindpool believes in the relevance of self-reflection and BEYOND IT by autonomously applying meta-methodologies to explore who we feel and think we are.\n\n"
        "We are more than others perceive of us, but also a lot more than what we appear to be, even to ourselves.\n\n"
        "This test uses public domain images based on research by Hermann Rorschach himself. "
        "It is us, looking at him, looking at you, as you see yourself through all those layers of deep reflection."
    )

    description_label = tk.Label(
        root,
        text=description,
        wraplength=550,
        justify="left",
        font=("Helvetica", 12)
    )
    description_label.pack(pady=(50, 60))  # Increased vertical padding

    dive_button = tk.Button(
        root,
        text="Dive in",
        font=("Helvetica", 12, "bold"),
        command=third_page
    )
    dive_button.pack()

# ------------ Third Page (Images) ------------
def third_page():
    global images, current_index, responses
    clear_window()
    current_index = 0
    responses = []
    images.clear()

    for path in image_paths:
        if os.path.exists(path):
            img = Image.open(path).resize((400, 400))
            images.append(ImageTk.PhotoImage(img))
        else:
            print(f"Image not found: {path}")

    if not images:
        tk.Label(root, text="No images found in /images/ folder.").pack()
        return

    show_image()

def show_image():
    global current_index
    clear_window()

    if current_index >= len(images):
        show_results()
        return

    img_label = tk.Label(root, image=images[current_index])
    img_label.image = images[current_index]
    img_label.pack(pady=10)

    prompt = (
        "Take a moment to reflect on this image. 1, 2, 3, 4, 5... Breathe.\n\n"
        "Now about the image, describe what you saw:"
    )
    prompt_label = tk.Label(root, text=prompt, font=("Helvetica", 12), wraplength=550, justify="left")
    prompt_label.pack(pady=(20, 10))

    options = {
        "A": "A: I saw something in the whole image, as one complete shape.",
        "B": "B: I focused on the tinted, main part of the inkblot.",
        "C": "C: I noticed a small or unusual detail hidden in the blot.",
        "D": "D: I interpreted the white space or background around the blot."
    }

    for key, label in options.items():
        tk.Button(
            root,
            text=label,
            font=("Helvetica", 11),
            wraplength=500,
            anchor="w",
            justify="left",
            width=50,
            command=lambda k=key: next_image(k)
        ).pack(pady=4)

def next_image(response):
    global current_index, responses
    responses.append(response)
    current_index += 1
    show_image()

# ------------ Interpretation ------------
def interpret_results(result_counts):
    max_val = max(result_counts.values())
    dominant = [k for k, v in result_counts.items() if v == max_val]

    messages = {
        "A": "You are a global thinker: You perceive the whole before the parts. You are likely to synthesize, dream, and seek unity.",
        "B": "You focus on core elements. You bring order and logic to your perception, seeing what matters most, first.",
        "C": "You are tuned to detail. You notice the subtle, the rare, the hidden patterns others often miss.",
        "D": "You find meaning in what surrounds — in context, emptiness, the unsaid. You dance with ambiguity and background."
    }

    if len(dominant) == 1:
        letter = dominant[0]
        return f"Your dominant type: {letter}\n\n{messages[letter]}"
    else:
        title = "You showed a tie between: " + ", ".join(dominant)
        explanation = "\n\n".join([messages[d] for d in dominant])
        return f"{title}\n\n{explanation}"

# ------------ Results Page ------------
def show_results():
    clear_window()

    result_counts = {"A": 0, "B": 0, "C": 0, "D": 0}
    for r in responses:
        if r in result_counts:
            result_counts[r] += 1

    x = result_counts["A"] - result_counts["B"]
    y = result_counts["D"] - result_counts["C"]

    fig, ax = plt.subplots(figsize=(5, 4.5))
    ax.axhline(0, color='gray', linewidth=1)
    ax.axvline(0, color='gray', linewidth=1)
    ax.set_xlim(-10, 10)
    ax.set_ylim(-10, 10)
    ax.scatter(x, y, color='purple', s=100)
    ax.set_title("Mindpool Rorschach Map", fontsize=14)

    ax.text(5, 9, "Imaginative + Global", fontsize=9, ha='center')
    ax.text(-5, 9, "Imaginative + Detail", fontsize=9, ha='center')
    ax.text(-5, -9, "Concrete + Detail", fontsize=9, ha='center')
    ax.text(5, -9, "Concrete + Global", fontsize=9, ha='center')

    plt.tight_layout()
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()
    canvas.get_tk_widget().pack(pady=20)

    interpretation = interpret_results(result_counts)
    tk.Label(root, text=interpretation, font=("Helvetica", 11), wraplength=600, justify="left").pack(pady=(5, 10))

    tk.Button(root, text="Restart", font=("Helvetica", 12, "bold"), command=first_page).pack(pady=10)

# ------------ Start App ------------
first_page()
root.mainloop()

