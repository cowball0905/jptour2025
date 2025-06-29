import os
from PIL import Image

def resize_image_inplace(file_path):
    """
    Resize image in-place if shortside > 1920, otherwise leave unchanged
    """
    try:
        with Image.open(file_path) as img:
            width, height = img.size
            shortside = min(width, height)
            
            # If shortside <= 1920, do nothing
            if shortside <= 1920:
                print(f"Skipped (shortside {shortside}): {file_path}")
                return
                
            # Calculate new size maintaining aspect ratio
            if width < height:
                new_width = 1920
                new_height = int((height / width) * new_width)
            else:
                new_height = 1920
                new_width = int((width / height) * new_height)
                
            # Resize image using high-quality resampling
            resized_img = img.resize((new_width, new_height), Image.LANCZOS)
            
            # Save resized image, replacing the original
            resized_img.save(file_path, optimize=True, quality=95)
            print(f"Resized {shortside} -> 1920: {file_path}")
            
    except Exception as e:
        print(f"Error processing {file_path}: {str(e)}")

def process_images_recursively(root_path):
    """
    Recursively process all WebP images in the given path and subdirectories
    """
    processed_count = 0
    skipped_count = 0
    
    for root, dirs, files in os.walk(root_path):
        for file in files:
            if file.lower().endswith('.webp'):
                file_path = os.path.join(root, file)
                
                # Get original size for logging
                try:
                    with Image.open(file_path) as img:
                        original_shortside = min(img.size)
                    
                    resize_image_inplace(file_path)
                    
                    if original_shortside > 1920:
                        processed_count += 1
                    else:
                        skipped_count += 1
                        
                except Exception as e:
                    print(f"Error reading {file_path}: {str(e)}")
    
    print(f"\nProcessing complete!")
    print(f"Images resized: {processed_count}")
    print(f"Images skipped: {skipped_count}")

# Usage
if __name__ == "__main__":
    # Replace with your actual path
    image_directory = "./assets/img/25-slide"
    
    # Confirm before processing
    print(f"This will process all WebP images in: {image_directory}")
    print("Images with shortside > 1920 will be resized and ORIGINAL FILES WILL BE REPLACED")
    
    confirm = input("Do you want to continue? (yes/no): ").lower().strip()
    
    if confirm in ['yes', 'y']:
        process_images_recursively(image_directory)
    else:
        print("Operation cancelled.")
