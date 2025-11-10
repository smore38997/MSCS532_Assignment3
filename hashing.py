import random
import time
from typing import Any, Optional, List, Tuple

class UniversalHashFunction:
    """
    Universal hash function from family H = {h_{a,b}(k) = ((ak + b) mod p) mod m}
    where p is a prime larger than the universe size, and a, b are random coefficients.
    """
    def __init__(self, table_size: int, prime: int = 2147483647):
        self.m = table_size
        self.p = prime  # Large prime (2^31 - 1)
        self.a = random.randint(1, self.p - 1)
        self.b = random.randint(0, self.p - 1)
    
    def hash(self, key: Any) -> int:
        """Compute hash value for the given key."""
        # Convert key to integer if it's not already
        if isinstance(key, str):
            key_int = hash(key)
        else:
            key_int = key
        
        return ((self.a * key_int + self.b) % self.p) % self.m


class HashTableChaining:
    """
    Hash table implementation using chaining for collision resolution.
    Features:
    - Universal hashing to minimize collisions
    - Dynamic resizing to maintain low load factor
    - Efficient insert, search, and delete operations
    """
    
    def __init__(self, initial_capacity: int = 16, max_load_factor: float = 0.75):
        self.capacity = initial_capacity
        self.max_load_factor = max_load_factor
        self.size = 0
        self.table: List[List[Tuple[Any, Any]]] = [[] for _ in range(self.capacity)]
        self.hash_func = UniversalHashFunction(self.capacity)
        
        # Statistics
        self.num_collisions = 0
        self.num_resizes = 0
    
    def _get_load_factor(self) -> float:
        """Calculate current load factor (α = n/m)."""
        return self.size / self.capacity if self.capacity > 0 else 0
    
    def _resize(self, new_capacity: int):
        """
        Resize the hash table and rehash all elements.
        Time Complexity: O(n) where n is the number of elements.
        """
        self.num_resizes += 1
        old_table = self.table
        
        # Create new table
        self.capacity = new_capacity
        self.table = [[] for _ in range(self.capacity)]
        self.hash_func = UniversalHashFunction(self.capacity)
        old_size = self.size
        self.size = 0
        
        # Rehash all elements
        for chain in old_table:
            for key, value in chain:
                self._insert_no_resize(key, value)
        
        self.size = old_size
    
    def _insert_no_resize(self, key: Any, value: Any):
        """Insert without triggering resize (used during rehashing)."""
        index = self.hash_func.hash(key)
        chain = self.table[index]
        
        # Update if key exists
        for i, (k, v) in enumerate(chain):
            if k == key:
                chain[i] = (key, value)
                return
        
        # Insert new key-value pair
        if len(chain) > 0:
            self.num_collisions += 1
        chain.append((key, value))
    
    def insert(self, key: Any, value: Any):
        """
        Insert a key-value pair into the hash table.
        Expected Time Complexity: O(1) under simple uniform hashing.
        
        Args:
            key: The key to insert
            value: The value associated with the key
        """
        # Check if resize is needed
        if self._get_load_factor() >= self.max_load_factor:
            self._resize(self.capacity * 2)
        
        index = self.hash_func.hash(key)
        chain = self.table[index]
        
        # Update if key already exists
        for i, (k, v) in enumerate(chain):
            if k == key:
                chain[i] = (key, value)
                return
        
        # Insert new key-value pair
        if len(chain) > 0:
            self.num_collisions += 1
        chain.append((key, value))
        self.size += 1
    
    def search(self, key: Any) -> Optional[Any]:
        """
        Search for a value associated with the given key.
        Expected Time Complexity: O(1 + α) where α is the load factor.
        
        Args:
            key: The key to search for
            
        Returns:
            The value associated with the key, or None if not found
        """
        index = self.hash_func.hash(key)
        chain = self.table[index]
        
        for k, v in chain:
            if k == key:
                return v
        return None
    
    def delete(self, key: Any) -> bool:
        """
        Delete a key-value pair from the hash table.
        Expected Time Complexity: O(1 + α) where α is the load factor.
        
        Args:
            key: The key to delete
            
        Returns:
            True if the key was found and deleted, False otherwise
        """
        index = self.hash_func.hash(key)
        chain = self.table[index]
        
        for i, (k, v) in enumerate(chain):
            if k == key:
                chain.pop(i)
                self.size -= 1
                
                # Optionally shrink table if load factor is too low
                if self.size > 0 and self._get_load_factor() < 0.25 and self.capacity > 16:
                    self._resize(self.capacity // 2)
                
                return True
        return False
    
    def get_statistics(self) -> dict:
        """Return statistics about the hash table."""
        chain_lengths = [len(chain) for chain in self.table]
        max_chain_length = max(chain_lengths) if chain_lengths else 0
        avg_chain_length = sum(chain_lengths) / len(chain_lengths) if chain_lengths else 0
        non_empty_chains = sum(1 for length in chain_lengths if length > 0)
        
        return {
            "size": self.size,
            "capacity": self.capacity,
            "load_factor": self._get_load_factor(),
            "num_collisions": self.num_collisions,
            "num_resizes": self.num_resizes,
            "max_chain_length": max_chain_length,
            "avg_chain_length": avg_chain_length,
            "non_empty_chains": non_empty_chains,
            "empty_chains": self.capacity - non_empty_chains
        }
    
    def __str__(self) -> str:
        """String representation showing non-empty chains."""
        result = []
        for i, chain in enumerate(self.table):
            if chain:
                result.append(f"  Slot {i}: {chain}")
        return "Hash Table:\n" + "\n".join(result) if result else "Hash Table: (empty)"


# === Performance Testing ===

def benchmark_operations(num_operations: int = 10000):
    """
    Benchmark insert, search, and delete operations.
    Demonstrates the effect of load factor on performance.
    """
    print("\n" + "="*80)
    print("HASH TABLE WITH CHAINING - PERFORMANCE BENCHMARK")
    print("="*80)
    
    ht = HashTableChaining(initial_capacity=16, max_load_factor=0.75)
    
    # Insert benchmark
    print(f"\n1. INSERTING {num_operations} elements...")
    insert_times = []
    for i in range(num_operations):
        start = time.perf_counter()
        ht.insert(i, f"value_{i}")
        elapsed = time.perf_counter() - start
        insert_times.append(elapsed)
    
    stats = ht.get_statistics()
    print(f"   ✓ Average insert time: {sum(insert_times)/len(insert_times)*1e6:.4f} μs")
    print(f"   ✓ Load factor: {stats['load_factor']:.4f}")
    print(f"   ✓ Capacity: {stats['capacity']}")
    print(f"   ✓ Collisions: {stats['num_collisions']}")
    print(f"   ✓ Resizes: {stats['num_resizes']}")
    print(f"   ✓ Max chain length: {stats['max_chain_length']}")
    print(f"   ✓ Avg chain length: {stats['avg_chain_length']:.4f}")
    
    # Search benchmark
    print(f"\n2. SEARCHING for {num_operations} elements...")
    search_times = []
    for i in range(num_operations):
        start = time.perf_counter()
        value = ht.search(i)
        elapsed = time.perf_counter() - start
        search_times.append(elapsed)
        assert value == f"value_{i}", f"Search failed for key {i}"
    
    print(f"   ✓ Average search time: {sum(search_times)/len(search_times)*1e6:.4f} μs")
    
    # Search for non-existent keys
    print(f"\n3. SEARCHING for {num_operations} non-existent keys...")
    not_found_times = []
    for i in range(num_operations, 2 * num_operations):
        start = time.perf_counter()
        value = ht.search(i)
        elapsed = time.perf_counter() - start
        not_found_times.append(elapsed)
        assert value is None, f"Found unexpected value for key {i}"
    
    print(f"   ✓ Average search time (not found): {sum(not_found_times)/len(not_found_times)*1e6:.4f} μs")
    
    # Delete benchmark
    print(f"\n4. DELETING {num_operations // 2} elements...")
    delete_times = []
    for i in range(0, num_operations, 2):
        start = time.perf_counter()
        result = ht.delete(i)
        elapsed = time.perf_counter() - start
        delete_times.append(elapsed)
        assert result, f"Delete failed for key {i}"
    
    stats = ht.get_statistics()
    print(f"   ✓ Average delete time: {sum(delete_times)/len(delete_times)*1e6:.4f} μs")
    print(f"   ✓ Final size: {stats['size']}")
    print(f"   ✓ Final load factor: {stats['load_factor']:.4f}")
    print(f"   ✓ Final capacity: {stats['capacity']}")
    
    print("\n" + "="*80)


def demonstrate_load_factor_impact():
    """
    Demonstrate how different load factors affect performance.
    """
    print("\n" + "="*80)
    print("LOAD FACTOR IMPACT ON PERFORMANCE")
    print("="*80)
    print(f"\n{'Max Load Factor':<20} | {'Avg Insert (μs)':<16} | {'Avg Search (μs)':<16} | {'Max Chain':<10}")
    print("-"*80)
    
    test_sizes = 5000
    load_factors = [0.5, 0.75, 1.0, 1.5, 2.0]
    
    for lf in load_factors:
        ht = HashTableChaining(initial_capacity=16, max_load_factor=lf)
        
        # Insert
        insert_times = []
        for i in range(test_sizes):
            start = time.perf_counter()
            ht.insert(i, f"value_{i}")
            elapsed = time.perf_counter() - start
            insert_times.append(elapsed)
        
        # Search
        search_times = []
        for i in range(test_sizes):
            start = time.perf_counter()
            ht.search(i)
            elapsed = time.perf_counter() - start
            search_times.append(elapsed)
        
        stats = ht.get_statistics()
        avg_insert = sum(insert_times) / len(insert_times) * 1e6
        avg_search = sum(search_times) / len(search_times) * 1e6
        
        print(f"{lf:<20.2f} | {avg_insert:<16.4f} | {avg_search:<16.4f} | {stats['max_chain_length']:<10}")
    
    print("-"*80)
    print("\nObservation: As load factor increases, chain lengths grow, degrading performance.")
    print("="*80)


if __name__ == "__main__":
    # Run basic demonstration
    print("\nDEMONSTRATION: Basic Operations")
    print("-" * 40)
    ht = HashTableChaining(initial_capacity=8)
    
    # Insert some values
    for i in range(20):
        ht.insert(i, f"value_{i}")
    
    print(f"Inserted 20 elements")
    print(f"Load factor: {ht.get_statistics()['load_factor']:.4f}")
    
    # Search
    print(f"\nSearch key 5: {ht.search(5)}")
    print(f"Search key 100: {ht.search(100)}")
    
    # Delete
    print(f"\nDelete key 5: {ht.delete(5)}")
    print(f"Search key 5 after delete: {ht.search(5)}")
    
    # Run benchmarks
    benchmark_operations(10000)
    demonstrate_load_factor_impact()