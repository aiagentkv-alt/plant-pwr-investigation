#!/usr/bin/env python3
"""
Test if the provided ID is a folder (not Shared Drive).
"""

import json
from google.oauth2 import service_account
from googleapiclient.discovery import build

def test_as_folder():
    """Test if ID is a folder within a drive"""
    print("🔍 TESTING IF ID IS A FOLDER (NOT SHARED DRIVE)")
    print("=" * 60)
    
    folder_id = '1qOfODb_1jXOlDuF0kc6nnKaHYWMVLWUR'
    
    try:
        # Load credentials
        with open('/root/.openclaw/google-service-account.json', 'r') as f:
            creds_info = json.load(f)
        
        credentials = service_account.Credentials.from_service_account_info(creds_info)
        drive_service = build('drive', 'v3', credentials=credentials)
        
        print(f"Testing ID: {folder_id}")
        
        # Try to get file/folder metadata
        try:
            file_info = drive_service.files().get(
                fileId=folder_id,
                fields='id, name, mimeType, parents, driveId',
                supportsAllDrives=True
            ).execute()
            
            print(f"\n✅ FOUND: {file_info['name']}")
            print(f"   Type: {file_info['mimeType']}")
            print(f"   ID: {file_info['id']}")
            
            if 'driveId' in file_info:
                print(f"   Shared Drive ID: {file_info['driveId']}")
                print(f"\n🎯 This is a FOLDER within Shared Drive: {file_info['driveId']}")
                print("   You provided the FOLDER ID, not the SHARED DRIVE ID")
                
            if 'parents' in file_info:
                print(f"   Parent folders: {file_info['parents']}")
                
            return True
            
        except Exception as e:
            print(f"\n❌ Cannot access as file/folder either: {type(e).__name__}")
            print(f"   Error: {e}")
            return False
            
    except Exception as e:
        print(f"❌ General error: {type(e).__name__}: {e}")
        return False

def main():
    """Main function"""
    success = test_as_folder()
    
    print("\n" + "=" * 60)
    if success:
        print("🎯 CONCLUSION:")
        print("The ID you provided is likely a FOLDER ID, not a SHARED DRIVE ID.")
        print("\n📋 WHAT TO DO:")
        print("1. Go to the folder in Google Drive")
        print("2. Navigate UP to the Shared Drive root")
        print("3. Get the Shared Drive ID from that URL")
        print("4. Share the ENTIRE Shared Drive with Service Account")
    else:
        print("🎯 CONCLUSION:")
        print("The ID is not accessible at all.")
        print("\n📋 WHAT TO DO:")
        print("1. Verify the ID is correct")
        print("2. Ensure Shared Drive is shared with Service Account")
        print("3. Create new Shared Drive if needed")
    
    return 0

if __name__ == "__main__":
    exit(main())