#!/usr/bin/env python3
"""
Query Zeo One washing machine for available data and commands.
"""
import asyncio
import json
from roborock.web_api import RoborockApiClient
from roborock import RoborockCategory
from roborock.version_1_apis import RoborockMqttClientV1 as RoborockMqttClient

USERNAME = "dennis.rawet@gmail.com"

async def query_zeo():
    """Query Zeo One for available data."""
    print("=" * 60)
    print("Zeo One Status Query")
    print("=" * 60)
    print(f"\nLogging in as: {USERNAME}\n")
    
    try:
        client = RoborockApiClient(USERNAME, "https://euiot.roborock.com")
        await client.request_code()
        print(f"✓ Verification code sent")
        
        code = input("Enter verification code: ").strip()
        user_data = await client.code_login(code)
        print("✓ Login successful!\n")
        
        home_data = await client.get_home_data_v2(user_data)
        
        # Find Zeo One
        zeo_device = None
        for device in home_data.devices:
            product = next((p for p in home_data.products if p.id == device.product_id), None)
            if product and product.category == RoborockCategory.WASHING_MACHINE:
                zeo_device = device
                zeo_product = product
                break
        
        if not zeo_device:
            print("❌ No Zeo One found!")
            return
        
        print("=" * 60)
        print("ZEO ONE FOUND")
        print("=" * 60)
        print(f"Name: {zeo_device.name}")
        print(f"Model: {zeo_product.model}")
        print(f"Online: {zeo_device.online}")
        print(f"DUID: {zeo_device.duid}")
        
        # Create device info for API client
        class DeviceInfo:
            def __init__(self, device, model):
                self.device = device
                self.model = model
        
        device_info = DeviceInfo(zeo_device, zeo_product.model)
        
        # Connect via MQTT
        print("\n" + "=" * 60)
        print("CONNECTING TO ZEO ONE")
        print("=" * 60)
        
        mqtt_client = RoborockMqttClient(user_data, device_info)
        await mqtt_client.async_connect()
        
        print("✓ Connected!\n")
        
        # Try various commands to get status
        print("=" * 60)
        print("QUERYING STATUS")
        print("=" * 60)
        
        commands_to_try = [
            ("get_status", []),
            ("get_prop", []),
            ("app_get_dryer_status", []),
            ("app_get_wash_status", []),
        ]
        
        for cmd_name, params in commands_to_try:
            try:
                print(f"\nTrying: {cmd_name}({params})")
                result = await mqtt_client.send_command(cmd_name, params)
                print(f"  ✅ Success!")
                print(f"  Result: {json.dumps(result, indent=2, default=str)}")
            except Exception as e:
                print(f"  ❌ Failed: {e}")
        
        # Check the product schema for available properties
        print("\n" + "=" * 60)
        print("AVAILABLE PROPERTIES (from product schema)")
        print("=" * 60)
        
        for i, schema_item in enumerate(zeo_product.schema[:20], 1):
            print(f"\n{i}. {schema_item.name} ({schema_item.code})")
            print(f"   Type: {schema_item.type}")
            print(f"   Mode: {schema_item.mode}")
            if schema_item.property:
                print(f"   Property: {schema_item.property}")
        
        if len(zeo_product.schema) > 20:
            print(f"\n... and {len(zeo_product.schema) - 20} more")
        
        await mqtt_client.async_disconnect()
        
    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(query_zeo())
