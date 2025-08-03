package main

import (
	"crypto/aes"
	"crypto/cipher"
	"encoding/base64"
	"io/ioutil"
	"os"
	"strings"
)

var hardcodedIV = []byte{
	0x4a, 0x78, 0x13, 0x2f, 0xaa, 0xbb, 0x7c, 0x00,
	0x19, 0x88, 0x39, 0x4f, 0xff, 0xcc, 0x11, 0x09,
}

func xorVariants(data []byte, key byte, variant int) []byte {
	output := make([]byte, len(data))
	switch variant {
	case 0:
		for i := range data {
			output[i] = data[i] ^ key
		}
	case 1:
		for i := range data {
			output[i] = data[i] ^ (key + byte(i%255))
		}
	case 2:
		for i := range data {
			output[i] = (data[i] ^ key) ^ byte(i%7)
		}
	}
	return output
}

func decryptAES_CTR(data, key, iv []byte) ([]byte, error) {
	block, err := aes.NewCipher(key)
	if err != nil {
		return nil, err
	}
	stream := cipher.NewCTR(block, iv)
	decrypted := make([]byte, len(data))
	stream.XORKeyStream(decrypted, data)
	return decrypted, nil
}

func loadKeyFragments() ([]byte, byte, int, error) {
	frag1, err := ioutil.ReadFile("frag1.bin")
	if err != nil {
		return nil, 0, 0, err
	}

	frag2, err := ioutil.ReadFile("frag2.bin")
	if err != nil {
		return nil, 0, 0, err
	}

	if len(frag1) != 16 || len(frag2) != 18 {
		return nil, 0, 0, err
	}

	aesKey := append(frag1, frag2[:16]...)
	xorKey := frag2[16]
	variant := int(frag2[17])

	return aesKey, xorKey, variant, nil
}

func decryptFile(filePath string, aesKey []byte, xorKey byte, variant int) error {
	if !strings.HasSuffix(filePath, ".stucknet") {
		return nil
	}

	b64Data, err := ioutil.ReadFile(filePath)
	if err != nil {
		return err
	}

	encryptedData, err := base64.StdEncoding.DecodeString(string(b64Data))
	if err != nil {
		return err
	}

	decryptedAES, err := decryptAES_CTR(encryptedData, aesKey, hardcodedIV)
	if err != nil {
		return err
	}

	originalData := xorVariants(decryptedAES, xorKey, variant)

	originalPath := strings.TrimSuffix(filePath, ".stucknet")
	return ioutil.WriteFile(originalPath, originalData, 0644)
}

func main() {
	if len(os.Args) != 2 {
		return
	}

	filePath := os.Args[1]

	aesKey, xorKey, variant, err := loadKeyFragments()
	if err != nil {
		return
	}

	_ = decryptFile(filePath, aesKey, xorKey, variant)
}