"""
Image processing module using Pillow for the Kivy Image Editor.
Handles all image manipulation operations including filters, rotations, and effects.
"""

from PIL import Image, ImageEnhance, ImageFilter
import io
from typing import Optional, Tuple


class ImageProcessor:
    """Handles all image processing operations using Pillow."""
    
    def __init__(self):
        self.current_image: Optional[Image.Image] = None
        self.previous_image: Optional[Image.Image] = None  # For undo functionality
        self.original_image: Optional[Image.Image] = None
    
    def load_image(self, filepath: str) -> bool:
        """
        Load an image from file path.
        
        Args:
            filepath: Path to the image file
            
        Returns:
            True if successful, False otherwise
        """
        try:
            self.current_image = Image.open(filepath)
            # Convert to RGB if necessary (for consistency)
            if self.current_image.mode != 'RGB':
                self.current_image = self.current_image.convert('RGB')
            
            # Store original for reset functionality
            self.original_image = self.current_image.copy()
            self.previous_image = None  # Reset undo state
            return True
        except Exception as e:
            print(f"Error loading image: {e}")
            return False
    
    def save_current_state(self):
        """Save current image state for undo functionality."""
        if self.current_image:
            self.previous_image = self.current_image.copy()
    
    def undo(self) -> bool:
        """
        Undo the last operation.
        
        Returns:
            True if undo was possible, False otherwise
        """
        if self.previous_image:
            self.current_image = self.previous_image.copy()
            self.previous_image = None  # Clear undo state after using it
            return True
        return False
    
    def rotate_clockwise(self):
        """Rotate image 90 degrees clockwise."""
        if self.current_image:
            self.save_current_state()
            self.current_image = self.current_image.rotate(-90, expand=True)
    
    def convert_to_grayscale(self):
        """Convert image to grayscale."""
        if self.current_image:
            self.save_current_state()
            self.current_image = self.current_image.convert('L').convert('RGB')
    
    def adjust_brightness(self, factor: float):
        """
        Adjust image brightness.
        
        Args:
            factor: Brightness factor (1.0 = no change, >1.0 = brighter, <1.0 = darker)
        """
        if self.current_image:
            self.save_current_state()
            enhancer = ImageEnhance.Brightness(self.current_image)
            self.current_image = enhancer.enhance(factor)
    
    def adjust_contrast(self, factor: float):
        """
        Adjust image contrast.
        
        Args:
            factor: Contrast factor (1.0 = no change, >1.0 = more contrast, <1.0 = less contrast)
        """
        if self.current_image:
            self.save_current_state()
            enhancer = ImageEnhance.Contrast(self.current_image)
            self.current_image = enhancer.enhance(factor)
    
    def apply_gaussian_blur(self, radius: float = 2.0):
        """
        Apply Gaussian blur filter.
        
        Args:
            radius: Blur radius
        """
        if self.current_image:
            self.save_current_state()
            self.current_image = self.current_image.filter(ImageFilter.GaussianBlur(radius))
    
    def flip_horizontal(self):
        """Flip image horizontally."""
        if self.current_image:
            self.save_current_state()
            self.current_image = self.current_image.transpose(Image.FLIP_LEFT_RIGHT)
    
    def flip_vertical(self):
        """Flip image vertically."""
        if self.current_image:
            self.save_current_state()
            self.current_image = self.current_image.transpose(Image.FLIP_TOP_BOTTOM)
    
    def save_image(self, filepath: str) -> bool:
        """
        Save current image to file.
        
        Args:
            filepath: Path where to save the image
            
        Returns:
            True if successful, False otherwise
        """
        if self.current_image:
            try:
                self.current_image.save(filepath)
                return True
            except Exception as e:
                print(f"Error saving image: {e}")
                return False
        return False
    
    def get_image_data(self) -> Optional[bytes]:
        """
        Convert current Pillow Image to bytes for Kivy Texture.
        
        Returns:
            Image data as bytes, or None if no image loaded
        """
        if self.current_image:
            # Convert image to bytes format that Kivy can use
            img_io = io.BytesIO()
            self.current_image.save(img_io, format='PNG')
            img_io.seek(0)
            return img_io.getvalue()
        return None
    
    def get_image_size(self) -> Optional[Tuple[int, int]]:
        """
        Get current image dimensions.
        
        Returns:
            Tuple of (width, height) or None if no image loaded
        """
        if self.current_image:
            return self.current_image.size
        return None
    
    def has_image(self) -> bool:
        """Check if an image is currently loaded."""
        return self.current_image is not None
    
    def can_undo(self) -> bool:
        """Check if undo operation is available."""
        return self.previous_image is not None
    
    def reset_to_original(self):
        """Reset current image to original state."""
        if self.original_image:
            self.save_current_state()
            self.current_image = self.original_image.copy()
    
    def adjust_brightness_absolute(self, factor: float):
        """
        Adjust image brightness from the original image.
        
        Args:
            factor: Brightness factor (1.0 = no change, >1.0 = brighter, <1.0 = darker)
        """
        if self.original_image:
            self.save_current_state()
            enhancer = ImageEnhance.Brightness(self.original_image)
            self.current_image = enhancer.enhance(factor)
    
    def adjust_contrast_absolute(self, factor: float):
        """
        Adjust image contrast from the original image.
        
        Args:
            factor: Contrast factor (1.0 = no change, >1.0 = more contrast, <1.0 = less contrast)
        """
        if self.original_image:
            self.save_current_state()
            enhancer = ImageEnhance.Contrast(self.original_image)
            self.current_image = enhancer.enhance(factor)
    
    def adjust_brightness_and_contrast_absolute(self, brightness_factor: float, contrast_factor: float):
        """
        Adjust both brightness and contrast from the original image.
        
        Args:
            brightness_factor: Brightness factor (1.0 = no change)
            contrast_factor: Contrast factor (1.0 = no change)
        """
        if self.original_image:
            self.save_current_state()
            # Apply brightness first
            brightness_enhancer = ImageEnhance.Brightness(self.original_image)
            temp_image = brightness_enhancer.enhance(brightness_factor)
            # Then apply contrast
            contrast_enhancer = ImageEnhance.Contrast(temp_image)
            self.current_image = contrast_enhancer.enhance(contrast_factor) 