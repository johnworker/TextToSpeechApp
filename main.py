import os
import tkinter as tk
from tkinter import filedialog, messagebox
from gtts import gTTS
import pygame
import speech_recognition as sr
from tkinter import ttk
import threading

audio_folder = "audio"
os.makedirs(audio_folder, exist_ok=True)

# 設定版本模式: 免費版 (free) 或 付費版 (pro)
VERSION = "free"  # 更改為 "pro" 以啟用付費版功能

# 免費版語言清單
FREE_LANGUAGES = ["zh-TW", "en", "ja", "fr", "de"]

# 付費版語言清單
PRO_LANGUAGES = FREE_LANGUAGES + ["es", "it", "ko", "ru", "pt"]

# 付費版聲音區域
PRO_VOICES = ["com", "co.uk", "ca", "ie", "co.in", "com.au"]

# 錄音控制變數
is_recording = False
recognizer = sr.Recognizer()
def toggle_recording():
    global is_recording
    if is_recording:
        is_recording = False
        record_button.config(text="🎤 開啟錄音")
        messagebox.showinfo("🎤 停止錄音", "錄音已關閉。")
    else:
        is_recording = True
        record_button.config(text="🛑 停止錄音")
        messagebox.showinfo("🎤 開始錄音", "錄音已開啟，請說話...")
        threading.Thread(target=record_speech).start()

def record_speech():
    global is_recording
    with sr.Microphone() as source:
        while is_recording:
            try:
                audio = recognizer.listen(source, timeout=5)
                text = recognizer.recognize_google(audio, language=language_var.get())
                text_entry.insert(tk.END, text + " ")
            except sr.UnknownValueError:
                pass
            except sr.RequestError:
                messagebox.showerror("❌ 錯誤", "語音辨識服務無法使用")
                is_recording = False

def text_to_speech():
    text = text_entry.get("1.0", tk.END).strip()
    if not text:
        messagebox.showerror("❌ 錯誤", "請輸入文字！")
        return
    
    try:
        lang = language_var.get()
        tld = "com"  # 免費版固定美式英語
        
        if VERSION == "pro":
            tld = voice_var.get()
        
        tts = gTTS(text=text, lang=lang, tld=tld)
        filename = os.path.join(audio_folder, "output.mp3")
        tts.save(filename)
        messagebox.showinfo("✅ 成功", "語音已產生！")
        play_audio(filename)
    except Exception as e:
        messagebox.showerror("❌ 錯誤", f"語音轉換失敗：{str(e)}")

def play_audio(filename):
    pygame.mixer.init()
    pygame.mixer.music.load(filename)
    pygame.mixer.music.play()

def save_audio():
    text = text_entry.get("1.0", tk.END).strip()
    if not text:
        messagebox.showerror("❌ 錯誤", "請輸入文字！")
        return
    
    save_path = filedialog.asksaveasfilename(defaultextension=".mp3", filetypes=[("MP3 files", "*.mp3"), ("All Files", "*.*")])
    if save_path:
        try:
            lang = language_var.get()
            tld = "com"  # 免費版固定美式英語
            
            if VERSION == "pro":
                tld = voice_var.get()
            
            tts = gTTS(text=text, lang=lang, tld=tld)
            tts.save(save_path)
            messagebox.showinfo("✅ 成功", "語音檔案已保存！")
        except Exception as e:
            messagebox.showerror("❌ 錯誤", f"保存失敗：{str(e)}")

# 建立 GUI 視窗
root = tk.Tk()
root.title("✨ 文字轉語音 AI 工具 ✨")
root.geometry("800x700")
root.configure(bg="#dbeafe")

style = ttk.Style()
style.configure("TFrame", background="#dbeafe", relief="flat")
style.configure("TButton", font=("Arial", 14, "bold"), padding=14, background="#0078D7", foreground="black", borderwidth=0, relief="flat")
style.configure("TLabel", background="#dbeafe", font=("Arial", 20, "bold"), foreground="#333333")
style.configure("TCombobox", font=("Arial", 14))

frame = ttk.Frame(root, padding=30, style="TFrame")
frame.pack(fill="both", expand=True)

app_title = ttk.Label(frame, text="🎙️ 文字轉語音 AI 工具", font=("Arial", 28, "bold"))
app_title.pack(pady=20)

text_label = ttk.Label(frame, text="📝 輸入文字:")
text_label.pack()
text_entry = tk.Text(frame, height=10, width=80, font=("Arial", 14), bg="#FFFFFF", fg="#333333", borderwidth=2, relief="solid")
text_entry.pack(pady=15)

language_label = ttk.Label(frame, text="🌎 選擇語言:")
language_label.pack()
language_var = tk.StringVar(value="zh-TW")
language_menu = ttk.Combobox(frame, textvariable=language_var, values=FREE_LANGUAGES if VERSION == "free" else PRO_LANGUAGES, state="readonly")
language_menu.pack()
language_menu.current(0)

if VERSION == "pro":
    voice_label = ttk.Label(frame, text="🔊 語音區域:")
    voice_label.pack()
    voice_var = tk.StringVar(value="com")
    voice_menu = ttk.Combobox(frame, textvariable=voice_var, values=PRO_VOICES, state="readonly")
    voice_menu.pack()
    voice_menu.current(0)

btn_frame = ttk.Frame(frame, padding=20, style="TFrame")
btn_frame.pack()

ttk.Button(btn_frame, text="🎧 轉換語音", command=text_to_speech).pack(side="left", padx=20, pady=10)
ttk.Button(btn_frame, text="💾 下載音檔", command=save_audio).pack(side="left", padx=20, pady=10)
record_button = ttk.Button(btn_frame, text="🎤 開啟錄音", command=toggle_recording)
record_button.pack(side="left", padx=20, pady=10)

root.mainloop()
