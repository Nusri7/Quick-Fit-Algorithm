import streamlit as st

class QuickFitMemoryAllocator:
    def __init__(self, total_memory=1024, min_block_size=4):
        self.total_memory = total_memory  # Total memory in KB
        self.min_block_size = min_block_size  # Minimum block size in KB
        self.free_lists = {}  # Free lists for different block sizes
        self.allocated_blocks = {}  # Dictionary to store allocated blocks with starting address
        self.starting_address = 0  # Track the starting address of allocations
        self.initialize_memory()

    def initialize_memory(self):
        """Initialize memory blocks and free lists."""
        current_size = self.min_block_size
        while current_size <= self.total_memory:
            self.free_lists[current_size] = [current_size]  # Initialize with one free block
            current_size *= 2

    def allocate(self, size, process_name):
        """Allocate memory block."""
        block_size = self._find_suitable_block(size)
        if block_size is None:
            return f"No suitable block found for allocation of {size}KB to {process_name}."
        
        # Allocate memory and update free lists
        self.free_lists[block_size].remove(block_size)
        self.allocated_blocks[self.starting_address] = {
            "size": block_size,
            "process": process_name,
            "free": False
        }
        log_message = f"Allocated {block_size}KB to {process_name} starting at address {self.starting_address}."
        self.starting_address += block_size
        return log_message

    def _find_suitable_block(self, size):
        """Find the smallest block size that fits the requested size."""
        for block_size in sorted(self.free_lists.keys()):
            if block_size >= size and len(self.free_lists[block_size]) > 0:
                return block_size
        return None

    def display_memory_state(self):
        """Display the current memory state."""
        memory_state = []
        for address, block in sorted(self.allocated_blocks.items()):
            memory_state.append(
                f"Start: {address}, Size: {block['size']}KB, Free: {block['free']}, Process: {block['process']}"
            )
        for block_size in sorted(self.free_lists.keys()):
            for _ in self.free_lists[block_size]:
                memory_state.append(
                    f"Start: {self.starting_address}, Size: {block_size}KB, Free: True"
                )
                self.starting_address += block_size
        return memory_state


# Initialize Streamlit App
st.title("Quick Fit Memory Allocation")
st.sidebar.header("Allocate Memory")

# Create an instance of the QuickFitMemoryAllocator
allocator = QuickFitMemoryAllocator()

# Sidebar Inputs for Memory Allocation
process_name = st.sidebar.text_input("Enter Process Name", value="Process")
memory_request = st.sidebar.number_input("Enter Memory Size (KB)", min_value=4, max_value=1024, step=1)
if st.sidebar.button("Allocate Memory"):
    result = allocator.allocate(memory_request, process_name)
    st.success(result)

# Display Memory State
st.header("Memory State")
memory_state = allocator.display_memory_state()
for line in memory_state:
    st.text(line)
