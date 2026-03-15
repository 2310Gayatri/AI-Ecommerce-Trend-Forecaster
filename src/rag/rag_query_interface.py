import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from src.rag.rag_engine import generate_rag_response


def run_query_interface():

    print("\nRAG Market Intelligence Interface\n")

    while True:

        query = input("Ask market question (type 'exit' to quit): ")

        if query.lower() == "exit":
            break

        response = generate_rag_response(query)

        print("\nMarket Insight:\n")
        print(response)
        print("\n----------------------------------\n")


if __name__ == "__main__":

    run_query_interface()