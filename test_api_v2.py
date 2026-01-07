#!/usr/bin/env python3
"""
Test get_home_data_v2 API to find Zeo One.
"""
import asyncio
from roborock.web_api import RoborockApiClient
from roborock import RoborockCategory

USERNAME = "dennis.rawet@gmail.com"

async def test_v2_api():
    """Test v2 API."""
    print("=" * 60)
    print("Testing get_home_data_v2 API")
    print("=" * 60)
    print(f"\nLogging in as: {USERNAME}\n")
    
    try:
        client = RoborockApiClient(USERNAME, "https://euiot.roborock.com")
        await client.request_code()
        print(f"✓ Verification code sent")
        
        code = input("Enter verification code: ").strip()
        user_data = await client.code_login(code)
        print("✓ Login successful!\n")
        
        # Try v1 API
        print("=" * 60)
        print("V1 API (get_home_data)")
        print("=" * 60)
        home_data_v1 = await client.get_home_data(user_data)
        print(f"Devices: {len(home_data_v1.devices)}")
        print(f"Received devices: {len(home_data_v1.received_devices)}")
        print(f"Products: {len(home_data_v1.products)}")
        
        # Try v2 API
        print("\n" + "=" * 60)
        print("V2 API (get_home_data_v2)")
        print("=" * 60)
        try:
            home_data_v2 = await client.get_home_data_v2(user_data)
            print(f"✓ V2 API call succeeded!")
            print(f"\nV2 Devices: {len(home_data_v2.devices)}")
            print(f"V2 Received devices: {len(home_data_v2.received_devices)}")
            print(f"V2 Products: {len(home_data_v2.products)}")
            
            # Compare
            print("\n" + "=" * 60)
            print("COMPARISON")
            print("=" * 60)
            
            v1_device_ids = {d.duid for d in home_data_v1.devices}
            v2_device_ids = {d.duid for d in home_data_v2.devices}
            
            new_in_v2 = v2_device_ids - v1_device_ids
            if new_in_v2:
                print(f"\n🎉 V2 API found {len(new_in_v2)} additional device(s)!")
                for duid in new_in_v2:
                    device = next(d for d in home_data_v2.devices if d.duid == duid)
                    product = next((p for p in home_data_v2.products if p.id == device.product_id), None)
                    print(f"\n  New device: {device.name}")
                    print(f"    DUID: {device.duid}")
                    print(f"    Model: {product.model if product else 'Unknown'}")
                    print(f"    Category: {product.category.name if product else 'Unknown'}")
                    print(f"    Online: {device.online}")
                    
                    if product and product.category == RoborockCategory.WASHING_MACHINE:
                        print(f"    ⭐ THIS IS ZEO ONE!")
            else:
                print("\n❌ No additional devices in V2 API")
            
            # List all V2 devices
            print("\n" + "=" * 60)
            print("ALL V2 DEVICES")
            print("=" * 60)
            for device in home_data_v2.devices:
                product = next((p for p in home_data_v2.products if p.id == device.product_id), None)
                category_name = product.category.name if product else "Unknown"
                print(f"\n  {device.name}")
                print(f"    Category: {category_name}")
                print(f"    Online: {device.online}")
                
        except Exception as e:
            print(f"❌ V2 API failed: {e}")
            import traceback
            traceback.print_exc()
        
    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_v2_api())
