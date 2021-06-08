# Utils
# Written by Rutuparn Pawar <InputBlackBoxOutput>

#---------------------------------------------------------------------------------------
import os, shutil, hashlib
from zipfile import ZipFile


# Get the SHA-256 hash of a file
def sha256(fname, size=4096):
 
	sha256_hash = hashlib.sha256()
	with open(fname, 'rb') as f:
		for byte_block in iter(lambda: f.read(4096), b""):
			sha256_hash.update(byte_block)
		
	return sha256_hash.hexdigest()

# Find difference between files using SHA-256 and remove duplicates
def removeDuplicateImages(dir):
	fileList = list(os.walk(dir))[0][-1]

	unique = []
	for file in fileList:
		filepath = os.path.join(dir, file)
		filehash = sha256(filepath)

		if filehash not in unique:
			unique.append(filehash)
		else:
			print(f"Removing {filepath}")
			os.remove(filepath)		

def compressDirectory(dir):
	with ZipFile(f"{dir}.zip", 'w') as zipObj:
		for folderName, subfolders, filenames in os.walk(dir):
			for filename in filenames:
				filePath = os.path.join(folderName, filename)
				zipObj.write(filePath, os.path.basename(filePath))

	shutil.rmtree(dir)

if __name__ == "__main__":
	print(sha256("README.md"))
	findDuplicateImages("test/car")
	compressFiles("test/car")