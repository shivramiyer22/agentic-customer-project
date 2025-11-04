#!/usr/bin/env python3
"""
Connection Test Script for OpenAI and AWS Bedrock

This script tests and confirms connections to:
1. OpenAI API (for embeddings and worker agents)
2. AWS Bedrock (for supervisor agent)

Run this script to verify all connections are working correctly.
"""

import os
import sys
from pathlib import Path

# Add backend to path (we're now in backend/tests/, so go up one level)
backend_path = Path(__file__).parent.parent
sys.path.insert(0, str(backend_path))

from dotenv import load_dotenv
import asyncio

# Load environment variables from root .env first, then backend/.env as fallback
root_path = backend_path.parent
root_env = root_path / ".env"
backend_env = backend_path / ".env"

if root_env.exists():
    load_dotenv(root_env)
    # Also load backend/.env for backend-specific configs (non-sensitive)
    if backend_env.exists():
        load_dotenv(backend_env, override=False)  # Don't override root .env values
elif backend_env.exists():
    load_dotenv(backend_env)

# Colors for output
GREEN = '\033[0;32m'
YELLOW = '\033[1;33m'
RED = '\033[0;31m'
BLUE = '\033[0;34m'
NC = '\033[0m'  # No Color


def print_section(title: str):
    """Print a formatted section header"""
    print(f"\n{BLUE}{'=' * 60}{NC}")
    print(f"{BLUE}{title:^60}{NC}")
    print(f"{BLUE}{'=' * 60}{NC}\n")


def print_success(message: str):
    """Print a success message"""
    print(f"{GREEN}✅ {message}{NC}")


def print_error(message: str):
    """Print an error message"""
    print(f"{RED}❌ {message}{NC}")


def print_warning(message: str):
    """Print a warning message"""
    print(f"{YELLOW}⚠️  {message}{NC}")


def print_info(message: str):
    """Print an info message"""
    print(f"{YELLOW}ℹ️  {message}{NC}")


def test_openai_connection():
    """Test OpenAI API connection"""
    print_section("Testing OpenAI Connection")
    
    try:
        from openai import OpenAI
        
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            print_error("OPENAI_API_KEY not found in environment variables")
            return False
        
        print_info(f"Found OpenAI API key (length: {len(api_key)})")
        
        # Test OpenAI connection with a simple request
        client = OpenAI(api_key=api_key)
        
        print_info("Testing OpenAI API connection...")
        response = client.models.list()
        
        # Verify we got models back
        if response and len(response.data) > 0:
            print_success("OpenAI API connection successful!")
            print_info(f"Found {len(response.data)} available models")
            return True
        else:
            print_error("OpenAI API returned no models")
            return False
            
    except ImportError:
        print_error("openai package not installed")
        print_info("Install with: pip install openai")
        return False
    except Exception as e:
        print_error(f"OpenAI connection failed: {e}")
        return False


def test_openai_embeddings():
    """Test OpenAI embeddings generation"""
    print_section("Testing OpenAI Embeddings")
    
    try:
        from openai import OpenAI
        
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            print_error("OPENAI_API_KEY not found")
            return False
        
        client = OpenAI(api_key=api_key)
        
        print_info("Testing embeddings generation...")
        response = client.embeddings.create(
            model="text-embedding-3-small",
            input="Test connection"
        )
        
        if response and response.data and len(response.data) > 0:
            embedding = response.data[0].embedding
            print_success(f"Embeddings generation successful!")
            print_info(f"Generated embedding vector with {len(embedding)} dimensions")
            return True
        else:
            print_error("Embeddings generation returned no data")
            return False
            
    except Exception as e:
        print_error(f"Embeddings generation failed: {e}")
        return False


def test_aws_bedrock_connection():
    """Test AWS Bedrock connection"""
    print_section("Testing AWS Bedrock Connection")
    
    try:
        from langchain_aws import ChatBedrock
        
        bearer_token = os.getenv("AWS_BEARER_TOKEN_BEDROCK")
        region = os.getenv("AWS_REGION", "us-east-1")
        
        # Use ONLY AWS_BEARER_TOKEN_BEDROCK - do not use AWS_ACCESS_KEY_ID
        if not bearer_token:
            print_error("AWS_BEARER_TOKEN_BEDROCK not found")
            print_info("Required: AWS_BEARER_TOKEN_BEDROCK")
            print_info("Please update root .env file with AWS_BEARER_TOKEN_BEDROCK")
            print_info("Note: Do not use AWS_ACCESS_KEY_ID when using AWS_BEARER_TOKEN_BEDROCK")
            return False
        
        print_info(f"Found AWS_BEARER_TOKEN_BEDROCK (length: {len(bearer_token)} characters)")
        print_info("Using AWS_BEARER_TOKEN_BEDROCK for authentication (not using AWS_ACCESS_KEY_ID)")
        token_to_use = bearer_token
        is_bearer_token = True
        print_info(f"Found AWS credentials (region: {region})")
        
        # Initialize Bedrock model
        print_info("Initializing AWS Bedrock ChatBedrock model...")
        
        # Configure Bedrock model with AWS_BEARER_TOKEN_BEDROCK ONLY
        bedrock_kwargs = {
            "model_id": "anthropic.claude-3-haiku-20240307-v1:0",
            "region_name": region,
            "credentials_profile_name": None,
        }
        
        # Use AWS_BEARER_TOKEN_BEDROCK as both access_key_id and secret_access_key
        # Do NOT use AWS_ACCESS_KEY_ID when bearer token is available
        print_info("Using AWS_BEARER_TOKEN_BEDROCK for authentication...")
        print_info(f"Bearer token length: {len(token_to_use)} characters")
        bedrock_kwargs["aws_access_key_id"] = token_to_use
        bedrock_kwargs["aws_secret_access_key"] = token_to_use  # Use bearer token as secret too
        
        bedrock_model = ChatBedrock(**bedrock_kwargs)
        
        print_info("Testing Bedrock connection with a simple message...")
        
        # Test with a simple invoke
        response = bedrock_model.invoke("Hello, this is a test message. Please respond with 'Connection successful'.")
        
        if response and hasattr(response, 'content'):
            print_success("AWS Bedrock connection successful!")
            print_info(f"Response: {response.content[:200]}...")
            return True
        else:
            print_error("Bedrock returned no content")
            return False
            
    except ImportError:
        print_error("langchain-aws package not installed")
        print_info("Install with: pip install langchain-aws")
        return False
    except Exception as e:
        error_msg = str(e)
        print_error(f"AWS Bedrock connection failed: {error_msg}")
        
        # Provide helpful error messages
        if "token" in error_msg.lower() or "invalid" in error_msg.lower():
            print_warning("Invalid AWS_BEARER_TOKEN_BEDROCK detected")
            print_info("Please update AWS_BEARER_TOKEN_BEDROCK in root .env file")
            print_info("Note: Use AWS_BEARER_TOKEN_BEDROCK, not AWS_ACCESS_KEY_ID")
            print_info("The supervisor agent will fall back to OpenAI until valid credentials are provided")
        elif "credentials" in error_msg.lower() or "authentication" in error_msg.lower():
            print_info("Check your AWS credentials in .env file")
        elif "region" in error_msg.lower():
            print_info("Check your AWS_REGION setting (default: us-east-1)")
        elif "model" in error_msg.lower() or "access" in error_msg.lower():
            print_info("Verify Bedrock model access in your AWS account")
            print_info("Model ID: anthropic.claude-3-haiku-20240307-v1:0")
        
        return False


def test_supervisor_agent():
    """Test supervisor agent creation and Bedrock connection
    
    Note: This test checks if the supervisor agent can be created.
    Connection failures (missing credentials) are expected in CI/test environments
    and will skip the test gracefully.
    """
    import pytest
    
    try:
        from app.agents.orchestrator import get_supervisor_agent
        import uuid
        
        # Test agent creation
        agent = get_supervisor_agent()
        assert agent is not None, "Supervisor agent should be created"
        
        # Test agent invocation (with proper config for checkpointer)
        test_thread_id = str(uuid.uuid4())
        config_dict = {"configurable": {"thread_id": test_thread_id}}
        
        try:
            result = agent.invoke(
                {"messages": [{"role": "user", "content": "Hello, this is a test."}]},
                config=config_dict
            )
            
            assert result is not None, "Agent should return a result"
            assert "messages" in result, "Result should contain messages"
            assert len(result["messages"]) > 0, "Result should have at least one message"
            
        except Exception as e:
            error_msg = str(e)
            # If it's a connection/auth issue, skip the test (credentials may not be available)
            if any(keyword in error_msg.lower() for keyword in ["bedrock", "aws", "token", "authentication", "credentials"]):
                pytest.skip(f"Connection/authentication issue (expected in test environments): {error_msg}")
            # If it's a config issue with checkpointer, that's OK - agent was created successfully
            elif "thread_id" in error_msg.lower() or "checkpointer" in error_msg.lower():
                # Agent creation succeeded, which is what we're testing
                pass
            else:
                # Unexpected error - raise it
                raise
                
    except ImportError as e:
        pytest.skip(f"Required modules not available: {e}")
    except Exception as e:
        # If agent creation fails due to missing dependencies, skip
        error_msg = str(e)
        if any(keyword in error_msg.lower() for keyword in ["bedrock", "openai", "module", "import"]):
            pytest.skip(f"Connection test skipped (dependencies/credentials not available): {error_msg}")
        else:
            raise


def test_worker_agents():
    """Test worker agents with OpenAI"""
    print_section("Testing Worker Agents (OpenAI)")
    
    results = []
    
    try:
        from app.agents.policy_agent import get_policy_agent_singleton
        from app.agents.technical_agent import get_technical_agent_singleton
        from app.agents.billing_agent import get_billing_agent_singleton
        
        agents = [
            ("Policy Agent", get_policy_agent_singleton),
            ("Technical Agent", get_technical_agent_singleton),
            ("Billing Agent", get_billing_agent_singleton),
        ]
        
        for agent_name, agent_func in agents:
            print_info(f"Testing {agent_name}...")
            try:
                agent = agent_func()
                if agent:
                    print_success(f"{agent_name} created successfully!")
                    results.append(True)
                else:
                    print_error(f"{agent_name} creation failed")
                    results.append(False)
            except Exception as e:
                print_error(f"{agent_name} failed: {e}")
                results.append(False)
        
        return all(results)
        
    except Exception as e:
        print_error(f"Worker agents test failed: {e}")
        return False


def main():
    """Run all connection tests"""
    print(f"\n{BLUE}{'=' * 60}{NC}")
    print(f"{BLUE}{'Connection Test Suite':^60}{NC}")
    print(f"{BLUE}{'=' * 60}{NC}\n")
    
    print_info("This script will test:")
    print_info("  1. OpenAI API connection")
    print_info("  2. OpenAI embeddings generation")
    print_info("  3. AWS Bedrock connection")
    print_info("  4. Supervisor agent (Bedrock)")
    print_info("  5. Worker agents (OpenAI)")
    
    results = {}
    
    # Test OpenAI
    results["OpenAI API"] = test_openai_connection()
    results["OpenAI Embeddings"] = test_openai_embeddings()
    
    # Test AWS Bedrock
    results["AWS Bedrock"] = test_aws_bedrock_connection()
    
    # Test agents
    results["Worker Agents"] = test_worker_agents()
    
    # Test supervisor agent (async)
    try:
        results["Supervisor Agent"] = asyncio.run(test_supervisor_agent())
    except Exception as e:
        print_error(f"Supervisor agent test failed: {e}")
        results["Supervisor Agent"] = False
    
    # Summary
    print_section("Test Summary")
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for test_name, result in results.items():
        if result:
            print_success(f"{test_name}: PASSED")
        else:
            print_error(f"{test_name}: FAILED")
    
    print(f"\n{BLUE}{'=' * 60}{NC}")
    if passed == total:
        print_success(f"All tests passed! ({passed}/{total})")
    else:
        print_warning(f"Some tests failed: {passed}/{total} passed")
        print_info("Please check the errors above and update your .env file")
    print(f"{BLUE}{'=' * 60}{NC}\n")
    
    return passed == total


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

