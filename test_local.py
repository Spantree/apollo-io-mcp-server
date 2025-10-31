#!/usr/bin/env python3
"""
Local test script for Apollo.io bulk operations and usage stats.

This script demonstrates the new functionality without requiring real API calls
by using the unit test approach with mocked responses.
"""
import asyncio
from apollo_client import ApolloClient
import os

async def test_with_real_api():
    """Test with real API (requires APOLLO_IO_API_KEY environment variable)"""
    api_key = os.getenv('APOLLO_IO_API_KEY')

    if not api_key:
        print("❌ APOLLO_IO_API_KEY not set. Set it to test with real API.")
        print("   export APOLLO_IO_API_KEY='your_key_here'")
        return

    client = ApolloClient(api_key=api_key)

    print("=" * 60)
    print("Testing Apollo.io Bulk Operations & Usage Stats")
    print("=" * 60)

    # Test 1: Usage Stats (master API key required)
    print("\n📊 Test 1: Getting API Usage Stats...")
    try:
        stats = await client.usage_stats()
        if stats:
            print("✅ Usage stats retrieved successfully!")
            stats_dict = stats.model_dump()

            # Display a few endpoints
            for endpoint_name in list(stats_dict.keys())[:3]:
                endpoint_stats = stats_dict[endpoint_name]
                if isinstance(endpoint_stats, dict) and 'day' in endpoint_stats:
                    print(f"\n   {endpoint_name}:")
                    print(f"   - Daily: {endpoint_stats['day']['consumed']}/{endpoint_stats['day']['limit']} used")
                    print(f"   - Remaining: {endpoint_stats['day']['left_over']}")
        else:
            print("❌ Failed to get usage stats (may need master API key)")
    except Exception as e:
        print(f"❌ Error: {e}")

    # Test 2: Bulk Create (creates test contacts)
    print("\n📝 Test 2: Bulk Creating Test Contacts...")
    try:
        import time
        timestamp = int(time.time())

        contacts = [
            {
                "first_name": "Test",
                "last_name": "User1",
                "email": f"test-bulk-1-{timestamp}@example.com",
                "title": "Test Engineer",
                "organization_name": "Test Corp",
                "label_names": ["MCP Test"]
            },
            {
                "first_name": "Test",
                "last_name": "User2",
                "email": f"test-bulk-2-{timestamp}@example.com",
                "title": "Test Manager",
                "organization_name": "Test Corp",
                "label_names": ["MCP Test"]
            }
        ]

        result = await client.contact_bulk_create(contacts=contacts)
        if result:
            print(f"✅ Bulk create completed!")
            print(f"   - Created: {len(result.created_contacts)} contacts")
            print(f"   - Existing: {len(result.existing_contacts)} contacts")

            # Store IDs for bulk update test
            contact_ids = [c.get('id') for c in result.created_contacts if c.get('id')]

            # Test 3: Bulk Update (if we created contacts)
            if contact_ids:
                print("\n✏️  Test 3: Bulk Updating Contacts...")
                update_contacts = [
                    {
                        "id": contact_ids[0],
                        "title": "Senior Test Engineer"
                    }
                ]

                if len(contact_ids) > 1:
                    update_contacts.append({
                        "id": contact_ids[1],
                        "title": "Senior Test Manager"
                    })

                update_result = await client.contact_bulk_update(contacts=update_contacts)
                if update_result:
                    print(f"✅ Bulk update completed!")
                    print(f"   - Updated: {len(update_result.contacts)} contacts")
                else:
                    print("❌ Bulk update failed")
        else:
            print("❌ Bulk create failed")

    except Exception as e:
        print(f"❌ Error: {e}")

    print("\n" + "=" * 60)
    print("✅ Testing complete!")
    print("=" * 60)

async def show_examples():
    """Show usage examples without making API calls"""
    print("=" * 60)
    print("Apollo.io Bulk Operations - Usage Examples")
    print("=" * 60)

    print("\n1️⃣  Bulk Create Example:")
    print("""
    result = await client.contact_bulk_create(
        contacts=[
            {
                "first_name": "Alice",
                "last_name": "Smith",
                "email": "alice@example.com",
                "title": "Product Manager",
                "organization_name": "Test Corp",
                "label_names": ["Hot Leads"]
            },
            {
                "first_name": "Bob",
                "last_name": "Jones",
                "email": "bob@testco.com",
                "title": "Engineer"
            }
        ]
    )

    # Returns:
    # - created_contacts: Newly created contacts
    # - existing_contacts: Contacts that already existed (not updated)
    """)

    print("\n2️⃣  Bulk Update Example:")
    print("""
    result = await client.contact_bulk_update(
        contacts=[
            {
                "id": "contact_id_1",
                "title": "Senior Product Manager",
                "label_names": ["Hot Leads", "Q1 2024"]
            },
            {
                "id": "contact_id_2",
                "email": "newemail@example.com"
            }
        ]
    )
    """)

    print("\n3️⃣  Usage Stats Example:")
    print("""
    stats = await client.usage_stats()

    # Returns rate limits per endpoint:
    # - minute, hour, day limits
    # - consumed, left_over counts
    # Note: Requires master API key
    """)

    print("\n" + "=" * 60)

if __name__ == "__main__":
    print("\n🚀 Apollo.io Bulk Operations Test Script\n")

    # Check if API key is set
    if os.getenv('APOLLO_IO_API_KEY'):
        print("✅ APOLLO_IO_API_KEY is set")
        print("\n⚠️  This will create real test contacts in your Apollo CRM!")
        print("   Press Ctrl+C to cancel, or Enter to continue...")
        try:
            input()
            asyncio.run(test_with_real_api())
        except KeyboardInterrupt:
            print("\n\n❌ Cancelled by user")
    else:
        print("ℹ️  APOLLO_IO_API_KEY not set - showing examples only\n")
        asyncio.run(show_examples())
        print("\n💡 To test with real API:")
        print("   export APOLLO_IO_API_KEY='your_key_here'")
        print("   uv run python test_local.py")
