import tkinter as tk
from tkinter import ttk
from tkinter import filedialog

class FatihKalem:
    def __init__(self, root):
        self.root = root
        self.root.title("Tuvalim")
        self.root.config(bg="#23232f")

        # Ana çizim tuvali
        self.canvas = tk.Canvas(root, bg="white", width=500, height=500)
        self.canvas.pack(side="left", expand="YES", fill="both")
        self.canvas.configure(bg="#636363")

        # Sağ tarafındaki kontrol alanı
        self.kontrol_frame = tk.Frame(root, bg="#23232f")
        self.kontrol_frame.pack(side="right", fill="y", padx=10)

        # Mod seçenekleri
        modlar = ["Kalem", "Daire", "Kare", "Silgi"]
        self.mod_combobox = ttk.Combobox(self.kontrol_frame, values=modlar, state="readonly", font=("Comic Sans MS", 10, "bold"))
        self.mod_combobox.set(modlar[0])
        self.mod_combobox.pack(pady=10)
        self.mod_combobox.bind("<<ComboboxSelected>>", lambda event: self.araclari_sec())

        # Clear butonu
        self.clear_button = tk.Button(self.kontrol_frame, text="Clear", command=self.temizle, bg="#23232f", fg="#fcf", font=("Comic Sans MS", 10, "bold"))
        self.clear_button.pack(pady=10)

        # Kalem boyutu slider
        self.kalem_boyutu_slider = tk.Scale(self.kontrol_frame, from_=1, to=10, orient="horizontal", label="Kalem Boyutu", length=200, command=self.kalem_boyutu, bg="#23232f", fg="#fcf", font=("Comic Sans MS", 10, "bold"))
        self.kalem_boyutu_slider.pack(pady=10)
        self.kalem_boyutu_slider.set(2)

        self.aktif_arac = "kalem"
        self.holding = False
        self.start_x = None
        self.start_y = None
        self.kalem_renk = "black"
        self.kalem_boyut = 2
                # Menu Bar
        menubar = tk.Menu(root)
        root.config(menu=menubar)


        self.canvas.bind("<Button-1>", self.baslangic_konum)
        self.canvas.bind("<B1-Motion>", self.cizim)
        self.canvas.bind("<ButtonRelease-1>", self.cizimi_bitir)
        # File Menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Save", command=self.save_canvas)

    def save_canvas(self):
        file_path = filedialog.asksaveasfilename(title="Kaydet | YK Tuvalim",defaultextension="*.ykt", filetypes=[("PNG Resim Dosyası", "*.png"),  ("YK Tuval Dosyası", "*.ykt"),("Tüm Dosyalar", "*.*")])
        
        if file_path:
            try:
                self.canvas.postscript(file=file_path, colormode='color')
                print(f"Canvas saved to {file_path}")
            except Exception as e:
                print(f"Error saving canvas: {e}")
    
    def araclari_sec(self):
        arac = self.mod_combobox.get()
        if arac in ["Kalem", "Daire", "Kare", "Silgi"]:
            self.aktif_arac = arac
        print("Aktif Araç:", self.aktif_arac)

    def baslangic_konum(self, event):
        self.start_x = event.x
        self.start_y = event.y
        self.holding = True

    def cizim(self, event):
        if self.holding:
            current_x = event.x
            current_y = event.y

            if self.aktif_arac == "Kalem" and self.start_x is not None and self.start_y is not None:
                self.canvas.create_line(self.start_x, self.start_y, current_x, current_y, fill=self.kalem_renk, width=self.kalem_boyut)
                self.start_x = current_x
                self.start_y = current_y
            elif self.aktif_arac == "Silgi" and self.start_x is not None and self.start_y is not None:
                self.canvas.create_line(self.start_x, self.start_y, current_x, current_y, fill="#636363", width=self.kalem_boyut)
                self.start_x = current_x
                self.start_y = current_y
            elif self.aktif_arac in ["Daire", "Kare"]:
                if self.start_x is not None and self.start_y is not None:
                    self.canvas.delete("temp_shape")
                if self.aktif_arac == "Daire":
                    self.canvas.create_oval(self.start_x, self.start_y, current_x, current_y, outline=self.kalem_renk, width=self.kalem_boyut, tags="temp_shape")
                elif self.aktif_arac == "Kare":
                    self.canvas.create_rectangle(self.start_x, self.start_y, current_x, current_y, outline=self.kalem_renk, width=self.kalem_boyut, tags="temp_shape")

    def cizimi_bitir(self, event):
        if self.start_x is not None and self.start_y is not None:
            self.canvas.delete("temp_shape")
            current_x = event.x
            current_y = event.y
            if self.aktif_arac == "Daire":
                self.canvas.create_oval(self.start_x, self.start_y, current_x, current_y, outline=self.kalem_renk, width=self.kalem_boyut)
            elif self.aktif_arac == "Kare":
                self.canvas.create_rectangle(self.start_x, self.start_y, current_x, current_y, outline=self.kalem_renk, width=self.kalem_boyut)
        self.start_x = None
        self.start_y = None
        self.holding = False

    def temizle(self):
        print("Clear")
        self.canvas.delete("all")

    def kalem_boyutu(self, value):
        print("Kalem Boyutu:", value)
        self.kalem_boyut = int(value)
class EditorMenu:
    def __init__(self, mwindow):
        self.mwindow = mwindow
        self.mwindow.title("Yutupn Kedisi | Tuvalim 0.5")
        self.mwindow.geometry("600x500")
        self.mwindow.resizable(False, False)
        self.mwindow.config(bg="#23232f")
        
        # Create a button
        new_tuval_button = tk.Button(self.mwindow, text="Yeni Tuval", bg="#23232f", fg="#ffffff", command=self.create_tuval, font=("Comic Sans MS", 10, "bold"))
        label_text = "YK Tuval | Versiyon = 0.5 \n :3 Kanalıma Abone Oy :3 \n Daha Çok Program İstiyorsanız... Yaparım ;3\n Kullandığınız İçin Teşekküerler "
        Label1 = tk.Label(self.mwindow, text=label_text, bg="#23232f", fg="#fcf", font=("Comic Sans MS", 10, "bold"))

        # Pack the button and label
        new_tuval_button.pack()
        Label1.pack()

    def create_tuval(self):
        tuval = tk.Tk()
        self.mwindow.destroy()
        tuval.title("Yeni Tuval")
        tuval_new = FatihKalem(tuval)
        tuval.mainloop()

if __name__ == "__main__":
    menued = tk.Tk()
    MenuMain = EditorMenu(menued)
    menued.mainloop()

