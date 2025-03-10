import subprocess

MODEL_PATH = "/Users/sayantahazra/Desktop/local-rag-project/backend-python/llama.cpp/models/mistral-7b-instruct-v0.1.Q4_K_M.gguf"
LLAMA_CLI_PATH = "/Users/sayantahazra/Desktop/local-rag-project/backend-python/llama.cpp/build/bin/llama-cli"

def generate_response(prompt: str, max_tokens: int = 128, stream: bool = False):
    """Run Mistral-7B using llama.cpp and stream responses if enabled."""
    cmd = [
        LLAMA_CLI_PATH, "-m", MODEL_PATH, "-p", prompt, "-n", str(max_tokens), "-no-cnv"
    ]
    
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, text=True, bufsize=1)

    if stream:
        for line in process.stdout:
            yield line.strip()  # Stream each line as it's generated
    else:
        return process.communicate()[0].strip()

# Test
if __name__ == "__main__":
    response = generate_response("What is fundamental analysis?")
    print(f"Mistral-7B Response:\n{response}")
