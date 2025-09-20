 ## C++ STL容器用法大全

### 容器分类概览

STL容器主要分为四大类：
- **序列式容器**：如vector、deque、list等，按插入顺序存储元素。
- **关联式容器**：如set、map等，按键值自动排序存储。
- **无序关联式容器**：如unordered_set、unordered_map等，基于哈希表实现，不排序。
- **容器适配器**：如stack、queue等，对基础容器进行接口封装。

### 一、序列式容器

#### ✅ vector（动态数组）

**特点**：连续内存存储，支持随机访问，尾部插入/删除高效。

**声明方法**：
```cpp
#include <vector>
using namespace std;

// 基本声明
vector<int> vec;
vector<string> strVec;

// 声明并初始化
vector<int> vec1(5);            // 5个默认值元素
vector<int> vec2(5, 10);       // 5个值为10的元素
vector<int> vec3 = {1, 2, 3}; // 列表初始化
```

**常用操作**：
```cpp
vec.push_back(10);    // 尾部插入元素
vec.pop_back();        // 尾部删除元素
vec前端元素：vec[0] 或 vec.at(0);
vec尾端元素：vec.back();
vec大小：vec.size();
vec容量：vec.capacity();
vec预分配内存：vec.reserve(100); // 预留空间，避免频繁扩容
```

**遍历方式**：
```cpp
// 迭代器遍历
for (auto it = vec.begin(); it != vec.end(); ++it) {
    cout << *it << " ";
}

// 范围for循环（推荐）
for (const auto& x : vec) {
    cout << x << " ";
}
```

**注意事项**：
⚠️ **迭代器失效**：
- 插入操作（如insert）可能导致内存重新分配，使所有迭代器失效
- 删除操作（erase）使被删除元素的迭代器失效

⚠️ **范围for循环**：
- 使用`const auto&`遍历时无法修改元素值
- 如需修改，应使用`auto&`：`for (auto& x : vec) x *= 2;`

⚠️ **性能优化**：
- 频繁插入/删除时，使用`reserve()`预分配内存可显著提升性能
- 调整后使用`shrink_to_fit()`尝试释放多余内存

#### ✅ deque（双端队列）

**特点**：分块连续内存，支持随机访问，首尾插入/删除高效。

**声明方法**：
```cpp
#include <deque>
using namespace std;

// 基本声明
deque<string> strDeq;

// 声明并初始化
deque<int> deq1(10);          // 10个默认值元素
deque<int> deq2(10, 20);     // 10个值为20的元素
deque<int> deq3 = {1, 2, 3}; // 列表初始化
```

**常用操作**：
```cpp
deq.push_back(100);  // 尾部插入
deq.push_front(50);   // 头部插入
deq.pop_back();        // 尾部删除
deq.pop_front();       // 头部删除
deq前端元素：deq[0];
deq尾端元素：deq.back();
```

**遍历方式**：
```cpp
for (const auto& x : deq) {
    cout << x << " ";
}
```

**注意事项**：
⚠️ **迭代器失效**：
- 中间位置插入/删除可能导致迭代器失效
- 扩容时所有迭代器可能失效

⚠️ **性能特性**：
- 首尾操作时间复杂度O(1)，中间操作O(n)
- 访问元素效率低于vector，但高于list

#### ✅ list（双向链表）

**特点**：非连续内存存储，支持双向迭代，任意位置插入/删除高效。

**声明方法**：
```cpp
#include <list>
using namespace std;

// 基本声明
list<int> lst;

// 声明并初始化
list<int> lst1(5, 10);     // 5个值为10的元素
list<int> lst2 = {1, 2, 3}; // 列表初始化
```

**常用操作**：
```cpp
lst.push_back(100);  // 尾部插入
lst.push_front(50);   // 头部插入
lst.insert(pos, 20);  // 在迭代器pos位置插入元素20
lst前端元素：lst front();
lst尾端元素：lst back();
lst大小：lst.size();
```

**遍历方式**：
```cpp
// 迭代器遍历
for (auto it = lst.begin(); it != lst.end(); ++it) {
    cout << *it << " ";
}

// 范围for循环（推荐）
for (const auto& x : lst) {
    cout << x << " ";
}
```

**注意事项**：
⚠️ **迭代器稳定性**：
- 插入操作不会使其他迭代器失效
- 删除操作仅使被删除元素的迭代器失效

⚠️ **性能特性**：
- 不支持随机访问，访问元素需线性时间
- 内存开销较大（每个元素存储前后指针）

#### ✅ forward_list（单向链表）

**特点**：非连续内存存储，仅支持前向迭代，任意位置插入/删除高效。

**声明方法**：
```cpp
#include <forward_list>
using namespace std;

// 基本声明
forward_list<int> flst;

// 声明并初始化
forward_list<int> flst1(5, 10);   // 5个值为10的元素
forward_list<int> flst2 = {1, 2, 3}; // 列表初始化
```

**常用操作**：
```cpp
flst.push_front(100); // 头部插入
flst.insert_after(pos, 20); // 在迭代器pos后插入元素20
flst前端元素：flst front();
flst大小：distance(flst.begin(), flst.end());
```

**遍历方式**：
```cpp
// 迭代器遍历（不支持范围for循环）
for (auto it = flst.begin(); it != flst.end(); ++it) {
    cout << *it << " ";
}
```

**注意事项**：
⚠️ **特性限制**：
- 不支持随机访问
- 未提供size()成员函数，需用distance()计算
- 只能通过迭代器进行前向遍历

⚠️ **迭代器稳定性**：
- 插入操作不会使其他迭代器失效
- 删除操作仅使被删除元素的迭代器失效

### 二、关联式容器

#### ✅ set / multiset

**特点**：基于红黑树实现，自动排序，元素唯一（set）或可重复（multiset）。

**声明方法**：
```cpp
#include <set>
using namespace std;

// 基本声明（默认升序）
set<int> s;
multiset<string> ms;

// 指定降序排序
set<int, greater<int>> sDesc;

// 指定自定义比较函数
struct Compare {
    bool operator()(const string& s1, const string& s2) {
        return s1.length() < s2.length();
    }
};
set<string, Compare> sCustom;
```

**常用操作**：
```cpp
s.insert(100);      // 插入元素
s.find(50);           // 查找元素，返回迭代器
s.count(20);          // 统计元素出现次数
s前端元素：s.begin();
s尾端元素：s.rbegin();
```

**遍历方式**：
```cpp
// 按升序遍历
for (const auto& x : s) {
    cout << x << " ";
}

// 按降序遍历
for (auto it = s.rbegin(); it != s.rend(); ++it) {
    cout << *it << " ";
}
```

**注意事项**：
⚠️ **键值不可修改**：
- set/multiset的元素是常量，无法直接修改键值
- 如需修改键值，必须先 erase 再 insert

⚠️ **迭代器失效**：
- 插入操作不会使其他迭代器失效
- 删除操作仅使被删除元素的迭代器失效

#### ✅ map / multimap

**特点**：基于红黑树实现，按键值自动排序的键值对容器。

**声明方法**：
```cpp
#include <map>
using namespace std;

// 基本声明（默认升序）
map<string, int> m;
multimap<int, string> mm;

// 指定降序排序
map<int, string, greater<int>> mDesc;

// 指定自定义比较函数
struct CompareKey {
    bool operator()(const string& k1, const string& k2) {
        return k1.length() < k2.length();
    }
};
map<string, int, CompareKey> mCustom;
```

**常用操作**：
```cpp
m.insert({"age", 30});         // 插入键值对
m["name"] = "Alice";             // 直接赋值
m.find(20);                         // 查找键值
m.count(10);                        // 统计键值出现次数
m前端键值对：m.begin();
m尾端键值对：m.rbegin();
```

**遍历方式**：
```cpp
// 使用引用修改值（C++11起）
for (auto& p : m) {
    cout << p.first << ": " << p.second << " ";
    p.second *= 2; // 正确修改值
}

// 迭代器遍历
for (auto it = m.begin(); it != m.end(); ++it) {
    cout << it->first << ": " << it->second << " ";
}
```

**注意事项**：
⚠️ **键值不可修改**：
- map/multimap的键是常量，无法直接修改
- 如需修改键值，必须先 erase 再 insert

⚠️ **迭代器失效**：
- 插入操作不会使其他迭代器失效
- 删除操作仅使被删除元素的迭代器失效

#### ✅ multiset / multimap

**特点**：允许键值重复的关联容器，其他特性与set(map相同。

**声明方法**：
```cpp
// 声明方式与set(map基本相同
multiset<int> ms;
multimap<string, int> mm;
```

**注意事项**：
⚠️ **查找效率**：
- 使用`equal_range()`查找所有相等键值的范围
- 使用`lower_bound()`和`upper_bound()`获取键值的边界

### 三、无序关联式容器

#### ✅ unordered_set / unordered_multiset

**特点**：基于哈希表实现，不排序，查找效率高。

**声明方法**：
```cpp
#include <unordered_set>
using namespace std;

// 基本声明
unordered_set<int> us;
unordered_multiset<string> ms;

// 指定自定义哈希函数
struct MyHash {
    size_t operator()(const string& s) const {
        return hash<string>()(s);
    }
};
unordered_set<string, MyHash> usCustom;

// 指定自定义比较函数
struct Compare {
    bool operator()(const int& a, const int& b) const {
        return a < b;
    }
};
unordered_set<int, Compare> usCompare;
```

**常用操作**：
```cpp
us.insert(100);      // 插入元素
us.find(50);           // 查找元素
us.count(20);          // 统计出现次数
us前端元素：us.begin();
```

**遍历方式**：
```cpp
for (const auto& x : us) {
    cout << x << " ";
}
```

**注意事项**：
⚠️ **哈希特性**：
- 元素存储顺序由哈希函数决定，不保证稳定
- 负载因子超过阈值时会触发rehash，使所有迭代器失效

⚠️ **迭代器失效**：
- 普通插入/删除操作不会使其他迭代器失效
- rehash操作会使所有迭代器失效

#### ✅ unordered_map / unordered_multimap

**特点**：基于哈希表实现，按键值存储键值对，不排序。

**声明方法**：
```cpp
#include <unordered_map>
using namespace std;

// 基本声明
unordered_map<string, int> um;
unordered_multimap<int, string> mm;

// 指定自定义哈希函数
struct KeyHash {
    size_t operator()(const string& key) const {
        return hash<string>()(key);
    }
};
unordered_map<string, int, KeyHash> umCustom;

// 指定自定义比较函数
struct KeyCompare {
    bool operator()(const string& k1, const string& k2) const {
        return k1.length() < k2.length();
    }
};
unordered_map<string, int, KeyHash, KeyCompare> umFull;
```

**常用操作**：
```cpp
um.insert({"age", 30});         // 插入键值对
um["name"] = "Alice";             // 直接赋值
um.find(20);                         // 查找键值
um.count(10);                        // 统计出现次数
um前端键值对：um.begin();
```

**遍历方式**：
```cpp
// 使用结构化绑定（C++17起）
for (const auto& [k, v] : um) {
    cout << k << ": " << v << " ";
}

// 兼容写法
for (const auto& p : um) {
    cout << p.first << ": " << p.second << " ";
}
```

**注意事项**：
⚠️ **键值不可修改**：
- unordered_map/multimap的键是常量，无法直接修改
- 如需修改键值，必须先 erase 再 insert

⚠️ **哈希特性**：
- 元素存储顺序由哈希函数决定，不保证稳定
- 负载因子超过阈值时会触发rehash，使所有迭代器失效

⚠️ **性能优化**：
- 使用`reserve()`预分配桶数，减少rehash次数
- 选择合适的哈希函数和比较函数以提高性能

### 四、容器适配器

#### ✅ stack（栈）

**特点**：LIFO（后进先出）数据结构，仅支持栈顶操作。

**声明方法**：
```cpp
#include <stack>
using namespace std;

// 默认使用vector作为底层容器
stack<int> st;

// 指定底层容器为deque
stack<int, deque<int>> stDeque;

// 指定底层容器为list（支持更高效的pop操作）
stack<int, list<int>> stList;
```

**常用操作**：
```cpp
st.push(100);   // 入栈
st.pop();        // 出栈
栈顶元素：st.top();
栈是否为空：st.empty();
```

**遍历方式**：
```cpp
// 需要先复制到临时容器
vector<int> temp;
while (!st.empty()) {
    temp.push_back(st.top());
    st.pop();
}

// 反向遍历（恢复栈内容）
for (auto x : temp) {
    cout << x << " ";
    st.push(x);
}
```

**注意事项**：
⚠️ **底层容器选择**：
- 默认使用vector，适合大多数场景
- 若需要频繁弹出操作，可考虑使用list作为底层容器

⚠️ **迭代器限制**：
- stack适配器本身不提供迭代器
- 需要遍历元素时，应考虑使用其他容器或临时复制

#### ✅ queue（队列）

**特点**：FIFO（先进先出）数据结构，支持队首删除和队尾插入。

**声明方法**：
```cpp
#include <queue>
using namespace std;

// 默认使用deque作为底层容器
queue<string> que;

// 指定底层容器为list
queue<int, list<int>> queList;
```

**常用操作**：
```cpp
que.push(100);   // 入队
que.pop();        // 出队
队首元素：que.front();
队尾元素：que.back();
队列是否为空：que.empty();
```

**遍历方式**：
```cpp
// 需要先复制到临时容器
deque<int> temp;
while (!que.empty()) {
    temp.push_back(que.front());
    que.pop();
}

// 遍历并恢复队列内容
for (auto x : temp) {
    cout << x << " ";
    que.push(x);
}
```

**注意事项**：
⚠️ **底层容器选择**：
- 默认使用deque，支持高效的首尾操作
- 若需要其他特性，可选择vector或list作为底层容器

⚠️ **迭代器限制**：
- queue适配器本身不提供迭代器
- 需要遍历元素时，应考虑使用其他容器或临时复制

#### ✅ priority_queue（优先队列）

**特点**：基于堆实现，自动维护元素优先级，支持高效插入和提取最高优先级元素。

**声明方法**：
```cpp
#include <queue>
using namespace std;

// 默认大根堆（vector作为底层容器）
priority_queue<int> pq;

// 指定底层容器为deque
priority_queue<int, deque<int>> pqDeque;

// 小根堆（使用greater<int>作为比较函数）
priority_queue<int, vector<int>, greater<int>> pqSmall;

// 自定义结构体和比较函数
struct Item {
    int priority;
    string value;
};

struct Compare {
    bool operator()(const Item& a, const Item& b) {
        return a.priority > b.priority; // 按优先级升序排列
    }
};

priority_queue<Item, vector<Item>, Compare> pqCustom;
```

**常用操作**：
```cpp
pq.push(100);   // 插入元素
pq.pop();        // 弹出最高优先级元素
最高优先级元素：pq.top();
```

**遍历方式**：
```cpp
// 不推荐直接遍历优先队列元素
// 如需遍历，应先复制到临时容器
vector<int> temp;
while (!pq.empty()) {
    temp.push_back(pq.top());
    pq.pop();
}

// 遍历并恢复优先队列内容
for (auto x : temp) {
    cout << x << " ";
    pq.push(x);
}
```

**注意事项**：
⚠️ **底层容器选择**：
- 默认使用vector，支持高效的堆操作
- 若需要其他特性，可选择deque或list作为底层容器

⚠️ **堆结构特性**：
- 元素存储顺序由堆结构决定，不保证稳定
- 优先队列不提供直接遍历或访问内部元素的接口

⚠️ **比较函数**：
- 默认使用`less<T>`实现大根堆
- 实现小根堆需使用`greater<T>`作为比较函数

### 五、容器操作通用注意事项

#### 1. 范围for循环的限制

**问题描述**：范围for循环中的元素是拷贝还是引用，直接影响能否修改容器元素。

**错误示例**：
```cpp
vector<int> vec = {1, 2, 3};
for (auto x : vec) { // x是拷贝
    x *= 2;             // 仅修改拷贝，不影响vec
}
```

**正确做法**：
```cpp
// 使用引用修改元素值
for (auto& x : vec) { // x是引用
    x *= 2;             // 正确修改vec中的元素
}

// 使用迭代器修改元素值
for (auto it = vec.begin(); it != vec.end(); ++it) {
    *it *= 2;           // 正确修改vec中的元素
}
```

**注意事项**：
⚠️ 范围for循环中变量是元素的拷贝，直接修改不会影响容器
⚠️ 如需修改元素值，必须使用`auto&`或迭代器
⚠️ 对于关联容器（如map），键值不可修改，只能修改值部分

#### 2. erase操作导致的迭代器失效

**问题描述**：调用erase后，指向被删除元素的迭代器将失效，继续使用会导致未定义行为。

**错误示例**：
```cpp
vector<int> vec = {1, 2, 3, 4, 5};
auto it = vec.begin();
vec.erase(it); // it失效
++it;           // ❌ 未定义行为！
```

**正确做法**：
```cpp
// 使用erase返回值更新迭代器
auto it = vec.begin();
it = vec.erase(it); // it指向下一个有效元素

// 安全删除模式
for (auto it = vec.begin(); it != vec.end(); ) {
    if (*it == 3) {
        it = vec.erase(it); // vector/deque
    } else {
        ++it;
    }
}
```

**注意事项**：
⚠️ **关联容器（set(map））**：erase返回void，应使用`it = m.erase(it)`或`m.erase(it++)`  
⚠️ **unordered容器**：erase仅使被删除元素的迭代器失效
⚠️ **list/forward_list**：erase后迭代器指向下一个有效元素

#### 3. insert操作导致的迭代器失效

**问题描述**：某些容器的insert操作可能导致其他迭代器失效，影响程序稳定性。

**风险等级**：
| 容器类型 | 插入操作风险 | 失效范围 |
|----------|--------------|----------|
| vector/deque | 高风险 | 可能导致所有迭代器失效 |
| list/forward_list | 低风险 | 仅使被操作的迭代器失效 |
| set(map) | 中风险 | 仅使被操作的迭代器失效 |
| unordered容器 | 中低风险 | 一般不失效，除非触发rehash |

**正确做法**：
```cpp
// vector/deque：插入后重新获取迭代器
auto it = vec.begin() + 2;
it = vec.insert(it, 100); // it指向插入位置

// list/forward_list：插入后迭代器仍有效
auto pos = lst.begin();
lst.insert(pos, 200); // pos仍指向原位置

// 关联容器：插入后迭代器仍有效
auto it = s.find(50);
s.insert({60, "sixty"}); // it仍有效
```

**注意事项**：
⚠️ **vector/deque**：插入可能导致内存重新分配，使所有迭代器失效
⚠️ **unordered容器**：rehash操作会使所有迭代器失效
⚠️ **性能优化**：频繁插入时，考虑使用list或unordered容器

### 六、容器特性对比速查表

| 容器类型 | 内存布局 | 随机访问 | 插入/删除效率 | 排序 | 迭代器失效风险 | 声明示例 |
|----------|----------|----------|----------------|------|----------------|----------|
| vector | 连续内存 | ✅ | 尾部O(1)，中间O(n) | 否 | 插入可能失效 | vector<int> v; |
| deque | 分块连续内存 | ✅ | 首尾O(1)，中间O(n) | 否 | 插入可能失效 | deque<string> deq; |
| list | 双向链表 | ❌ | 任意位置O(1) | 否 | 仅被删元素失效 | list<int> lst; |
| forward_list | 单向链表 | ❌ | 任意位置O(1) | 否 | 仅被删元素失效 | forward_list<int> flst; |
| set | 红黑树 | ❌ | O(log n) | 是（自动排序） | 仅被删元素失效 | set<int> s; |
| map | 红黑树 | ❌ | O(log n) | 是（按键排序） | 仅被删元素失效 | map<string, int> m; |
| unordered_set | 哈希表 | ✅ | 平均O(1)，最坏O(n) | 否 | 一般不失效，除非rehash | unordered_set<int> us; |
| unordered_map | 哈希表 | ✅ | 平均O(1)，最坏O(n) | 否 | 一般不失效，除非rehash | unordered_map<string, int> um; |
| stack | 依赖底层容器 | 依赖底层容器 | 依赖底层容器 | 依赖底层容器 | 依赖底层容器 | stack<int> st; |
| queue | 依赖底层容器 | 依赖底层容器 | 依赖底层容器 | 依赖底层容器 | 依赖底层容器 | queue<string> que; |
| priority_queue | 依赖底层容器 | 依赖底层容器 | 依赖底层容器 | 是（按优先级排序） | 依赖底层容器 | priority_queue<int> pq; |

**选择建议**：
- 频繁随机访问 → vector/deque
- 频繁插入/删除 → list/forward_list
- 需要自动排序 → set(map)
- 高效查找 → unordered_set(map)
- LIFO/FIFO → stack/queue
- 优先级管理 → priority_queue

### 七、容器使用最佳实践


#### 1. 遍历与修改安全模式

**删除元素通用模式**：
```cpp
// vector/deque
for (auto it = vec.begin(); it != vec.end(); ) {
    if (shouldDelete(*it)) {
        it = vec.erase(it); // 使用返回值更新迭代器
    } else {
        ++it;
    }
}

// list/forward_list
for (auto it = lst.begin(); it != lst.end(); ) {
    if (shouldDelete(*it)) {
        it = lst.erase(it); // 使用返回值更新迭代器
    } else {
        ++it;
    }
}

// set(map)/unordered容器
for (auto it = s.begin(); it != s.end(); ) {
    if (shouldDelete(*it)) {
        it = s.erase(it); // C++11起可使用返回值
    } else {
        ++it;
    }
}
```

**关联容器键值修改模式**：
```cpp
// set的键值修改
auto it = s.find(50);
if (it != s.end()) {
    int oldKey = *it;
    s.insert(oldKey + 10); // 新键值
    s.erase(oldKey);         // 删除旧键值
}

// map的键值修改
auto it = m.find("oldKey");
if (it != m.end()) {
    string newKey = "newKey";
    m[newKey] = it->second; // 新键值
    m.erase(it);               // 删除旧键值
}
```

#### 2. 性能关键点

**时间复杂度对比**：
| 操作 | vector | deque | list | set(map) | unordered容器 |
|------|--------|-------|------|----------|--------------|
| 随机访问 | O(1) | O(1) | O(n) | O(log n) | O(1)平均 |
| 尾部插入 | O(1)均摊 | O(1)均摊 | O(1) | O(log n) | O(1)平均 |
| 首部插入 | O(n) | O(1)均摊 | O(1) | O(log n) | O(1)平均 |
| 中间插入 | O(n) | O(n) | O(1) | O(log n) | O(n)平均 |
| 删除操作 | O(n) | O(n) | O(1) | O(log n) | O(1)平均 |

**空间复杂度对比**：
| 容器类型 | 空间复杂度 | 内存碎片 |
|----------|------------|----------|
| vector/deque | O(n) | 低（连续/分块连续） |
| list/forward_list | O(n) + O(指针开销) | 高（非连续） |
| set(map) | O(n) + O(树结构开销) | 中等 |
| unordered容器 | O(n) + O(桶结构开销) | 中等 |

### 八、总结与建议


**通用建议**：
- 优先使用范围for循环遍历容器
- 需要修改元素时，使用`auto&`或迭代器
- 频繁删除元素时，采用安全删除模式
- 考虑内存管理优化（如reserve、shrink_to_fit）
- 根据数据访问模式选择合适容器

