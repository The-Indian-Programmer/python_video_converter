import subprocess

def generate_models(database_url, output_file):
    try:
        # Run sqlacodegen command
        subprocess.run(
            ["sqlacodegen", database_url, "--outfile", output_file],
            check=True
        )
        print(f"Models generated and saved to {output_file}")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    # Define your database URL
    database_url = "mysql+pymysql://root:123456@localhost/mydatabase"
    
    # Define the output file for the generated models
    output_file = "models.py"
    
    # Generate the models
    generate_models(database_url, output_file)
