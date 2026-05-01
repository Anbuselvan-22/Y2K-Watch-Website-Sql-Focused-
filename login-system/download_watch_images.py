import urllib.request
import os

# Create images directory if it doesn't exist
images_dir = 'static/images'
os.makedirs(images_dir, exist_ok=True)

# Free Unsplash watch images (these are direct download links)
watch_images = {
    'watch-1.jpg': 'https://images.unsplash.com/photo-1523170335258-f5ed11844a49?w=800&q=80',  # Luxury watch
    'watch-2.jpg': 'https://images.unsplash.com/photo-1587836374828-4dbafa94cf0e?w=800&q=80',  # Rolex style
    'watch-3.jpg': 'https://images.unsplash.com/photo-1524805444758-089113d48a6d?w=800&q=80',  # Classic watch
    'watch-4.jpg': 'https://images.unsplash.com/photo-1522312346375-d1a52e2b99b3?w=800&q=80',  # Sport watch
    'watch-5.jpg': 'https://images.unsplash.com/photo-1533139502658-0198f920d8e8?w=800&q=80',  # Chronograph
    'watch-6.jpg': 'https://images.unsplash.com/photo-1614164185128-e4ec99c436d7?w=800&q=80',  # Diving watch
    'watch-7.jpg': 'https://images.unsplash.com/photo-1611930022073-b7a4ba5fcccd?w=800&q=80',  # Elegant watch
    'watch-8.jpg': 'https://images.unsplash.com/photo-1509048191080-d2984bad6ae5?w=800&q=80',  # Modern watch
    'watch-9.jpg': 'https://images.unsplash.com/photo-1542496658-e33a6d0d50f6?w=800&q=80',  # Luxury sport
    'watch-10.jpg': 'https://images.unsplash.com/photo-1547996160-81dfa63595aa?w=800&q=80', # Aviation watch
}

def download_images():
    print("📥 Downloading luxury watch images from Unsplash...")
    
    for filename, url in watch_images.items():
        filepath = os.path.join(images_dir, filename)
        
        # Skip if file already exists
        if os.path.exists(filepath):
            print(f"⏭️  Skipping {filename} (already exists)")
            continue
        
        try:
            print(f"⬇️  Downloading {filename}...")
            urllib.request.urlretrieve(url, filepath)
            print(f"✅ Downloaded {filename}")
        except Exception as e:
            print(f"❌ Error downloading {filename}: {e}")
    
    print("\n🎉 Image download complete!")

if __name__ == '__main__':
    download_images()
