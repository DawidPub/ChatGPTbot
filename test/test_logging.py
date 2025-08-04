# Test the new logging functionality
import time

def test_response_callback():
    """Test the response callback functionality"""
    
    # Simulate response text
    test_response = """Here's a comprehensive answer about Pydantic AI:

Pydantic AI is a Python library that combines the power of Pydantic for data validation with AI/LLM capabilities.

Key features include:
1. Type-safe AI interactions
2. Automatic validation of inputs and outputs
3. Structured data handling
4. Integration with popular LLM providers

This makes it easier to build reliable AI applications with proper data validation."""
    
    def status_callback(message):
        print(f"STATUS: {message}")
    
    def response_callback(text):
        print(f"RESPONSE UPDATE:\n{text}\n{'='*50}")
    
    def log_response_line(line, line_number=None):
        if line_number is not None:
            print(f"LINE {line_number}: {line[:100]}{'...' if len(line) > 100 else ''}")
        else:
            print(f"RESPONSE LINE: {line[:100]}{'...' if len(line) > 100 else ''}")
    
    # Test the logging functionality
    print("Testing response line logging:")
    print("-" * 40)
    
    lines = test_response.split('\n')
    for line_num, line in enumerate(lines, 1):
        if line.strip():  # Only log non-empty lines
            log_response_line(line.strip(), line_num)
    
    print("\nTesting response callback:")
    print("-" * 40)
    response_callback(test_response)
    
    print("\nTest completed successfully!")

if __name__ == "__main__":
    test_response_callback()
