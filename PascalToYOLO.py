import os
import tkinter as tk
from tkinter import filedialog, messagebox
import xml.etree.ElementTree as ET


def convert_bbox_to_yolo(size, box):
    """
    size: (width, height) obrazu
    box: (xmin, ymin, xmax, ymax) w pikselach (Pascal VOC)

    Zwraca krotkę (x_center, y_center, w, h) w formacie YOLO
    - wszystkie wartości znormalizowane (od 0 do 1)
    """
    w_img, h_img = size
    xmin, ymin, xmax, ymax = box

    x_center = (xmin + xmax) / 2.0
    y_center = (ymin + ymax) / 2.0
    w = xmax - xmin
    h = ymax - ymin

    # Normalizacja (dzielenie przez wymiary obrazu)
    x_center /= w_img
    y_center /= h_img
    w /= w_img
    h /= h_img

    return (x_center, y_center, w, h)


def convert_pascal_to_yolo(pascal_dir, yolo_dir, classes_list):
    """
    Iteruje po wszystkich plikach .xml w folderze pascal_dir,
    konwertuje je do formatu YOLO i zapisuje w folderze yolo_dir.

    :param pascal_dir: ścieżka do folderu z plikami .xml (Pascal VOC)
    :param yolo_dir:   ścieżka do folderu, gdzie zapiszemy pliki .txt (YOLO)
    :param classes_list: lista klas (np. ["class1", "class2", "class3", ...])
    """
    if not os.path.exists(yolo_dir):
        os.makedirs(yolo_dir)

    # Pobranie listy plików XML
    xml_files = [f for f in os.listdir(pascal_dir) if f.endswith(".xml")]

    for xml_file in xml_files:
        xml_path = os.path.join(pascal_dir, xml_file)

        try:
            tree = ET.parse(xml_path)
        except ET.ParseError:
            print(f"[WARN] XML parsing error in file: {xml_file}")
            continue

        root = tree.getroot()

        # Odczyt wymiarów obrazu
        size_tag = root.find("size")
        if size_tag is None:
            print(f"[WARN] No tag <size> in file: {xml_file}. I'm skipping it.")
            continue

        width = int(size_tag.find("width").text)
        height = int(size_tag.find("height").text)

        # Nazwa pliku wyjściowego
        base_name = os.path.splitext(xml_file)[0]
        txt_file_path = os.path.join(yolo_dir, base_name + ".txt")

        # Otwarcie pliku do zapisu
        with open(txt_file_path, "w", encoding="utf-8") as txt_file:
            # Wyszukiwanie obiektów (tag <object>)
            for obj in root.findall("object"):
                class_name = obj.find("name").text

                # Jeżeli klasa nie jest w naszym spisie, pomijamy
                if class_name not in classes_list:
                    continue

                class_id = classes_list.index(class_name)

                # Pobranie współrzędnych bounding box
                bndbox = obj.find("bndbox")
                xmin = float(bndbox.find("xmin").text)
                ymin = float(bndbox.find("ymin").text)
                xmax = float(bndbox.find("xmax").text)
                ymax = float(bndbox.find("ymax").text)

                # Konwersja do formatu YOLO
                x_center, y_center, w, h = convert_bbox_to_yolo(
                    (width, height),
                    (xmin, ymin, xmax, ymax)
                )

                # Zapis do pliku w formacie:
                #   class_id x_center y_center w h
                txt_file.write(
                    f"{class_id} {x_center:.6f} {y_center:.6f} {w:.6f} {h:.6f}\n"
                )

        print(f"[INFO] Created: {txt_file_path}")

    print("[INFO] Conversion completed!")


class App:
    def __init__(self, master):
        self.master = master
        self.master.title("Konwerter Pascal VOC -> YOLO")

        # Zmienna przechowująca ścieżkę do folderu z plikami .xml
        self.pascal_dir = ""
        # Zmienna przechowująca ścieżkę do folderu docelowego
        self.yolo_dir = ""

        # --- Sekcja wyboru folderu z plikami XML ---
        self.label_pascal = tk.Label(self.master, text="Folder with .xml (Pascal VOC):")
        self.label_pascal.grid(row=0, column=0, padx=10, pady=5, sticky="e")

        self.entry_pascal = tk.Label(self.master, text="(not selected)")
        self.entry_pascal.grid(row=0, column=1, padx=10, pady=5, sticky="w")

        self.btn_pascal = tk.Button(self.master, text="Wybierz folder", command=self.choose_pascal_folder)
        self.btn_pascal.grid(row=0, column=2, padx=10, pady=5)

        # --- Sekcja wyboru folderu wyjściowego ---
        self.label_yolo = tk.Label(self.master, text="Destination folder (YOLO):")
        self.label_yolo.grid(row=1, column=0, padx=10, pady=5, sticky="e")

        self.entry_yolo = tk.Label(self.master, text="(not selected)")
        self.entry_yolo.grid(row=1, column=1, padx=10, pady=5, sticky="w")

        self.btn_yolo = tk.Button(self.master, text="Select folder", command=self.choose_yolo_folder)
        self.btn_yolo.grid(row=1, column=2, padx=10, pady=5)

        # --- Sekcja wpisania listy klas ---
        self.label_classes = tk.Label(self.master, text="List of classes (comma separated):")
        self.label_classes.grid(row=2, column=0, padx=10, pady=5, sticky="e")

        self.entry_classes = tk.Entry(self.master, width=50)
        self.entry_classes.insert(0, "class1, class2, class3")  # przykładowe klasy
        self.entry_classes.grid(row=2, column=1, padx=10, pady=5, columnspan=2, sticky="w")

        # --- Przycisk konwersji ---
        self.btn_convert = tk.Button(self.master, text="Convert", command=self.convert_action, bg="lightgreen")
        self.btn_convert.grid(row=3, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")

    def choose_pascal_folder(self):
        folder_selected = filedialog.askdirectory(title="Select the folder with files .xml")
        if folder_selected:
            self.pascal_dir = folder_selected
            self.entry_pascal.config(text=self.pascal_dir)

    def choose_yolo_folder(self):
        folder_selected = filedialog.askdirectory(title="Select destination folder (.txt)")
        if folder_selected:
            self.yolo_dir = folder_selected
            self.entry_yolo.config(text=self.yolo_dir)

    def convert_action(self):
        # Sprawdzamy, czy użytkownik wybrał oba foldery
        if not self.pascal_dir or not self.yolo_dir:
            messagebox.showwarning("No path", "Select both folders before conversion!")
            return

        # Pobranie listy klas – rozdzielamy po przecinku
        raw_classes = self.entry_classes.get()
        if not raw_classes.strip():
            messagebox.showwarning("No classes", "Please enter at least one class.")
            return

        classes_list = [cls.strip() for cls in raw_classes.split(",") if cls.strip()]

        if not classes_list:
            messagebox.showwarning("No classes", "Please enter at least one class.")
            return

        try:
            convert_pascal_to_yolo(self.pascal_dir, self.yolo_dir, classes_list)
            messagebox.showinfo("Success", "Conversion completed!")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred:\n{e}")


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
