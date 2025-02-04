import tkinter as tk
from tkinter import ttk, messagebox
import random

class VTMZarUygulamasi:
    def __init__(self, root):
        self.root = root
        self.root.title("VTM v20 Zar Atıcı")
        self.root.geometry("500x600")
        self.stil_ayarla()
        self.widgetlari_olustur()
        
    def stil_ayarla(self):
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure('TButton', font=('Helvetica', 12), padding=10)
        self.style.configure('TLabel', font=('Helvetica', 11))
        self.style.configure('Title.TLabel', font=('Helvetica', 14, 'bold'))
        
    def widgetlari_olustur(self):
        # Başlık
        self.lbl_baslik = ttk.Label(self.root, text="Vampire: The Masquerade v20 Zar Atıcı", style='Title.TLabel')
        self.lbl_baslik.pack(pady=10)
        
        # Giriş Paneli
        self.frm_giris = ttk.Frame(self.root)
        self.frm_giris.pack(pady=10, fill='x', padx=20)
        
        # Zar Havuzu
        self.lbl_zar_havuzu = ttk.Label(self.frm_giris, text="Zar Havuzu:")
        self.lbl_zar_havuzu.grid(row=0, column=0, sticky='w')
        self.spn_zar_havuzu = ttk.Spinbox(self.frm_giris, from_=1, to=50, width=5)
        self.spn_zar_havuzu.grid(row=0, column=1, padx=5)
        self.spn_zar_havuzu.set(5)
        
        # Zorluk Derecesi
        self.lbl_zorluk = ttk.Label(self.frm_giris, text="Zorluk Derecesi:")
        self.lbl_zorluk.grid(row=1, column=0, sticky='w', pady=5)
        self.spn_zorluk = ttk.Spinbox(self.frm_giris, from_=2, to=10, width=5)
        self.spn_zorluk.grid(row=1, column=1, padx=5)
        self.spn_zorluk.set(6)
        
        # Kritik Seçenek
        self.lbl_kritik = ttk.Label(self.frm_giris, text="10'lar Ekstra Başarı:")
        self.lbl_kritik.grid(row=2, column=0, sticky='w', pady=5)
        self.kritik_var = tk.BooleanVar(value=True)
        self.chk_kritik = ttk.Checkbutton(self.frm_giris, variable=self.kritik_var)
        self.chk_kritik.grid(row=2, column=1)
        
        # Zar At Butonu
        self.btn_zar_at = ttk.Button(self.root, text="ZARLARI AT", command=self.zar_at)
        self.btn_zar_at.pack(pady=10)
        
        # Sonuç Paneli
        self.frm_sonuc = ttk.Frame(self.root)
        self.frm_sonuc.pack(fill='both', expand=True, padx=20)
        
        # Sonuç Gösterimi
        self.txt_sonuc = tk.Text(self.frm_sonuc, width=50, height=15, state='disabled')
        self.txt_sonuc.pack(side='left', fill='both', expand=True)
        
        # Kaydırma Çubuğu
        self.scrollbar = ttk.Scrollbar(self.frm_sonuc, orient='vertical', command=self.txt_sonuc.yview)
        self.scrollbar.pack(side='right', fill='y')
        self.txt_sonuc.configure(yscrollcommand=self.scrollbar.set)
        
        # Renk Tag'leri
        self.txt_sonuc.tag_configure('kritik', foreground='green')
        self.txt_sonuc.tag_configure('botch', foreground='red')
        self.txt_sonuc.tag_configure('baslik', font=('Helvetica', 11, 'bold'))
        
    def zar_at(self):
        try:
            zar_havuzu = int(self.spn_zar_havuzu.get())
            zorluk = int(self.spn_zorluk.get())
            kritik_extra = self.kritik_var.get()
        except ValueError:
            messagebox.showerror("Hata", "Geçersiz değer girişi!")
            return

        atilan_zarlar = []
        basarılar = 0
        birler = 0
        
        for _ in range(zar_havuzu):
            current_roll = random.randint(1, 10)
            atilan_zarlar.append(current_roll)
            
            while True:
                # Başarı ve 1'leri hesapla
                if current_roll >= zorluk:
                    basarılar += 1
                if current_roll == 1:
                    birler += 1
                
                # Kritik kontrol
                if current_roll == 10:
                    if kritik_extra:
                        basarılar += 1
                    current_roll = random.randint(1, 10)
                    atilan_zarlar.append(current_roll)
                else:
                    break
        
        # Sonuçları göster
        self.sonuc_goster(atilan_zarlar, basarılar, birler)
    
    def sonuc_goster(self, zarlar, basarılar, birler):
        self.txt_sonuc.config(state='normal')
        self.txt_sonuc.delete(1.0, tk.END)
        
        # Zarları yazdır
        self.txt_sonuc.insert(tk.END, "Atılan Zarlar:\n", 'baslik')
        for zar in zarlar:
            if zar == 10:
                self.txt_sonuc.insert(tk.END, f"{zar} ", 'kritik')
            elif zar == 1:
                self.txt_sonuc.insert(tk.END, f"{zar} ", 'botch')
            else:
                self.txt_sonuc.insert(tk.END, f"{zar} ", 'normal')
        
        # Sonuç hesaplamaları
        net_basarı = basarılar - birler
        self.txt_sonuc.insert(tk.END, "\n\nSonuçlar:\n", 'baslik')
        self.txt_sonuc.insert(tk.END, f"Toplam Başarı: {basarılar}\n")
        self.txt_sonuc.insert(tk.END, f"1'lerin Sayısı: {birler}\n")
        
        if net_basarı > 0:
            self.txt_sonuc.insert(tk.END, f"\nNet Başarı: {net_basarı}\n", 'kritik')
            self.txt_sonuc.insert(tk.END, "BAŞARILI!", 'kritik')
        elif net_basarı == 0:
            self.txt_sonuc.insert(tk.END, "\nNet Başarı: 0\n", 'botch')
            self.txt_sonuc.insert(tk.END, "BAŞARISIZ!", 'botch')
        else:
            self.txt_sonuc.insert(tk.END, "\nNet Başarı: 0\n", 'botch')
            self.txt_sonuc.insert(tk.END, "BOTCH!", 'botch')
        
        self.txt_sonuc.config(state='disabled')

if __name__ == "__main__":
    root = tk.Tk()
    app = VTMZarUygulamasi(root)
    root.mainloop()