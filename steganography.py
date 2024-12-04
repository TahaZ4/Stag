def encode_message_in_image(image_path, message, output_path):
    """Encodes a secret message into an image."""
    try:
        # Read the image file in binary mode
        with open(image_path, 'rb') as image_file:
            image_data = bytearray(image_file.read())

        # Convert the message to binary and add a delimiter
        binary_message = ''.join(format(ord(char), '08b') for char in message)
        binary_message += '11111111'  # Delimiter to mark the end

        # Encode the binary message into the image
        message_index = 0
        for i in range(len(image_data)):
            if message_index < len(binary_message):
                image_data[i] = (image_data[i] & 254) | int(binary_message[message_index])
                message_index += 1

        # Save the modified image
        with open(output_path, 'wb') as output_file:
            output_file.write(image_data)

        print(f"Message successfully encoded and saved to '{output_path}'.")

    except FileNotFoundError:
        print("Error: The specified image file was not found.Please check the file path.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


def decode_message_from_image(image_path):
    """Decodes and extracts the secret message from an image. """
    try:
        # Open the image file in binary mode
        with open(image_path, 'rb') as image_file:
            image_data = bytearray(image_file.read()) 

        # Extract binary message from the image
        binary_message = ''
        for byte in image_data:
            binary_message += str(byte & 1)

        # Convert the binary message back to text
        message = ''
        for i in range(0, len(binary_message), 8):
            byte = binary_message[i:i+8]
            if byte == '11111111':  # Stop at the delimiter
                break
            if len(byte) == 8:  # Ensure valid byte before conversion
                message += chr(int(byte, 2))

        return message

    except FileNotFoundError:
        print("Error: The specified image file was not found. Please check the file path.")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e} ")
        return None


if __name__ == "__main__":
    # User interaction to encode and decode a message
    print("Steganography: Encode and Decode Messages in Images")
    print("1. Encode a message")
    print("2. Decode a message")
    choice = input("Choose an option (1 or 2): ").strip()

    if choice == "1":
        # Encoding process
        image_path = input("Enter the path of the image to encode the message in: ").strip()
        output_path = input("Enter the path to save the encoded image: ").strip()
        message = input("Enter secret message to encode: ").strip()
        encode_message_in_image(image_path, message, output_path)
    elif choice == "2":
        # Decoding process
        image_path = input("Enter path of the encoded image: ").strip()
        decoded_message = decode_message_from_image(image_path)
        if decoded_message is not None:
            print("Decoded secret message:", decoded_message)
    else:
        print("Invalid. Please run the program again.")
