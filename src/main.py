import retriever
import sys

def main():
    inpute = retriever.retrieve()
    print()
    if (inpute == 'EXIT'):
       sys.exit(0)
    outpute = retriever.process_retrieval(inpute)
    print(outpute)
    print()

if __name__ == "__main__":
    print("="*50)
    print("="*14,"WELCOME TO COURSE AI","="*14)
    print("="*50)
    while True:
        main()