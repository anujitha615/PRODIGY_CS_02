from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
from Crypto.Hash import SHA256
from PIL import Image
import io
import getpass

def password_to_key(password):
    # Hash the password to get a 32-byte (256-bit) AES key
    return SHA256.new(password.encode('utf-8')).digest()
    #Encryption of image
def encrypt_image(input_image_path, output_file_path, key):
    image = Image.open(input_image_path)
    img_byte_arr = io.BytesIO()
    image.save(img_byte_arr, format=image.format)
    img_bytes = img_byte_arr.getvalue()

    iv = get_random_bytes(16)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    encrypted_data = cipher.encrypt(pad(img_bytes, AES.block_size))

    with open(output_file_path, 'wb') as f:
        f.write(iv + encrypted_data)
    print(f"Encrypted image saved to {output_file_path}")
    #Decryption of image
def decrypt_image(encrypted_file_path, output_image_path, key):
    with open(encrypted_file_path, 'rb') as f:
        iv = f.read(16)
        encrypted_data = f.read()
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted_data = unpad(cipher.decrypt(encrypted_data), AES.block_size)
    img = Image.open(io.BytesIO(decrypted_data))
    img.save(output_image_path)
    print(f"Decrypted image saved to {output_image_path}")
    #Main Part
def main():
    print("AES Image Encryption/Decryption Tool")
    mode = input("Type 'encrypt' to encrypt or 'decrypt' to decrypt: ").strip().lower()
    if mode == 'encrypt':
        input_path = input("Enter path to image to encrypt: ")
        output_path = input("Enter output file name (e.g., encrypted.bin): ")
    elif mode == 'decrypt':
        input_path = input("Enter path to encrypted file: ")
        output_path = input("Enter output image file name (e.g., decrypted.jpg): ")
    else:
        print("Invalid mode selected.")
        return

    password = getpass.getpass("Enter password: ")
    key = password_to_key(password)

    if mode == 'encrypt':
        encrypt_image(input_path, output_path, key)
    else:
        decrypt_image(input_path, output_path, key)

if __name__ == "__main__":
    main()
