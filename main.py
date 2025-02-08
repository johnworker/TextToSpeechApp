import os
import tkinter as tk
from tkinter import filedialog, messagebox
from gtts import gTTS
import pygame

audio_folder = "audio"
os.makedirs(audio_folder, exist_ok=True)

def text_to_speech():
    text = text_entry.get("1.0", tk.END).strip()
    if not text:
        messagebox.showerror("錯誤", "請輸入文字！")
        return
    
    try:
        tts = gTTS(text=text, lang=language_var.get())
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
            tts = gTTS(text=text, lang=language_var.get())
            tts.save(save_path)
            messagebox.showinfo("成功", "語音檔案已保存！")
        except Exception as e:
            messagebox.showerror("錯誤", f"保存失敗：{str(e)}")

# 建立 GUI 視窗
root = tk.Tk()
root.title("文字轉語音小工具")
root.geometry("400x300")

tk.Label(root, text="請輸入文字:").pack()
text_entry = tk.Text(root, height=5)
text_entry.pack()

language_var = tk.StringVar(value="zh-TW")
tk.Label(root, text="選擇語言:").pack()
language_menu = tk.OptionMenu(root, language_var, "zh-TW", "en", "ja", "fr", "de")
language_menu.pack()

tk.Button(root, text="轉換語音", command=text_to_speech).pack()
tk.Button(root, text="下載音檔", command=save_audio).pack()

root.mainloop()
