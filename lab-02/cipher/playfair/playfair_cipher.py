class PlayFairCipher:
    def __init__(self):
        # Phương thức __init__ chỉ cần khởi tạo đối tượng, không cần làm gì thêm ở đây
        pass

    def create_playfair_matrix(self, key):
        """
        Tạo ma trận Playfair 5x5 từ khóa.
        Loại bỏ 'J' và chuyển thành 'I'.
        """
        key = key.replace("J", "I") # Chuyển "J" thành "I" trong khóa
        key = key.upper()
        
        # Tạo tập hợp các ký tự duy nhất từ khóa để loại bỏ trùng lặp và giữ thứ tự ban đầu
        key_chars = []
        for char in key:
            if char not in key_chars:
                key_chars.append(char)

        alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        
        # Thêm các chữ cái còn lại của bảng chữ cái vào sau khóa
        for letter in alphabet:
            if letter == "J": # Bỏ qua 'J'
                continue
            if letter not in key_chars:
                key_chars.append(letter)
        
        # Chắc chắn rằng ma trận có 25 ký tự
        if len(key_chars) != 25:
             # Đây là một kiểm tra an toàn, trong trường hợp bình thường sẽ luôn là 25
             # nhưng có thể có vấn đề nếu alphabet hoặc key_chars bị lỗi.
             print("Warning: Playfair matrix does not contain 25 unique characters.")

        # Tạo ma trận 5x5
        playfair_matrix = [key_chars[i:i+5] for i in range(0, 25, 5)]
        return playfair_matrix

    def find_letter_coords(self, matrix, letter):
        """
        Tìm tọa độ (hàng, cột) của một chữ cái trong ma trận Playfair.
        """
        for row in range(len(matrix)):
            for col in range(len(matrix[row])):
                if matrix[row][col] == letter:
                    return row, col
        return -1, -1 # Trả về -1 nếu không tìm thấy (trường hợp không mong muốn)

    def playfair_encrypt(self, plain_text, matrix):
        """
        Mã hóa văn bản gốc bằng thuật toán Playfair.
        """
        plain_text = plain_text.replace("J", "I") # Chuyển "J" thành "I" trong văn bản đầu vào
        plain_text = plain_text.upper().replace(" ", "") # Chuyển sang chữ hoa và bỏ khoảng trắng
        encrypted_text = ""
        
        # Chuẩn bị văn bản gốc: chèn 'X' nếu có hai ký tự giống nhau liền kề hoặc số lượng ký tự lẻ
        processed_plain_text = ""
        i = 0
        while i < len(plain_text):
            processed_plain_text += plain_text[i]
            if i + 1 < len(plain_text):
                if plain_text[i] == plain_text[i+1]:
                    processed_plain_text += "X" # Chèn 'X' nếu hai ký tự liền kề giống nhau
                else:
                    processed_plain_text += plain_text[i+1]
                    i += 1 # Tăng i lên 1 nếu đã dùng ký tự tiếp theo
            i += 1
        
        # Nếu độ dài của processed_plain_text là lẻ, thêm 'X' vào cuối
        if len(processed_plain_text) % 2 != 0:
            processed_plain_text += "X"

        for i in range(0, len(processed_plain_text), 2):
            pair = processed_plain_text[i:i+2]
            
            # Đảm bảo pair luôn có 2 ký tự (đã xử lý ở bước trên)
            if len(pair) < 2:
                # Đây là trường hợp không mong muốn nếu logic chuẩn bị văn bản đúng
                print(f"Error: Encountered single character pair '{pair}' during encryption.")
                continue 

            char1, char2 = pair[0], pair[1]
            row1, col1 = self.find_letter_coords(matrix, char1)
            row2, col2 = self.find_letter_coords(matrix, char2)

            if row1 == -1 or row2 == -1:
                # Xử lý trường hợp ký tự không có trong ma trận (ví dụ: ký tự đặc biệt)
                # Tùy thuộc yêu cầu, có thể bỏ qua, giữ nguyên hoặc báo lỗi.
                # Ở đây ta giữ nguyên ký tự đó
                encrypted_text += char1
                if row2 == -1: # Nếu chỉ char1 được tìm thấy
                    encrypted_text += char2
                continue


            if row1 == row2: # Cùng hàng
                encrypted_text += matrix[row1][(col1 + 1) % 5] + matrix[row2][(col2 + 1) % 5]
            elif col1 == col2: # Cùng cột
                encrypted_text += matrix[(row1 + 1) % 5][col1] + matrix[(row2 + 1) % 5][col2]
            else: # Tạo hình chữ nhật
                encrypted_text += matrix[row1][col2] + matrix[row2][col1]
        return encrypted_text

    def playfair_decrypt(self, cipher_text, matrix):
        """
        Giải mã văn bản mã hóa bằng thuật toán Playfair.
        """
        cipher_text = cipher_text.replace("J", "I") # Đảm bảo "J" được thay thế bằng "I"
        cipher_text = cipher_text.upper().replace(" ", "") # Chuyển sang chữ hoa và bỏ khoảng trắng
        decrypted_text_raw = "" # Kết quả giải mã thô, có thể chứa 'X' đệm
        
        # Đảm bảo chuỗi mã hóa có độ dài chẵn để tránh IndexError.
        # Nếu độ dài lẻ, có thể do lỗi đầu vào hoặc mã hóa, thêm 'X' để xử lý cặp cuối.
        if len(cipher_text) % 2 != 0:
            cipher_text += "X" 
            # Cảnh báo: Thêm 'X' ở đây có thể dẫn đến kết quả sai lệch nếu
            # chuỗi mã hóa thực sự bị cắt cụt. Lý tưởng là cipher_text phải luôn chẵn.

        for i in range(0, len(cipher_text), 2):
            pair = cipher_text[i:i+2]
            
            # Đảm bảo pair luôn có 2 ký tự
            if len(pair) < 2:
                print(f"Error: Encountered single character pair '{pair}' during decryption.")
                continue

            char1, char2 = pair[0], pair[1]
            row1, col1 = self.find_letter_coords(matrix, char1)
            row2, col2 = self.find_letter_coords(matrix, char2)

            if row1 == -1 or row2 == -1:
                # Xử lý trường hợp ký tự không có trong ma trận
                decrypted_text_raw += char1
                if row2 == -1:
                    decrypted_text_raw += char2
                continue

            if row1 == row2: # Cùng hàng
                decrypted_text_raw += matrix[row1][(col1 - 1) % 5] + matrix[row2][(col2 - 1) % 5]
            elif col1 == col2: # Cùng cột
                decrypted_text_raw += matrix[(row1 - 1) % 5][col1] + matrix[(row2 - 1) % 5][col2]
            else: # Tạo hình chữ nhật
                decrypted_text_raw += matrix[row1][col2] + matrix[row2][col1]

        # Loại bỏ các ký tự 'X' được thêm vào để đệm và các 'X' trùng lặp
        final_decrypted_text = ""
        i = 0
        while i < len(decrypted_text_raw):
            final_decrypted_text += decrypted_text_raw[i]
            # Kiểm tra nếu ký tự hiện tại và ký tự tiếp theo giống nhau, và ký tự tiếp theo không phải là ký tự cuối
            # Điều này là để loại bỏ 'X' được thêm vào giữa các cặp trùng lặp
            if i + 2 < len(decrypted_text_raw) and decrypted_text_raw[i] == decrypted_text_raw[i+2] and decrypted_text_raw[i+1] == 'X':
                i += 1 # Bỏ qua 'X'
            i += 1

        # Loại bỏ 'X' cuối cùng nếu nó được thêm vào để làm chẵn chuỗi
        if final_decrypted_text.endswith("X") and len(final_decrypted_text) > 1 and final_decrypted_text[-2] != 'X':
             final_decrypted_text = final_decrypted_text[:-1]

        return final_decrypted_text.strip() # Bỏ khoảng trắng thừa ở đầu/cuối nếu có