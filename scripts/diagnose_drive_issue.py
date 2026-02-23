#!/usr/bin/env python3
"""
Diagnose Google Drive Shared Drive access issues.
"""

import json

print("🔍 DIAGNOSING GOOGLE DRIVE SHARED DRIVE ISSUE")
print("=" * 60)

print("\n📋 PROBLEM: Service Account cannot access Shared Drive")
print("   Error: 'Shared drive not found: 1qOfODb_1jXOlDuF0kc6nnKaHYWMVLWUR'")
print("\n🔍 POSSIBLE CAUSES:")
print("=" * 60)

print("\n1. 📍 INCORRECT SHARED DRIVE ID")
print("   • The ID you provided: 1qOfODb_1jXOlDuF0kc6nnKaHYWMVLWUR")
print("   • How to verify:")
print("     a. Open the Shared Drive in Google Drive")
print("     b. Look at the URL in address bar")
print("     c. Should be: https://drive.google.com/drive/folders/DRIVE_ID")
print("     d. The ID is after '/folders/'")
print("\n   Example URLs:")
print("     ✅ Correct: https://drive.google.com/drive/folders/1ABC123def456")
print("     ❌ Wrong:   https://drive.google.com/drive/u/0/folders/1ABC123def456")
print("     ❌ Wrong:   https://drive.google.com/drive/shared-with-me")

print("\n2. 🔐 SHARING NOT CONFIGURED")
print("   • Service Account email: openclaw2@openclaw-charlie.iam.gserviceaccount.com")
print("   • Steps to share:")
print("     a. Open Shared Drive in Google Drive")
print("     b. Click on drive name → 'Manage members'")
print("     c. Add email: openclaw2@openclaw-charlie.iam.gserviceaccount.com")
print("     d. Set permission: 'Content manager'")
print("     e. Click 'Send'")

print("\n3. ⏳ PERMISSIONS NOT PROPAGATED")
print("   • Sometimes permissions take a few minutes to propagate")
print("   • Wait 2-3 minutes after sharing")
print("   • Try accessing again")

print("\n4. 🚫 WRONG TYPE OF DRIVE")
print("   • Must be a 'Shared Drive' (Team Drive), not 'My Drive'")
print("   • Check: Left sidebar → 'Shared drives' (not 'My Drive')")

print("\n" + "=" * 60)
print("🎯 QUICK FIX INSTRUCTIONS:")
print("=" * 60)

print("\n📋 STEP-BY-STEP FIX:")
print("1. Go to https://drive.google.com")
print("2. Click 'Shared drives' on left sidebar")
print("3. Find your 'Plant-PWR-Investigation-Klean-Vet' drive")
print("4. Click on the drive name")
print("5. Click 'Manage members' (person+ icon)")
print("6. Add: openclaw2@openclaw-charlie.iam.gserviceaccount.com")
print("7. Set permission: 'Content manager'")
print("8. Click 'Send'")
print("9. Wait 2 minutes")
print("10. Copy the drive ID from URL")
print("11. Send me the ID again")

print("\n🔍 HOW TO GET CORRECT DRIVE ID:")
print("1. After step 3 above, look at browser URL")
print("2. Should look like: https://drive.google.com/drive/folders/1ABC123def456")
print("3. Copy ONLY the part after '/folders/'")
print("4. That's your Shared Drive ID")

print("\n" + "=" * 60)
print("🔄 ALTERNATIVE: CREATE NEW SHARED DRIVE")
print("=" * 60)

print("\nIf still having issues, create a new Shared Drive:")
print("1. Click '+' → 'New Shared Drive'")
print("2. Name: Plant-PWR-Investigation")
print("3. Click 'Create'")
print("4. Immediately share with Service Account")
print("5. Get the new Drive ID")
print("6. Send me the new ID")

print("\n" + "=" * 60)
print("📞 NEED HELP?")
print("=" * 60)
print("• Send me a screenshot of the Shared Drive URL")
print("• Or the exact error message")
print("• Or create a new Shared Drive and share it")

print("\nThe Service Account is ready and waiting for access!")
print("Once properly shared, I'll upload all investigation files.")