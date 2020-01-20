from tkinter import filedialog as fd


def browse_img():
    while True:
        pname = fd.askopenfilename(
            filetypes=[("Image format", ".tif .tiff .jpg .jpeg .gif .png .bmp .eps .raw .cr2 .nef .orf .sr2")])
        if pname is not None:
            break
    return pname
