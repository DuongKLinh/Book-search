from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct, Distance, VectorParams

class ProductCollection:
    def __init__(self):
        self.client = QdrantClient(url="http://localhost:6333")
        self.collection_name = "products_collection"

    def create_collection(self):
        self.client.create_collection(
            collection_name=self.collection_name,
            vectors_config=VectorParams(size=3, distance=Distance.COSINE),
        )

        products = [
            PointStruct(id=1, vector=[1.0, 0.0, 0.0], payload={"product_code": "P001", "product_name": "Laptop", "quantity": 50, "price": 1000}),
            PointStruct(id=2, vector=[0.0, 1.0, 0.0], payload={"product_code": "P002", "product_name": "Smartphone", "quantity": 100, "price": 800}),
            PointStruct(id=3, vector=[0.0, 0.0, 1.0], payload={"product_code": "P003", "product_name": "Tablet", "quantity": 75, "price": 600}),
            PointStruct(id=4, vector=[0.5, 0.5, 0.0], payload={"product_code": "P004", "product_name": "Monitor", "quantity": 30, "price": 300}),
            PointStruct(id=5, vector=[0.2, 0.3, 0.5], payload={"product_code": "P005", "product_name": "Keyboard", "quantity": 150, "price": 50}),
        ]

        self.client.upsert(
            collection_name=self.collection_name,
            points=products
        )
        print("Collection và sản phẩm đã được tạo thành công.")

    def search_by_price(self, max_price):
        search_result = self.client.search(
            collection_name=self.collection_name,
            query_filter={
                "must": [
                    {
                        "key": "price",
                        "range": {"lte": max_price}
                    }
                ]
            },
            query_vector=[0.0, 0.0, 0.0],
            limit=10
        )
        for result in search_result:
            print(f"Product: {result.payload['product_name']}, Price: {result.payload['price']}")

    def search_by_code(self, product_code):
        search_result = self.client.search(
            collection_name=self.collection_name,
            query_filter={
                "must": [
                    {
                        "key": "product_code",
                        "match": {"value": product_code}
                    }
                ]
            },
            query_vector=[0.0, 0.0, 0.0],
            limit=1
        )
        for result in search_result:
            print(f"Product: {result.payload['product_name']}, Price: {result.payload['price']}")

    def search_by_vector(self, query_vector):
        search_result = self.client.search(
            collection_name=self.collection_name,
            query_vector=query_vector,
            limit=3
        )
        for result in search_result:
            print(f"Product: {result.payload['product_name']}, Similarity: {result.score}")

    def delete_collection(self):
        self.client.delete_collection(collection_name=self.collection_name)
        print(f"Collection {self.collection_name} đã được xóa.")
        
def main():
    product_collection = ProductCollection()
    
    while True:
        print("\nChọn một lệnh:")
        print("1. Tạo collection và thêm sản phẩm (có sẵn)")
        print("2. Tìm sản phẩm có giá nhỏ hơn hoặc bằng giá chỉ định")
        print("3. Tìm sản phẩm theo mã sản phẩm")
        print("4. Tìm sản phẩm gần nhất với một vector truy vấn")
        print("5. Xóa collection")
        print("6. Thoát")
        
        choice = input("Nhập lựa chọn của bạn: ")

        if choice == "1":
            product_collection.create_collection()

        elif choice == "2":
            max_price = float(input("Nhập giá tối đa: "))
            product_collection.search_by_price(max_price)

        elif choice == "3":
            product_code = input("Nhập mã sản phẩm: ")
            product_collection.search_by_code(product_code)

        elif choice == "4":
            vector_str = input("Nhập vector (các phần tử cách nhau bằng dấu phẩy): ")
            query_vector = [float(x) for x in vector_str.split(",")]
            product_collection.search_by_vector(query_vector)

        elif choice == "5":
            product_collection.delete_collection()

        elif choice == "6":
            print("Thoát chương trình.")
            break

        else:
            print("Lựa chọn không hợp lệ. Vui lòng thử lại.")

if __name__ == "__main__":
    main()

