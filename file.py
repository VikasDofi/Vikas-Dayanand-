# 1. CREATE AND WRITE A FILE
f = open("demo.txt", "w")
f.write("Hello Raspberry Pi!\n")
f.write("This is my first file.")
f.close()

print("File created and written successfully")

# 2. READ A FILE
f = open("demo.txt", "r")
print("\nFile contents:")
print(f.read())
f.close()

# 3. APPEND TO A FILE
f = open("demo.txt", "a")
f.write("\nThis line is appended.")
f.close()

print("\nData appended successfully")

# 4. READ THE UPDATED FILE
f = open("demo.txt", "r")
print("\nUpdated file contents:")
print(f.read())
f.close()