#!/usr/bin/env python3
"""
Create a test image for the Kivy Image Editor application.
"""

from PIL import Image, ImageDraw, ImageFont
import os

def create_test_image():
    """Create a colorful test image with text and shapes."""
    
    # Create a new image with RGB mode
    width, height = 800, 600
    image = Image.new('RGB', (width, height), color='white')
    draw = ImageDraw.Draw(image)
    
    # Draw gradient background
    for y in range(height):
        color_value = int(255 * (y / height))
        draw.line([(0, y), (width, y)], fill=(100, color_value, 255 - color_value))
    
    # Draw some geometric shapes
    # Rectangle
    draw.rectangle([50, 50, 200, 150], fill='red', outline='darkred', width=3)
    
    # Circle
    draw.ellipse([250, 50, 400, 200], fill='green', outline='darkgreen', width=3)
    
    # Triangle (using polygon)
    draw.polygon([(500, 180), (450, 80), (550, 80)], fill='blue', outline='darkblue')
    
    # Draw some text
    try:
        # Try to use a default font
        font = ImageFont.load_default()
    except:
        font = None
    
    draw.text((50, 250), "Image Editor Test Image", fill='black', font=font)
    draw.text((50, 300), "Try the filters and effects!", fill='darkblue', font=font)
    draw.text((50, 350), "- Rotate", fill='purple', font=font)
    draw.text((50, 380), "- Grayscale", fill='gray', font=font)
    draw.text((50, 410), "- Brightness & Contrast", fill='orange', font=font)
    draw.text((50, 440), "- Blur Effect", fill='brown', font=font)
    draw.text((50, 470), "- Flip Horizontally/Vertically", fill='green', font=font)
    
    # Draw a pattern in the bottom right
    for i in range(10):
        x = 600 + i * 15
        y = 400 + i * 10
        draw.ellipse([x, y, x + 20, y + 20], fill=(255, 255 - i * 20, i * 25))
    
    # Save the image
    image.save('test_image.png')
    print("Test image 'test_image.png' created successfully!")
    print("You can now load this image in the Image Editor to test all features.")

if __name__ == "__main__":
    create_test_image() 