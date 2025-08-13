import tkinter as tk
from tkinter import messagebox
import sqlite3

def create_db():
    conn = sqlite3.connect("nilai_siswa.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS nilai_siswa (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nama_siswa TEXT NOT NULL,
            biologi INTEGER NOT NULL,
            fisika INTEGER NOT NULL,
            inggris INTEGER NOT NULL,
            prediksi_fakultas TEXT NOT NULL      
        )
    """)
    conn.commit()
    conn.close()

create_db()

def prediksi_fakultas(biologi, fisika, inggris):
    if biologi > fisika and biologi > inggris:
        return "Kedokteran"
    elif fisika > biologi and fisika > inggris:
        return "Teknik"
    elif inggris > biologi and inggris > fisika:
        return "Bahasa"
    else:
        return "Tidak Dapat Ditentukan"
    
def submit_nilai():
    nama = entry_nama.get().strip()
    try:
        bio = int(entry_bio.get())
        fis = int(entry_fis.get())
        ing = int(entry_ing.get())
    except ValueError:
        messagebox.showerror("Error", "Nilai harus berupa angka!")
        return
    
    if not nama:
        messagebox.showerror("Error", "Nama siswa tidak boleh kosong!")
        return
    
    hasil_prediksi = prediksi_fakultas(bio, fis, ing)

    conn = sqlite3.connect("nilai_siswa.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO nilai_siswa (nama_siswa, biologi, fisika, inggris, prediksi_fakultas)
        VALUES (?, ?, ?, ?, ?)       
    """, (nama, bio, fis, ing, hasil_prediksi))
    conn.commit()
    conn.close()

    messagebox.showinfo("Hasil Prediksi", f"Prediksi Fakultas: {hasil_prediksi}")

    entry_nama.delete(0, tk.END)
    entry_bio.delete(0, tk.END)
    entry_fis.delete(0, tk.END)
    entry_ing.delete(0, tk.END)


def on_enter(e):
        btn_submit["bg"] = "#50fa7b"
        btn_submit["fg"] = "black"

def on_leave(e):
        btn_submit["bg"] = "#44475a"
        btn_submit["fg"] = "black"


root = tk.Tk()
root.title("Prediksi Fakultas Siswa")
root.geometry("420x380")
root.configure(bg="#282a36")


title_label = tk.Label(root, text="📊 Prediksi Fakultas",
                       font=("Helvetica", 18, "bold"), fg="#ff79c6", bg="#282a36" )
title_label.pack(pady=15)

form_frame = tk.Frame(root, bg="#282a36")
form_frame.pack(pady=10)

def create_field(label_text):
    label = tk.Label(form_frame, text=label_text, fg="white", bg="#282a36", font=("Helvetica", 11))
    label.pack(pady=(5,0))
    entry = tk.Entry(form_frame, font=("Helvetica", 11),
                     bg="#44475a", fg="white", insertbackground="white", relief="flat", width=30)
    entry.pack(pady=3)
    return entry

entry_nama = create_field("Nama Siswa")
entry_bio = create_field("Nilai Biologi")
entry_fis = create_field("Nilai Fisika")
entry_ing = create_field("Nilai Inggris")


btn_submit = tk.Button(root, text="Submit Nilai", command=submit_nilai,
                       bg="#44475a", fg="black", font=("Helvetica", 12, "bold"),
                       relief="flat", width=20, height=2, cursor="hand2")
btn_submit.pack(pady=20)

btn_submit.bind("<Enter>", on_enter)
btn_submit.bind("<Leave>", on_leave)

footer_label = tk.Label(root, text="© 2025 Data Prediksi Fakultas",
                        fg="#6272a4", bg="#282a36", font=("Helvetica", 9))
footer_label.pack(side="bottom", pady=5)

root.mainloop()


