import numpy as np
from PIL import Image
from scipy.fft import dct, idct
import tkinter as tk
from tkinter import filedialog, messagebox
import os


def crea_bloc(image, block_size=8):
    h, w = image.shape
    blocks = []
    for i in range(0, h, block_size):
        for j in range(0, w, block_size):
            block = image[i:i + block_size, j:j + block_size]
            blocks.append(block)
    return blocks


def dct2(block):
    return dct(dct(block.T, norm='ortho').T, norm='ortho')


def idct2(block):
    return idct(idct(block.T, norm='ortho').T, norm='ortho')


def reconstruct_image(blocks, width, height, block_size=8):
    image = np.zeros((height, width), dtype=np.float32)
    index = 0
    for i in range(0, height, block_size):
        for j in range(0, width, block_size):
            image[i:i + block_size, j:j + block_size] = blocks[index]
            index += 1
    return image


def compress_image(input_path, output_path):
    img = Image.open(input_path).convert("L")
    img.save(output_path, "JPEG", quality=50)
    messagebox.showinfo("Compression réussie", f"L'image compressée a été enregistrée sous :\n{output_path}")


def restore_image(input_path, output_path):
    img = Image.open(input_path).convert("L")
    img_array = np.array(img, dtype=np.float32)

    blocks = crea_bloc(img_array)
    restored_blocks = []

    for block in blocks:
        dct_block = dct2(block)
        restored_block = idct2(dct_block)
        restored_blocks.append(restored_block)

    restored_image = reconstruct_image(restored_blocks, img_array.shape[1], img_array.shape[0])
    restored_image = np.clip(restored_image, 0, 255).astype(np.uint8)

    Image.fromarray(restored_image).save(output_path)
    messagebox.showinfo("Restauration réussie", f"L'image restaurée a été enregistrée sous :\n{output_path}")


def main():
    root = tk.Tk()
    root.withdraw()

    action = messagebox.askquestion("Action", "Voulez-vous compresser une image ?\nNon pour restaurer une image.")

    if action == "yes":
        input_path = filedialog.askopenfilename(title="Sélectionnez une image à compresser", filetypes=[("Fichiers images", "*.jpg *.jpeg *.png")])
        if not input_path:
            return

        base_name = os.path.splitext(os.path.basename(input_path))[0]
        output_path = os.path.join(os.path.dirname(input_path), f"{base_name}_compress.jpg")

        compress_image(input_path, output_path)
    else:
        input_path = filedialog.askopenfilename(title="Sélectionnez une image à restaurer", filetypes=[("Fichiers images", "*.jpg *.jpeg")])
        if not input_path:
            return

        base_name = os.path.splitext(os.path.basename(input_path))[0].replace("_compress", "")
        output_path = os.path.join(os.path.dirname(input_path), f"{base_name}_restaure.jpg")

        restore_image(input_path, output_path)


if __name__ == "__main__":
    main()
