#!/usr/bin/env python3
"""
QR Code Generator for Saudi Tourism Script Generator
Run this after deploying to get a QR code for your live app
"""

import qrcode
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers import RoundedModuleDrawer
from qrcode.image.styles.colormasks import SolidFillColorMask

def generate_qr_code(url, filename="app_qr_code.png"):
    """
    Generate a QR code for the app URL
    
    Args:
        url: The deployed app URL (e.g., https://your-app.onrender.com)
        filename: Output filename for the QR code image
    """
    
    print(f"🎨 Generating QR code for: {url}")
    
    # Create QR code instance
    qr = qrcode.QRCode(
        version=1,  # Auto-adjust size
        error_correction=qrcode.constants.ERROR_CORRECT_H,  # High error correction
        box_size=10,
        border=4,
    )
    
    # Add data
    qr.add_data(url)
    qr.make(fit=True)
    
    # Create styled image
    img = qr.make_image(
        image_factory=StyledPilImage,
        module_drawer=RoundedModuleDrawer(),
        color_mask=SolidFillColorMask(
            back_color=(255, 255, 255),  # White background
            front_color=(30, 60, 114)    # Saudi blue color
        )
    )
    
    # Save
    img.save(filename)
    print(f"✅ QR code saved as: {filename}")
    print(f"\n📱 Users can scan this QR code to access your app!")
    print(f"🌐 URL: {url}")
    
    return filename


def generate_qr_with_logo(url, logo_path=None, filename="app_qr_code_with_logo.png"):
    """
    Generate QR code with optional logo in center
    
    Args:
        url: The deployed app URL
        logo_path: Path to logo image (optional)
        filename: Output filename
    """
    
    print(f"🎨 Generating QR code with logo for: {url}")
    
    # Create QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    
    qr.add_data(url)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color=(30, 60, 114), back_color="white")
    
    # Add logo if provided
    if logo_path:
        try:
            from PIL import Image
            logo = Image.open(logo_path)
            
            # Calculate logo size (10% of QR code)
            qr_width, qr_height = img.size
            logo_size = qr_width // 10
            logo = logo.resize((logo_size, logo_size), Image.Resampling.LANCZOS)
            
            # Paste logo in center
            logo_pos = ((qr_width - logo_size) // 2, (qr_height - logo_size) // 2)
            img.paste(logo, logo_pos)
            
            print(f"✅ Logo added to QR code")
        except Exception as e:
            print(f"⚠️  Could not add logo: {e}")
    
    img.save(filename)
    print(f"✅ QR code saved as: {filename}")
    
    return filename


if __name__ == "__main__":
    import sys
    
    print("=" * 70)
    print("🎯 Saudi Tourism Script Generator - QR Code Generator")
    print("=" * 70)
    print()
    
    # Get URL from command line or prompt
    if len(sys.argv) > 1:
        app_url = sys.argv[1]
    else:
        print("Enter your deployed app URL:")
        print("Example: https://saudi-tourism-script.onrender.com")
        app_url = input("URL: ").strip()
    
    if not app_url:
        print("❌ No URL provided. Exiting.")
        sys.exit(1)
    
    # Add https:// if missing
    if not app_url.startswith(('http://', 'https://')):
        app_url = 'https://' + app_url
    
    print()
    
    # Generate QR codes
    try:
        # Basic QR code
        generate_qr_code(app_url, "app_qr_code.png")
        
        print()
        print("=" * 70)
        print("✅ Done! Share the QR code with your users!")
        print("=" * 70)
        
    except ImportError:
        print()
        print("❌ Error: qrcode library not installed")
        print()
        print("Install it with:")
        print("  pip install qrcode[pil]")
        print()
        sys.exit(1)
    
    except Exception as e:
        print(f"❌ Error generating QR code: {e}")
        sys.exit(1)
