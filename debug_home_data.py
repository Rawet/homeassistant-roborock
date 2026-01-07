#!/usr/bin/env python3
"""
Debug script to show all home data.
"""
import asyncio
import json
from roborock.web_api import RoborockApiClient

USERNAME = "dennis.rawet@gmail.com"

async def debug_home_data():
    """Show all home data."""
    print("=" * 60)
    print("Home Data Debug")
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
        print("RAW HOME DATA")
        print("=" * 60)
        print(f"\nTotal devices: {len(home_data.devices)}")
        print(f"Total received_devices: {len(home_data.received_devices)}")
        print(f"Total products: {len(home_data.products)}")
        
        print("\n" + "=" * 60)
        print("DEVICES")
        print("=" * 60)
        for i, device in enumerate(home_data.devices, 1):
            print(f"\n[{i}] {device.name}")
            print(f"    duid: {device.duid}")
            print(f"    product_id: {device.product_id}")
            print(f"    online: {device.online}")
        
        print("\n" + "=" * 60)
        print("RECEIVED DEVICES (shared)")
        print("=" * 60)
        if home_data.received_devices:
            for i, device in enumerate(home_data.received_devices, 1):
                print(f"\n[{i}] {device.name}")
                print(f"    duid: {device.duid}")
                print(f"    product_id: {device.product_id}")
                print(f"    online: {device.online}")
        else:
            print("None")
        
        print("\n" + "=" * 60)
        print("PRODUCTS")
        print("=" * 60)
        for i, product in enumerate(home_data.products, 1):
            print(f"\n[{i}] {product.name}")
            print(f"    id: {product.id}")
            print(f"    model: {product.model}")
            print(f"    category: {product.category}")
            print(f"    category.name: {product.category.name}")
            print(f"    category.value: {product.category.value}")
            
            # Check if any device uses this product
            device_count = sum(1 for d in home_data.devices if d.product_id == product.id)
            received_device_count = sum(1 for d in home_data.received_devices if d.product_id == product.id)
            print(f"    used by {device_count} devices")
            print(f"    used by {received_device_count} received_devices")
        
        print("\n" + "=" * 60)
        print("ANALYSIS")
        print("=" * 60)
        
        # Find products without devices
        products_without_devices = [
            p for p in home_data.products
            if not any(d.product_id == p.id for d in home_data.devices + home_data.received_devices)
        ]
        
        if products_without_devices:
            print(f"\n⚠️  Found {len(products_without_devices)} products without devices:")
            for p in products_without_devices:
                print(f"   - {p.name} ({p.model}) - {p.category.name}")
                print(f"     This means you have access to this product type but no actual device")
        
    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(debug_home_data())
