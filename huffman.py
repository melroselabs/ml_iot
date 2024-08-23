# Filename: huffman.py

# Command-line: python3 huffman.py -m '{"deviceId":"01:23:45:67:89:ab:cd:ef"}' -w '"deviceId"'

import heapq
import argparse
import json
from collections import Counter, defaultdict

# Define a class for the nodes in the Huffman tree
class HuffmanNode:
    def __init__(self, freq, symbol=None, left=None, right=None):
        self.freq = freq
        self.symbol = symbol
        self.left = left
        self.right = right
    
    def __lt__(self, other):
        return self.freq < other.freq

# Burrows-Wheeler Transform function
def bwt_transform(text):
    n = len(text)
    m = sorted([text[i:] + text[:i] for i in range(n)])
    last_column = [row[-1] for row in m]
    return ''.join(last_column), m.index(text)

# Burrows-Wheeler Inverse Transform function
def bwt_inverse(last_column, index):
    n = len(last_column)
    table = [""] * n
    for _ in range(n):
        table = sorted([last_column[i] + table[i] for i in range(n)])
    return table[index]

# Function to build the Huffman tree
def build_huffman_tree(symbols_with_freq):
    heap = [HuffmanNode(freq, symbol) for symbol, freq in symbols_with_freq.items()]
    heapq.heapify(heap)
    
    while len(heap) > 1:
        node1 = heapq.heappop(heap)
        node2 = heapq.heappop(heap)
        merged_node = HuffmanNode(node1.freq + node2.freq, left=node1, right=node2)
        heapq.heappush(heap, merged_node)
    
    return heap[0]

# Function to generate the Huffman codes by traversing the tree
def generate_huffman_codes(node, prefix="", huffman_codes={}):
    if node is not None:
        if node.symbol is not None:
            huffman_codes[node.symbol] = prefix
        generate_huffman_codes(node.left, prefix + "0", huffman_codes)
        generate_huffman_codes(node.right, prefix + "1", huffman_codes)
    return huffman_codes

# Function to encode a message using the Huffman codes
def huffman_encode(message, huffman_codes):
    # Sort the symbols by length in descending order to prioritize longer symbols
    sorted_symbols = sorted(huffman_codes.keys(), key=len, reverse=True)
    
    encoded_segments = []  # This will store tuples of (index, huffman_code)
    
    message_working = message
    
    # Process each symbol length in turn
    for symbol in sorted_symbols:
        start = 0  # Start search from the beginning of the message
        while start < len(message):
            # Find the index of the symbol in the message
            index = message.find(symbol, start)
            if index == -1:  # If the symbol is not found, break the loop
                break
            # Store the (index, huffman_code) in the encoded_segments array
            encoded_segments.append((index, huffman_codes[symbol]))
            print(f"Found '{symbol}' at position {index} -> encoding as '{huffman_codes[symbol]}'")
            # Replace the found symbol in the message with * characters
            message = message[:index] + '\0' * len(symbol) + message[index + len(symbol):]
            message_working = message[:index] + '*' * len(symbol) + message[index + len(symbol):]
            
            print(message_working)
            # Move start beyond this occurrence for the next search
            start = index + len(symbol)

    # Sort encoded segments by index to ensure they are in the correct order
    encoded_segments.sort(key=lambda x: x[0])

    # Build the final encoded message by concatenating the Huffman codes in order
    encoded_message = "".join(code for _, code in encoded_segments)
    
    return encoded_message

# Function to decode an encoded message using the Huffman tree
def huffman_decode(encoded_message, huffman_codes):
    # Reverse the Huffman codes to create a decoding map
    reverse_huffman_codes = {v: k for k, v in huffman_codes.items()}
    
    decoded_message = []
    current_code = ""
    
    for bit in encoded_message:
        current_code += bit
        if current_code in reverse_huffman_codes:
            decoded_message.append(reverse_huffman_codes[current_code])
            print(current_code,"->",reverse_huffman_codes[current_code])
            current_code = ""
    
    return ''.join(decoded_message)

# Function to calculate the efficiency of Huffman encoding
def calculate_efficiency(original_message, encoded_message):
    # Calculate the size of the original message in bits (assuming 8 bits per character)
    original_size = len(original_message) * 8
    
    # Calculate the size of the encoded message in bits
    encoded_size = len(encoded_message)
    
    # Calculate compression ratio
    compression_ratio = original_size / encoded_size
    
    # Calculate savings percentage
    savings_percentage = (1 - (encoded_size / original_size)) * 100
    
    return original_size, encoded_size, compression_ratio, savings_percentage

def preprocess_message_for_tree(message, words_to_replace):
    symbols_with_freq = defaultdict(int)
    i = 0
    while i < len(message):
        matched = False
        for word in sorted(words_to_replace, key=len, reverse=True):
            if message.startswith(word, i):
                symbols_with_freq[word] += 1
                i += len(word)
                matched = True
                break
        if not matched:
            symbols_with_freq[message[i]] += 1
            i += 1
    print(symbols_with_freq)
    return symbols_with_freq

def main():
    # Set up command-line argument parsing
    parser = argparse.ArgumentParser(description="Optional BWT followed by Huffman Encoding and Decoding")
    parser.add_argument('-m', '--message', type=str, help="The message to encode using Huffman encoding.")
    parser.add_argument('-w', '--words', type=str, nargs='+', help="Words to be represented by nodes in the Huffman tree.")
    parser.add_argument('--bwt', action='store_true', help="Apply Burrows-Wheeler Transform before Huffman encoding.")
    args = parser.parse_args()

    # Updated Default JSON message used to build the Huffman tree
    default_message_json = """
    {
      "version": "2023-04-01",
      "data": [
        {
          "sensorId": "the quick brown fox jumps over the lazy dog",
          "value": "23.5297"
        },
        {
          "sensorId": "THE QUICK BROWN FOX JUMPS OVER THE LAZY DOG",
          "value": "23.5297"
        }
      ],
      "other": " !\\"#$%&'()*+,-./0123456789:;<=>?@[\\\\]^_`{|}~"
    }
    """

    # Load the default message
    message_dict = json.loads(default_message_json)
    default_message = json.dumps(message_dict, separators=(',', ':'))

    # Use the provided message for encoding, or the default message if none is provided
    message_to_buildtree = args.message if args.message else default_message
    message_to_encode = args.message if args.message else default_message

    # Step 1: Apply Burrows-Wheeler Transform (BWT) to the message if requested
    if args.bwt:
        transformed_message, bwt_index = bwt_transform(message_to_encode)
    else:
        transformed_message = message_to_encode
        message_to_build_tree = default_message + message_to_encode

    # Step 2: Create a frequency dictionary for the Huffman tree using the transformed message
    words_to_replace = args.words if args.words else []
    symbols_with_freq = preprocess_message_for_tree(message_to_build_tree, words_to_replace)

    # Step 3: Build the Huffman tree using the preprocessed message
    huffman_tree = build_huffman_tree(symbols_with_freq)

    # Step 4: Generate Huffman codes using the tree
    huffman_codes = generate_huffman_codes(huffman_tree)

    # Step 5: Encode the transformed message
    encoded_message = huffman_encode(transformed_message, huffman_codes)

    # Step 6: Calculate efficiency
    original_size, encoded_size, compression_ratio, savings_percentage = calculate_efficiency(message_to_encode, encoded_message)

    # Step 7: Decode the message using Huffman decoding
    decoded_message = huffman_decode(encoded_message, huffman_codes)

    # Step 8: Apply Burrows-Wheeler Inverse Transform (BWT Inverse) if BWT was applied
    if args.bwt:
        decoded_message = bwt_inverse(decoded_message, bwt_index)

    # Output the results
    print("Message to build tree:", message_to_build_tree)
    print("Transformed Message:", transformed_message)
    print("Encoded Message:", encoded_message)
    print("Huffman Codes:", huffman_codes)
    print("Original Size (bits):", original_size)
    print("Encoded Size (bits):", encoded_size)
    print("Compression Ratio:", compression_ratio)
    print("Savings Percentage:", savings_percentage)
    print("Decoded Message:", decoded_message)

if __name__ == "__main__":
    main()
