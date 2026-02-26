import asyncio
import edge_tts
import pygame
import os
import time


VOICE = "en-IN-NeerjaNeural" 

async def generate_audio(TEXT, output_file):
    try:
       
        clean_text = str(TEXT).strip()
        if not clean_text:
            return False
            
      
        communicate = edge_tts.Communicate(clean_text, VOICE)
        
       
        await communicate.save(output_file)
        
       
        if os.path.exists(output_file) and os.path.getsize(output_file) > 0:
            return True
        return False
    except Exception as e:
        print(f"❌ Detail Error: {e}")
        return False

def speak(TEXT):
   
    file_path = f"temp_{int(time.time())}.mp3"
    
    # generate audio with retries
    success = False
    print(f"🎙️ Jarvis is thinking: {TEXT}")
    
    for i in range(3):
        
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(generate_audio(TEXT, file_path))
        loop.close()
        
        if result:
            success = True
            break
        print(f"⚠️ Attempt {i+1} failed, retrying...")
        time.sleep(1)

    if not success:
        print("❌ Final Error: Edge-TTS server not responding.")
        return

    # 2. Play Speech
    try:
        pygame.mixer.init()
        pygame.mixer.music.load(file_path)
        pygame.mixer.music.play()
        
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
            
        pygame.mixer.music.unload()
        pygame.mixer.quit() 
    except Exception as e:
        print(f"❌ Playback Error: {e}")
    finally:
        # 3. Cleanup
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
            except:
                pass

