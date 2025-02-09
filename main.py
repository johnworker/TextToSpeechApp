import os
import tkinter as tk
from tkinter import filedialog, messagebox
from gtts import gTTS
import pygame
import speech_recognition as sr


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

def recognize_speech():
    global text_entry, language_var  # 確保函式內能存取全域變數
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        messagebox.showinfo("錄音", "請說話...")
        try:
            audio = recognizer.listen(source)
            text = recognizer.recognize_google(audio, language=language_var.get())
            text_entry.delete("1.0", tk.END)
            text_entry.insert(tk.END, text)
        except sr.UnknownValueError:
            messagebox.showerror("錯誤", "無法辨識語音")
        except sr.RequestError:
            messagebox.showerror("錯誤", "語音辨識服務無法使用")


def text_to_speech():
    text = text_entry.get("1.0", tk.END).strip()
    if not text:
        messagebox.showerror("錯誤", "請輸入文字！")
        return
    
    try:
        lang = language_var.get()
        tld = "com"  # 免費版固定美式英語
        
        if VERSION == "pro":
            tld = voice_var.get()
        
        tts = gTTS(text=text, lang=lang, tld=tld)
        filename = os.path.join(audio_folder, "output.mp3")
        tts.save(filename)
        messagebox.showinfo("成功", "語音已產生！")
        play_audio(filename)
    except Exception as e:
        messagebox.showerror("錯誤", f"語音轉換失敗：{str(e)}")

def play_audio(filename):
    pygame.mixer.init()
    pygame.mixer.music.load(filename)
    pygame.mixer.music.play()

def save_audio():
    text = text_entry.get("1.0", tk.END).strip()
    if not text:
        messagebox.showerror("錯誤", "請輸入文字！")
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
            messagebox.showinfo("成功", "語音檔案已保存！")
        except Exception as e:
            messagebox.showerror("錯誤", f"保存失敗：{str(e)}")

        # 建立 GUI 視窗
        root = tk.Tk()
        root.title("文字轉語音小工具")
        root.geometry("400x400")

        # 建立輸入框
        tk.Label(root, text="請輸入文字:").pack()
        text_entry = tk.Text(root, height=5)
        text_entry.pack()
        

        # 設定語言選單
        tk.Label(root, text="選擇語言:").pack()
        language_var = tk.StringVar(value="zh-TW")
        if VERSION == "pro":
            language_menu = tk.OptionMenu(root, language_var, *PRO_LANGUAGES)
        else:
            language_menu = tk.OptionMenu(root, language_var, *FREE_LANGUAGES)
        language_menu.pack()
        
        # 設定語音區域選單 (僅付費版可選)
        if VERSION == "pro":
            tk.Label(root, text="選擇語音區域:").pack()
            voice_var = tk.StringVar(value="com")
            voice_menu = tk.OptionMenu(root, voice_var, *PRO_VOICES)
            voice_menu.pack()
        
        tk.Button(root, text="轉換語音", command=text_to_speech).pack()
        tk.Button(root, text="下載音檔", command=save_audio).pack()
        tk.Button(root, text="語音辨識 (錄音)", command=recognize_speech).pack()


        root.mainloop()
