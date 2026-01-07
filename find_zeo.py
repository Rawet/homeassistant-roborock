#!/usr/bin/env python3
"""
Comprehensive search for Zeo One in API data.
"""
import asyncio
import json
from roborock.web_api import RoborockApiClient
from roborock import RoborockCategory

USERNAME = "dennis.rawet@gmail.com"

async def find_zeo():
    """Find Zeo One in all possible locations."""
    print("=" * 60)
    print("Comprehensive Zeo One Search")
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
        print("SEARCHING FOR ZEO ONE")
        print("=" * 60)
        
        # Search in devices
        print("\n1️⃣ Checking home_data.devices...")
        zeo_devices = []
        for device in home_data.devices:
            product = next((p for p in home_data.products if p.id == device.product_id), None)
            if product and product.category == RoborockCategory.WASHING_MACHINE:
                zeo_devices.append((device, product))
                print(f"   ✅ FOUND: {device.name}")
                print(f"      DUID: {device.duid}")
                print(f"      Product ID: {device.product_id}")
                print(f"      Model: {product.model}")
                print(f"      Online: {device.online}")
        
        if not zeo_devices:
            print("   ❌ No Zeo devices in home_data.devices")
        
        # Search in received_devices
        print("\n2️⃣ Checking home_data.received_devices...")
        zeo_received = []
        for device in home_data.received_devices:
            product = next((p for p in home_data.products if p.id == device.product_id), None)
            if product and product.category == RoborockCategory.WASHING_MACHINE:
                zeo_received.append((device, product))
                print(f"   ✅ FOUND (shared): {device.name}")
                print(f"      DUID: {device.duid}")
                print(f"      Product ID: {device.product_id}")
                print(f"      Model: {product.model}")
                print(f"      Online: {device.online}")
        
        if not zeo_received:
            print("   ❌ No Zeo devices in home_data.received_devices")
        
        # Check products
        print("\n3️⃣ Checking home_data.products...")
        zeo_products = [p for p in home_data.products if p.category == RoborockCategory.WASHING_MACHINE]
        if zeo_products:
            for product in zeo_products:
                print(f"   ℹ️  Product available: {product.name}")
                print(f"      ID: {product.id}")
                print(f"      Model: {product.model}")
                print(f"      Category: {product.category.name}")
                has_device = any(d.product_id == product.id for d in home_data.devices + home_data.received_devices)
                print(f"      Has registered device: {has_device}")
        else:
            print("   ❌ No Zeo products found")
        
        print("\n" + "=" * 60)
        print("SUMMARY")
        print("=" * 60)
        
        total_zeo = len(zeo_devices) + len(zeo_received)
        if total_zeo > 0:
            print(f"\n🎉 SUCCESS! Found {total_zeo} Zeo One device(s)!")
            print("\n✅ We can implement full Zeo support!")
            
            # Show device details
            for device, product in (zeo_devices + zeo_received):
                print(f"\nDevice details for implementation:")
                print(f"  Name: {device.name}")
                print(f"  DUID: {device.duid}")
                print(f"  Model: {product.model}")
                print(f"  Online: {device.online}")
                
                # Try to get more device info
                if hasattr(device, '__dict__'):
                    print(f"\n  Full device attributes:")
                    for key, value in device.__dict__.items():
                        if not key.startswith('_'):
                            print(f"    {key}: {value}")
        else:
            print("\n❌ No Zeo One devices found in API response")
            print("\nPossible reasons:")
            print("  1. Zeo One not registered in the Roborock app")
            print("  2. Zeo One registered on a different account")
            print("  3. Zeo One registered in a different 'home' in the app")
            print("  4. Need to check if Zeo One appears in the app")
            print("\n💡 Check your Roborock app - does Zeo One appear there?")
        
    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(find_zeo())
