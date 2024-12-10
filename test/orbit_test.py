import subprocess
import os
import orbit

# Define files to be generated and cleaned up
generated_files = ['X.txt', 'Y.txt', 'output.pdf']

try:
    # Run the main function in the orbit module to generate X.txt
    orbit.main(input_file='input.txt', output_file='output.pdf', x_file='X.txt')

    # Compare the generated X.txt with the pregenerated X_pregenerated.txt
    result = subprocess.run(
        ["diff", "X.txt", "X_pregenerated.txt"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    if result.returncode == 0:
        print("Test passed: X.txt matches X_pregenerated.txt")
    else:
        print("Test failed: X.txt differs from X_pregenerated.txt")
        print(result.stdout)  # Print the differences

except FileNotFoundError as e:
    print(f"Error: {e}. Ensure 'diff' is installed and available.")

finally:
    # Clean up generated files
    for file in generated_files:
        if os.path.exists(file):
            os.remove(file)
