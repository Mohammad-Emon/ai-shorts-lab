#!/usr/bin/env python3
"""
GitHub Setup Script
Prepare the complete AI avatar system for GitHub
"""

import os
import subprocess
import sys
from pathlib import Path

def setup_github():
    """Setup the repository for GitHub"""
    
    print("🚀 Setting up AI Shorts Lab for GitHub")
    print("=" * 40)
    
    # Check if we're in a git repository
    if not os.path.exists('.git'):
        print("📁 Initializing Git repository...")
        subprocess.run(['git', 'init'], check=True)
        print("✅ Git repository initialized")
    
    # Create necessary directories
    directories = [
        'silas-chat-ui/generated_videos',
        'SadTalker/checkpoints',
        'Wav2Lip/checkpoints'
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        
        # Add .gitkeep to empty directories
        gitkeep_path = os.path.join(directory, '.gitkeep')
        if not os.path.exists(gitkeep_path):
            with open(gitkeep_path, 'w') as f:
                f.write('# Keep this directory in git\n')
    
    print("✅ Directory structure created")
    
    # Create example photo placeholder
    example_photo_path = 'silas-chat-ui/avatar_template.jpg'
    if not os.path.exists(example_photo_path):
        print("📸 Creating photo template...")
        # Create a simple text file as placeholder
        with open('silas-chat-ui/PHOTO_SETUP.md', 'w') as f:
            f.write("""# 📸 Photo Setup Instructions

## Add Your Photo

1. **Take a good photo** of yourself:
   - Clear face, good lighting
   - Looking at camera
   - Square-ish crop works best

2. **Save as JPG** and copy to:
   ```bash
   cp your_photo.jpg silas-chat-ui/my_photo.jpg
   ```

3. **Test the system**:
   ```bash
   python silas-chat-ui/launch_complete_avatar.py
   ```

## Photo Requirements
- **Format**: JPG, JPEG, PNG
- **Size**: Any size (will be resized to 512x512)
- **Quality**: Higher resolution = better results
- **Face**: Clear, well-lit, facing camera

## Example
```bash
# Good photo names
silas-chat-ui/my_photo.jpg
silas-chat-ui/user_photo.jpg
silas-chat-ui/avatar.jpg
```

Your photo will be used to create realistic talking head videos!
""")
        print("✅ Photo setup instructions created")
    
    # Add all files to git
    print("📝 Adding files to git...")
    subprocess.run(['git', 'add', '.'], check=True)
    
    # Check git status
    result = subprocess.run(['git', 'status', '--porcelain'], 
                          capture_output=True, text=True)
    
    if result.stdout.strip():
        print("📋 Files ready to commit:")
        print(result.stdout)
        
        # Create initial commit
        try:
            subprocess.run(['git', 'commit', '-m', 'Initial commit: Complete AI Avatar System'], 
                         check=True)
            print("✅ Initial commit created")
        except subprocess.CalledProcessError:
            print("ℹ️  Files already committed or no changes")
    else:
        print("ℹ️  No new files to commit")
    
    # Show repository info
    print("\n🎯 Repository Ready for GitHub!")
    print("=" * 30)
    print("📁 Project: AI Shorts Lab")
    print("🎭 Main Feature: Complete Avatar System")
    print("🔊 TTS: Dual system (Browser + Server)")
    print("🎬 Video: Real face talking heads")
    print("💬 AI: Multi-agent chat system")
    
    print("\n🚀 Next Steps:")
    print("1. Create GitHub repository")
    print("2. Add remote: git remote add origin <your-repo-url>")
    print("3. Push: git push -u origin main")
    print("4. Add your photo: cp photo.jpg silas-chat-ui/my_photo.jpg")
    print("5. Test: python silas-chat-ui/launch_complete_avatar.py")
    
    print("\n📚 Documentation Created:")
    print("✅ README.md - Main documentation")
    print("✅ QUICK_START.md - 30-second setup")
    print("✅ FEATURES.md - Complete feature list")
    print("✅ LICENSE - MIT license")
    print("✅ requirements.txt - Python dependencies")
    print("✅ .gitignore - Proper file exclusions")
    
    print("\n🎉 Your AI Avatar System is GitHub Ready!")
    
    return True

if __name__ == "__main__":
    setup_github()