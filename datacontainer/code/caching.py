from storage import FileSystemStorage

class Node:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.prev = None
        self.next = None

class LRUCacheStorage:
    def __init__(self, capacity):
        self.capacity = capacity
        self.utilization = 0
        self.cache = {}
        self.head = Node(None, None)
        self.tail = Node(None, None)
        self.head.next = self.tail
        self.tail.prev = self.head
        self.filesystem = FileSystemStorage('/data/objects')
        
    def exists(self, key):
        return key in self.cache or self.filesystem.exists(key)
    
    def evict(self, key):
        if key in self.cache:
            node = self.cache[key]
            self._remove_node(node)
            del self.cache[key]

        try:
            self.filesystem.delete(key)
        except Exception as e:
            raise Exception("Error deleting from disk. Exception " + str(e))
            
    def get(self, key):
        if key in self.cache:
            node = self.cache[key]
            self._move_to_front(node)
            return node.value
        else:
            #read from disk
            try:
                data = self.filesystem.read(key)
                self.put(key, data)
                return data
            except Exception as e:
                raise Exception("Error reading from disk.  Exception " + str(e))

    def put(self, key, value):
        print(key, "\n",  flush=True)
        if key in self.cache:
            print("ENTRO AQUI", key, flush=True)
            node = self.cache[key]
            node.value = value
            self._move_to_front(node)
        else:
            print("ENTRO AQUI",self.utilization >= self.capacity,self.utilization,self.capacity, key, flush=True)
            if self.utilization >= self.capacity:
                self._evict()
            print(key, "\n",  flush=True)
            node = Node(key, value)
            self.cache[key] = node
            self._add_to_front(node)
            self.utilization += len(value)
            
            #write to disk
            try:
                print(key, "\n", flush=True)
                if key is not None:
                    self.filesystem.write(key, value)
            except Exception as e:
                raise Exception("Error writing to disk.  Exception " + str(e))

    def _move_to_front(self, node):
        self._remove_node(node)
        self._add_to_front(node)

    def _add_to_front(self, node):
        node.prev = self.head
        node.next = self.head.next
        self.head.next.prev = node
        self.head.next = node

    def _remove_node(self, node):
        if node.prev is not None:
            node.prev.next = node.next
            
        if node.next is not None:
            node.next.prev = node.prev

    #remove from memory and move to disk
    def _evict(self):
        node = self.tail.prev
        print("EVICT",node.key, flush=True)
        if node.key is not None:
            self.filesystem.write(node.key, node.value)
            self.utilization -= len(node.value)
            self._remove_node(node)
            del self.cache[node.key]
        
    def clean(self):
        self.cache = {}
        self.utilization = 0
        self.filesystem.clean()
        
