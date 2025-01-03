# steganography.py
import numpy as np
import cv2
import wave

class TextSteganography:
    ZWC = {"00": u'\u200C', "01": u'\u202C', "11": u'\u202D', "10": u'\u200E'}
    ZWC_reverse = {u'\u200C': "00", u'\u202C': "01", u'\u202D': "11", u'\u200E': "10"}

    @staticmethod
    def txt_encode(text, cover_text_file, stego_file):
        l = len(text)
        add = ''
        for i in range(l):
            t = ord(text[i])
            if 32 <= t <= 64:
                t1 = t + 48
                t2 = t1 ^ 170  # 170: 10101010
                res = bin(t2)[2:].zfill(8)
                add += "0011" + res
            else:
                t1 = t - 48
                t2 = t1 ^ 170
                res = bin(t2)[2:].zfill(8)
                add += "0110" + res
        res1 = add + "111111111111"

        with open(cover_text_file, "r", encoding="utf-8") as file1, open(stego_file, "w+", encoding="utf-8") as file3:
            word = []
            for line in file1:
                word += line.split()

            i = 0
            while i < len(res1):
                s = word[int(i / 12)]
                HM_SK = ""
                for j in range(0, 12, 2):
                    x = res1[i + j] + res1[i + j + 1]
                    HM_SK += TextSteganography.ZWC[x]
                s1 = s + HM_SK
                file3.write(s1 + " ")
                i += 12

            t = int(len(res1) / 12)
            while t < len(word):
                file3.write(word[t] + " ")
                t += 1

    @staticmethod
    def decode_txt_data(stego_file):
        temp = ''
        with open(stego_file, "r", encoding="utf-8") as file4:
            for line in file4:
                for word in line.split():
                    T1 = word
                    binary_extract = ""
                    for letter in T1:
                        if letter in TextSteganography.ZWC_reverse:
                            binary_extract += TextSteganography.ZWC_reverse[letter]
                    if binary_extract == "111111111111":
                        break
                    else:
                        temp += binary_extract

        i, final = 0, ''
        while i < len(temp):
            t3, t4 = temp[i:i+4], temp[i+4:i+12]
            if t3 == '0110':
                final += chr((int(t4, 2) ^ 170) + 48)
            elif t3 == '0011':
                final += chr((int(t4, 2) ^ 170) - 48)
            i += 12
        return final

class ImageSteganography:
    @staticmethod
    def msg_to_binary(msg):
        if isinstance(msg, str):
            return ''.join([format(ord(i), "08b") for i in msg])
        elif isinstance(msg, bytes):
            return ''.join([format(i, "08b") for i in msg])
        elif isinstance(msg, int):
            return format(msg, "08b")
        else:
            raise TypeError("Input type not supported")

    @staticmethod
    def encode_image(image_path, data, output_image):
        img = cv2.imread(image_path)
        binary_data = ImageSteganography.msg_to_binary(data + '*^*^*')

        index_data = 0
        for row in img:
            for pixel in row:
                r, g, b = ImageSteganography.msg_to_binary(pixel[0]), ImageSteganography.msg_to_binary(pixel[1]), ImageSteganography.msg_to_binary(pixel[2])
                if index_data < len(binary_data):
                    pixel[0] = int(r[:-1] + binary_data[index_data], 2)
                    index_data += 1
                if index_data < len(binary_data):
                    pixel[1] = int(g[:-1] + binary_data[index_data], 2)
                    index_data += 1
                if index_data < len(binary_data):
                    pixel[2] = int(b[:-1] + binary_data[index_data], 2)
                    index_data += 1
                if index_data >= len(binary_data):
                    break

        cv2.imwrite(output_image, img)

    @staticmethod
    def decode_image(image_path):
        img = cv2.imread(image_path)
        binary_data = ""
        for row in img:
            for pixel in row:
                binary_data += ImageSteganography.msg_to_binary(pixel[0])[-1]
                binary_data += ImageSteganography.msg_to_binary(pixel[1])[-1]
                binary_data += ImageSteganography.msg_to_binary(pixel[2])[-1]
                if "*^*^*" in "".join([chr(int(binary_data[i:i+8], 2)) for i in range(0, len(binary_data), 8)]):
                    decoded_data = "".join([chr(int(binary_data[i:i+8], 2)) for i in range(0, len(binary_data), 8)])
                    return decoded_data.split("*^*^*")[0]

class AudioSteganography:
    @staticmethod
    def encode_audio(audio_path, data, output_audio):
        song = wave.open(audio_path, mode='rb')
        frames = song.readframes(song.getnframes())
        frame_bytes = bytearray(list(frames))

        data += '*^*^*'
        binary_data = ''.join(format(ord(i), '08b') for i in data)

        index_data = 0
        for i in range(len(frame_bytes)):
            if index_data < len(binary_data):
                frame_bytes[i] = (frame_bytes[i] & 254) | int(binary_data[index_data])
                index_data += 1

        with wave.open(output_audio, 'wb') as fd:
            fd.setparams(song.getparams())
            fd.writeframes(frame_bytes)
        song.close()

    @staticmethod
    def decode_audio(audio_path):
        song = wave.open(audio_path, mode='rb')
        frames = song.readframes(song.getnframes())
        frame_bytes = bytearray(list(frames))

        binary_data = "".join([str(frame_bytes[i] & 1) for i in range(len(frame_bytes))])
        decoded_data = "".join([chr(int(binary_data[i:i+8], 2)) for i in range(0, len(binary_data), 8)])

        return decoded_data.split("*^*^*")[0]

class VideoSteganography:
    
    @staticmethod
    def msg_to_binary(msg):
        if type(msg) == str:
            return ''.join([format(ord(i), "08b") for i in msg])
        elif type(msg) == bytes or type(msg) == np.ndarray:
            return [format(i, "08b") for i in msg]
        elif type(msg) == int or type(msg) == np.uint8:
            return format(msg, "08b")
        else:
            raise TypeError("Input type is not supported in this function")

    @staticmethod
    def encryption(plaintext, key):
        key = VideoSteganography.preparing_key_array(key)
        S = VideoSteganography.KSA(key)
        keystream = np.array(VideoSteganography.PRGA(S, len(plaintext)))
        plaintext = np.array([ord(i) for i in plaintext])
        cipher = keystream ^ plaintext
        return ''.join([chr(c) for c in cipher])

    @staticmethod
    def decryption(ciphertext, key):
        key = VideoSteganography.preparing_key_array(key)
        S = VideoSteganography.KSA(key)
        keystream = np.array(VideoSteganography.PRGA(S, len(ciphertext)))
        ciphertext = np.array([ord(i) for i in ciphertext])
        decoded = keystream ^ ciphertext
        return ''.join([chr(c) for c in decoded])

    @staticmethod
    def preparing_key_array(s):
        return [ord(c) for c in s]

    @staticmethod
    def KSA(key):
        key_length = len(key)
        S = list(range(256))
        j = 0
        for i in range(256):
            j = (j + S[i] + key[i % key_length]) % 256
            S[i], S[j] = S[j], S[i]
        return S

    @staticmethod
    def PRGA(S, n):
        i = 0
        j = 0
        key = []
        while n > 0:
            n -= 1
            i = (i + 1) % 256
            j = (j + S[i]) % 256
            S[i], S[j] = S[j], S[i]
            K = S[(S[i] + S[j]) % 256]
            key.append(K)
        return key

    def embed(self, frame, data, key):
        data = self.encryption(data, key)
        data += '*^*^*'
        binary_data = self.msg_to_binary(data)
        length_data = len(binary_data)
        index_data = 0

        for i in frame:
            for pixel in i:
                r, g, b = self.msg_to_binary(pixel)
                if index_data < length_data:
                    pixel[0] = int(r[:-1] + binary_data[index_data], 2)
                    index_data += 1
                if index_data < length_data:
                    pixel[1] = int(g[:-1] + binary_data[index_data], 2)
                    index_data += 1
                if index_data < length_data:
                    pixel[2] = int(b[:-1] + binary_data[index_data], 2)
                    index_data += 1
                if index_data >= length_data:
                    break
            return frame

    def extract(self, frame, key):
        data_binary = ""
        final_decoded_msg = ""

        for i in frame:
            for pixel in i:
                r, g, b = self.msg_to_binary(pixel)
                data_binary += r[-1]
                data_binary += g[-1]
                data_binary += b[-1]
                total_bytes = [data_binary[i: i + 8] for i in range(0, len(data_binary), 8)]
                decoded_data = ""
                for byte in total_bytes:
                    decoded_data += chr(int(byte, 2))
                    if decoded_data[-5:] == "*^*^*":
                        final_decoded_msg = self.decryption(decoded_data[:-5], key)
                        return final_decoded_msg

    def encode_video(self, video_path, key, output_path='stego_video.mp4'):
        cap = cv2.VideoCapture(video_path)
        vidcap = cv2.VideoCapture(video_path)
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        frame_width = int(vidcap.get(3))
        frame_height = int(vidcap.get(4))
        size = (frame_width, frame_height)
        out = cv2.VideoWriter(output_path, fourcc, 25.0, size)
        max_frame = 0

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            max_frame += 1
        cap.release()
        print("Total number of frames in the selected video:", max_frame)
        frame_number = int(input("Enter the frame number where you want to embed data: "))
        data = input("\nEnter the data to be encoded in the video: ")
        frame_number_counter = 0

        while vidcap.isOpened():
            frame_number_counter += 1
            ret, frame = vidcap.read()
            if not ret:
                break
            if frame_number_counter == frame_number:
                frame_with_data = self.embed(frame, data, key)
                frame = frame_with_data
            out.write(frame)

        vidcap.release()
        out.release()
        print("\nEncoded the data successfully in the video file.")

    def decode_video(self, video_path, key):
        cap = cv2.VideoCapture(video_path)
        max_frame = 0

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            max_frame += 1
        print("Total number of frames in the selected video:", max_frame)
        frame_number = int(input("Enter the frame number to extract data from: "))
        vidcap = cv2.VideoCapture(video_path)
        frame_number_counter = 0

        while vidcap.isOpened():
            frame_number_counter += 1
            ret, frame = vidcap.read()
            if not ret:
                break
            if frame_number_counter == frame_number:
                decoded_message = self.extract(frame, key)
                print(f"\n\nThe encoded data hidden in the video is:\n{decoded_message}")
                break
        vidcap.release()
