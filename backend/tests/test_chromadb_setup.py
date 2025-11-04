"""
Test script to verify ChromaDB setup and three collections are created successfully
"""

import sys
import os

# Add app directory to path (we're now in backend/tests/, so go up one level to backend/)
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from app.retrieval.chroma_client import get_chroma_client, initialize_collections
    from app.utils.config import config
    from app.utils.logger import app_logger
    
    print("=" * 60)
    print("Testing ChromaDB Setup")
    print("=" * 60)
    
    # Validate configuration
    print("\n1. Validating configuration...")
    config_errors = config.validate()
    if config_errors:
        print(f"❌ Configuration errors found:")
        for error in config_errors:
            print(f"   - {error}")
        sys.exit(1)
    else:
        print("✅ Configuration valid")
        print(f"   - ChromaDB path: {config.CHROMA_DB_PATH}")
        print(f"   - Embedding model: {config.OPENAI_EMBEDDING_MODEL}")
        print(f"   - Embedding dimensions: {config.OPENAI_EMBEDDING_DIMENSIONS}")
    
    # Initialize ChromaDB client
    print("\n2. Initializing ChromaDB client...")
    try:
        client = get_chroma_client()
        print("✅ ChromaDB client initialized")
    except Exception as e:
        print(f"❌ Failed to initialize ChromaDB client: {e}")
        sys.exit(1)
    
    # Initialize collections
    print("\n3. Initializing knowledge base collections...")
    try:
        collections = initialize_collections()
        print(f"✅ Initialized {len(collections)} collections:")
        for name in collections.keys():
            print(f"   - {name}")
    except Exception as e:
        print(f"❌ Failed to initialize collections: {e}")
        sys.exit(1)
    
    # Verify collections exist
    print("\n4. Verifying collections exist in ChromaDB...")
    try:
        all_collections = client.list_collections()
        print(f"✅ Found {len(all_collections)} collections in ChromaDB:")
        for name in all_collections:
            print(f"   - {name}")
        
        # Check if all required collections exist
        required_collections = config.get_all_collections()
        missing_collections = set(required_collections) - set(all_collections)
        
        if missing_collections:
            print(f"\n⚠️  Missing collections: {missing_collections}")
        else:
            print("\n✅ All required collections are present")
            
    except Exception as e:
        print(f"❌ Failed to list collections: {e}")
        sys.exit(1)
    
    # Test collection access
    print("\n5. Testing collection access...")
    try:
        for collection_name in config.get_all_collections():
            collection = client.get_collection(collection_name)
            if collection:
                print(f"✅ Successfully accessed collection: {collection_name}")
            else:
                print(f"❌ Failed to access collection: {collection_name}")
                sys.exit(1)
    except Exception as e:
        print(f"❌ Failed to access collections: {e}")
        sys.exit(1)
    
    print("\n" + "=" * 60)
    print("✅ All ChromaDB setup tests passed!")
    print("=" * 60)
    
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("\nPlease install dependencies first:")
    print("  pip install -r requirements.txt")
    sys.exit(1)
except Exception as e:
    print(f"❌ Unexpected error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

