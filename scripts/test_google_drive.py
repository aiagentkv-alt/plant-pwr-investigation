#!/usr/bin/env python3
"""
Test Google Drive connection with Service Account and Shared Drive.
"""

import os
import json
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

def test_drive_connection():
    """Test connection to Google Drive with Service Account"""
    print("🔧 TESTING GOOGLE DRIVE CONNECTION")
    print("=" * 60)
    
    try:
        # Load service account credentials
        creds_path = "/root/.openclaw/google-service-account.json"
        print(f"📁 Loading credentials from: {creds_path}")
        
        with open(creds_path, 'r') as f:
            creds_info = json.load(f)
        
        print(f"👤 Service Account: {creds_info['client_email']}")
        
        # Create credentials
        credentials = service_account.Credentials.from_service_account_info(creds_info)
        
        # Build Drive service
        drive_service = build('drive', 'v3', credentials=credentials)
        print("✅ Drive service created")
        
        # Test 1: List Shared Drives
        print("\n🔍 Testing Shared Drive access...")
        shared_drives = drive_service.drives().list().execute()
        drives = shared_drives.get('drives', [])
        
        print(f"📊 Found {len(drives)} Shared Drives:")
        for drive in drives:
            print(f"   • {drive['name']} (ID: {drive['id']})")
            if drive['id'] == '1qOfODb_1jXOlDuF0kc6nnKaHYWMVLWUR':
                print(f"      ✅ TARGET SHARED DRIVE FOUND: {drive['name']}")
        
        # Test 2: Access specific Shared Drive
        target_drive_id = '1qOfODb_1jXOlDuF0kc6nnKaHYWMVLWUR'
        print(f"\n🎯 Testing access to Shared Drive ID: {target_drive_id}")
        
        try:
            # List files in Shared Drive
            results = drive_service.files().list(
                corpora='drive',
                driveId=target_drive_id,
                includeItemsFromAllDrives=True,
                supportsAllDrives=True,
                pageSize=10,
                fields='files(id, name, mimeType)'
            ).execute()
            
            files = results.get('files', [])
            print(f"📁 Found {len(files)} files in Shared Drive:")
            
            if files:
                for file in files:
                    file_type = "📄" if file['mimeType'] != 'application/vnd.google-apps.folder' else "📁"
                    print(f"   {file_type} {file['name']} ({file['id']})")
            else:
                print("   ℹ️  Shared Drive is empty (expected)")
            
            # Test 3: Create a test folder
            print("\n🧪 Testing folder creation in Shared Drive...")
            folder_metadata = {
                'name': 'Test-Folder-Plant-PWR',
                'mimeType': 'application/vnd.google-apps.folder',
                'parents': [target_drive_id],
                'driveId': target_drive_id
            }
            
            folder = drive_service.files().create(
                body=folder_metadata,
                supportsAllDrives=True,
                fields='id, name'
            ).execute()
            
            print(f"✅ Test folder created: {folder['name']} (ID: {folder['id']})")
            
            # Test 4: Upload a test file
            print("\n📤 Testing file upload to Shared Drive...")
            
            # Create a test file
            test_file_path = "/tmp/test_plant_pwr.txt"
            with open(test_file_path, 'w') as f:
                f.write("Test file for Plant PWR investigation system.\n")
                f.write(f"Created: {json.dumps(folder, indent=2)}\n")
                f.write("This confirms Google Drive integration is working.\n")
            
            file_metadata = {
                'name': 'test_connection.txt',
                'parents': [folder['id']],
                'driveId': target_drive_id
            }
            
            media = MediaFileUpload(
                test_file_path,
                mimetype='text/plain',
                resumable=True
            )
            
            file = drive_service.files().create(
                body=file_metadata,
                media_body=media,
                supportsAllDrives=True,
                fields='id, name, webViewLink'
            ).execute()
            
            print(f"✅ Test file uploaded: {file['name']}")
            print(f"🔗 File URL: {file.get('webViewLink', 'N/A')}")
            
            # Clean up test files
            print("\n🧹 Cleaning up test files...")
            drive_service.files().delete(
                fileId=folder['id'],
                supportsAllDrives=True
            ).execute()
            print("✅ Test files cleaned up")
            
            os.remove(test_file_path)
            
            print("\n" + "=" * 60)
            print("🎉 GOOGLE DRIVE CONNECTION TEST: SUCCESS!")
            print("=" * 60)
            print("✅ Service Account authenticated")
            print("✅ Shared Drive access confirmed")
            print("✅ Folder creation working")
            print("✅ File upload working")
            print(f"✅ Target Drive: {target_drive_id}")
            
            return True
            
        except Exception as e:
            print(f"❌ Error accessing Shared Drive: {type(e).__name__}: {e}")
            return False
        
    except Exception as e:
        print(f"❌ General error: {type(e).__name__}: {e}")
        return False

def check_permissions():
    """Check if Service Account has proper permissions"""
    print("\n🔐 CHECKING SERVICE ACCOUNT PERMISSIONS")
    print("=" * 60)
    
    print("1. Service Account Email:")
    print("   openclaw2@openclaw-charlie.iam.gserviceaccount.com")
    print("\n2. Required Permission Level:")
    print("   • Content manager (can organize, add, edit)")
    print("   • OR Editor (can edit)")
    print("\n3. What to check in Google Drive:")
    print("   • Go to Shared Drive → Manage members")
    print("   • Verify email is listed with correct permission")
    print("\n4. If access is denied:")
    print("   • Re-share the Shared Drive")
    print("   • Ensure correct email address")
    print("   • Set permission to 'Content manager'")
    
    return True

def main():
    """Main test function"""
    print("🔧 GOOGLE DRIVE SETUP TEST FOR PLANT PWR INVESTIGATION")
    print("=" * 60)
    
    # Check permissions first
    check_permissions()
    
    print("\n" + "=" * 60)
    print("🚀 STARTING CONNECTION TEST")
    print("=" * 60)
    
    # Test the connection
    success = test_drive_connection()
    
    if success:
        print("\n🎯 NEXT STEPS:")
        print("1. The Service Account can access the Shared Drive")
        print("2. I'll now upload all Plant PWR investigation files")
        print("3. Configure automatic sync for future files")
        print("4. Set up folder structure in Google Drive")
    else:
        print("\n⚠️  TROUBLESHOOTING REQUIRED:")
        print("1. Verify Shared Drive is shared with Service Account")
        print("2. Check permission level (Content manager or Editor)")
        print("3. Ensure correct Shared Drive ID")
        print("4. Try re-sharing the Shared Drive")
    
    return 0 if success else 1

if __name__ == "__main__":
    exit(main())