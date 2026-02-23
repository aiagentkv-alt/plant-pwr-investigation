#!/usr/bin/env python3
"""
Test uploading files to the specific folder.
"""

import os
import json
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

def test_folder_upload():
    """Test uploading to the specific folder"""
    print("📤 TESTING UPLOAD TO FOLDER")
    print("=" * 60)
    
    folder_id = '1qOfODb_1jXOlDuF0kc6nnKaHYWMVLWUR'
    
    try:
        # Load credentials
        with open('/root/.openclaw/google-service-account.json', 'r') as f:
            creds_info = json.load(f)
        
        print(f"👤 Service Account: {creds_info['client_email']}")
        
        credentials = service_account.Credentials.from_service_account_info(creds_info)
        drive_service = build('drive', 'v3', credentials=credentials)
        
        # First, verify we can access the folder
        print(f"\n🔍 Verifying access to folder: {folder_id}")
        
        folder_info = drive_service.files().get(
            fileId=folder_id,
            fields='id, name, mimeType, capabilities',
            supportsAllDrives=True
        ).execute()
        
        print(f"✅ Folder found: {folder_info['name']}")
        print(f"   Type: {folder_info['mimeType']}")
        print(f"   Capabilities: {json.dumps(folder_info.get('capabilities', {}), indent=4)}")
        
        # Test upload
        print("\n📤 Testing file upload to folder...")
        
        # Create a test file
        test_content = """# Plant PWR Investigation - Test Upload

This is a test file to verify Google Drive integration.

## System Status:
- ✅ Service Account authenticated
- ✅ Folder access confirmed
- ✅ Upload capability tested

## Next Steps:
1. Upload all investigation files
2. Set up automatic sync
3. Configure regular backups

Folder ID: 1qOfODb_1jXOlDuF0kc6nnKaHYWMVLWUR
Test completed successfully!
"""
        
        test_file_path = "/tmp/plant_pwr_test_upload.md"
        with open(test_file_path, 'w', encoding='utf-8') as f:
            f.write(test_content)
        
        file_metadata = {
            'name': 'TEST-Plant-PWR-Integration.md',
            'parents': [folder_id],
            'mimeType': 'text/markdown'
        }
        
        media = MediaFileUpload(
            test_file_path,
            mimetype='text/markdown',
            resumable=True
        )
        
        file = drive_service.files().create(
            body=file_metadata,
            media_body=media,
            supportsAllDrives=True,
            fields='id, name, webViewLink, createdTime'
        ).execute()
        
        print(f"✅ File uploaded successfully!")
        print(f"   File: {file['name']}")
        print(f"   Created: {file['createdTime']}")
        print(f"   URL: {file.get('webViewLink', 'N/A')}")
        
        # List files in folder to confirm
        print("\n📋 Listing files in folder...")
        
        results = drive_service.files().list(
            q=f"'{folder_id}' in parents",
            pageSize=10,
            fields='files(id, name, createdTime)',
            supportsAllDrives=True
        ).execute()
        
        files = results.get('files', [])
        print(f"📁 Found {len(files)} files in folder:")
        
        for f in files:
            print(f"   • {f['name']} ({f['id']})")
        
        # Clean up test file
        os.remove(test_file_path)
        
        print("\n" + "=" * 60)
        print("🎉 FOLDER UPLOAD TEST: SUCCESS!")
        print("=" * 60)
        print("✅ Service Account can access folder")
        print("✅ File upload working")
        print("✅ Folder: Plant-PWR-Investigation-Klean-Vet")
        print(f"✅ Folder ID: {folder_id}")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Error: {type(e).__name__}: {e}")
        
        # More detailed error info
        if hasattr(e, 'error_details'):
            print(f"   Details: {e.error_details}")
        
        print("\n🔧 TROUBLESHOOTING:")
        print("1. Ensure folder is in a Shared Drive (not My Drive)")
        print("2. Share the ENTIRE Shared Drive with Service Account")
        print("3. Permission level: 'Content manager' or 'Editor'")
        print("4. Wait 2 minutes after sharing")
        
        return False

def main():
    """Main function"""
    print("🔧 GOOGLE DRIVE FOLDER UPLOAD TEST")
    print("=" * 60)
    
    success = test_folder_upload()
    
    if success:
        print("\n🚀 READY FOR FULL UPLOAD!")
        print("I can now upload all Plant PWR investigation files.")
        print("\n📁 Files to upload:")
        print("1. INFORME_COMPLETO_PLANT_PWR.md")
        print("2. whoogle_results.json")
        print("3. critical_domains.json")
        print("4. All scripts and logs")
        print("5. Daily monitoring results")
    else:
        print("\n⚠️  ACTION REQUIRED:")
        print("Please ensure:")
        print("1. Folder is in a SHARED DRIVE (not My Drive)")
        print("2. Entire Shared Drive is shared with Service Account")
        print("3. Permission: 'Content manager'")
        print("4. Wait a few minutes after sharing")
    
    return 0 if success else 1

if __name__ == "__main__":
    exit(main())