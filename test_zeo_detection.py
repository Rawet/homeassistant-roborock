#!/usr/bin/env python3
"""
Test script to verify Zeo One detection.
"""
import asyncio
from roborock.web_api import RoborockApiClient, UserData
from roborock import RoborockCategory

USERNAME = "dennis.rawet@gmail.com"

async def test_zeo_detection():
    """Test if Zeo devices are detected correctly."""
    print("=" * 60)
    print("Zeo One Detection Test")
    print("=" * 60)
    print(f"\nLogging in as: {USERNAME}\n")
    
    try:
        client = RoborockApiClient(USERNAME, "https://euiot.roborock.com")
        await client.request_code()
        print(f"✓ Verification code sent to {USERNAME}")
        
        code = input("Enter verification code: ").strip()
        user_data = await client.code_login(code)
        print("✓ Login successful!\n")
        
        home_data = await client.get_home_data(user_data)
        
        print("=" * 60)
        print("DEVICE ANALYSIS")
        print("=" * 60)
        
        for device in home_data.devices:
            product = next(
                (p for p in home_data.products if p.id == device.product_id),
                None
            )
            
            if product:
                print(f"\n📱 {device.name}")
                print(f"   Model: {product.model}")
                print(f"   Category: {product.category}")
                print(f"   Category Name: {product.category.name}")
                print(f"   Category Value: {product.category.value}")
                print(f"   Online: {device.online}")
                
                if product.category == RoborockCategory.WASHING_MACHINE:
                    print("   ⚠️  This is a WASHING MACHINE (Zeo)")
                elif product.category == RoborockCategory.VACUUM:
                    print("   ✅ This is a VACUUM")
                elif product.category == RoborockCategory.WET_DRY_VAC:
                    print("   ✅ This is a WET/DRY VAC (Dyad)")
                else:
                    print(f"   ❓ Unknown category: {product.category}")
        
        print("\n" + "=" * 60)
        print("SUMMARY")
        print("=" * 60)
        
        vacuums = [d for d in home_data.devices if any(
            p.id == d.product_id and p.category == RoborockCategory.VACUUM
            for p in home_data.products
        )]
        washing_machines = [d for d in home_data.devices if any(
            p.id == d.product_id and p.category == RoborockCategory.WASHING_MACHINE
            for p in home_data.products
        )]
        
        print(f"\nVacuums found: {len(vacuums)}")
        print(f"Washing machines found: {len(washing_machines)}")
        
        if washing_machines:
            print("\n🎯 Zeo washing machine detected!")
            print("   The integration should now skip this device gracefully.")
        
    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_zeo_detection())
