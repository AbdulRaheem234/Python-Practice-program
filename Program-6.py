# pip install pytesseract pillow python-docx PyPDF2 pytube SpeechRecognition
import os
import re
import pytesseract
from PIL import Image
import docx
import PyPDF2
from pytube import YouTube
import speech_recognition as sr

# Configure Tesseract path (change according to your system)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Binod variations to detect (case-insensitive)
BINOD_PATTERNS = re.compile(r'binod|b i n o d|8inod|bin0d', re.IGNORECASE)

def detect_in_text(text):
    """Check if any Binod variation exists in text"""
    return bool(BINOD_PATTERNS.search(text))

def scan_text_file(file_path):
    """Scan .txt, .pdf, .docx files"""
    if file_path.endswith('.txt'):
        with open(file_path, 'r', encoding='utf-8') as f:
            text = f.read()
    elif file_path.endswith('.pdf'):
        text = ""
        with open(file_path, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            for page in reader.pages:
                text += page.extract_text()
    elif file_path.endswith('.docx'):
        doc = docx.Document(file_path)
        text = '\n'.join([para.text for para in doc.paragraphs])
    else:
        return False
    
    return detect_in_text(text)

def scan_image(file_path):
    """Extract text from images using OCR"""
    try:
        img = Image.open(file_path)
        text = pytesseract.image_to_string(img)
        return detect_in_text(text)
    except Exception as e:
        print(f"Error scanning image: {e}")
        return False

def scan_youtube_video(video_url):
    """Scan YouTube video's subtitles for Binod"""
    try:
        yt = YouTube(video_url)
        stream = yt.streams.filter(only_audio=True).first()
        audio_file = stream.download(filename_prefix="yt_audio_")
        
        recognizer = sr.Recognizer()
        with sr.AudioFile(audio_file) as source:
            audio = recognizer.record(source)
            text = recognizer.recognize_google(audio)
            return detect_in_text(text)
    except Exception as e:
        print(f"Error scanning YouTube video: {e}")
        return False

def scan_directory(directory):
    """Scan all files in a directory"""
    results = {"found": False, "files": []}
    
    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            detected = False
            
            if file.lower().endswith(('.txt', '.pdf', '.docx')):
                detected = scan_text_file(file_path)
            elif file.lower().endswith(('.png', '.jpg', '.jpeg')):
                detected = scan_image(file_path)
            
            if detected:
                results["found"] = True
                results["files"].append(file_path)
    
    return results

def main():
    print("🔍 Binod Detector 🔍")
    print("1. Scan a text file (.txt, .pdf, .docx)")
    print("2. Scan an image (.png, .jpg)")
    print("3. Scan a YouTube video")
    print("4. Scan a directory/folder")
    choice = input("Choose an option (1-4): ")
    
    if choice == "1":
        file_path = input("Enter file path: ")
        if scan_text_file(file_path):
            print("🚨 BINOD DETECTED!")
        else:
            print("No Binod found.")
    
    elif choice == "2":
        file_path = input("Enter image path: ")
        if scan_image(file_path):
            print("🚨 BINOD DETECTED!")
        else:
            print("No Binod found.")
    
    elif choice == "3":
        video_url = input("Enter YouTube URL: ")
        if scan_youtube_video(video_url):
            print("🚨 BINOD DETECTED!")
        else:
            print("No Binod found.")
    
    elif choice == "4":
        directory = input("Enter directory path: ")
        results = scan_directory(directory)
        if results["found"]:
            print("🚨 BINOD DETECTED IN THESE FILES:")
            for file in results["files"]:
                print(f"- {file}")
        else:
            print("No Binod found in any files.")
    
    else:
        print("Invalid choice!")

if __name__ == "__main__":
    main()