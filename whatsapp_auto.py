import pyautogui
import time
import os
import subprocess
from TTS_DS import speak

# ================= CONTACTS =================
contacts = {
    "subhan": "+923276553175",
    "rahman": "+923294380027",
    "haseeb bro": "+923175260570",
    "happy life": "+923330607174",
    "kamran": "+923292138510",
    "khan": "+923193494208",
    "ahmad": "+923299226236"
}

last_contact = ""

# ================= CORE FUNCTIONS =================

def focus_whatsapp():
    """WhatsApp Desktop App ko background se samne layega ya open karega"""
    try:
        subprocess.run("start whatsapp:", shell=True)
        time.sleep(3) # App khulne ka intezar
    except Exception as e:
        speak("WhatsApp open karne mein masla ho raha hai.")

def open_chat(name):
    """Bina coordinates ke chat dhoond kar open karega"""
    global last_contact
    focus_whatsapp()
    
    # Search Shortcut (Ctrl + F ya Ctrl + N)
    pyautogui.hotkey("ctrl", "f") 
    time.sleep(0.5)
    
    # Clear purani search
    pyautogui.hotkey("ctrl", "a")
    pyautogui.press("backspace")
    
    # Number ya Name likhein
    number = contacts.get(name.lower(), name)
    pyautogui.write(number, interval=0.05)
    time.sleep(1.5) # List load hone ka intezar
    
    # Pehlay result par janay ke liye
    pyautogui.press("enter")
    last_contact = name
    time.sleep(0.5)

def send_selected_file():
    """Pro Logic: File bhejny ke liye clipboard ka sahi istemal"""
    speak("File attach kar rahi hoon.")
    
    # Clipboard se paste karein
    pyautogui.hotkey("ctrl", "v")
    time.sleep(2) # Preview screen delay
    
    # Desktop app mein Enter direct kaam karta hai preview screen par
    pyautogui.press("enter")
    time.sleep(1)
    pyautogui.press("enter") # Safety Double Enter
    
    speak("File bhej di hai boss.")

def whatsapp_pro_brain(text):
    global last_contact
    text = text.lower().strip()

    # 1. Open WhatsApp
    if "open whatsapp" in text or "whatsapp chalao" in text:
        focus_whatsapp()
        speak("WhatsApp open kar diya hai.")
        return

    # 2. Identify Contact
    target_contact = ""
    for name in contacts:
        if name in text:
            target_contact = name
            break

    # 3. Chat Opening Logic
    if target_contact:
        open_chat(target_contact)
        
        # Agar sirf chat kholni thi
        if "chat kholo" in text or "open chat" in text:
            if "likho" not in text:
                speak(f"{target_contact} ki chat hazir hai.")
                return

    # 4. File Sending Logic
    if "file" in text or "photo" in text or "video" in text:
        send_selected_file()
        return

    # 5. Writing and Sending Logic (Pro Logic)
    if "likho" in text:
        # Message alag karein
        try:
            msg = text.split("likho", 1)[1]
            # Extra words saaf karein
            for word in ["bhej do", "send kar do", "kar do", "aur"]:
                msg = msg.replace(word, "")
            msg = msg.strip()

            if msg:
                # Coordinate free typing: WhatsApp desktop mein chat khulne ke baad direct typing hoti hai
                pyautogui.write(msg, interval=0.04)
                speak("Likh diya hai.")

                # Agar bhejny ka bhi kaha hai
                if any(word in text for word in ["bhej do", "send kar do", "kar do"]):
                    time.sleep(0.5)
                    pyautogui.press("enter")
                    speak("Aur bhej bhi diya hai.")
            else:
                speak("Boss, likhna kya hai?")
        except:
            speak("Message samajh nahi aaya.")

    # 6. Just Send (If already written)
    elif any(word in text for word in ["bhej do", "send kar do", "kar do"]):
        pyautogui.press("enter")
        speak("Bhej diya Boss.")