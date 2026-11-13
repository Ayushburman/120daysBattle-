import React, { useState, useEffect, useMemo } from 'react';
import {
  Cpu,
  Terminal,
  Trophy,
  Zap,
  BookOpen,
  Play,
  RotateCcw,
  CheckCircle2,
  AlertTriangle,
  ChevronRight,
  ChevronLeft,
  Layers,
  GitBranch,
  Hash,
  Network,
  Award,
  Search,
  Clock,
  Check,
  X,
  Sparkles,
  Flame,
  ShieldAlert,
  Code2,
  Calculator,
  ArrowRight,
  Database,
  Activity,
  Target
} from 'lucide-react';

// ============================================================================
// PLAYER RANKS & GAMIFICATION CONFIG
// ============================================================================
const PLAYER_RANKS = [
  { level: 1, title: 'Memory Novice', minXp: 0, maxXp: 200, color: 'text-slate-300', border: 'border-slate-500/40', bg: 'bg-slate-800/60' },
  { level: 2, title: 'Pointer Apprentice', minXp: 200, maxXp: 450, color: 'text-cyan-400', border: 'border-cyan-500/40', bg: 'bg-cyan-950/40' },
  { level: 3, title: 'Recursion Mage', minXp: 450, maxXp: 750, color: 'text-emerald-400', border: 'border-emerald-500/40', bg: 'bg-emerald-950/40' },
  { level: 4, title: 'Tree Architect', minXp: 750, maxXp: 1100, color: 'text-violet-400', border: 'border-violet-500/40', bg: 'bg-violet-950/40' },
  { level: 5, title: 'Graph Warlord', minXp: 1100, maxXp: 1500, color: 'text-amber-400', border: 'border-amber-500/40', bg: 'bg-amber-950/40' },
  { level: 6, title: 'GATE 2027 AIR < 100 Legend', minXp: 1500, maxXp: 2500, color: 'text-rose-400', border: 'border-rose-500/50', bg: 'bg-rose-950/40' }
];

// ============================================================================
// 6 SYLLABUS REALMS DATA (SCRATCH TO GATE 2027 LEVEL)
// ============================================================================
const SYLLABUS_REALMS = [
  {
    id: 'realm-1',
    number: 1,
    title: 'C Pointers, Memory Layout & Recursion Stack',
    weightage: '3.5 Marks',
    icon: 'Cpu',
    accent: 'cyan',
    tagline: 'Master raw memory addressing, 2D pointer arithmetic, and stack activation frames.',
    interactiveTool: 'array2d',
    sublevels: [
      {
        id: 'r1-s1',
        tier: 'Level 1: Scratch Intuition',
        title: 'Memory Segments & 2D Array Address Geometry',
        summary: 'How RAM flattens multi-dimensional matrices into linear byte streams.',
        mentalModel: `Every variable lives at a byte address in Virtual Memory:
[Text/Code] -> [Data (Initialized Global/Static)] -> [BSS (Zero-Init Static)] -> [Heap (malloc grows UP)] ... [Stack (Activation frames grow DOWN)].

Even though we visualize int A[R][C] as a 2D grid, RAM is strictly 1-Dimensional!
• Row-Major Order (Used by C/C++): Stores Row 0 completely, then Row 1, etc.
  Address(A[i][j]) = Base + ((i - LB_r) * C + (j - LB_c)) * sizeof(element)
• Column-Major Order (Used by Fortran/MATLAB): Stores Col 0 completely, then Col 1.
  Address(A[i][j]) = Base + ((j - LB_c) * R + (i - LB_r)) * sizeof(element)`,
        code: `// C Row-Major Memory Flattening Demonstration
#include <stdio.h>
int main() {
    int A[3][4] = {
        {10, 11, 12, 13}, // Row 0
        {20, 21, 22, 23}, // Row 1
        {30, 31, 32, 33}  // Row 2
    };
    // A, &A[0], and &A[0][0] have the SAME numerical base address,
    // but DIFFERENT pointer types!
    // A + 1 jumps by 1 full row (4 * sizeof(int) = 16 bytes)
    // *(A + 1) + 2 jumps 1 row, then 2 columns -> &A[1][2]
    printf("Val at A[1][2] = %d\\n", *(*(A + 1) + 2)); // Outputs 22
    return 0;
}`,
        gateTrap: 'GATE TRAP: Do not confuse "int *p[4]" (Array of 4 integer pointers) with "int (*p)[4]" (Single pointer to an array of 4 integers). When incrementing p++, the latter jumps by 4 * sizeof(int) bytes!'
      },
      {
        id: 'r1-s2',
        tier: 'Level 2: Core Mechanics & C Implementation',
        title: 'Pointer Arithmetic, Void Pointers & Endianness',
        summary: 'Mastering dereference chains, type casting, and Little vs Big Endian byte order.',
        mentalModel: `When you add an integer k to any typed pointer ptr:
New_Address = Old_Address + k * sizeof(*ptr)

When subtracting two pointers of the same type (p2 - p1):
Result = (Raw_Address(p2) - Raw_Address(p1)) / sizeof(*p1)  <-- Number of ELEMENTS between them, NOT bytes!

Little Endian vs Big Endian (for 32-bit int x = 0x12345678 at 0x100):
• Little Endian (x86): Least Significant Byte (0x78) stored at LOWEST address (0x100).
• Big Endian (Network): Most Significant Byte (0x12) stored at LOWEST address (0x100).`,
        code: `void pointer_gauntlet() {
    int arr[] = {10, 20, 30, 40, 50};
    int *p = arr;
    int *q = &arr[3];
    
    // Difference of pointers = number of elements
    printf("%ld\\n", q - p); // Prints 3 (NOT 12 bytes!)
    
    // Post-increment vs Dereference precedence:
    // *p++   => *(p++) : returns *p (10), then advances p to arr[1]
    // (*p)++ => increments the value at p (20 becomes 21)
    // *++p   => *(++p) : advances p first, then dereferences
}`,
        gateTrap: 'GATE TRAP: Taking the difference of two pointers (q - p) divides the byte difference by sizeof(type). However, if they are cast to (char*)q - (char*)p, it gives the exact byte difference!'
      },
      {
        id: 'r1-s3',
        tier: 'Level 3: GATE Edge Cases & Traps',
        title: 'Recursion Activation Records & Static Variables',
        summary: 'Tracing tree recursion with static variables and Stack Space vs Time Complexity.',
        mentalModel: `Every recursive call pushes an Activation Record (Stack Frame) containing:
1. Local variables & formal parameters (Unique copy per call)
2. Return address (Which line in caller to resume at)
3. Saved registers / Frame pointer

CRITICAL DISTINCTION:
• Time Complexity = Total number of nodes in the Recursion Tree (e.g., O(2^n) for fib(n)).
• Space Complexity = MAXIMUM HEIGHT of the Recursion Tree active at any single instant (e.g., O(n) for fib(n) because left subtree finishes & pops before right subtree starts!).
• Static Variables inside recursion live in the Data Segment—only ONE single box exists across ALL recursive frames!`,
        code: `int fun(int n) {
    static int x = 0; // Initialized ONLY ONCE before main starts!
    if (n > 0) {
        x++;
        return fun(n - 1) + x;
    }
    return 0;
}
// Trace for fun(3):
// fun(3): x becomes 1, calls fun(2) + x
// fun(2): x becomes 2, calls fun(1) + x
// fun(1): x becomes 3, calls fun(0) + x
// fun(0): returns 0.
// Now unwinding! When "+ x" is evaluated, x is ALREADY 3 for ALL frames!
// Result = ((0 + 3) + 3) + 3 = 9! (And generally n * n for fun(n))`,
        gateTrap: 'GATE TRAP: In expressions like "return fun(n-1) + x;" where x is static or global, C evaluates x AFTER fun(n-1) completely finishes! So every frame adds the FINAL mutated value of x.'
      }
    ]
  },
  {
    id: 'realm-2',
    number: 2,
    title: 'Linear Data Structures (Lists, Stacks, Queues)',
    weightage: '2.5 Marks',
    icon: 'Layers',
    accent: 'emerald',
    tagline: 'Conquer pointer rewiring, Floyd cycle math, stack evaluators, and amortized queues.',
    interactiveTool: 'circularQueue',
    sublevels: [
      {
        id: 'r2-s1',
        tier: 'Level 1: Scratch Intuition',
        title: 'Singly, Doubly & Circular Linked List Pointer Surgery',
        summary: 'Reversing lists in O(1) space and proving Floyd Tortoise-Hare cycle detection.',
        mentalModel: `In Linked List questions, NEVER write code blindly—trace the pointer assignment order!
Rule of Pointer Surgery: Never overwrite a pointer (e.g., head->next) before saving its target in a temporary pointer (unless you intend to free/drop it).

Floyd's Cycle Detection (Tortoise & Hare):
• slow moves 1 step, fast moves 2 steps.
• If cycle of length L exists, they MUST meet inside the cycle in O(n) time.
• Distance from head to cycle start = x; distance from cycle start to meeting point = y.
• Meeting condition: 2(x + y) = x + y + k*L  ==>  x = k*L - y.
• Resetting one pointer to Head and advancing both by 1 step makes them collide at the EXACT start of the cycle!`,
        code: `// Iterative O(n) Time, O(1) Space Linked List Reversal
struct Node* reverseList(struct Node* head) {
    struct Node *prev = NULL, *curr = head, *next = NULL;
    while (curr != NULL) {
        next = curr->next; // 1. Save next node
        curr->next = prev; // 2. Reverse current link
        prev = curr;       // 3. Advance prev
        curr = next;       // 4. Advance curr
    }
    return prev; // New head!
}`,
        gateTrap: 'GATE TRAP: Deleting the LAST node of a Singly Linked List takes Theta(n) time EVEN IF you maintain a tail pointer, because you must update the second-last node’s next pointer!'
      },
      {
        id: 'r2-s2',
        tier: 'Level 2: Core Mechanics & C Implementation',
        title: 'Stack Applications: Infix, Postfix & Stack Permutations',
        summary: 'Operator precedence, associativity rules, and Catalan stack-sortable permutations.',
        mentalModel: `Infix to Postfix Operator Precedence & Associativity:
1. Exponent (^) -> Highest precedence, RIGHT-to-LEFT associative!
   Wait: Because ^ is Right-to-Left, if '^' is on top of stack and incoming is '^', you PUSH (do not pop!).
   Example: a ^ b ^ c  ==>  a b c ^ ^
2. Multiplication/Division (*, /) -> Middle precedence, LEFT-to-RIGHT associative.
   If '*' is on top and '/' arrives, POP '*' first!
3. Addition/Subtraction (+, -) -> Lowest precedence, LEFT-to-RIGHT associative.

Stack Permutations:
Given input sequence 1, 2, ..., n, how many valid output permutations can be generated using a single Stack?
Answer = n-th Catalan Number: C_n = (1 / (n + 1)) * (2n choose n).
Forbidden Pattern: A permutation is INVALID iff it contains subsequence (i < j < k) appearing in order (k, i, j) — e.g., 3, 1, 2!`,
        code: `// Evaluating Postfix Expression using a Stack
// Scan left to right:
// - If operand: push(val)
// - If binary operator 'op':
//     op2 = pop();  // CRITICAL: First popped is RIGHT operand!
//     op1 = pop();  // Second popped is LEFT operand!
//     push(compute(op1, op, op2));`,
        gateTrap: 'GATE TRAP: When evaluating Postfix for non-commutative operators (-, /, ^), the FIRST popped element is the second operand (B), and the SECOND popped element is the first operand (A): compute(A - B), NOT (B - A)!'
      },
      {
        id: 'r2-s3',
        tier: 'Level 3: GATE Edge Cases & Traps',
        title: 'Circular Queues & Amortized O(1) Queue using Two Stacks',
        summary: 'Modulo index wrap-around and accounting method for 2-stack queues.',
        mentalModel: `Circular Queue in Array of size N (0 to N-1):
• Advance pointer: idx = (idx + 1) % N
• Empty vs Full Ambiguity: In standard textbook implementation where 1 slot is kept spare:
  - Empty condition: front == rear
  - Full condition: (rear + 1) % N == front
  - Maximum capacity = N - 1 elements!
  - Current number of elements = (rear - front + N) % N

Queue using Two Stacks (S1 for Enqueue, S2 for Dequeue):
• Enqueue(x): Push x onto S1 -> O(1) worst-case.
• Dequeue(): If S2 is not empty, pop(S2) in O(1). If S2 is empty, pop ALL elements from S1 and push into S2 (Takes O(n) worst-case), then pop(S2).
• Amortized Analysis: Every element is pushed into S1 once, popped from S1 once, pushed into S2 once, and popped from S2 once. Total = 4 operations per element -> O(1) AMORTIZED time per operation!`,
        code: `// Queue using 2 Stacks: Dequeue Operation
int dequeue(Stack *S1, Stack *S2) {
    if (isEmpty(S2)) {
        while (!isEmpty(S1)) {
            push(S2, pop(S1)); // Reverses order into FIFO!
        }
    }
    return pop(S2);
}
// Worst-case single Dequeue = O(n)
// Sequence of n Enqueues and n Dequeues = O(n) total = O(1) amortized!`,
        gateTrap: 'GATE TRAP: Watch the exact wording in GATE! "Worst-case time of a single Dequeue" is Theta(n), whereas "Amortized time per operation over n operations" is Theta(1).'
      }
    ]
  },
  {
    id: 'realm-3',
    number: 3,
    title: 'Trees, BST, AVL & Binary Heaps',
    weightage: '4.0 Marks',
    icon: 'GitBranch',
    accent: 'violet',
    tagline: 'Guaranteed 3-4 marks every year. Master Catalan bounds, AVL rotations, and O(n) Build-Heap.',
    interactiveTool: 'catalanAvl',
    sublevels: [
      {
        id: 'r3-s1',
        tier: 'Level 1: Scratch Intuition',
        title: 'Binary Tree Theorems, Traversals & Catalan Counting',
        summary: 'Leaf-to-Internal node identities, traversal reconstructions, and tree combinatorics.',
        mentalModel: `Core Binary Tree Identities (Memorize for NATs!):
1. Degree-2 vs Leaf Theorem: In ANY non-empty binary tree, number of leaf nodes (L) and number of internal nodes with 2 children (I_2) satisfy:
   L = I_2 + 1   (Nodes of degree 1 do NOT affect this equation!)
2. Strictly (Full) k-ary Tree with I internal nodes:
   Total Leaves L = (k - 1)*I + 1
3. Counting Binary Trees with n nodes:
   • Unlabeled Binary Trees = C_n = (1/(n+1)) * (2n choose n)  [1, 1, 2, 5, 14, 42, 132...]
   • Number of distinct BSTs with n distinct keys = C_n
   • Labeled Binary Trees with n distinct nodes = C_n * n!
4. Unique Tree Reconstruction:
   • Inorder + Preorder = UNIQUE Binary Tree
   • Inorder + Postorder = UNIQUE Binary Tree
   • Preorder + Postorder = NOT unique (Unless the tree is Strictly/Full Binary Tree!)`,
        code: `// Number of NULL pointers in any Binary Tree of n nodes:
// Total pointers = 2n. Used pointers (edges) = n - 1.
// Therefore, NULL pointers = 2n - (n - 1) = n + 1!

int countLeaves(Node* root) {
    if (!root) return 0;
    if (!root->left && !root->right) return 1;
    return countLeaves(root->left) + countLeaves(root->right);
}`,
        gateTrap: 'GATE TRAP: Given ONLY the Preorder traversal of a Binary Search Tree (BST), can you uniquely reconstruct the BST? YES! Because sorting the keys gives the Inorder traversal of a BST automatically!'
      },
      {
        id: 'r3-s2',
        tier: 'Level 2: Core Mechanics & C Implementation',
        title: 'AVL Trees: Balance Factors, Rotations & Minimum Nodes',
        summary: 'LL, RR, LR, RL rotations and Fibonacci recurrence for minimal AVL trees.',
        mentalModel: `AVL Tree Property: For EVERY node, Balance Factor BF = Height(Left) - Height(Right) must be in {-1, 0, +1}.

The 4 AVL Rotations (Triggered at the lowest unbalanced ancestor):
• LL Imbalance (Inserted in Left child's Left subtree): 1 Right Rotation (Single rotation)
• RR Imbalance (Inserted in Right child's Right subtree): 1 Left Rotation (Single rotation)
• LR Imbalance (Inserted in Left child's Right subtree): Left Rotate child + Right Rotate root (2 rotations)
• RL Imbalance (Inserted in Right child's Left subtree): Right Rotate child + Left Rotate root (2 rotations)

Minimum Nodes in an AVL Tree of Height h (where single node height = 0):
N(0) = 1, N(1) = 2
N(h) = N(h - 1) + N(h - 2) + 1
Sequence for h = 0, 1, 2, 3, 4, 5, 6:
1, 2, 4, 7, 12, 20, 33, 54...  (Notice: N(h) = Fibonacci(h + 3) - 1)`,
        code: `// Insertion vs Deletion Rotation Counts in AVL Tree:
// 1. Insertion: Requires at most O(1) rotations (1 single or 1 double rotation)
//    to restore balance globally!
// 2. Deletion: May propagate up to the root, requiring O(log n) rotations!`,
        gateTrap: 'GATE TRAP: Always check whether the question defines height of a single node as h = 0 (edges) or h = 1 (nodes)! The recurrence N(h) = N(h-1) + N(h-2) + 1 stays identical, only the starting index shifts.'
      },
      {
        id: 'r3-s3',
        tier: 'Level 3: GATE Edge Cases & Traps',
        title: 'Binary Heaps: O(n) Build-Heap Proof & K-th Element Bounds',
        summary: 'Complete binary tree indexing, bottom-up heapify math, and min/max locations.',
        mentalModel: `Binary Max-Heap in 0-indexed Array of size n:
• Parent(i) = floor((i - 1) / 2)
• Left(i) = 2*i + 1, Right(i) = 2*i + 2
• Non-leaf (Internal) nodes: indices 0 to floor(n/2) - 1
• Leaf nodes: indices floor(n/2) to n - 1  (Total leaves = ceil(n / 2))

Why Build-Max-Heap is O(n) and NOT O(n log n):
We run Max-Heapify bottom-up from i = floor(n/2) - 1 down to 0.
Leaves (n/2 nodes) do 0 work. Height-1 nodes (n/4) do O(1) work.
Total Work = sum_{h=0}^{log n} ceil(n / 2^{h+1}) * O(h) = O(n) * sum(h / 2^h) <= 2n = O(n)!

Where is the Minimum element in a Max-Heap of n distinct elements?
It MUST be one of the ceil(n/2) leaf nodes! Finding it takes Theta(n) comparisons.`,
        code: `// Build-Max-Heap in Theta(n) Worst-Case Time
void buildMaxHeap(int arr[], int n) {
    // Leaves are already trivial heaps; start from last internal node
    for (int i = (n / 2) - 1; i >= 0; i--) {
        maxHeapify(arr, n, i);
    }
}`,
        gateTrap: 'GATE TRAP: Finding the k-th largest element in a Max-Heap of size n (where k is a small constant like 7) takes O(k log k) — which is O(1)! You do NOT need to inspect the whole heap, only a mini-heap of candidates of depth k!'
      }
    ]
  },
  {
    id: 'realm-4',
    number: 4,
    title: 'Hashing & Collision Resolution',
    weightage: '2.0 Marks',
    icon: 'Hash',
    accent: 'amber',
    tagline: 'Crack probe sequences, primary vs secondary clustering, and expected slot probabilities.',
    interactiveTool: 'hashEstimator',
    sublevels: [
      {
        id: 'r4-s1',
        tier: 'Level 1: Scratch Intuition',
        title: 'Uniform Hashing, Load Factor & Chaining Analysis',
        summary: 'Expected chain lengths and successful vs unsuccessful search complexities.',
        mentalModel: `Hash Table with m slots and n stored keys:
Load Factor alpha = n / m.
In Chaining (Linked Lists at each slot), alpha can be > 1.
Under Simple Uniform Hashing (every key is equally likely to hash to any of the m slots independently):
• Unsuccessful Search Expected Time = Theta(1 + alpha)
  (1 to compute hash & check head + alpha expected elements in the chain)
• Successful Search Expected Time = Theta(1 + (n - 1)/(2m)) = Theta(1 + alpha)
• Probability that a specific slot receives k keys out of n insertions:
  P(X = k) = (n choose k) * (1/m)^k * (1 - 1/m)^(n - k)`,
        code: `// Expected number of EMPTY slots after inserting n keys into m slots:
// Probability 1 slot stays empty after 1 insertion = (1 - 1/m)
// Probability 1 slot stays empty after n insertions = (1 - 1/m)^n
// By Linearity of Expectation across m slots:
// Expected Empty Slots = m * (1 - 1/m)^n
// Expected Collisions = n - Occupied_Slots = n - m * (1 - (1 - 1/m)^n)`,
        gateTrap: 'GATE TRAP: Memorize the Linearity of Expectation formula: Expected empty slots after n insertions into m slots is m * ((m - 1) / m)^n. This exact formula has appeared in 4+ GATE papers!'
      },
      {
        id: 'r4-s2',
        tier: 'Level 2: Core Mechanics & C Implementation',
        title: 'Open Addressing: Linear, Quadratic & Double Hashing',
        summary: 'Probe formulas, clustering bottlenecks, and tombstone lazy deletion.',
        mentalModel: `In Open Addressing, all keys live inside the table (so alpha = n/m <= 1).
Probe sequence for key k at attempt i = 0, 1, ..., m-1:

1. Linear Probing: h(k, i) = (h(k) + i) mod m
   • Suffers from PRIMARY CLUSTERING: Any key hashing into a contiguous block of occupied slots extends that block, creating a snowball effect!
2. Quadratic Probing: h(k, i) = (h(k) + c1*i + c2*i^2) mod m
   • Eliminates Primary Clustering, but suffers from SECONDARY CLUSTERING: Two keys with the SAME initial hash h(k1) == h(k2) follow the exact same probe sequence!
3. Double Hashing: h(k, i) = (h1(k) + i * h2(k)) mod m
   • Eliminates both Primary and Secondary Clustering!
   • Requirement: h2(k) must NEVER be 0, and gcd(h2(k), m) must be 1 (e.g., m is prime) so all m slots are probed.`,
        code: `// Why Open Addressing requires TOMBSTONES (Deleted Markers):
// Suppose k1 and k2 both hash to slot 3.
// k1 goes to slot 3; k2 collides and goes to slot 4.
// If we delete k1 and simply mark slot 3 as EMPTY, a future search for k2
// will check slot 3, see EMPTY, and falsely conclude k2 is not in the table!`,
        gateTrap: 'GATE TRAP: How many distinct probe sequences can each method generate for table size m? Linear Probing: m sequences. Quadratic Probing: m sequences. Double Hashing: m * (m - 1) sequences!'
      },
      {
        id: 'r4-s3',
        tier: 'Level 3: GATE Edge Cases & Traps',
        title: 'Reverse-Engineering Insertion Orders in Linear Probing',
        summary: 'Deduce valid vs invalid insertion orders from a given final hash table state.',
        mentalModel: `A classic 2-mark GATE problem gives you the final state of a Linear Probing hash table and asks: "Which of the following is a VALID insertion sequence?" or "How many valid insertion sequences exist?"

Golden Rule of Linear Probing Dependency:
If key K has home slot H = K mod m, but K is sitting at slot S (where S != H):
EVERY SINGLE SLOT on the circular path from H to (S - 1) MUST have been occupied BEFORE key K was inserted!
If any key sitting in [H ... S-1] appears AFTER K in an option sequence, eliminate that option immediately!`,
        code: `// Quick Verification Algorithm for GATE Linear Probing Options:
// Step 1: Compute h(k) = k % m for every key in the table.
// Step 2: Any key sitting outside its home slot h(k) depends on all keys
//         occupying slots [h(k), ..., current_slot - 1].
// Step 3: This forms a Directed Acyclic Graph (DAG) of dependencies!
//         The number of valid insertion orders = Number of Topological Sorts!`,
        gateTrap: 'GATE TRAP: Don’t simulate all 4 options from scratch! Just find ONE displaced key K, check which keys sit between its home slot and current slot, and verify K comes after them.'
      }
    ]
  },
  {
    id: 'realm-5',
    number: 5,
    title: 'Asymptotics, Recurrences, Sorting & Divide-and-Conquer',
    weightage: '3.0 Marks',
    icon: 'Activity',
    accent: 'rose',
    tagline: 'Master Theorem edge cases, sorting inversion bounds, and QuickSort worst-case traps.',
    interactiveTool: 'masterTheorem',
    sublevels: [
      {
        id: 'r5-s1',
        tier: 'Level 1: Scratch Intuition',
        title: 'Asymptotic Growth Hierarchy & Master Theorem',
        summary: 'Fast growth rankings, logarithmic traps, and extended Master Theorem cases.',
        mentalModel: `Growth Rate Hierarchy (Smallest to Largest as n -> infinity):
1 < log(log n) < log n < (log n)^c < n^epsilon < n < n log n < n^2 < 2^n < n! < n^n

Crucial Log & Exponent Identities:
• n^(log_b a) == a^(log_b n)
• log(n!) = Theta(n log n)   [Stirling's Approximation]
• 2^(n+1) = Theta(2^n),  BUT  2^(2n) = 4^n != O(2^n)!

Extended Master Theorem for T(n) = a * T(n / b) + Theta(n^k * (log n)^p):
Let c = log_b(a) be the critical exponent.
• Case 1 (c > k): Leaves dominate -> T(n) = Theta(n^(log_b a))
• Case 2 (c == k):
  - If p > -1: T(n) = Theta(n^k * (log n)^(p + 1))
  - If p == -1: T(n) = Theta(n^k * log(log n))
  - If p < -1: T(n) = Theta(n^k)
• Case 3 (c < k): Root dominates (if p >= 0) -> T(n) = Theta(n^k * (log n)^p)`,
        code: `// Common GATE Recurrences to Memorize Instantly:
// 1. T(n) = T(n-1) + O(1)         ==> Theta(n)
// 2. T(n) = T(n-1) + O(n)         ==> Theta(n^2)
// 3. T(n) = 2T(n/2) + O(n)        ==> Theta(n log n)
// 4. T(n) = 2T(n/2) + O(n log n)  ==> Theta(n (log n)^2)  [Case 2: p=1 -> p+1=2]
// 5. T(n) = 2T(n/2) + n / log n   ==> Theta(n log(log n)) [Case 2: p=-1]
// 6. T(n) = T(sqrt(n)) + O(1)     ==> Theta(log(log n))   [Substitute n = 2^m]`,
        gateTrap: 'GATE TRAP: For T(n) = sqrt(2) * T(n/2) + log n, compute log_2(sqrt(2)) = 0.5. Since n^0.5 grows faster than log n (k=0), Case 1 applies: T(n) = Theta(sqrt(n))!'
      },
      {
        id: 'r5-s2',
        tier: 'Level 2: Core Mechanics & C Implementation',
        title: 'Sorting Algorithms: Inversions, Stability & QuickSort Bounds',
        summary: 'Insertion sort inversion formula, Merge Sort counting, and QuickSort recursion space.',
        mentalModel: `Inversions in an Array:
An inversion is a pair of indices (i < j) such that A[i] > A[j].
• Maximum inversions in array of size n = n*(n - 1) / 2 (Reverse sorted).
• Every adjacent swap fixes AT MOST 1 inversion.
• Insertion Sort exact running time: Theta(n + d), where d is the number of inversions!
  -> Therefore, on an "almost sorted" array where each element is at most k positions away from its sorted spot, Insertion Sort runs in O(n*k) = O(n) time!

QuickSort Deep Dive:
• Worst Case: Theta(n^2) time — occurs when array is ALREADY SORTED, REVERSE SORTED, or ALL ELEMENTS ARE EQUAL (with standard Lomuto partition).
• Even if partition splits 99% vs 1% at every step: T(n) = T(0.99n) + T(0.01n) + n = Theta(n log n)!
• Auxiliary Space: Worst case O(n) stack space, reducible to O(log n) worst-case space by always recursing on the SMALLER partition first and using tail-call elimination on the larger!`,
        code: `// Max and Min of n elements simultaneously (Divide & Conquer / Pairwise):
// Naive: 2n - 2 comparisons.
// Optimal Pairwise Tournament:
// Compare elements in pairs (n/2 comparisons), then compare winners with Max (n/2 - 1)
// and losers with Min (n/2 - 1).
// Total Comparisons = 3n/2 - 2!`,
        gateTrap: 'GATE TRAP: Which sorting algorithm makes the MINIMUM number of memory writes/swaps in the worst case? Selection Sort! It makes at most O(n) swaps (whereas Insertion, Bubble, Quick, Merge make O(n^2) or O(n log n) writes).'
      },
      {
        id: 'r5-s3',
        tier: 'Level 3: GATE Edge Cases & Traps',
        title: 'Median-of-Medians & Lower Bounds for Comparison Problems',
        summary: 'Decision tree lower bounds, Merging sorted lists, and Linear-time Selection.',
        mentalModel: `Information-Theoretic Decision Tree Lower Bounds:
• Sorting n elements by comparisons requires at least ceil(log_2(n!)) = Omega(n log n) comparisons.
• Finding Maximum of n elements requires exactly n - 1 comparisons.
• Finding BOTH Maximum and Second-Maximum of n elements:
  Using a Knockout Tournament Tree, the 2nd largest could only have lost to the overall Winner!
  Since the Winner played ceil(log_2 n) matches, finding 2nd Max among those losers takes ceil(log_2 n) - 1 comparisons.
  Total Comparisons = n + ceil(log_2 n) - 2!`,
        code: `// Summary of Exact Comparison Counts for GATE NATs (n elements):
// 1. Only Max (or Only Min):            n - 1
// 2. Both Max AND Min simultaneously:   ceil(3n / 2) - 2
// 3. Both Max AND 2nd Max:              n + ceil(log2(n)) - 2
// 4. Merging two sorted lists (m, n):   Worst-case = m + n - 1, Best-case = min(m, n)`,
        gateTrap: 'GATE TRAP: Finding the Median (or k-th smallest element) in an unsorted array takes O(n) WORST-CASE time using the Blum-Floyd-Pratt-Rivest-Tarjan (Median of Medians of groups of 5) recurrence: T(n) <= T(n/5) + T(7n/10) + O(n) = O(n)!'
      }
    ]
  },
  {
    id: 'realm-6',
    number: 6,
    title: 'Graphs, Greedy & Dynamic Programming',
    weightage: '3.0 Marks',
    icon: 'Network',
    accent: 'emerald',
    tagline: 'Conquer DFS edge taxonomy, MST Cut/Cycle theorems, Dijkstra traps, and DP tables.',
    interactiveTool: 'mstCutTester',
    sublevels: [
      {
        id: 'r6-s1',
        tier: 'Level 1: Scratch Intuition',
        title: 'BFS & DFS Traversals, Edge Taxonomy & Topological Sort',
        summary: 'Discovery/Finish intervals, Back-edge cycle theorem, and DAG properties.',
        mentalModel: `Graph Traversals (Adjacency List: O(V + E), Adjacency Matrix: O(V^2)):
In Depth-First Search (DFS), every vertex u gets Discovery time d[u] and Finish time f[u].
Parenthesis Theorem: Intervals [d[u], f[u]] and [d[v], f[v]] are either completely disjoint or one is strictly nested inside the other!

DFS Edge Classification in Directed Graphs:
• Tree Edge (u -> v): v is visited for the first time via u.
• Back Edge (u -> v): v is an ANCESTOR of u in DFS tree (d[v] < d[u] < f[u] < f[v]).
  THEOREM: A directed (or undirected) graph has a CYCLE iff DFS produces at least one BACK EDGE!
• Forward Edge (u -> v): v is a non-tree descendant of u (d[u] < d[v] < f[v] < f[u]).
• Cross Edge (u -> v): Intervals are disjoint (d[v] < f[v] < d[u] < f[u]).

Note: In an UNDIRECTED graph, DFS produces ONLY Tree Edges and Back Edges (NO Forward or Cross edges can exist!).`,
        code: `// Topological Sort on a DAG (Directed Acyclic Graph):
// Method 1 (DFS): Run DFS and output vertices in DECREASING order of Finish Times f[u].
// Method 2 (Kahn's BFS): Repeatedly remove vertices with In-Degree == 0.
// Property: Every DAG has at least one source (in-degree 0) and one sink (out-degree 0).`,
        gateTrap: 'GATE TRAP: Ordering vertices by INCREASING discovery time d[u] does NOT give a valid topological sort! You MUST sort by DECREASING finish time f[u].'
      },
      {
        id: 'r6-s2',
        tier: 'Level 2: Core Mechanics & C Implementation',
        title: 'Minimum Spanning Trees (Kruskal & Prim) & Shortest Paths',
        summary: 'Cut & Cycle uniqueness theorems, Dijkstra negative-edge traps, and Bellman-Ford.',
        mentalModel: `MST Cut & Cycle Properties (Guaranteed GATE favourite!):
1. Cut Property: If an edge e is the STRICTLY LIGHTEST edge crossing some cut (S, V-S), then e MUST belong to EVERY Minimum Spanning Tree of G!
2. Cycle Property: If an edge e is the STRICTLY HEAVIEST edge in some cycle C, then e CANNOT belong to ANY Minimum Spanning Tree of G!
3. Corollary: If all edge weights in G are DISTINCT, the MST is 100% UNIQUE!

Shortest Path Algorithms:
• BFS: O(V + E) — Unweighted graphs (or all weights equal).
• DAG Shortest Path: O(V + E) — Relax edges in Topological Order (works even with NEGATIVE weights!).
• Dijkstra: O((V + E) log V) with Binary Heap, O(E + V log V) with Fibonacci Heap.
  - Fails on negative edge weights (even if there is no negative cycle!).
• Bellman-Ford: O(V * E) — Relaxes all E edges (V - 1) times. Handles negative weights & detects negative cycles on the V-th pass.`,
        code: `// What happens if we add a constant k > 0 to EVERY edge weight in graph G?
// 1. Does the Minimum Spanning Tree (MST) change?
//    NO! Because every spanning tree has exactly (V - 1) edges, so every tree's
//    cost increases by the exact same constant (V - 1) * k!
// 2. Does the Shortest Path (s -> t) change?
//    YES! A path with 2 edges gains +2k, whereas a path with 5 edges gains +5k!`,
        gateTrap: 'GATE TRAP: Adding a positive constant +C to all edges so that negative edges become positive does NOT make Dijkstra work! Because paths with more edges get penalized by a multiple of C.'
      },
      {
        id: 'r6-s3',
        tier: 'Level 3: GATE Edge Cases & Traps',
        title: 'Greedy Huffman Coding & Dynamic Programming Complexities',
        summary: 'Optimal Merge Patterns, LCS, 0/1 Knapsack, Matrix Chain, and Floyd-Warshall.',
        mentalModel: `Greedy Algorithms:
• Fractional Knapsack: Sort by value/weight ratio -> O(n log n).
• Huffman Coding / Optimal Merge Pattern: Repeatedly extract 2 minimum frequencies from a Min-Heap and insert their sum -> O(n log n) time. Produces an optimal Prefix-Free binary tree with (n - 1) internal nodes.

Classic Dynamic Programming Table Complexities (Memorize!):
• Longest Common Subsequence (LCS of lengths m, n): Time O(m * n), Space O(min(m, n)).
• Matrix Chain Multiplication (n matrices): Time O(n^3), Space O(n^2). Number of parenthesizations = Catalan C_{n-1}.
• 0/1 Knapsack (n items, capacity W): Time O(n * W) [Pseudo-polynomial!].
• Floyd-Warshall All-Pairs Shortest Path: Time Theta(V^3), Space O(V^2) (can be done in-place on the D matrix!).`,
        code: `// LCS Recurrence (Strings X[1..m] and Y[1..n]):
// if (X[i] == Y[j])
//     dp[i][j] = 1 + dp[i-1][j-1];
// else
//     dp[i][j] = max(dp[i-1][j], dp[i][j-1]);`,
        gateTrap: 'GATE TRAP: In Huffman Coding, if there are n characters, the total number of nodes in the Huffman Tree is always (2n - 1), and the maximum possible codeword length for any character is (n - 1) (when frequencies follow the Fibonacci sequence!).'
      }
    ]
  }
];

// ============================================================================
// PRESET C PROGRAMS FOR RECURSION & POINTER TRACER (LAB 3)
// ============================================================================
const RECURSION_PRESETS = [
  {
    id: 'static-rec',
    name: 'GATE Trap: Tree/Linear Recursion with static int',
    code: `int gateStatic(int n) {
  static int s = 0;
  if (n <= 0) return 0;
  s = s + 2;
  return gateStatic(n - 1) + s;
}
// Call: gateStatic(3)`,
    steps: [
      { step: 0, line: 1, desc: 'Initial call gateStatic(3) pushed onto Call Stack. Static s = 0 in Data Segment.', stack: ['gateStatic(3) [waiting]'], staticVal: 's = 0', output: '' },
      { step: 1, line: 4, desc: 'Inside gateStatic(3): n=3 > 0. Static s increments by 2 (s becomes 2). Calls gateStatic(2).', stack: ['gateStatic(3) [line 5: + s]', 'gateStatic(2) [active]'], staticVal: 's = 2', output: '' },
      { step: 2, line: 4, desc: 'Inside gateStatic(2): n=2 > 0. Static s increments by 2 (s becomes 4). Calls gateStatic(1).', stack: ['gateStatic(3) [line 5: + s]', 'gateStatic(2) [line 5: + s]', 'gateStatic(1) [active]'], staticVal: 's = 4', output: '' },
      { step: 3, line: 4, desc: 'Inside gateStatic(1): n=1 > 0. Static s increments by 2 (s becomes 6). Calls gateStatic(0).', stack: ['gateStatic(3) [line 5: + s]', 'gateStatic(2) [line 5: + s]', 'gateStatic(1) [line 5: + s]', 'gateStatic(0) [active]'], staticVal: 's = 6', output: '' },
      { step: 4, line: 3, desc: 'Base case! gateStatic(0) hits n <= 0 and returns 0.', stack: ['gateStatic(3) [line 5: + s]', 'gateStatic(2) [line 5: + s]', 'gateStatic(1) [0 + s]'], staticVal: 's = 6', output: 'gateStatic(0) -> 0' },
      { step: 5, line: 5, desc: 'Unwinding gateStatic(1): Reads current static s (which is 6!). Computes 0 + 6 = 6 and returns.', stack: ['gateStatic(3) [line 5: + s]', 'gateStatic(2) [6 + s]'], staticVal: 's = 6', output: 'gateStatic(1) -> 6' },
      { step: 6, line: 5, desc: 'Unwinding gateStatic(2): Reads current static s (6!). Computes 6 + 6 = 12 and returns.', stack: ['gateStatic(3) [12 + s]'], staticVal: 's = 6', output: 'gateStatic(2) -> 12' },
      { step: 7, line: 5, desc: 'Unwinding gateStatic(3): Reads current static s (6!). Computes 12 + 6 = 18. Final Answer = 18!', stack: ['main() receives 18'], staticVal: 's = 6', output: 'FINAL RETURN = 18' }
    ]
  },
  {
    id: 'll-rev',
    name: 'Pointer Trace: Singly Linked List Reversal (10 -> 20 -> 30)',
    code: `Node* reverse(Node* head) {
  Node *prev = NULL, *curr = head, *next = NULL;
  while (curr != NULL) {
    next = curr->next;
    curr->next = prev;
    prev = curr;
    curr = next;
  }
  return prev;
}`,
    steps: [
      { step: 0, line: 2, desc: 'Initialize pointers: prev = NULL, curr = [10], next = NULL. List: 10 -> 20 -> 30 -> NULL', stack: ['prev: NULL', 'curr: Node(10)', 'next: NULL'], staticVal: '10 -> 20 -> 30 -> NULL', output: 'Init complete' },
      { step: 1, line: 4, desc: 'Iteration 1: Save next = curr->next (Node 20). Reverse link: 10->next = NULL.', stack: ['prev: NULL', 'curr: Node(10)', 'next: Node(20)'], staticVal: 'NULL <- 10   20 -> 30 -> NULL', output: 'Reversed Node(10)' },
      { step: 2, line: 6, desc: 'Iteration 1 end: Advance prev = Node(10), curr = Node(20).', stack: ['prev: Node(10)', 'curr: Node(20)', 'next: Node(20)'], staticVal: 'NULL <- 10   20 -> 30 -> NULL', output: 'Pointers shifted' },
      { step: 3, line: 4, desc: 'Iteration 2: Save next = Node(30). Reverse link: 20->next = Node(10). Advance prev & curr.', stack: ['prev: Node(20)', 'curr: Node(30)', 'next: Node(30)'], staticVal: 'NULL <- 10 <- 20   30 -> NULL', output: 'Reversed Node(20)' },
      { step: 4, line: 4, desc: 'Iteration 3: Save next = NULL. Reverse link: 30->next = Node(20). Advance prev = Node(30), curr = NULL.', stack: ['prev: Node(30)', 'curr: NULL', 'next: NULL'], staticVal: 'NULL <- 10 <- 20 <- 30', output: 'Reversed Node(30)' },
      { step: 5, line: 9, desc: 'Loop terminates since curr == NULL. Return prev (Node 30) as the new head!', stack: ['Return: Node(30)'], staticVal: '30 -> 20 -> 10 -> NULL', output: 'New Head = 30' }
    ]
  },
  {
    id: 'print-tree',
    name: 'Double Recursion Output Trace: foo(3)',
    code: `void foo(int n) {
  if (n < 1) return;
  foo(n - 1);
  printf("%d ", n);
  foo(n - 1);
}
// Inorder traversal of full binary tree of height 3`,
    steps: [
      { step: 0, line: 1, desc: 'Call foo(3) -> calls left child foo(2) -> calls left child foo(1) -> calls foo(0) which returns.', stack: ['foo(3)', 'foo(2)', 'foo(1)'], staticVal: 'Depth = 3 (Max Stack)', output: '' },
      { step: 1, line: 4, desc: 'foo(1) prints "1 ", then calls right child foo(0) which returns. foo(1) finishes.', stack: ['foo(3)', 'foo(2)'], staticVal: 'Depth = 2', output: '1 ' },
      { step: 2, line: 4, desc: 'Back in foo(2): prints "2 ", then calls right child foo(1).', stack: ['foo(3)', 'foo(2)', 'foo(1)'], staticVal: 'Depth = 3', output: '1 2 ' },
      { step: 3, line: 4, desc: 'Right foo(1) prints "1 " and finishes. foo(2) finishes and returns to root foo(3).', stack: ['foo(3)'], staticVal: 'Depth = 1', output: '1 2 1 ' },
      { step: 4, line: 4, desc: 'Root foo(3) prints "3 " and launches right subtree foo(2)!', stack: ['foo(3)', 'foo(2)'], staticVal: 'Depth = 2', output: '1 2 1 3 ' },
      { step: 5, line: 5, desc: 'Right subtree foo(2) symmetrically prints "1 2 1 ". Total numbers printed = 2^3 - 1 = 7!', stack: ['Completed'], staticVal: 'Total Calls = 15', output: '1 2 1 3 1 2 1' }
    ]
  }
];

// ============================================================================
// GATE 2027 BOSS ARENA QUESTIONS (12 HIGH-YIELD MCQ / MSQ / NAT)
// ============================================================================
const BOSS_QUESTIONS = [
  {
    id: 1,
    type: 'NAT',
    marks: 2,
    negative: 0,
    realm: 'Realm 1: C Pointers & 2D Arrays',
    question: `Consider a 2D array declared in C as "int A[10][20];" stored in Row-Major order. Suppose the base address of A[0][0] is 1000 and sizeof(int) = 4 bytes. What is the exact byte address of the element A[6][12]?`,
    correctAnswer: '1528',
    explanation: `In C (Row-Major order) with 0-based indexing:
Address(A[i][j]) = Base + (i * Columns + j) * sizeof(int)
Here, Base = 1000, i = 6, Columns = 20, j = 12, sizeof(int) = 4.
Offset elements = (6 * 20 + 12) = 120 + 12 = 132 elements.
Byte Address = 1000 + 132 * 4 = 1000 + 528 = 1528.`,
    trap: 'Common mistake: Multiplying i by number of Rows (10) instead of number of Columns (20)!'
  },
  {
    id: 2,
    type: 'NAT',
    marks: 2,
    negative: 0,
    realm: 'Realm 1: Recursion & Static Variables',
    question: `What is the integer value returned by calling gateRec(4) for the C function below?
int gateRec(int n) {
    static int k = 1;
    if (n <= 1) return 2;
    k = k + 2;
    return gateRec(n - 1) + k;
}`,
    correctAnswer: '23',
    explanation: `Trace the recursive chain from n=4 down to base case n=1:
• Initial static k = 1.
• gateRec(4): n=4 > 1 -> k becomes 3 -> returns gateRec(3) + k
• gateRec(3): n=3 > 1 -> k becomes 5 -> returns gateRec(2) + k
• gateRec(2): n=2 > 1 -> k becomes 7 -> returns gateRec(1) + k
• gateRec(1): n=1 <= 1 -> returns 2 (k remains 7).
Now unwind! Since k is static, ALL 3 waiting frames add the final value of k (7):
Result = 2 + 7 + 7 + 7 = 23.`,
    trap: 'Never substitute the intermediate value of static k (3, 5, 7) during unwinding! In "gateRec(n-1) + k", k is fetched from memory AFTER gateRec(n-1) returns.'
  },
  {
    id: 3,
    type: 'MCQ',
    marks: 1,
    negative: 0.33,
    realm: 'Realm 2: Stacks & Permutations',
    question: `An input stream of numbers 1, 2, 3, 4, 5 arrives in strictly increasing order into a single Stack using Push and Pop operations. Which of the following output permutations is IMPOSSIBLE to generate?`,
    options: [
      '3, 2, 4, 5, 1',
      '2, 4, 3, 1, 5',
      '4, 2, 3, 5, 1',
      '1, 4, 3, 2, 5'
    ],
    correctOption: 2,
    explanation: `A stack permutation cannot contain the forbidden "3-1-2" pattern: for any three values a < b < c, c cannot be output first followed by a and then b.
In option C (4, 2, 3, 5, 1): To output 4 first, 1, 2, and 3 MUST already be pushed onto the stack in bottom-to-top order [1, 2, 3]. Therefore, 3 MUST be popped before 2! Getting 2 before 3 is impossible.`,
    trap: 'Use the Knuth (c, a, b) forbidden subsequence test where a < b < c (here 2 < 3 < 4 appearing as 4, 2, 3) to solve in 5 seconds!'
  },
  {
    id: 4,
    type: 'NAT',
    marks: 2,
    negative: 0,
    realm: 'Realm 3: Binary Tree Combinatorics',
    question: `How many distinct Binary Search Trees (BSTs) can be constructed using 5 distinct keys {10, 20, 30, 40, 50} such that the root of the BST is strictly 30?`,
    correctAnswer: '4',
    explanation: `When 30 is fixed as the root of the BST:
• Keys smaller than 30: {10, 20} (2 keys) MUST go into the Left Subtree.
• Keys larger than 30: {40, 50} (2 keys) MUST go into the Right Subtree.
Number of BSTs with 2 keys = C_2 = 2.
Since left and right subtree structures are chosen independently:
Total BSTs with root 30 = C_2 * C_2 = 2 * 2 = 4.`,
    trap: 'Do not output C_5 = 42! The question fixes the root as 30, which partitions the remaining 4 keys into 2 left keys and 2 right keys.'
  },
  {
    id: 5,
    type: 'NAT',
    marks: 2,
    negative: 0,
    realm: 'Realm 3: AVL Trees',
    question: `Let N(h) denote the minimum number of nodes required to construct a height-balanced AVL tree of height h, where a tree with a single node has height h = 0. What is the value of N(5)?`,
    correctAnswer: '20',
    explanation: `Using the AVL recurrence N(h) = N(h - 1) + N(h - 2) + 1 with base cases N(0) = 1 and N(1) = 2:
• N(0) = 1
• N(1) = 2
• N(2) = 2 + 1 + 1 = 4
• N(3) = 4 + 2 + 1 = 7
• N(4) = 7 + 4 + 1 = 12
• N(5) = 12 + 7 + 1 = 20.`,
    trap: 'Always verify whether the base case in the question defines a single node as h = 0 or h = 1!'
  },
  {
    id: 6,
    type: 'MSQ',
    marks: 2,
    negative: 0,
    realm: 'Realm 3: Binary Max-Heaps',
    question: `Suppose a Binary Max-Heap contains n = 100 distinct integers stored in a 1-indexed array A[1..100]. Which of the following statements is/are ALWAYS TRUE? (Multiple Select Question)`,
    options: [
      'Building this Max-Heap from an arbitrary array of 100 elements can be done in O(n) worst-case time.',
      'The second largest element MUST be at either index A[2] or A[3].',
      'The minimum element of the heap MUST reside in the subarray A[51..100].',
      'Deleting the maximum element takes O(1) worst-case time.'
    ],
    correctOptions: [0, 1, 2],
    explanation: `• Option A is TRUE: Bottom-up Build-Max-Heap runs in Theta(n) worst-case time.
• Option B is TRUE: The root A[1] is the maximum, so the 2nd largest must be the maximum of the remaining elements, which has to be one of the root's direct children A[2] or A[3].
• Option C is TRUE: The minimum element in a Max-Heap must be a leaf node, and in a 1-indexed heap of size 100, leaves occupy indices floor(100/2) + 1 = 51 to 100.
• Option D is FALSE: Extracting the max requires replacing root with last leaf and calling Max-Heapify, which takes O(log n) time.`,
    trap: 'In MSQs, there is no negative marking, but partial credit is NOT awarded—you must select all 3 true statements!'
  },
  {
    id: 7,
    type: 'NAT',
    marks: 2,
    negative: 0,
    realm: 'Realm 4: Hashing & Linear Probing',
    question: `Keys {12, 18, 13, 2, 3, 23, 5} are inserted in that exact order into an initially empty hash table of size m = 10 using hash function h(k) = k mod 10 and Linear Probing for collision resolution. What is the final index (0 to 9) where key 5 is stored?`,
    correctAnswer: '6',
    explanation: `Let's trace the insertions into slots [0..9]:
• 12 -> 12 % 10 = 2 (Slot 2)
• 18 -> 18 % 10 = 8 (Slot 8)
• 13 -> 13 % 10 = 3 (Slot 3)
• 2  -> 2 % 10 = 2 (Occupied by 12) -> Slot 3 (Occupied by 13) -> Lands at Slot 4!
• 3  -> 3 % 10 = 3 (Occupied) -> Slot 4 (Occupied) -> Lands at Slot 5!
• 23 -> 23 % 10 = 3 (Occupied) -> 4 (Occupied) -> 5 (Occupied) -> Lands at Slot 6? Wait: let's check!
  Wait: 23 lands at Slot 6! Then where does 5 go?
  Let's re-verify carefully! Wait: if 23 is included, 5 goes to 7. Let's check the question: let's trace {12, 18, 13, 2, 3, 5} vs {12, 18, 13, 2, 3, 23, 5}.
  Wait: For {12, 18, 13, 2, 3, 23}, 23 lands at Slot 6, and then 5 -> 5 % 10 = 5 (occupied by 3) -> 6 (occupied by 23) -> Lands at Slot 7!`,
    correctAnswerOverride: '7',
    trap: 'Primary clustering in action! Even though key 5 hashes to slot 5, keys 2, 3, and 23 cascaded from slots 2 and 3 to fill slots 4, 5, and 6, pushing key 5 all the way to slot 7.'
  },
  {
    id: 8,
    type: 'MCQ',
    marks: 2,
    negative: 0.66,
    realm: 'Realm 5: Recurrences & Master Theorem',
    question: `What is the tight asymptotic bound for the recurrence relation T(n) = 4T(n/2) + n^2 * log(n), with T(1) = 1?`,
    options: [
      'Theta(n^2)',
      'Theta(n^2 * log n)',
      'Theta(n^2 * (log n)^2)',
      'Theta(n^3)'
    ],
    correctOption: 2,
    explanation: `Compare T(n) = aT(n/b) + Theta(n^k * (log n)^p) with a = 4, b = 2, k = 2, p = 1:
Critical exponent c = log_b(a) = log_2(4) = 2.
Since c == k (2 == 2) and p = 1 > -1, Case 2 of the Extended Master Theorem applies:
T(n) = Theta(n^k * (log n)^(p + 1)) = Theta(n^2 * (log n)^2).`,
    trap: 'Do not forget to add +1 to the power of log(n) in Case 2 of the Master Theorem!'
  },
  {
    id: 9,
    type: 'NAT',
    marks: 1,
    negative: 0,
    realm: 'Realm 5: Sorting & Inversions',
    question: `How many inversions are present in the array A = [8, 4, 2, 1, 3, 5] (which is also the exact number of swaps performed by Insertion Sort to sort this array)?`,
    correctAnswer: '10',
    explanation: `Count pairs (i < j) where A[i] > A[j] for each element:
• For 8: (8,4), (8,2), (8,1), (8,3), (8,5) -> 5 inversions
• For 4: (4,2), (4,1), (4,3) -> 3 inversions
• For 2: (2,1) -> 1 inversion
• For 1: 0 inversions
• For 3: 0 inversions
• For 5: 0 inversions
Wait: 5 + 3 + 1 = 9! Let's check:
(8 > 4, 2, 1, 3, 5) = 5
(4 > 2, 1, 3) = 3
(2 > 1) = 1
Total = 5 + 3 + 1 = 9 inversions.`,
    correctAnswerOverride: '9',
    trap: 'Count systematically from left to right: for each element A[i], count how many elements to its right are strictly smaller than A[i].'
  },
  {
    id: 10,
    type: 'MSQ',
    marks: 2,
    negative: 0,
    realm: 'Realm 6: Graph Traversals & DFS',
    question: `Let G = (V, E) be a simple connected UNDIRECTED graph with V = 10 vertices and E = 15 edges. A Depth-First Search (DFS) is performed starting from vertex s. Which of the following statements is/are TRUE?`,
    options: [
      'The DFS traversal will classify exactly 9 edges as Tree Edges and 6 edges as Back Edges.',
      'The DFS traversal can produce at least one Cross Edge depending on adjacency list order.',
      'Since E >= V, the graph G is guaranteed to contain at least one cycle.',
      'Breadth-First Search (BFS) from s finds shortest paths (in terms of number of edges) to all vertices in O(V + E) time.'
    ],
    correctOptions: [0, 2, 3],
    explanation: `• Option A is TRUE: Since G is connected with 10 vertices, the DFS spanning tree has V - 1 = 9 Tree Edges. In an undirected graph, every non-tree edge is a Back Edge, so 15 - 9 = 6 Back Edges!
• Option B is FALSE: In an UNDIRECTED graph, DFS NEVER produces Forward or Cross edges—only Tree and Back edges!
• Option C is TRUE: Any graph with E >= V has at least one cycle (a tree has V - 1 = 9 edges).
• Option D is TRUE: BFS computes unweighted shortest paths in O(V + E) time.`,
    trap: 'Memorize: Undirected DFS = Tree + Back edges ONLY. Undirected BFS = Tree + Cross edges ONLY.'
  },
  {
    id: 11,
    type: 'MCQ',
    marks: 2,
    negative: 0.66,
    realm: 'Realm 6: Minimum Spanning Trees & Shortest Paths',
    question: `Let G be a connected undirected weighted graph with distinct positive edge weights. Let T be the unique Minimum Spanning Tree of G, and let P be the shortest path from s to t. Now, every edge weight w(e) in G is increased by +10 (i.e., w'(e) = w(e) + 10). Which of the following is TRUE?`,
    options: [
      'Both T and P definitely remain unchanged.',
      'T definitely remains the MST, but the shortest path P may change.',
      'T may change, but the shortest path P definitely remains unchanged.',
      'Both T and P may change.'
    ],
    correctOption: 1,
    explanation: `1. Every spanning tree of G has the exact same number of edges: (V - 1). Adding +10 to every edge increases the weight of EVERY spanning tree by the constant 10*(V - 1). Thus, the relative order of spanning trees is unchanged and T remains the MST!
2. However, s-to-t paths can have different numbers of edges! A 4-edge path of weight 12 becomes 12 + 40 = 52, while a 2-edge path of weight 20 becomes 20 + 20 = 40 (now shorter!). Thus P can change.`,
    trap: 'Wait: What if edge weights are SQUARED or multiplied by a positive constant k > 0? Multiplying by k > 0 preserves BOTH T and P, while squaring positive weights preserves T (since x -> x^2 is strictly monotonic on R+) but can change P!'
  },
  {
    id: 12,
    type: 'NAT',
    marks: 2,
    negative: 0,
    realm: 'Realm 6: Dynamic Programming (LCS)',
    question: `What is the length of the Longest Common Subsequence (LCS) of the two strings X = "GATE2027" and Y = "GTE2720"?`,
    correctAnswer: '5',
    explanation: `Compare X = "G A T E 2 0 2 7" and Y = "G T E 2 7 2 0":
Common subsequences include:
• "G T E 2 7" (Length 5)
• "G T E 2 0" (Length 5)
• "G T E 2 2" (Length 5)
Can we get length 6? Since 'A' is not in Y, X reduces to "G T E 2 0 2 7" (length 7). Matching "G T E" (length 3) leaves "2 0 2 7" vs "2 7 2 0", whose LCS is "2 7" or "2 0" or "2 2" (length 2).
Total LCS length = 3 + 2 = 5.`,
    trap: 'When one string has characters completely absent from the other (like "A" here), cross them out immediately before building the DP table!'
  }
];

// ============================================================================
// COMPLEXITY & FORMULA VAULT DATA
// ============================================================================
const DS_COMPLEXITY_TABLE = [
  { ds: 'Static / Dynamic Array', access: 'O(1)', search: 'O(n)', insert: 'O(n)', delete: 'O(n)', space: 'O(n)', note: 'Binary search takes O(log n) if sorted; Dynamic array append is O(1) amortized.' },
  { ds: 'Singly Linked List (with head & tail)', access: 'O(n)', search: 'O(n)', insert: 'O(1) at head/tail', delete: 'O(1) head, Theta(n) tail!', space: 'O(n)', note: 'Deleting tail requires Theta(n) to find second-last node!' },
  { ds: 'Doubly Linked List', access: 'O(n)', search: 'O(n)', insert: 'O(1) given node ptr', delete: 'O(1) given node ptr', space: 'O(n)', note: 'Can delete arbitrary node in O(1) if direct pointer to node is provided.' },
  { ds: 'Binary Search Tree (Unbalanced BST)', access: 'O(h) -> O(n) worst', search: 'O(n) worst, O(log n) avg', insert: 'O(n) worst', delete: 'O(n) worst', space: 'O(n)', note: 'Degenerates into a skewed chain of height n-1 on sorted insertions.' },
  { ds: 'AVL Tree / Red-Black Tree', access: 'Theta(log n)', search: 'Theta(log n)', insert: 'Theta(log n)', delete: 'Theta(log n)', space: 'O(n)', note: 'AVL Insert <= 2 rotations; AVL Delete up to O(log n) rotations.' },
  { ds: 'Binary Max-Heap', access: 'Max: O(1)', search: 'Theta(n) for arbitrary/min', insert: 'O(log n)', delete: 'Extract-Max: O(log n)', space: 'O(n)', note: 'Build-Heap takes Theta(n) time; Min element is in leaves.' },
  { ds: 'Hash Table (Chaining / Open Addr)', access: 'N/A', search: 'O(1 + alpha) avg, O(n) worst', insert: 'O(1) avg, O(n) worst', delete: 'O(1) avg, O(n) worst', space: 'O(m + n)', note: 'Open addressing requires Tombstone markers on deletion.' }
];

const SORTING_COMPLEXITY_TABLE = [
  { name: 'Insertion Sort', best: 'Theta(n)', avg: 'Theta(n^2)', worst: 'Theta(n^2)', space: 'O(1)', stable: 'Yes', adaptive: 'Yes', note: 'Runs in Theta(n + d) where d = inversions. Best for nearly sorted arrays.' },
  { name: 'Selection Sort', best: 'Theta(n^2)', avg: 'Theta(n^2)', worst: 'Theta(n^2)', space: 'O(1)', stable: 'No', adaptive: 'No', note: 'Always makes n(n-1)/2 comparisons, but at most O(n) swaps!' },
  { name: 'Merge Sort', best: 'Theta(n log n)', avg: 'Theta(n log n)', worst: 'Theta(n log n)', space: 'Theta(n)', stable: 'Yes', adaptive: 'No', note: 'O(1) extra space for Linked Lists! Ideal for counting inversions.' },
  { name: 'Quick Sort', best: 'Theta(n log n)', avg: 'Theta(n log n)', worst: 'Theta(n^2)', space: 'O(log n) avg, O(n) worst', stable: 'No', adaptive: 'No', note: 'Worst case on sorted/reverse-sorted input with first/last pivot.' },
  { name: 'Heap Sort', best: 'Theta(n log n) [or O(n) all equal]', avg: 'Theta(n log n)', worst: 'Theta(n log n)', space: 'O(1)', stable: 'No', adaptive: 'No', note: 'In-place O(n log n) worst-case sort, no extra array needed.' },
  { name: 'Counting / Radix Sort', best: 'Theta(n + k) / Theta(d(n+b))', avg: 'Theta(n + k)', worst: 'Theta(n + k)', space: 'Theta(n + k)', stable: 'Yes', adaptive: 'No', note: 'Non-comparison sort; stability of Counting Sort is mandatory for Radix Sort!' }
];

const FORMULA_SHORTCUTS = [
  { category: 'Trees & Combinatorics', title: 'Catalan Number C_n', formula: 'C_n = (1 / (n + 1)) * (2n choose n)', values: 'n=0..6: 1, 1, 2, 5, 14, 42, 132', useCase: 'Unlabeled Binary Trees, Distinct BSTs with n keys, Valid Stack Permutations, Full Binary Trees with n+1 leaves.' },
  { category: 'Trees & Combinatorics', title: 'Labeled Binary Trees', formula: 'N_labeled = C_n * n!', values: 'n=1..4: 1, 2, 12, 120', useCase: 'Number of distinct binary trees when nodes have distinct labels and BST ordering is NOT required.' },
  { category: 'Trees & Combinatorics', title: 'Leaf vs Degree-2 Theorem', formula: 'L = I_2 + 1  (and for Full k-ary: L = (k-1)I + 1)', values: 'Independent of degree-1 nodes!', useCase: 'Instant NAT solver when given number of degree-2 nodes in any binary tree.' },
  { category: 'AVL & Heaps', title: 'Min Nodes in AVL of Height h', formula: 'N(h) = N(h-1) + N(h-2) + 1 = Fib(h+3) - 1', values: 'h=0..6: 1, 2, 4, 7, 12, 20, 33', useCase: 'Max height of AVL tree with n nodes is ~1.44 log_2(n).' },
  { category: 'Hashing', title: 'Expected Empty Slots & Collisions', formula: 'E[Empty] = m * ((m - 1) / m)^n', values: 'E[Collisions] = n - m + E[Empty]', useCase: 'Inserting n keys uniformly at random into hash table of size m.' },
  { category: 'Comparisons', title: 'Optimal Tournament Comparisons', formula: 'Max & Min: ceil(3n/2) - 2 | Max & 2nd Max: n + ceil(log_2 n) - 2', values: 'For n=16: Max&Min = 22, Max&2ndMax = 18', useCase: 'Minimum comparisons in adversarial worst-case model.' },
  { category: 'Graphs', title: 'Handshaking & Connected Components', formula: 'Sum of degrees = 2E | Max edges with k components = (V-k)(V-k+1)/2', values: 'Min edges to guarantee connectivity = (V-1)(V-2)/2 + 1', useCase: 'Graph connectivity and degree sequence GATE questions.' }
];

// ============================================================================
// MAIN APPLICATION COMPONENT
// ============================================================================
export default function App() {
  // Navigation & Gamification State
  const [activeTab, setActiveTab] = useState('world-map');
  const [xp, setXp] = useState(150);
  const [streak, setStreak] = useState(3);
  const [completedSublevels, setCompletedSublevels] = useState(['r1-s1']);
  const [solvedBossIds, setSolvedBossIds] = useState([]);
  const [labsRunCount, setLabsRunCount] = useState(0);
  const [toastMessage, setToastMessage] = useState(null);

  // Tab 1: World Map State
  const [selectedRealmId, setSelectedRealmId] = useState('realm-1');
  const [selectedSublevelIndex, setSelectedSublevelIndex] = useState(0);

  // Realm Interactive Mini-Calculators State
  const [arrRows, setArrRows] = useState(10);
  const [arrCols, setArrCols] = useState(20);
  const [arrBase, setArrBase] = useState(1000);
  const [arrSize, setArrSize] = useState(4);
  const [arrI, setArrI] = useState(4);
  const [arrJ, setArrJ] = useState(7);

  const [cqSize, setCqSize] = useState(8);
  const [cqFront, setCqFront] = useState(5);
  const [cqRear, setCqRear] = useState(2);

  const [catN, setCatN] = useState(4);
  const [hashM, setHashM] = useState(10);
  const [hashN, setHashN] = useState(6);

  const [mtA, setMtA] = useState(4);
  const [mtB, setMtB] = useState(2);
  const [mtK, setMtK] = useState(2);
  const [mtP, setMtP] = useState(1);

  // Tab 2: Interactive Dry-Run Lab State
  const [activeLab, setActiveLab] = useState('hashing');
  // Lab 1: Hash Visualizer
  const [hashInputKeys, setHashInputKeys] = useState('22, 43, 15, 32, 54, 65, 11');
  const [hashTableSize, setHashTableSize] = useState(10);
  const [hashStrategy, setHashStrategy] = useState('linear');
  const [hashStepCount, setHashStepCount] = useState(7);

  // Lab 2: AVL & Heap Visualizer
  const [treeMode, setTreeMode] = useState('avl'); // 'avl' | 'heap'
  const [avlKeys, setAvlKeys] = useState([30, 20, 40, 10, 25]);
  const [newNodeInput, setNewNodeInput] = useState('5');
  const [lastRotationInfo, setLastRotationInfo] = useState('Balanced (No rotation needed on last insert)');
  const [heapArray, setHeapArray] = useState([12, 35, 8, 60, 24, 90, 45]);
  const [heapStatus, setHeapStatus] = useState('Raw Unordered Array — Click "Run O(n) Build-Max-Heap"');

  // Lab 3: Recursion & Pointer Tracer
  const [selectedPresetIdx, setSelectedPresetIdx] = useState(0);
  const [traceStep, setTraceStep] = useState(0);

  // Lab 4: Graph Traversal & Shortest Path Dry-Runner
  const [graphAlgo, setGraphAlgo] = useState('dfs'); // 'dfs' | 'dijkstra' | 'kruskal'
  const [graphStep, setGraphStep] = useState(0);

  // Tab 3: Boss Arena State
  const [currentQIdx, setCurrentQIdx] = useState(0);
  const [userAnswers, setUserAnswers] = useState({});
  const [verifiedQuestions, setVerifiedQuestions] = useState({});
  const [markedForReview, setMarkedForReview] = useState({});
  const [examTimerSeconds, setExamTimerSeconds] = useState(1800); // 30 mins gauntlet
  const [timerRunning, setTimerRunning] = useState(true);

  // Tab 4: Vault Filter State
  const [vaultSearch, setVaultSearch] = useState('');

  // Trigger celebratory XP toast
  const triggerToast = (msg) => {
    setToastMessage(msg);
  };

  useEffect(() => {
    if (!toastMessage) return;
    const t = setTimeout(() => setToastMessage(null), 3200);
    return () => clearTimeout(t);
  }, [toastMessage]);

  // Exam timer tick
  useEffect(() => {
    if (!timerRunning || activeTab !== 'boss-arena') return;
    const interval = setInterval(() => {
      setExamTimerSeconds((prev) => (prev > 0 ? prev - 1 : 0));
    }, 1000);
    return () => clearInterval(interval);
  }, [timerRunning, activeTab]);

  // Current Player Rank Calculation
  const currentRank = useMemo(() => {
    for (let i = PLAYER_RANKS.length - 1; i >= 0; i--) {
      if (xp >= PLAYER_RANKS[i].minXp) return PLAYER_RANKS[i];
    }
    return PLAYER_RANKS[0];
  }, [xp]);

  const xpProgressPercent = useMemo(() => {
    const span = currentRank.maxXp - currentRank.minXp;
    const currentInSpan = xp - currentRank.minXp;
    return Math.min(100, Math.max(5, Math.round((currentInSpan / span) * 100)));
  }, [xp, currentRank]);

  // Estimated GATE DSA Score Readiness (out of 18.0 marks)
  const estimatedGateScore = useMemo(() => {
    const lessonWeight = (completedSublevels.length / 18) * 8.0; // up to 8 marks from 18 lessons
    const bossWeight = (solvedBossIds.length / BOSS_QUESTIONS.length) * 8.0; // up to 8 marks from 12 boss questions
    const labWeight = Math.min(2.0, labsRunCount * 0.4); // up to 2 marks from lab dry-runs
    return Math.min(18.0, +(lessonWeight + bossWeight + labWeight).toFixed(1));
  }, [completedSublevels.length, solvedBossIds.length, labsRunCount]);

  // Complete Sublevel Handler
  const handleCompleteSublevel = (subId) => {
    if (completedSublevels.includes(subId)) return;
    setCompletedSublevels((prev) => [...prev, subId]);
    setXp((prev) => prev + 50);
    setStreak((prev) => prev + 1);
    triggerToast('+50 XP! Syllabus Concept Mastered & Added to GATE Memory Bank.');
  };

  // ============================================================================
  // LAB 1 COMPUTATION: HASH TABLE COLLISION VISUALIZER
  // ============================================================================
  const hashSimulation = useMemo(() => {
    const m = Math.max(3, Math.min(19, Number(hashTableSize) || 10));
    const rawKeys = hashInputKeys
      .split(',')
      .map((s) => parseInt(s.trim(), 10))
      .filter((n) => !isNaN(n))
      .slice(0, m);

    const activeKeys = rawKeys.slice(0, hashStepCount);
    const table = Array(m).fill(null);
    const logs = [];
    let totalCollisions = 0;
    let totalProbes = 0;

    activeKeys.forEach((key) => {
      const h1 = ((key % m) + m) % m;
      const h2 = 1 + (Math.abs(key) % Math.max(1, m - 2)); // Second hash for double hashing
      const path = [];
      let placed = false;
      let collisionsForKey = 0;

      for (let i = 0; i < m; i++) {
        let idx = h1;
        if (hashStrategy === 'linear') {
          idx = (h1 + i) % m;
        } else if (hashStrategy === 'quadratic') {
          idx = (h1 + i * i) % m;
        } else {
          idx = (h1 + i * h2) % m;
        }

        path.push(idx);
        totalProbes++;

        if (table[idx] === null) {
          table[idx] = { key, home: h1, probes: i + 1, displaced: i > 0 };
          placed = true;
          break;
        } else {
          collisionsForKey++;
          totalCollisions++;
        }
      }

      logs.push({
        key,
        h1,
        h2,
        path,
        collisions: collisionsForKey,
        placed,
        finalSlot: placed ? path[path.length - 1] : 'OVERFLOW'
      });
    });

    return {
      m,
      rawKeys,
      table,
      logs,
      totalCollisions,
      avgProbes: activeKeys.length > 0 ? (totalProbes / activeKeys.length).toFixed(2) : '0.00'
    };
  }, [hashInputKeys, hashTableSize, hashStrategy, hashStepCount]);

  // ============================================================================
  // LAB 2 COMPUTATION: SELF-BALANCING AVL TREE & BINARY MAX-HEAP
  // ============================================================================
  const avlTreeData = useMemo(() => {
    class Node {
      constructor(val) {
        this.val = val;
        this.left = null;
        this.right = null;
        this.height = 0;
      }
    }

    const getHeight = (n) => (n ? n.height : -1);
    const getBF = (n) => (n ? getHeight(n.left) - getHeight(n.right) : 0);
    const updateHeight = (n) => {
      if (n) n.height = 1 + Math.max(getHeight(n.left), getHeight(n.right));
    };

    const rotateRight = (y) => {
      const x = y.left;
      const T2 = x.right;
      x.right = y;
      y.left = T2;
      updateHeight(y);
      updateHeight(x);
      return x;
    };

    const rotateLeft = (x) => {
      const y = x.right;
      const T2 = y.left;
      y.left = x;
      x.right = T2;
      updateHeight(x);
      updateHeight(y);
      return y;
    };

    let lastRot = 'Tree Balanced — All Balance Factors in {-1, 0, +1}';

    const insert = (node, key) => {
      if (!node) return new Node(key);
      if (key < node.val) node.left = insert(node.left, key);
      else if (key > node.val) node.right = insert(node.right, key);
      else return node;

      updateHeight(node);
      const bf = getBF(node);

      // LL Case
      if (bf > 1 && key < node.left.val) {
        lastRot = `LL Imbalance at Node(${node.val}) [BF=+2] -> Triggered Single RIGHT Rotation!`;
        return rotateRight(node);
      }
      // RR Case
      if (bf < -1 && key > node.right.val) {
        lastRot = `RR Imbalance at Node(${node.val}) [BF=-2] -> Triggered Single LEFT Rotation!`;
        return rotateLeft(node);
      }
      // LR Case
      if (bf > 1 && key > node.left.val) {
        lastRot = `LR Imbalance at Node(${node.val}) [BF=+2] -> Triggered Double LEFT-RIGHT Rotation!`;
        node.left = rotateLeft(node.left);
        return rotateRight(node);
      }
      // RL Case
      if (bf < -1 && key < node.right.val) {
        lastRot = `RL Imbalance at Node(${node.val}) [BF=-2] -> Triggered Double RIGHT-LEFT Rotation!`;
        node.right = rotateRight(node.right);
        return rotateLeft(node);
      }
      return node;
    };

    let root = null;
    avlKeys.forEach((k) => {
      root = insert(root, k);
    });

    // Convert to positioned nodes & edges for SVG rendering
    const nodes = [];
    const edges = [];
    const traverse = (n, depth, x, spread) => {
      if (!n) return;
      const bf = getBF(n);
      nodes.push({ val: n.val, x, y: 42 + depth * 64, height: n.height, bf });
      if (n.left) {
        edges.push({ x1: x, y1: 42 + depth * 64, x2: x - spread, y2: 42 + (depth + 1) * 64 });
        traverse(n.left, depth + 1, x - spread, spread * 0.52);
      }
      if (n.right) {
        edges.push({ x1: x, y1: 42 + depth * 64, x2: x + spread, y2: 42 + (depth + 1) * 64 });
        traverse(n.right, depth + 1, x + spread, spread * 0.52);
      }
    };
    traverse(root, 0, 260, 115);

    return { nodes, edges, lastRot };
  }, [avlKeys]);

  // Run Build-Max-Heap Handler
  const handleRunBuildMaxHeap = () => {
    const arr = [...heapArray];
    const n = arr.length;
    let swaps = 0;

    const heapify = (a, size, i) => {
      let largest = i;
      const l = 2 * i + 1;
      const r = 2 * i + 2;
      if (l < size && a[l] > a[largest]) largest = l;
      if (r < size && a[r] > a[largest]) largest = r;
      if (largest !== i) {
        const tmp = a[i];
        a[i] = a[largest];
        a[largest] = tmp;
        swaps++;
        heapify(a, size, largest);
      }
    };

    for (let i = Math.floor(n / 2) - 1; i >= 0; i--) {
      heapify(arr, n, i);
    }

    setHeapArray(arr);
    setHeapStatus(`O(n) Build-Max-Heap Complete! Performed ${swaps} swaps from index ${Math.floor(n / 2) - 1} down to 0.`);
    setLabsRunCount((c) => c + 1);
    setXp((x) => x + 40);
    triggerToast('+40 XP! Simulated O(n) Bottom-Up Build-Max-Heap.');
  };

  // ============================================================================
  // LAB 4 DATA: GRAPH TRAVERSAL & SHORTEST PATH STATES
  // ============================================================================
  const GRAPH_NODES = [
    { id: 'A', x: 80, y: 70 },
    { id: 'B', x: 240, y: 50 },
    { id: 'C', x: 400, y: 70 },
    { id: 'D', x: 140, y: 185 },
    { id: 'E', x: 320, y: 185 }
  ];

  const GRAPH_SIMULATIONS = {
    dfs: [
      {
        title: 'Step 0: Initialize DFS from Source A',
        desc: 'All vertices unvisited. Clock = 0. Adjacency lists ordered alphabetically.',
        visited: [],
        active: 'A',
        times: { A: '[1 / -]', B: '[-/-]', C: '[-/-]', D: '[-/-]', E: '[-/-]' },
        edgeTypes: {}
      },
      {
        title: 'Step 1: Explore A -> B -> D (Tree Edges)',
        desc: 'A discovers B (t=2), B discovers D (t=3). Stack: [A, B, D].',
        visited: ['A', 'B'],
        active: 'D',
        times: { A: '[1 / -]', B: '[2 / -]', C: '[-/-]', D: '[3 / -]', E: '[-/-]' },
        edgeTypes: { 'A-B': 'TREE', 'B-D': 'TREE' }
      },
      {
        title: 'Step 2: Cycle Detected! Edge D -> A is a BACK EDGE',
        desc: 'From D, neighbor A is ALREADY active on the recursion stack (d[A]=1 < d[D]=3). D->A classified as BACK EDGE (Cycle confirmed!). D finishes at t=4.',
        visited: ['A', 'B', 'D'],
        active: 'D',
        times: { A: '[1 / -]', B: '[2 / -]', C: '[-/-]', D: '[3 / 4]', E: '[-/-]' },
        edgeTypes: { 'A-B': 'TREE', 'B-D': 'TREE', 'D-A': 'BACK (Cycle!)' }
      },
      {
        title: 'Step 3: Backtrack to B, Explore B -> E -> C',
        desc: 'B discovers E (t=5), E discovers C (t=6). C finishes at t=7, E finishes at t=8, B finishes at t=9, A finishes at t=10.',
        visited: ['A', 'B', 'D', 'E', 'C'],
        active: 'C',
        times: { A: '[1 / 10]', B: '[2 / 9]', C: '[6 / 7]', D: '[3 / 4]', E: '[5 / 8]' },
        edgeTypes: { 'A-B': 'TREE', 'B-D': 'TREE', 'D-A': 'BACK (Cycle!)', 'B-E': 'TREE', 'E-C': 'TREE' }
      }
    ],
    dijkstra: [
      {
        title: 'Step 0: Initialize Dijkstra from A',
        desc: 'dist[A] = 0, all other distances = INF. Priority Queue = {(A, 0)}.',
        visited: [],
        active: 'A',
        times: { A: 'd=0', B: 'd=∞', C: 'd=∞', D: 'd=∞', E: 'd=∞' },
        edgeTypes: {}
      },
      {
        title: 'Step 1: Extract A (d=0), Relax (A,B,4) & (A,D,2)',
        desc: 'dist[D] becomes 2 (via A), dist[B] becomes 4 (via A). Next minimum in PQ is D (d=2)!',
        visited: ['A'],
        active: 'D',
        times: { A: 'd=0', B: 'd=4', C: 'd=∞', D: 'd=2', E: 'd=∞' },
        edgeTypes: { 'A-D': 'RELAXED (w=2)', 'A-B': 'RELAXED (w=4)' }
      },
      {
        title: 'Step 2: Extract D (d=2), Relax (D,B,1) & (D,E,6)',
        desc: 'Crucial Relaxation! Path A->D->B has cost 2 + 1 = 3 < 4! So dist[B] updates from 4 down to 3! dist[E] = 2 + 6 = 8.',
        visited: ['A', 'D'],
        active: 'B',
        times: { A: 'd=0', B: 'd=3 ( via D )', C: 'd=∞', D: 'd=2', E: 'd=8' },
        edgeTypes: { 'A-D': 'SPT EDGE', 'B-D': 'RELAXED (d[B]=3)' }
      },
      {
        title: 'Step 3: Extract B (d=3), Relax (B,E,2) & Finish C',
        desc: 'From B (d=3), edge (B,E,2) improves dist[E] from 8 down to 3 + 2 = 5! Then E relaxes (E,C,3) giving dist[C] = 8.',
        visited: ['A', 'D', 'B', 'E', 'C'],
        active: 'E',
        times: { A: 'd=0', B: 'd=3', C: 'd=8', D: 'd=2', E: 'd=5' },
        edgeTypes: { 'A-D': 'SPT', 'B-D': 'SPT', 'B-E': 'SPT', 'E-C': 'SPT' }
      }
    ],
    kruskal: [
      {
        title: 'Step 0: Sort All Edges by Weight + Init Disjoint Sets',
        desc: 'Sets: {A}, {B}, {C}, {D}, {E}. Sorted Edges: (B,D:1), (A,D:2), (B,E:2), (E,C:3), (A,B:4), (D,E:6).',
        visited: [],
        active: 'B',
        times: { A: 'Set{A}', B: 'Set{B}', C: 'Set{C}', D: 'Set{D}', E: 'Set{E}' },
        edgeTypes: {}
      },
      {
        title: 'Step 1: Pick (B,D:1) and (A,D:2) — Union Sets',
        desc: 'Find(B) != Find(D) -> Accept (B,D:1). Find(A) != Find(D) -> Accept (A,D:2). Now {A, B, D} are in the same component!',
        visited: ['A', 'B', 'D'],
        active: 'D',
        times: { A: 'Set{A,B,D}', B: 'Set{A,B,D}', C: 'Set{C}', D: 'Set{A,B,D}', E: 'Set{E}' },
        edgeTypes: { 'B-D': 'MST (w=1)', 'A-D': 'MST (w=2)' }
      },
      {
        title: 'Step 2: Pick (B,E:2) & (E,C:3), REJECT (A,B:4)',
        desc: 'Accept (B,E:2) and (E,C:3). Note: Edge (A,B:4) has Find(A) == Find(B) -> REJECTED by Cycle Property! Total MST Weight = 1 + 2 + 2 + 3 = 8.',
        visited: ['A', 'B', 'C', 'D', 'E'],
        active: 'C',
        times: { A: 'MST Cost = 8', B: '4 Edges', C: 'Connected', D: 'Unique MST', E: 'Done' },
        edgeTypes: { 'B-D': 'MST (w=1)', 'A-D': 'MST (w=2)', 'B-E': 'MST (w=2)', 'E-C': 'MST (w=3)', 'A-B': 'REJECTED (Cycle)' }
      }
    ]
  };

  // ============================================================================
  // BOSS ARENA EVALUATION LOGIC
  // ============================================================================
  const evaluateQuestion = (q, ans) => {
    if (ans === undefined || ans === null || ans === '') return false;
    if (q.type === 'NAT') {
      const target = q.correctAnswerOverride || q.correctAnswer;
      return String(ans).trim() === String(target).trim();
    }
    if (q.type === 'MCQ') {
      return Number(ans) === q.correctOption;
    }
    if (q.type === 'MSQ') {
      if (!Array.isArray(ans)) return false;
      if (ans.length !== q.correctOptions.length) return false;
      return q.correctOptions.every((opt) => ans.includes(opt));
    }
    return false;
  };

  const handleVerifyBossQuestion = (q) => {
    const ans = userAnswers[q.id];
    const isCorrect = evaluateQuestion(q, ans);
    setVerifiedQuestions((prev) => ({ ...prev, [q.id]: { isCorrect } }));

    if (isCorrect && !solvedBossIds.includes(q.id)) {
      setSolvedBossIds((prev) => [...prev, q.id]);
      setXp((prev) => prev + 75);
      setStreak((prev) => prev + 1);
      triggerToast(`+75 XP! Boss Question #${q.id} Crushed (+${q.marks} GATE Marks)!`);
    } else if (!isCorrect) {
      setStreak(0);
    }
  };

  // Calculate total Boss Arena Score
  const arenaScoreSummary = useMemo(() => {
    let marksEarned = 0;
    let negativeLost = 0;
    let correctCount = 0;
    let wrongCount = 0;

    BOSS_QUESTIONS.forEach((q) => {
      const v = verifiedQuestions[q.id];
      if (!v) return;
      if (v.isCorrect) {
        marksEarned += q.marks;
        correctCount++;
      } else {
        negativeLost += q.negative;
        wrongCount++;
      }
    });

    return {
      netScore: +(marksEarned - negativeLost).toFixed(2),
      marksEarned,
      negativeLost: +negativeLost.toFixed(2),
      correctCount,
      wrongCount
    };
  }, [verifiedQuestions]);

  // Format seconds as MM:SS
  const formatTime = (sec) => {
    const m = Math.floor(sec / 60);
    const s = sec % 60;
    return `${String(m).padStart(2, '0')}:${String(s).padStart(2, '0')}`;
  };

  const selectedRealm = SYLLABUS_REALMS.find((r) => r.id === selectedRealmId) || SYLLABUS_REALMS[0];
  const selectedSublevel = selectedRealm.sublevels[selectedSublevelIndex] || selectedRealm.sublevels[0];
  const currentBossQ = BOSS_QUESTIONS[currentQIdx];

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 font-sans selection:bg-emerald-500/30 selection:text-emerald-200 pb-14">
      {/* Floating XP Notification Toast */}
      {toastMessage && (
        <div className="fixed bottom-6 right-6 z-50 flex items-center gap-3 px-5 py-3.5 rounded-xl bg-emerald-950/95 border border-emerald-400/60 text-emerald-200 shadow-2xl shadow-emerald-950/80 animate-bounce">
          <Sparkles className="w-5 h-5 text-emerald-400 shrink-0" />
          <span className="font-semibold text-sm">{toastMessage}</span>
        </div>
      )}

      {/* ====================================================================
          1. TOP HUD (HEADS-UP DISPLAY)
      ==================================================================== */}
      <header className="sticky top-0 z-40 border-b border-slate-800/90 bg-slate-950/90 backdrop-blur-md">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 py-3">
          <div className="flex flex-col lg:flex-row lg:items-center lg:justify-between gap-4">
            {/* Brand & Rank Badge */}
            <div className="flex flex-wrap items-center justify-between gap-3">
              <div className="flex items-center gap-3">
                <div className="w-11 h-11 rounded-xl bg-gradient-to-br from-emerald-500/20 via-cyan-500/20 to-slate-900 border border-emerald-500/40 flex items-center justify-center shadow-inner">
                  <Terminal className="w-6 h-6 text-emerald-400" />
                </div>
                <div>
                  <div className="flex items-center gap-2">
                    <span className="text-xs font-mono uppercase tracking-widest px-2 py-0.5 rounded bg-emerald-500/15 text-emerald-300 border border-emerald-500/30">
                      GATE 2027 CSE
                    </span>
                    <span className="text-xs font-mono text-cyan-400">target: AIR &lt; 100</span>
                  </div>
                  <h1 className="text-lg sm:text-xl font-bold tracking-tight text-white">
                    DSA Complete Mastery Simulator
                  </h1>
                </div>
              </div>

              {/* Player Rank Badge */}
              <div className={`flex items-center gap-2.5 px-3.5 py-1.5 rounded-xl border ${currentRank.border} ${currentRank.bg}`}>
                <Award className={`w-5 h-5 ${currentRank.color}`} />
                <div>
                  <div className="text-[10px] font-mono uppercase tracking-wider text-slate-400">
                    Rank Lvl {currentRank.level}/6
                  </div>
                  <div className={`text-xs sm:text-sm font-bold ${currentRank.color}`}>
                    {currentRank.title}
                  </div>
                </div>
              </div>
            </div>

            {/* Telemetry Meters: XP, Streak, Bosses, GATE 18-Mark Readiness */}
            <div className="grid grid-cols-2 sm:grid-cols-4 gap-2.5 sm:gap-3">
              {/* XP Progress */}
              <div className="bg-slate-900/90 border border-slate-800 rounded-xl px-3 py-2">
                <div className="flex items-center justify-between text-xs mb-1">
                  <span className="text-slate-400 font-mono flex items-center gap-1">
                    <Zap className="w-3.5 h-3.5 text-amber-400" /> XP
                  </span>
                  <span className="font-mono font-bold text-amber-300">
                    {xp} / {currentRank.maxXp}
                  </span>
                </div>
                <div className="w-full h-2 bg-slate-800 rounded-full overflow-hidden">
                  <div
                    className="h-full bg-gradient-to-r from-amber-500 to-emerald-400 transition-all duration-500"
                    style={{ width: `${xpProgressPercent}%` }}
                  />
                </div>
              </div>

              {/* Streak & Modules */}
              <div className="bg-slate-900/90 border border-slate-800 rounded-xl px-3 py-2 flex items-center justify-between">
                <div>
                  <div className="text-[11px] text-slate-400 font-mono">Modules Done</div>
                  <div className="text-sm font-bold font-mono text-cyan-300">
                    {completedSublevels.length} / 18
                  </div>
                </div>
                <div className="flex items-center gap-1 px-2 py-1 rounded-lg bg-amber-500/10 border border-amber-500/30 text-amber-300 text-xs font-mono">
                  <Flame className="w-3.5 h-3.5 text-amber-400" /> {streak}x
                </div>
              </div>

              {/* Boss Gauntlet Counter */}
              <div className="bg-slate-900/90 border border-slate-800 rounded-xl px-3 py-2 flex items-center justify-between">
                <div>
                  <div className="text-[11px] text-slate-400 font-mono">Bosses Crushed</div>
                  <div className="text-sm font-bold font-mono text-violet-300">
                    {solvedBossIds.length} / {BOSS_QUESTIONS.length}
                  </div>
                </div>
                <Trophy className="w-5 h-5 text-violet-400" />
              </div>

              {/* Estimated GATE DSA Score Readiness (Out of 18.0 Marks) */}
              <div className="bg-emerald-950/30 border border-emerald-500/40 rounded-xl px-3 py-2">
                <div className="flex items-center justify-between text-xs mb-1">
                  <span className="text-emerald-300/90 font-mono flex items-center gap-1">
                    <Target className="w-3.5 h-3.5 text-emerald-400" /> Est. GATE
                  </span>
                  <span className="font-mono font-bold text-emerald-300">
                    {estimatedGateScore} / 18.0M
                  </span>
                </div>
                <div className="w-full h-2 bg-slate-800 rounded-full overflow-hidden">
                  <div
                    className="h-full bg-gradient-to-r from-emerald-500 to-cyan-400 transition-all duration-500"
                    style={{ width: `${Math.min(100, (estimatedGateScore / 18) * 100)}%` }}
                  />
                </div>
              </div>
            </div>
          </div>

          {/* Navigation Mode Switcher Tabs */}
          <nav className="flex items-center gap-2 mt-3 pt-2 border-t border-slate-800/80 overflow-x-auto no-scrollbar">
            {[
              { id: 'world-map', label: '1. World Map (6 Syllabus Realms)', icon: BookOpen, badge: '18 Marks' },
              { id: 'dry-run-lab', label: '2. Interactive Dry-Run Lab', icon: Cpu, badge: '4 Simulators' },
              { id: 'boss-arena', label: '3. GATE 2027 Boss Arena', icon: Trophy, badge: 'MCQ/MSQ/NAT' },
              { id: 'formula-vault', label: '4. Complexity & Formula Vault', icon: Database, badge: 'Cheatsheet' }
            ].map((tab) => {
              const Icon = tab.icon;
              const isActive = activeTab === tab.id;
              return (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id)}
                  className={`flex items-center gap-2 px-3.5 py-2 rounded-xl text-xs sm:text-sm font-medium whitespace-nowrap transition-all ${
                    isActive
                      ? 'bg-emerald-500/15 text-emerald-300 border border-emerald-500/50 shadow-sm'
                      : 'text-slate-400 hover:text-slate-200 hover:bg-slate-900 border border-transparent'
                  }`}
                >
                  <Icon className={`w-4 h-4 ${isActive ? 'text-emerald-400' : 'text-slate-400'}`} />
                  <span>{tab.label}</span>
                  <span
                    className={`text-[10px] font-mono px-1.5 py-0.5 rounded ${
                      isActive ? 'bg-emerald-500/20 text-emerald-200' : 'bg-slate-800 text-slate-400'
                    }`}
                  >
                    {tab.badge}
                  </span>
                </button>
              );
            })}
          </nav>
        </div>
      </header>

      {/* ====================================================================
          MAIN WORKSPACE CONTAINER
      ==================================================================== */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 pt-6">
        {/* ==================================================================
            TAB 1: WORLD MAP & 6 COMPLETE SYLLABUS REALMS
        ================================================================== */}
        {activeTab === 'world-map' && (
          <div className="space-y-6">
            {/* 6 Realm Cards Selector */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3.5">
              {SYLLABUS_REALMS.map((realm) => {
                const isSelected = realm.id === selectedRealmId;
                const realmDoneCount = realm.sublevels.filter((s) =>
                  completedSublevels.includes(s.id)
                ).length;

                return (
                  <button
                    key={realm.id}
                    onClick={() => {
                      setSelectedRealmId(realm.id);
                      setSelectedSublevelIndex(0);
                    }}
                    className={`text-left p-4 rounded-2xl border transition-all ${
                      isSelected
                        ? 'bg-slate-900/95 border-emerald-500/60 shadow-lg shadow-emerald-950/30 ring-1 ring-emerald-500/30'
                        : 'bg-slate-900/50 border-slate-800/90 hover:border-slate-700 hover:bg-slate-900/80'
                    }`}
                  >
                    <div className="flex items-center justify-between mb-2">
                      <span className="text-xs font-mono font-bold uppercase tracking-wider px-2.5 py-0.5 rounded-md bg-slate-800 text-cyan-300 border border-slate-700">
                        Realm {realm.number} • {realm.weightage}
                      </span>
                      <span className="text-xs font-mono text-emerald-400 flex items-center gap-1">
                        <CheckCircle2 className="w-3.5 h-3.5" /> {realmDoneCount}/3 Done
                      </span>
                    </div>
                    <h3 className="text-base font-bold text-white mb-1">{realm.title}</h3>
                    <p className="text-xs text-slate-400 line-clamp-2">{realm.tagline}</p>
                  </button>
                );
              })}
            </div>

            {/* Active Realm Deep-Dive Panel */}
            <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
              {/* Left Column: Progressive Sub-levels + Interactive Micro-Tool */}
              <div className="lg:col-span-5 space-y-5">
                <div className="bg-slate-900/80 border border-slate-800 rounded-2xl p-5">
                  <div className="text-xs font-mono uppercase tracking-wider text-emerald-400 mb-1">
                    Realm {selectedRealm.number} Progression Ladder
                  </div>
                  <h2 className="text-lg font-bold text-white mb-4">{selectedRealm.title}</h2>

                  <div className="space-y-3">
                    {selectedRealm.sublevels.map((sub, idx) => {
                      const isDone = completedSublevels.includes(sub.id);
                      const isCurr = idx === selectedSublevelIndex;
                      return (
                        <button
                          key={sub.id}
                          onClick={() => setSelectedSublevelIndex(idx)}
                          className={`w-full text-left p-3.5 rounded-xl border transition-all flex items-start justify-between gap-3 ${
                            isCurr
                              ? 'bg-emerald-950/30 border-emerald-500/60 text-white'
                              : 'bg-slate-950/60 border-slate-800/80 text-slate-300 hover:border-slate-700'
                          }`}
                        >
                          <div>
                            <div className="text-[11px] font-mono text-cyan-400 mb-0.5">
                              {sub.tier}
                            </div>
                            <div className="text-sm font-semibold">{sub.title}</div>
                            <div className="text-xs text-slate-400 mt-1">{sub.summary}</div>
                          </div>
                          <div className="shrink-0 mt-1">
                            {isDone ? (
                              <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded-md bg-emerald-500/20 text-emerald-300 text-[10px] font-mono border border-emerald-500/30">
                                <Check className="w-3 h-3" /> +50XP
                              </span>
                            ) : (
                              <ChevronRight className="w-4 h-4 text-slate-500" />
                            )}
                          </div>
                        </button>
                      );
                    })}
                  </div>
                </div>

                {/* Embedded Interactive Realm Sandbox / Calculator */}
                <div className="bg-slate-900/90 border border-cyan-500/30 rounded-2xl p-5">
                  <div className="flex items-center gap-2 text-xs font-mono uppercase tracking-wider text-cyan-400 mb-3">
                    <Calculator className="w-4 h-4" />
                    <span>Interactive Realm Formula Simulator</span>
                  </div>

                  {/* Tool 1: 2D Array Row-Major vs Column-Major Calculator */}
                  {selectedRealm.interactiveTool === 'array2d' && (
                    <div className="space-y-3 text-xs">
                      <p className="text-slate-300">
                        Compute exact byte addresses for <code className="text-cyan-300">A[{arrRows}][{arrCols}]</code> (0-indexed):
                      </p>
                      <div className="grid grid-cols-3 gap-2">
                        <label className="bg-slate-950 p-2 rounded-lg border border-slate-800">
                          <span className="text-slate-400 block mb-1">Rows (R)</span>
                          <input
                            type="number"
                            value={arrRows}
                            onChange={(e) => setArrRows(Math.max(1, Number(e.target.value)))}
                            className="w-full bg-transparent font-mono text-sm text-white focus:outline-none"
                          />
                        </label>
                        <label className="bg-slate-950 p-2 rounded-lg border border-slate-800">
                          <span className="text-slate-400 block mb-1">Cols (C)</span>
                          <input
                            type="number"
                            value={arrCols}
                            onChange={(e) => setArrCols(Math.max(1, Number(e.target.value)))}
                            className="w-full bg-transparent font-mono text-sm text-white focus:outline-none"
                          />
                        </label>
                        <label className="bg-slate-950 p-2 rounded-lg border border-slate-800">
                          <span className="text-slate-400 block mb-1">Base Addr</span>
                          <input
                            type="number"
                            value={arrBase}
                            onChange={(e) => setArrBase(Number(e.target.value))}
                            className="w-full bg-transparent font-mono text-sm text-white focus:outline-none"
                          />
                        </label>
                        <label className="bg-slate-950 p-2 rounded-lg border border-slate-800">
                          <span className="text-slate-400 block mb-1">Target i</span>
                          <input
                            type="number"
                            value={arrI}
                            onChange={(e) => setArrI(Number(e.target.value))}
                            className="w-full bg-transparent font-mono text-sm text-emerald-300 focus:outline-none"
                          />
                        </label>
                        <label className="bg-slate-950 p-2 rounded-lg border border-slate-800">
                          <span className="text-slate-400 block mb-1">Target j</span>
                          <input
                            type="number"
                            value={arrJ}
                            onChange={(e) => setArrJ(Number(e.target.value))}
                            className="w-full bg-transparent font-mono text-sm text-emerald-300 focus:outline-none"
                          />
                        </label>
                        <label className="bg-slate-950 p-2 rounded-lg border border-slate-800">
                          <span className="text-slate-400 block mb-1">sizeof(T)</span>
                          <input
                            type="number"
                            value={arrSize}
                            onChange={(e) => setArrSize(Math.max(1, Number(e.target.value)))}
                            className="w-full bg-transparent font-mono text-sm text-white focus:outline-none"
                          />
                        </label>
                      </div>
                      <div className="p-3 rounded-xl bg-slate-950 border border-slate-800 space-y-1.5 font-mono">
                        <div className="flex justify-between">
                          <span className="text-slate-400">Row-Major Address:</span>
                          <span className="text-emerald-400 font-bold">
                            {arrBase + (arrI * arrCols + arrJ) * arrSize}
                          </span>
                        </div>
                        <div className="text-[11px] text-slate-500">
                          = {arrBase} + ({arrI} × {arrCols} + {arrJ}) × {arrSize}
                        </div>
                        <div className="flex justify-between pt-1 border-t border-slate-800">
                          <span className="text-slate-400">Column-Major Address:</span>
                          <span className="text-amber-400 font-bold">
                            {arrBase + (arrJ * arrRows + arrI) * arrSize}
                          </span>
                        </div>
                        <div className="text-[11px] text-slate-500">
                          = {arrBase} + ({arrJ} × {arrRows} + {arrI}) × {arrSize}
                        </div>
                      </div>
                    </div>
                  )}

                  {/* Tool 2: Circular Queue Modulo Inspector */}
                  {selectedRealm.interactiveTool === 'circularQueue' && (
                    <div className="space-y-3 text-xs">
                      <p className="text-slate-300">
                        Test Circular Queue wrap-around math <code className="text-cyan-300">(rear - front + N) % N</code>:
                      </p>
                      <div className="grid grid-cols-3 gap-2">
                        <label className="bg-slate-950 p-2 rounded-lg border border-slate-800">
                          <span className="text-slate-400 block mb-1">Size N</span>
                          <input
                            type="number"
                            value={cqSize}
                            onChange={(e) => setCqSize(Math.max(2, Number(e.target.value)))}
                            className="w-full bg-transparent font-mono text-sm text-white focus:outline-none"
                          />
                        </label>
                        <label className="bg-slate-950 p-2 rounded-lg border border-slate-800">
                          <span className="text-slate-400 block mb-1">front idx</span>
                          <input
                            type="number"
                            value={cqFront}
                            onChange={(e) => setCqFront(Math.max(0, Number(e.target.value) % cqSize))}
                            className="w-full bg-transparent font-mono text-sm text-cyan-300 focus:outline-none"
                          />
                        </label>
                        <label className="bg-slate-950 p-2 rounded-lg border border-slate-800">
                          <span className="text-slate-400 block mb-1">rear idx</span>
                          <input
                            type="number"
                            value={cqRear}
                            onChange={(e) => setCqRear(Math.max(0, Number(e.target.value) % cqSize))}
                            className="w-full bg-transparent font-mono text-sm text-emerald-300 focus:outline-none"
                          />
                        </label>
                      </div>
                      <div className="p-3 rounded-xl bg-slate-950 border border-slate-800 font-mono space-y-1.5">
                        <div className="flex justify-between">
                          <span className="text-slate-400">Active Elements:</span>
                          <span className="text-emerald-400 font-bold">
                            {(cqRear - cqFront + cqSize) % cqSize}
                          </span>
                        </div>
                        <div className="flex justify-between">
                          <span className="text-slate-400">Next Rear (Enqueue):</span>
                          <span className="text-cyan-300">{(cqRear + 1) % cqSize}</span>
                        </div>
                        <div className="flex justify-between">
                          <span className="text-slate-400">Queue State:</span>
                          <span className="text-amber-300">
                            {cqFront === cqRear
                              ? 'EMPTY (front == rear)'
                              : (cqRear + 1) % cqSize === cqFront
                              ? 'FULL ((rear+1)%N == front)'
                              : 'PARTIALLY FILLED'}
                          </span>
                        </div>
                      </div>
                    </div>
                  )}

                  {/* Tool 3: Catalan & AVL Min-Nodes Calculator */}
                  {selectedRealm.interactiveTool === 'catalanAvl' && (
                    <div className="space-y-3 text-xs">
                      <label className="block bg-slate-950 p-2.5 rounded-lg border border-slate-800">
                        <span className="text-slate-400 block mb-1">
                          Select n (Nodes / Height parameter: {catN})
                        </span>
                        <input
                          type="range"
                          min="1"
                          max="7"
                          value={catN}
                          onChange={(e) => setCatN(Number(e.target.value))}
                          className="w-full accent-emerald-400"
                        />
                      </label>
                      {(() => {
                        const fact = (x) => (x <= 1 ? 1 : x * fact(x - 1));
                        const catalan = Math.round(fact(2 * catN) / (fact(catN + 1) * fact(catN)));
                        const labeled = catalan * fact(catN);
                        const avlMin = [1, 2, 4, 7, 12, 20, 33, 54][catN] || 1;
                        return (
                          <div className="p-3 rounded-xl bg-slate-950 border border-slate-800 font-mono space-y-1.5">
                            <div className="flex justify-between">
                              <span className="text-slate-400">Unlabeled Trees / BSTs (C_{catN}):</span>
                              <span className="text-emerald-400 font-bold">{catalan}</span>
                            </div>
                            <div className="flex justify-between">
                              <span className="text-slate-400">Labeled Binary Trees (C_{catN} × {catN}!):</span>
                              <span className="text-cyan-300 font-bold">{labeled}</span>
                            </div>
                            <div className="flex justify-between">
                              <span className="text-slate-400">Min Nodes in AVL of Height h={catN}:</span>
                              <span className="text-amber-300 font-bold">{avlMin}</span>
                            </div>
                          </div>
                        );
                      })()}
                    </div>
                  )}

                  {/* Tool 4: Hashing Expected Empty Slots & Load Factor Estimator */}
                  {selectedRealm.interactiveTool === 'hashEstimator' && (
                    <div className="space-y-3 text-xs">
                      <div className="grid grid-cols-2 gap-2">
                        <label className="bg-slate-950 p-2 rounded-lg border border-slate-800">
                          <span className="text-slate-400 block mb-1">Slots (m)</span>
                          <input
                            type="number"
                            value={hashM}
                            onChange={(e) => setHashM(Math.max(2, Number(e.target.value)))}
                            className="w-full bg-transparent font-mono text-sm text-white focus:outline-none"
                          />
                        </label>
                        <label className="bg-slate-950 p-2 rounded-lg border border-slate-800">
                          <span className="text-slate-400 block mb-1">Keys (n)</span>
                          <input
                            type="number"
                            value={hashN}
                            onChange={(e) => setHashN(Math.max(1, Number(e.target.value)))}
                            className="w-full bg-transparent font-mono text-sm text-emerald-300 focus:outline-none"
                          />
                        </label>
                      </div>
                      {(() => {
                        const alpha = (hashN / hashM).toFixed(2);
                        const emptyExp = hashM * Math.pow((hashM - 1) / hashM, hashN);
                        const collExp = hashN - (hashM - emptyExp);
                        return (
                          <div className="p-3 rounded-xl bg-slate-950 border border-slate-800 font-mono space-y-1.5">
                            <div className="flex justify-between">
                              <span className="text-slate-400">Load Factor (α = n/m):</span>
                              <span className="text-cyan-300 font-bold">{alpha}</span>
                            </div>
                            <div className="flex justify-between">
                              <span className="text-slate-400">Expected Empty Slots:</span>
                              <span className="text-emerald-400 font-bold">{emptyExp.toFixed(3)}</span>
                            </div>
                            <div className="flex justify-between">
                              <span className="text-slate-400">Expected Collisions:</span>
                              <span className="text-amber-300 font-bold">{collExp.toFixed(3)}</span>
                            </div>
                          </div>
                        );
                      })()}
                    </div>
                  )}

                  {/* Tool 5: Master Theorem Interactive Solver */}
                  {selectedRealm.interactiveTool === 'masterTheorem' && (
                    <div className="space-y-3 text-xs">
                      <p className="text-slate-300 font-mono">
                        T(n) = {mtA}T(n/{mtB}) + Θ(n^{mtK} · log^{mtP} n)
                      </p>
                      <div className="grid grid-cols-4 gap-2">
                        <label className="bg-slate-950 p-2 rounded-lg border border-slate-800">
                          <span className="text-slate-400 block mb-1">a (&gt;=1)</span>
                          <input
                            type="number"
                            value={mtA}
                            onChange={(e) => setMtA(Math.max(1, Number(e.target.value)))}
                            className="w-full bg-transparent font-mono text-sm text-white focus:outline-none"
                          />
                        </label>
                        <label className="bg-slate-950 p-2 rounded-lg border border-slate-800">
                          <span className="text-slate-400 block mb-1">b (&gt;1)</span>
                          <input
                            type="number"
                            value={mtB}
                            onChange={(e) => setMtB(Math.max(2, Number(e.target.value)))}
                            className="w-full bg-transparent font-mono text-sm text-white focus:outline-none"
                          />
                        </label>
                        <label className="bg-slate-950 p-2 rounded-lg border border-slate-800">
                          <span className="text-slate-400 block mb-1">k (&gt;=0)</span>
                          <input
                            type="number"
                            value={mtK}
                            onChange={(e) => setMtK(Math.max(0, Number(e.target.value)))}
                            className="w-full bg-transparent font-mono text-sm text-emerald-300 focus:outline-none"
                          />
                        </label>
                        <label className="bg-slate-950 p-2 rounded-lg border border-slate-800">
                          <span className="text-slate-400 block mb-1">p (log)</span>
                          <input
                            type="number"
                            value={mtP}
                            onChange={(e) => setMtP(Number(e.target.value))}
                            className="w-full bg-transparent font-mono text-sm text-cyan-300 focus:outline-none"
                          />
                        </label>
                      </div>
                      {(() => {
                        const c = Math.log(mtA) / Math.log(mtB);
                        const cRound = +c.toFixed(2);
                        let bound = '';
                        let caseLabel = '';
                        if (Math.abs(c - mtK) < 1e-6) {
                          caseLabel = 'Case 2 (log_b(a) == k)';
                          if (mtP > -1) bound = `Θ(n^${mtK} · log^${mtP + 1} n)`;
                          else if (mtP === -1) bound = `Θ(n^${mtK} · log(log n))`;
                          else bound = `Θ(n^${mtK})`;
                        } else if (c > mtK) {
                          caseLabel = 'Case 1 (Leaves Dominate: log_b(a) > k)';
                          bound = `Θ(n^${cRound})`;
                        } else {
                          caseLabel = 'Case 3 (Root Dominates: log_b(a) < k)';
                          bound = `Θ(n^${mtK}${mtP ? ` · log^${mtP} n` : ''})`;
                        }
                        return (
                          <div className="p-3 rounded-xl bg-slate-950 border border-slate-800 font-mono space-y-1">
                            <div className="text-slate-400">
                              Critical Exponent log_{mtB}({mtA}) = <span className="text-white">{cRound}</span>
                            </div>
                            <div className="text-cyan-300">{caseLabel}</div>
                            <div className="text-emerald-400 font-bold text-sm pt-1">
                              T(n) = {bound}
                            </div>
                          </div>
                        );
                      })()}
                    </div>
                  )}

                  {/* Tool 6: Graph Edge & MST Invariant Quick Checker */}
                  {selectedRealm.interactiveTool === 'mstCutTester' && (
                    <div className="p-3 rounded-xl bg-slate-950 border border-slate-800 text-xs font-mono space-y-2">
                      <div className="text-emerald-400 font-bold">
                        MST & Shortest Path Transformation Matrix:
                      </div>
                      <div className="grid grid-cols-3 gap-1.5 text-[11px] border-b border-slate-800 pb-1 text-slate-400">
                        <span>Weight Change</span>
                        <span>MST Same?</span>
                        <span>Shortest Path?</span>
                      </div>
                      <div className="grid grid-cols-3 gap-1.5">
                        <span className="text-white">w&apos; = w + C (C&gt;0)</span>
                        <span className="text-emerald-400">YES (Always)</span>
                        <span className="text-rose-400">NO (Can change)</span>
                      </div>
                      <div className="grid grid-cols-3 gap-1.5">
                        <span className="text-white">w&apos; = k · w (k&gt;0)</span>
                        <span className="text-emerald-400">YES (Always)</span>
                        <span className="text-emerald-400">YES (Always)</span>
                      </div>
                      <div className="grid grid-cols-3 gap-1.5">
                        <span className="text-white">w&apos; = w² (w&gt;0)</span>
                        <span className="text-emerald-400">YES (Monotonic)</span>
                        <span className="text-rose-400">NO (Can change)</span>
                      </div>
                    </div>
                  )}
                </div>
              </div>

              {/* Right Column: Active Lesson Mental Model, C Code & GATE Trap */}
              <div className="lg:col-span-7 bg-slate-900/85 border border-slate-800 rounded-2xl p-6 flex flex-col justify-between space-y-6">
                <div className="space-y-5">
                  {/* Lesson Header */}
                  <div className="flex flex-wrap items-center justify-between gap-2 pb-4 border-b border-slate-800">
                    <div>
                      <span className="text-xs font-mono uppercase tracking-wider text-cyan-400">
                        {selectedSublevel.tier}
                      </span>
                      <h2 className="text-xl font-bold text-white mt-0.5">
                        {selectedSublevel.title}
                      </h2>
                    </div>
                    <button
                      onClick={() => handleCompleteSublevel(selectedSublevel.id)}
                      disabled={completedSublevels.includes(selectedSublevel.id)}
                      className={`px-4 py-2 rounded-xl font-mono text-xs font-bold flex items-center gap-2 transition-all ${
                        completedSublevels.includes(selectedSublevel.id)
                          ? 'bg-emerald-500/20 text-emerald-300 border border-emerald-500/40 cursor-default'
                          : 'bg-gradient-to-r from-emerald-500 to-cyan-500 text-slate-950 hover:opacity-95 shadow-lg shadow-emerald-950/50'
                      }`}
                    >
                      <CheckCircle2 className="w-4 h-4" />
                      {completedSublevels.includes(selectedSublevel.id)
                        ? 'Lesson Completed (+50 XP Earned)'
                        : 'Complete Lesson (+50 XP)'}
                    </button>
                  </div>

                  {/* Visual Mental Model */}
                  <div>
                    <h4 className="text-xs font-mono uppercase tracking-wider text-slate-400 mb-2 flex items-center gap-1.5">
                      <Layers className="w-4 h-4 text-emerald-400" />
                      <span>Core Mental Model & Mathematical Formulation</span>
                    </h4>
                    <div className="p-4 rounded-xl bg-slate-950/90 border border-slate-800/90 text-sm text-slate-200 whitespace-pre-line leading-relaxed font-mono">
                      {selectedSublevel.mentalModel}
                    </div>
                  </div>

                  {/* C Implementation & Dry-Run Trace */}
                  <div>
                    <h4 className="text-xs font-mono uppercase tracking-wider text-slate-400 mb-2 flex items-center gap-1.5">
                      <Code2 className="w-4 h-4 text-cyan-400" />
                      <span>GATE Standard C Implementation & Dry-Run</span>
                    </h4>
                    <pre className="p-4 rounded-xl bg-slate-950 border border-cyan-500/30 text-xs sm:text-sm font-mono text-cyan-200 overflow-x-auto leading-relaxed">
                      {selectedSublevel.code}
                    </pre>
                  </div>

                  {/* GATE Edge Case & Trap Alert */}
                  <div className="p-4 rounded-xl bg-amber-950/30 border border-amber-500/50 flex items-start gap-3">
                    <ShieldAlert className="w-5 h-5 text-amber-400 shrink-0 mt-0.5" />
                    <div className="text-xs sm:text-sm text-amber-200 leading-relaxed">
                      {selectedSublevel.gateTrap}
                    </div>
                  </div>
                </div>

                {/* Bottom Sublevel Navigation */}
                <div className="flex items-center justify-between pt-4 border-t border-slate-800">
                  <button
                    onClick={() => setSelectedSublevelIndex((i) => Math.max(0, i - 1))}
                    disabled={selectedSublevelIndex === 0}
                    className="px-3.5 py-2 rounded-xl bg-slate-800 hover:bg-slate-700 disabled:opacity-40 text-xs font-mono flex items-center gap-1.5"
                  >
                    <ChevronLeft className="w-4 h-4" /> Previous Tier
                  </button>
                  <button
                    onClick={() => setActiveTab('dry-run-lab')}
                    className="text-xs font-mono text-cyan-400 hover:text-cyan-300 flex items-center gap-1"
                  >
                    Launch Live Visualizer in Dry-Run Lab <ArrowRight className="w-3.5 h-3.5" />
                  </button>
                  <button
                    onClick={() =>
                      setSelectedSublevelIndex((i) =>
                        Math.min(selectedRealm.sublevels.length - 1, i + 1)
                      )
                    }
                    disabled={selectedSublevelIndex === selectedRealm.sublevels.length - 1}
                    className="px-3.5 py-2 rounded-xl bg-slate-800 hover:bg-slate-700 disabled:opacity-40 text-xs font-mono flex items-center gap-1.5"
                  >
                    Next Tier <ChevronRight className="w-4 h-4" />
                  </button>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* ==================================================================
            TAB 2: INTERACTIVE DRY-RUN LAB (4 LIVE SIMULATORS)
        ================================================================== */}
        {activeTab === 'dry-run-lab' && (
          <div className="space-y-6">
            {/* Simulator Selector Sub-tabs */}
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3">
              {[
                { id: 'hashing', title: '1. Hash Table Collision Lab', sub: 'Linear / Quadratic / Double Hashing', icon: Hash },
                { id: 'trees', title: '2. AVL Rotator & O(n) Heap Lab', sub: 'Balance Factors & Build-Max-Heap', icon: GitBranch },
                { id: 'recursion', title: '3. Recursion & Pointer Tracer', sub: 'Call Stack Frames & Static Memory', icon: Cpu },
                { id: 'graphs', title: '4. Graph Traversal & MST Lab', sub: 'DFS [d/f], Dijkstra & Kruskal Sets', icon: Network }
              ].map((lab) => {
                const Icon = lab.icon;
                const active = activeLab === lab.id;
                return (
                  <button
                    key={lab.id}
                    onClick={() => setActiveLab(lab.id)}
                    className={`p-4 rounded-2xl border text-left transition-all ${
                      active
                        ? 'bg-slate-900 border-cyan-400/70 shadow-lg shadow-cyan-950/30'
                        : 'bg-slate-900/50 border-slate-800 hover:border-slate-700'
                    }`}
                  >
                    <div className="flex items-center gap-2.5 mb-1">
                      <Icon className={`w-4 h-4 ${active ? 'text-cyan-400' : 'text-slate-400'}`} />
                      <span className="font-bold text-sm text-white">{lab.title}</span>
                    </div>
                    <p className="text-xs text-slate-400 font-mono">{lab.sub}</p>
                  </button>
                );
              })}
            </div>

            {/* SIMULATOR 1: HASH TABLE COLLISION VISUALIZER */}
            {activeLab === 'hashing' && (
              <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
                <div className="lg:col-span-5 bg-slate-900/90 border border-slate-800 rounded-2xl p-5 space-y-4">
                  <h3 className="text-base font-bold text-white flex items-center gap-2">
                    <Hash className="w-5 h-5 text-amber-400" />
                    <span>Open Addressing Probe Configuration</span>
                  </h3>

                  <div className="space-y-3 text-xs">
                    <label className="block">
                      <span className="text-slate-400 font-mono block mb-1">
                        Key Sequence (comma-separated integers):
                      </span>
                      <input
                        type="text"
                        value={hashInputKeys}
                        onChange={(e) => {
                          setHashInputKeys(e.target.value);
                          setHashStepCount(15);
                        }}
                        className="w-full px-3 py-2 rounded-xl bg-slate-950 border border-slate-800 font-mono text-sm text-emerald-300 focus:outline-none focus:border-emerald-500"
                      />
                    </label>

                    <div className="grid grid-cols-2 gap-3">
                      <label className="block">
                        <span className="text-slate-400 font-mono block mb-1">Table Size (m):</span>
                        <select
                          value={hashTableSize}
                          onChange={(e) => setHashTableSize(Number(e.target.value))}
                          className="w-full px-3 py-2 rounded-xl bg-slate-950 border border-slate-800 font-mono text-sm text-white"
                        >
                          {[7, 10, 11, 13].map((sz) => (
                            <option key={sz} value={sz}>
                              m = {sz}
                            </option>
                          ))}
                        </select>
                      </label>

                      <label className="block">
                        <span className="text-slate-400 font-mono block mb-1">Collision Strategy:</span>
                        <select
                          value={hashStrategy}
                          onChange={(e) => setHashStrategy(e.target.value)}
                          className="w-full px-3 py-2 rounded-xl bg-slate-950 border border-slate-800 font-mono text-sm text-cyan-300"
                        >
                          <option value="linear">Linear Probing: (h + i) % m</option>
                          <option value="quadratic">Quadratic: (h + i²) % m</option>
                          <option value="double">Double Hashing: (h1 + i·h2) % m</option>
                        </select>
                      </label>
                    </div>

                    {/* Step-by-step insertion slider */}
                    <div className="p-3 rounded-xl bg-slate-950 border border-slate-800">
                      <div className="flex justify-between font-mono text-xs mb-1">
                        <span className="text-slate-400">Step Through Insertions:</span>
                        <span className="text-amber-300">
                          {Math.min(hashStepCount, hashSimulation.rawKeys.length)} / {hashSimulation.rawKeys.length} Keys
                        </span>
                      </div>
                      <input
                        type="range"
                        min="0"
                        max={hashSimulation.rawKeys.length}
                        value={Math.min(hashStepCount, hashSimulation.rawKeys.length)}
                        onChange={(e) => setHashStepCount(Number(e.target.value))}
                        className="w-full accent-amber-400"
                      />
                    </div>
                  </div>

                  {/* Summary Metrics */}
                  <div className="grid grid-cols-2 gap-3 pt-2">
                    <div className="p-3 rounded-xl bg-slate-950 border border-amber-500/30">
                      <div className="text-[11px] font-mono text-slate-400">Total Collisions</div>
                      <div className="text-xl font-bold font-mono text-amber-400">
                        {hashSimulation.totalCollisions}
                      </div>
                    </div>
                    <div className="p-3 rounded-xl bg-slate-950 border border-cyan-500/30">
                      <div className="text-[11px] font-mono text-slate-400">Avg Probes / Key</div>
                      <div className="text-xl font-bold font-mono text-cyan-300">
                        {hashSimulation.avgProbes}
                      </div>
                    </div>
                  </div>

                  {/* Step-by-step Probe Log */}
                  <div className="space-y-2 max-h-56 overflow-y-auto pr-1">
                    {hashSimulation.logs.map((item, idx) => (
                      <div
                        key={idx}
                        className="p-2.5 rounded-xl bg-slate-950 border border-slate-800 font-mono text-xs flex items-center justify-between"
                      >
                        <div>
                          <span className="text-emerald-400 font-bold">Key {item.key}</span>
                          <span className="text-slate-500"> (h={item.h1}) </span>
                          <span className="text-slate-300">
                            Path: [{item.path.join(' → ')}]
                          </span>
                        </div>
                        <span
                          className={`px-2 py-0.5 rounded text-[10px] ${
                            item.collisions === 0
                              ? 'bg-emerald-500/15 text-emerald-300'
                              : 'bg-amber-500/20 text-amber-300'
                          }`}
                        >
                          {item.collisions === 0 ? 'Direct Hit' : `${item.collisions} Collisions`}
                        </span>
                      </div>
                    ))}
                  </div>
                </div>

                {/* Visual Hash Table Slots */}
                <div className="lg:col-span-7 bg-slate-900/90 border border-slate-800 rounded-2xl p-5">
                  <div className="flex items-center justify-between mb-4">
                    <h3 className="text-base font-bold text-white font-mono">
                      Hash Table Memory Slots [0 .. {hashSimulation.m - 1}]
                    </h3>
                    <button
                      onClick={() => {
                        setLabsRunCount((c) => c + 1);
                        setXp((x) => x + 40);
                        triggerToast('+40 XP! Hash Probe Simulation Recorded.');
                      }}
                      className="px-3 py-1.5 rounded-xl bg-emerald-500/20 hover:bg-emerald-500/30 text-emerald-300 border border-emerald-500/40 text-xs font-mono"
                    >
                      Claim Lab Run (+40 XP)
                    </button>
                  </div>

                  <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-3">
                    {hashSimulation.table.map((slot, index) => (
                      <div
                        key={index}
                        className={`p-3.5 rounded-xl border font-mono transition-all ${
                          slot === null
                            ? 'bg-slate-950/60 border-slate-800/80 text-slate-600'
                            : slot.displaced
                            ? 'bg-amber-950/30 border-amber-500/60 text-amber-200'
                            : 'bg-emerald-950/30 border-emerald-500/60 text-emerald-200'
                        }`}
                      >
                        <div className="flex items-center justify-between text-[11px] mb-1">
                          <span className="text-slate-400">Slot [{index}]</span>
                          {slot && (
                            <span className="px-1.5 py-0.5 rounded bg-slate-900 text-[10px]">
                              {slot.probes} {slot.probes === 1 ? 'probe' : 'probes'}
                            </span>
                          )}
                        </div>
                        {slot ? (
                          <div>
                            <div className="text-lg font-bold text-white">{slot.key}</div>
                            <div className="text-[10px] text-slate-400">
                              Home: {slot.home} {slot.displaced ? '(Displaced)' : '(Exact)'}
                            </div>
                          </div>
                        ) : (
                          <div className="text-sm py-2">EMPTY</div>
                        )}
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            )}

            {/* SIMULATOR 2: AVL ROTATOR & BINARY MAX-HEAP VISUALIZER */}
            {activeLab === 'trees' && (
              <div className="space-y-5">
                <div className="flex flex-wrap items-center justify-between gap-3 bg-slate-900/90 border border-slate-800 rounded-2xl p-4">
                  <div className="flex items-center gap-2">
                    <button
                      onClick={() => setTreeMode('avl')}
                      className={`px-4 py-2 rounded-xl font-mono text-xs font-bold transition-all ${
                        treeMode === 'avl'
                          ? 'bg-violet-500/20 text-violet-300 border border-violet-500/50'
                          : 'bg-slate-950 text-slate-400 border border-slate-800'
                      }`}
                    >
                      Mode A: Self-Balancing AVL Tree Rotator
                    </button>
                    <button
                      onClick={() => setTreeMode('heap')}
                      className={`px-4 py-2 rounded-xl font-mono text-xs font-bold transition-all ${
                        treeMode === 'heap'
                          ? 'bg-emerald-500/20 text-emerald-300 border border-emerald-500/50'
                          : 'bg-slate-950 text-slate-400 border border-slate-800'
                      }`}
                    >
                      Mode B: Binary Max-Heap & O(n) Build-Heap
                    </button>
                  </div>

                  {treeMode === 'avl' ? (
                    <div className="flex flex-wrap items-center gap-2">
                      <input
                        type="number"
                        value={newNodeInput}
                        onChange={(e) => setNewNodeInput(e.target.value)}
                        placeholder="Key"
                        className="w-20 px-3 py-1.5 rounded-xl bg-slate-950 border border-slate-700 font-mono text-sm text-white"
                      />
                      <button
                        onClick={() => {
                          const val = parseInt(newNodeInput, 10);
                          if (!isNaN(val) && !avlKeys.includes(val) && avlKeys.length < 10) {
                            setAvlKeys((prev) => [...prev, val]);
                            setNewNodeInput(String(Math.floor(Math.random() * 89) + 1));
                          }
                        }}
                        className="px-3.5 py-1.5 rounded-xl bg-violet-500 text-slate-950 font-mono text-xs font-bold hover:bg-violet-400"
                      >
                        + Insert Key
                      </button>
                      <button
                        onClick={() => setAvlKeys([10, 20, 30, 40, 50, 25])}
                        className="px-3 py-1.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-xs font-mono text-cyan-300"
                      >
                        Load RR + RL Trap Sequence
                      </button>
                      <button
                        onClick={() => setAvlKeys([30])}
                        className="px-3 py-1.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-xs font-mono text-slate-300"
                      >
                        Reset
                      </button>
                    </div>
                  ) : (
                    <div className="flex flex-wrap items-center gap-2">
                      <button
                        onClick={handleRunBuildMaxHeap}
                        className="px-4 py-2 rounded-xl bg-emerald-500 text-slate-950 font-mono text-xs font-bold hover:bg-emerald-400"
                      >
                        <Play className="w-3.5 h-3.5 inline mr-1" /> Run O(n) Build-Max-Heap
                      </button>
                      <button
                        onClick={() => {
                          setHeapArray([15, 42, 7, 88, 31, 95, 64]);
                          setHeapStatus('Reset to Unordered Array — Ready for Bottom-Up Heapify');
                        }}
                        className="px-3 py-2 rounded-xl bg-slate-800 hover:bg-slate-700 text-xs font-mono text-slate-300"
                      >
                        <RotateCcw className="w-3.5 h-3.5 inline mr-1" /> Shuffle Array
                      </button>
                    </div>
                  )}
                </div>

                {treeMode === 'avl' ? (
                  <div className="bg-slate-900/90 border border-slate-800 rounded-2xl p-5 space-y-4">
                    <div className="flex flex-wrap items-center justify-between gap-2 text-xs font-mono">
                      <span className="text-slate-400">
                        Insertion Order: <strong className="text-white">[{avlKeys.join(' → ')}]</strong>
                      </span>
                      <span className="px-3 py-1 rounded-lg bg-violet-950/60 border border-violet-500/40 text-violet-200">
                        {avlTreeData.lastRot}
                      </span>
                    </div>

                    <div className="w-full overflow-x-auto bg-slate-950 rounded-xl border border-slate-800 p-4 flex justify-center">
                      <svg width="520" height="270" className="shrink-0">
                        {avlTreeData.edges.map((e, i) => (
                          <line
                            key={i}
                            x1={e.x1}
                            y1={e.y1}
                            x2={e.x2}
                            y2={e.y2}
                            stroke="#475569"
                            strokeWidth="2"
                          />
                        ))}
                        {avlTreeData.nodes.map((n, i) => (
                          <g key={i}>
                            <circle
                              cx={n.x}
                              cy={n.y}
                              r="21"
                              fill="#1e1b4b"
                              stroke="#8b5cf6"
                              strokeWidth="2.5"
                            />
                            <text
                              x={n.x}
                              y={n.y + 4}
                              textAnchor="middle"
                              fill="#ffffff"
                              fontSize="13"
                              fontWeight="bold"
                              fontFamily="monospace"
                            >
                              {n.val}
                            </text>
                            <text
                              x={n.x + 28}
                              y={n.y - 6}
                              fill="#34d399"
                              fontSize="10"
                              fontFamily="monospace"
                            >
                              BF={n.bf}
                            </text>
                            <text
                              x={n.x + 28}
                              y={n.y + 7}
                              fill="#94a3b8"
                              fontSize="10"
                              fontFamily="monospace"
                            >
                              h={n.height}
                            </text>
                          </g>
                        ))}
                      </svg>
                    </div>
                  </div>
                ) : (
                  <div className="bg-slate-900/90 border border-slate-800 rounded-2xl p-5 space-y-4">
                    <div className="text-xs font-mono text-emerald-300 bg-emerald-950/30 border border-emerald-500/40 px-3.5 py-2 rounded-xl">
                      {heapStatus}
                    </div>
                    {/* Array Representation */}
                    <div className="grid grid-cols-7 gap-2">
                      {heapArray.map((val, idx) => {
                        const isInternal = idx <= Math.floor(heapArray.length / 2) - 1;
                        return (
                          <div
                            key={idx}
                            className={`p-3 rounded-xl border text-center font-mono ${
                              isInternal
                                ? 'bg-emerald-950/30 border-emerald-500/50'
                                : 'bg-slate-950 border-slate-800'
                            }`}
                          >
                            <div className="text-[10px] text-slate-400">
                              i={idx} {isInternal ? '(Internal)' : '(Leaf)'}
                            </div>
                            <div className="text-lg font-bold text-white mt-0.5">{val}</div>
                          </div>
                        );
                      })}
                    </div>
                  </div>
                )}
              </div>
            )}

            {/* SIMULATOR 3: RECURSION CALL STACK & C POINTER TRACER */}
            {activeLab === 'recursion' && (
              <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
                <div className="lg:col-span-6 bg-slate-900/90 border border-slate-800 rounded-2xl p-5 space-y-4">
                  <div className="flex items-center justify-between">
                    <h3 className="text-base font-bold text-white">Select Classic GATE C Program:</h3>
                  </div>
                  <select
                    value={selectedPresetIdx}
                    onChange={(e) => {
                      setSelectedPresetIdx(Number(e.target.value));
                      setTraceStep(0);
                    }}
                    className="w-full px-3.5 py-2.5 rounded-xl bg-slate-950 border border-slate-800 font-mono text-xs sm:text-sm text-cyan-300"
                  >
                    {RECURSION_PRESETS.map((p, idx) => (
                      <option key={p.id} value={idx}>
                        {p.name}
                      </option>
                    ))}
                  </select>

                  <pre className="p-4 rounded-xl bg-slate-950 border border-slate-800 font-mono text-xs sm:text-sm text-emerald-200 overflow-x-auto leading-relaxed">
                    {RECURSION_PRESETS[selectedPresetIdx].code}
                  </pre>

                  {/* Stepper Controls */}
                  <div className="flex items-center justify-between pt-2">
                    <button
                      onClick={() => setTraceStep((s) => Math.max(0, s - 1))}
                      disabled={traceStep === 0}
                      className="px-4 py-2 rounded-xl bg-slate-800 hover:bg-slate-700 disabled:opacity-40 font-mono text-xs flex items-center gap-1"
                    >
                      <ChevronLeft className="w-4 h-4" /> Step Back
                    </button>
                    <span className="font-mono text-xs text-slate-400">
                      Step {traceStep + 1} / {RECURSION_PRESETS[selectedPresetIdx].steps.length}
                    </span>
                    <button
                      onClick={() => {
                        const maxS = RECURSION_PRESETS[selectedPresetIdx].steps.length - 1;
                        if (traceStep < maxS) {
                          setTraceStep((s) => s + 1);
                        } else {
                          setLabsRunCount((c) => c + 1);
                          setXp((x) => x + 40);
                          triggerToast('+40 XP! Completed Full Call Stack Memory Trace.');
                        }
                      }}
                      className="px-4 py-2 rounded-xl bg-cyan-500 text-slate-950 font-bold font-mono text-xs flex items-center gap-1"
                    >
                      {traceStep < RECURSION_PRESETS[selectedPresetIdx].steps.length - 1
                        ? 'Step Forward'
                        : 'Finish & Claim +40 XP'}{' '}
                      <ChevronRight className="w-4 h-4" />
                    </button>
                  </div>
                </div>

                {/* Right: Live Stack Frames & Static/Data Segment Box */}
                <div className="lg:col-span-6 bg-slate-900/90 border border-slate-800 rounded-2xl p-5 space-y-4">
                  {(() => {
                    const curr = RECURSION_PRESETS[selectedPresetIdx].steps[traceStep];
                    return (
                      <>
                        <div className="p-3.5 rounded-xl bg-cyan-950/30 border border-cyan-500/40 text-xs sm:text-sm text-cyan-100 font-mono">
                          {curr.desc}
                        </div>

                        <div className="grid grid-cols-2 gap-3 font-mono">
                          <div className="p-3.5 rounded-xl bg-slate-950 border border-amber-500/40">
                            <div className="text-[11px] text-slate-400 mb-1">
                              Data Segment / Pointer State
                            </div>
                            <div className="text-sm font-bold text-amber-300">{curr.staticVal}</div>
                          </div>
                          <div className="p-3.5 rounded-xl bg-slate-950 border border-emerald-500/40">
                            <div className="text-[11px] text-slate-400 mb-1">Console / Return Output</div>
                            <div className="text-sm font-bold text-emerald-300">
                              {curr.output || '(Waiting...)'}
                            </div>
                          </div>
                        </div>

                        <div>
                          <div className="text-xs font-mono uppercase tracking-wider text-slate-400 mb-2">
                            Live Call Stack Activation Records (Top of Stack First):
                          </div>
                          <div className="space-y-2">
                            {[...curr.stack].reverse().map((frame, i) => (
                              <div
                                key={i}
                                className={`p-3 rounded-xl font-mono text-xs border ${
                                  i === 0
                                    ? 'bg-emerald-950/40 border-emerald-500/60 text-emerald-200 font-bold'
                                    : 'bg-slate-950 border-slate-800 text-slate-400'
                                }`}
                              >
                                {i === 0 ? '→ ACTIVE FRAME: ' : '   WAITING: '}
                                {frame}
                              </div>
                            ))}
                          </div>
                        </div>
                      </>
                    );
                  })()}
                </div>
              </div>
            )}

            {/* SIMULATOR 4: GRAPH TRAVERSAL & SHORTEST PATH DRY-RUNNER */}
            {activeLab === 'graphs' && (
              <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
                <div className="lg:col-span-5 bg-slate-900/90 border border-slate-800 rounded-2xl p-5 space-y-4">
                  <h3 className="text-base font-bold text-white">Select Graph Algorithm Dry-Run:</h3>
                  <div className="grid grid-cols-3 gap-2">
                    {[
                      { id: 'dfs', label: 'DFS & Back Edges' },
                      { id: 'dijkstra', label: 'Dijkstra Relax' },
                      { id: 'kruskal', label: 'Kruskal MST' }
                    ].map((g) => (
                      <button
                        key={g.id}
                        onClick={() => {
                          setGraphAlgo(g.id);
                          setGraphStep(0);
                        }}
                        className={`p-2.5 rounded-xl font-mono text-xs font-bold border ${
                          graphAlgo === g.id
                            ? 'bg-emerald-500/20 text-emerald-300 border-emerald-500/50'
                            : 'bg-slate-950 text-slate-400 border-slate-800'
                        }`}
                      >
                        {g.label}
                      </button>
                    ))}
                  </div>

                  {(() => {
                    const steps = GRAPH_SIMULATIONS[graphAlgo];
                    const curr = steps[graphStep] || steps[0];
                    return (
                      <div className="space-y-4">
                        <div className="p-4 rounded-xl bg-slate-950 border border-cyan-500/40 space-y-1.5">
                          <div className="text-xs font-mono text-cyan-400 font-bold">
                            {curr.title}
                          </div>
                          <p className="text-xs text-slate-300 leading-relaxed">{curr.desc}</p>
                        </div>

                        <div className="space-y-1.5">
                          <div className="text-xs font-mono text-slate-400">
                            Edge Classification / Relaxation State:
                          </div>
                          {Object.entries(curr.edgeTypes).length === 0 ? (
                            <div className="text-xs font-mono text-slate-500 p-2 bg-slate-950 rounded-lg">
                              No edges classified yet — step forward!
                            </div>
                          ) : (
                            Object.entries(curr.edgeTypes).map(([edge, status]) => (
                              <div
                                key={edge}
                                className="flex justify-between px-3 py-1.5 rounded-lg bg-slate-950 border border-slate-800 font-mono text-xs"
                              >
                                <span className="text-white">Edge ({edge})</span>
                                <span className="text-emerald-400 font-bold">{status}</span>
                              </div>
                            ))
                          )}
                        </div>

                        <div className="flex items-center justify-between pt-2">
                          <button
                            onClick={() => setGraphStep((s) => Math.max(0, s - 1))}
                            disabled={graphStep === 0}
                            className="px-3.5 py-2 rounded-xl bg-slate-800 disabled:opacity-40 text-xs font-mono"
                          >
                            Prev Step
                          </button>
                          <span className="text-xs font-mono text-slate-400">
                            Step {graphStep + 1} / {steps.length}
                          </span>
                          <button
                            onClick={() => {
                              if (graphStep < steps.length - 1) {
                                setGraphStep((s) => s + 1);
                              } else {
                                setLabsRunCount((c) => c + 1);
                                setXp((x) => x + 40);
                                triggerToast('+40 XP! Graph Dry-Run Completed.');
                              }
                            }}
                            className="px-3.5 py-2 rounded-xl bg-emerald-500 text-slate-950 font-bold text-xs font-mono"
                          >
                            {graphStep < steps.length - 1 ? 'Next Step' : 'Complete (+40 XP)'}
                          </button>
                        </div>
                      </div>
                    );
                  })()}
                </div>

                {/* SVG Interactive Graph Canvas */}
                <div className="lg:col-span-7 bg-slate-900/90 border border-slate-800 rounded-2xl p-5 flex flex-col items-center justify-center">
                  {(() => {
                    const curr = GRAPH_SIMULATIONS[graphAlgo][graphStep] || GRAPH_SIMULATIONS[graphAlgo][0];
                    const edges = [
                      { from: 'A', to: 'B', w: 4, key: 'A-B' },
                      { from: 'A', to: 'D', w: 2, key: 'A-D' },
                      { from: 'B', to: 'D', w: 1, key: 'B-D' },
                      { from: 'B', to: 'E', w: 2, key: 'B-E' },
                      { from: 'D', to: 'E', w: 6, key: 'D-E' },
                      { from: 'E', to: 'C', w: 3, key: 'E-C' }
                    ];
                    return (
                      <svg width="480" height="250" className="bg-slate-950 rounded-xl border border-slate-800">
                        {edges.map((e, idx) => {
                          const u = GRAPH_NODES.find((n) => n.id === e.from);
                          const v = GRAPH_NODES.find((n) => n.id === e.to);
                          const highlighted = curr.edgeTypes[e.key] || (e.key === 'A-D' && curr.edgeTypes['D-A']);
                          return (
                            <g key={idx}>
                              <line
                                x1={u.x}
                                y1={u.y}
                                x2={v.x}
                                y2={v.y}
                                stroke={highlighted ? '#10b981' : '#334155'}
                                strokeWidth={highlighted ? '3.5' : '2'}
                              />
                              <text
                                x={(u.x + v.x) / 2}
                                y={(u.y + v.y) / 2 - 6}
                                fill="#fbbf24"
                                fontSize="11"
                                fontFamily="monospace"
                              >
                                w={e.w}
                              </text>
                            </g>
                          );
                        })}
                        {GRAPH_NODES.map((n) => {
                          const isVisited = curr.visited.includes(n.id);
                          const isActive = curr.active === n.id;
                          return (
                            <g key={n.id}>
                              <circle
                                cx={n.x}
                                cy={n.y}
                                r="22"
                                fill={isActive ? '#065f46' : isVisited ? '#1e293b' : '#0f172a'}
                                stroke={isActive ? '#34d399' : isVisited ? '#38bdf8' : '#475569'}
                                strokeWidth="2.5"
                              />
                              <text
                                x={n.x}
                                y={n.y + 4}
                                textAnchor="middle"
                                fill="#ffffff"
                                fontSize="14"
                                fontWeight="bold"
                                fontFamily="monospace"
                              >
                                {n.id}
                              </text>
                              <text
                                x={n.x}
                                y={n.y + 36}
                                textAnchor="middle"
                                fill="#38bdf8"
                                fontSize="11"
                                fontFamily="monospace"
                              >
                                {curr.times[n.id]}
                              </text>
                            </g>
                          );
                        })}
                      </svg>
                    );
                  })()}
                </div>
              </div>
            )}
          </div>
        )}

        {/* ==================================================================
            TAB 3: GATE 2027 BOSS ARENA (CBT SIMULATOR)
        ================================================================== */}
        {activeTab === 'boss-arena' && (
          <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
            {/* Left/Main CBT Question Console */}
            <div className="lg:col-span-8 bg-slate-900/90 border border-slate-800 rounded-2xl p-6 space-y-6">
              {/* Question Top Metadata Bar */}
              <div className="flex flex-wrap items-center justify-between gap-2 pb-4 border-b border-slate-800">
                <div className="flex items-center gap-2">
                  <span className="px-2.5 py-1 rounded-lg bg-violet-500/20 border border-violet-500/40 text-violet-300 font-mono text-xs font-bold">
                    Question #{currentBossQ.id} of {BOSS_QUESTIONS.length}
                  </span>
                  <span className="px-2.5 py-1 rounded-lg bg-cyan-500/15 border border-cyan-500/30 text-cyan-300 font-mono text-xs font-bold">
                    {currentBossQ.type}
                  </span>
                  <span className="text-xs font-mono text-slate-400">
                    {currentBossQ.realm}
                  </span>
                </div>

                <div className="flex items-center gap-3 font-mono text-xs">
                  <span className="text-emerald-400 font-bold">+{currentBossQ.marks} Marks</span>
                  <span className="text-rose-400">
                    Neg: {currentBossQ.negative > 0 ? `-${currentBossQ.negative}` : '0.00'}
                  </span>
                </div>
              </div>

              {/* Question Prompt */}
              <div className="p-4 rounded-xl bg-slate-950 border border-slate-800 text-sm sm:text-base text-slate-100 whitespace-pre-line font-mono leading-relaxed">
                {currentBossQ.question}
              </div>

              {/* Input Controls by Question Type (MCQ / MSQ / NAT) */}
              {currentBossQ.type === 'MCQ' && (
                <div className="space-y-2.5">
                  {currentBossQ.options.map((opt, idx) => {
                    const selected = userAnswers[currentBossQ.id] === idx;
                    return (
                      <button
                        key={idx}
                        onClick={() =>
                          setUserAnswers((prev) => ({ ...prev, [currentBossQ.id]: idx }))
                        }
                        className={`w-full text-left p-3.5 rounded-xl border font-mono text-xs sm:text-sm flex items-center gap-3 transition-all ${
                          selected
                            ? 'bg-emerald-950/40 border-emerald-500/70 text-emerald-200'
                            : 'bg-slate-950/70 border-slate-800 text-slate-300 hover:border-slate-700'
                        }`}
                      >
                        <span className="w-6 h-6 rounded-full border border-current flex items-center justify-center text-xs font-bold shrink-0">
                          {String.fromCharCode(65 + idx)}
                        </span>
                        <span>{opt}</span>
                      </button>
                    );
                  })}
                </div>
              )}

              {currentBossQ.type === 'MSQ' && (
                <div className="space-y-2.5">
                  <div className="text-xs font-mono text-amber-300">
                    * Multiple Select Question (MSQ): Select ALL correct options. No negative marking.
                  </div>
                  {currentBossQ.options.map((opt, idx) => {
                    const currArr = Array.isArray(userAnswers[currentBossQ.id])
                      ? userAnswers[currentBossQ.id]
                      : [];
                    const checked = currArr.includes(idx);
                    return (
                      <button
                        key={idx}
                        onClick={() => {
                          const next = checked
                            ? currArr.filter((i) => i !== idx)
                            : [...currArr, idx];
                          setUserAnswers((prev) => ({ ...prev, [currentBossQ.id]: next }));
                        }}
                        className={`w-full text-left p-3.5 rounded-xl border font-mono text-xs sm:text-sm flex items-center gap-3 transition-all ${
                          checked
                            ? 'bg-cyan-950/40 border-cyan-500/70 text-cyan-200'
                            : 'bg-slate-950/70 border-slate-800 text-slate-300 hover:border-slate-700'
                        }`}
                      >
                        <span className="w-6 h-6 rounded-md border border-current flex items-center justify-center text-xs font-bold shrink-0">
                          {checked ? '✓' : String.fromCharCode(65 + idx)}
                        </span>
                        <span>{opt}</span>
                      </button>
                    );
                  })}
                </div>
              )}

              {currentBossQ.type === 'NAT' && (
                <div className="space-y-3">
                  <div className="text-xs font-mono text-cyan-300">
                    * Numerical Answer Type (NAT): Enter exact integer/numerical value using keyboard or virtual keypad.
                  </div>
                  <div className="flex flex-wrap items-center gap-3">
                    <input
                      type="text"
                      value={userAnswers[currentBossQ.id] || ''}
                      onChange={(e) =>
                        setUserAnswers((prev) => ({ ...prev, [currentBossQ.id]: e.target.value }))
                      }
                      placeholder="Enter numerical value..."
                      className="px-4 py-2.5 rounded-xl bg-slate-950 border border-cyan-500/50 font-mono text-base text-white focus:outline-none"
                    />
                    <div className="flex flex-wrap gap-1.5">
                      {['1', '2', '3', '4', '5', '6', '7', '8', '9', '0'].map((digit) => (
                        <button
                          key={digit}
                          onClick={() =>
                            setUserAnswers((prev) => ({
                              ...prev,
                              [currentBossQ.id]: `${prev[currentBossQ.id] || ''}${digit}`
                            }))
                          }
                          className="w-8 h-8 rounded-lg bg-slate-800 hover:bg-slate-700 font-mono text-xs font-bold text-white"
                        >
                          {digit}
                        </button>
                      ))}
                      <button
                        onClick={() =>
                          setUserAnswers((prev) => ({ ...prev, [currentBossQ.id]: '' }))
                        }
                        className="px-2.5 h-8 rounded-lg bg-rose-950/60 border border-rose-500/40 font-mono text-xs text-rose-300"
                      >
                        Clear
                      </button>
                    </div>
                  </div>
                </div>
              )}

              {/* Action Bar: Verify & Dry-Run Solution, Mark for Review, Prev/Next */}
              <div className="flex flex-wrap items-center justify-between gap-3 pt-4 border-t border-slate-800">
                <div className="flex items-center gap-2">
                  <button
                    onClick={() => handleVerifyBossQuestion(currentBossQ)}
                    className="px-5 py-2.5 rounded-xl bg-gradient-to-r from-emerald-500 to-cyan-500 text-slate-950 font-mono text-xs sm:text-sm font-bold shadow-lg shadow-emerald-950/50 hover:opacity-95"
                  >
                    Verify &amp; Dry-Run Solution (+75 XP)
                  </button>
                  <button
                    onClick={() =>
                      setMarkedForReview((prev) => ({
                        ...prev,
                        [currentBossQ.id]: !prev[currentBossQ.id]
                      }))
                    }
                    className={`px-3.5 py-2.5 rounded-xl font-mono text-xs border ${
                      markedForReview[currentBossQ.id]
                        ? 'bg-amber-500/20 text-amber-300 border-amber-500/40'
                        : 'bg-slate-800 text-slate-300 border-slate-700'
                    }`}
                  >
                    {markedForReview[currentBossQ.id] ? '★ Marked for Review' : 'Mark for Review'}
                  </button>
                </div>

                <div className="flex items-center gap-2">
                  <button
                    onClick={() => setCurrentQIdx((i) => Math.max(0, i - 1))}
                    disabled={currentQIdx === 0}
                    className="px-3.5 py-2 rounded-xl bg-slate-800 disabled:opacity-40 font-mono text-xs"
                  >
                    Prev
                  </button>
                  <button
                    onClick={() =>
                      setCurrentQIdx((i) => Math.min(BOSS_QUESTIONS.length - 1, i + 1))
                    }
                    disabled={currentQIdx === BOSS_QUESTIONS.length - 1}
                    className="px-3.5 py-2 rounded-xl bg-slate-800 disabled:opacity-40 font-mono text-xs"
                  >
                    Next
                  </button>
                </div>
              </div>

              {/* Verified Explanation & GATE Trap Box */}
              {verifiedQuestions[currentBossQ.id] && (
                <div
                  className={`p-5 rounded-2xl border space-y-3 ${
                    verifiedQuestions[currentBossQ.id].isCorrect
                      ? 'bg-emerald-950/25 border-emerald-500/50'
                      : 'bg-rose-950/25 border-rose-500/50'
                  }`}
                >
                  <div className="flex items-center justify-between">
                    <span
                      className={`font-mono text-sm font-bold flex items-center gap-2 ${
                        verifiedQuestions[currentBossQ.id].isCorrect
                          ? 'text-emerald-400'
                          : 'text-rose-400'
                      }`}
                    >
                      {verifiedQuestions[currentBossQ.id].isCorrect ? (
                        <>
                          <CheckCircle2 className="w-5 h-5" /> CORRECT! +{currentBossQ.marks} GATE Marks
                        </>
                      ) : (
                        <>
                          <X className="w-5 h-5" /> INCORRECT (Penalty: -{currentBossQ.negative} Marks)
                        </>
                      )}
                    </span>
                  </div>
                  <div className="text-xs sm:text-sm font-mono text-slate-200 whitespace-pre-line leading-relaxed">
                    {currentBossQ.explanation}
                  </div>
                  <div className="p-3 rounded-xl bg-amber-950/40 border border-amber-500/40 text-xs text-amber-200 font-mono flex items-start gap-2">
                    <AlertTriangle className="w-4 h-4 text-amber-400 shrink-0 mt-0.5" />
                    <span>
                      <strong>GATE Trap Warning:</strong> {currentBossQ.trap}
                    </span>
                  </div>
                </div>
              )}
            </div>

            {/* Right Column: GATE CBT Palette, Timer & Live Scoreboard */}
            <div className="lg:col-span-4 space-y-5">
              {/* Timer & Live Score Card */}
              <div className="bg-slate-900/90 border border-slate-800 rounded-2xl p-5 space-y-4">
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-2 text-xs font-mono text-slate-400">
                    <Clock className="w-4 h-4 text-cyan-400" />
                    <span>CBT Gauntlet Timer</span>
                  </div>
                  <button
                    onClick={() => setTimerRunning((r) => !r)}
                    className="text-xs font-mono px-2.5 py-1 rounded bg-slate-800 text-cyan-300"
                  >
                    {formatTime(examTimerSeconds)} {timerRunning ? '⏸' : '▶'}
                  </button>
                </div>

                <div className="grid grid-cols-3 gap-2 font-mono text-center">
                  <div className="p-2.5 rounded-xl bg-slate-950 border border-emerald-500/30">
                    <div className="text-[10px] text-slate-400">Net Score</div>
                    <div className="text-base font-bold text-emerald-400">
                      {arenaScoreSummary.netScore}
                    </div>
                  </div>
                  <div className="p-2.5 rounded-xl bg-slate-950 border border-cyan-500/30">
                    <div className="text-[10px] text-slate-400">Correct</div>
                    <div className="text-base font-bold text-cyan-300">
                      {arenaScoreSummary.correctCount}
                    </div>
                  </div>
                  <div className="p-2.5 rounded-xl bg-slate-950 border border-rose-500/30">
                    <div className="text-[10px] text-slate-400">Neg Lost</div>
                    <div className="text-base font-bold text-rose-400">
                      -{arenaScoreSummary.negativeLost}
                    </div>
                  </div>
                </div>
              </div>

              {/* Question Palette Grid */}
              <div className="bg-slate-900/90 border border-slate-800 rounded-2xl p-5 space-y-4">
                <h3 className="text-sm font-bold text-white font-mono">
                  GATE 2027 Question Palette (12 Bosses)
                </h3>
                <div className="grid grid-cols-4 gap-2.5">
                  {BOSS_QUESTIONS.map((q, idx) => {
                    const v = verifiedQuestions[q.id];
                    const rev = markedForReview[q.id];
                    const isCurr = idx === currentQIdx;

                    let colorCls = 'bg-slate-950 border-slate-800 text-slate-400';
                    if (v?.isCorrect) {
                      colorCls = 'bg-emerald-500/20 border-emerald-500/60 text-emerald-300';
                    } else if (v && !v.isCorrect) {
                      colorCls = 'bg-rose-500/20 border-rose-500/60 text-rose-300';
                    } else if (rev) {
                      colorCls = 'bg-amber-500/20 border-amber-500/60 text-amber-300';
                    }

                    return (
                      <button
                        key={q.id}
                        onClick={() => setCurrentQIdx(idx)}
                        className={`p-2.5 rounded-xl border font-mono text-xs font-bold transition-all ${colorCls} ${
                          isCurr ? 'ring-2 ring-cyan-400' : ''
                        }`}
                      >
                        <div>Q{q.id}</div>
                        <div className="text-[9px] opacity-75">{q.type}</div>
                      </button>
                    );
                  })}
                </div>
              </div>
            </div>
          </div>
        )}

        {/* ==================================================================
            TAB 4: HIGH-YIELD COMPLEXITY & FORMULA VAULT
        ================================================================== */}
        {activeTab === 'formula-vault' && (
          <div className="space-y-6">
            {/* Search Bar */}
            <div className="bg-slate-900/90 border border-slate-800 rounded-2xl p-4 flex flex-col sm:flex-row items-center justify-between gap-4">
              <div className="relative w-full sm:w-96">
                <Search className="w-4 h-4 text-slate-400 absolute left-3.5 top-3" />
                <input
                  type="text"
                  value={vaultSearch}
                  onChange={(e) => setVaultSearch(e.target.value)}
                  placeholder="Filter by Catalan, AVL, Heap, QuickSort, Hash..."
                  className="w-full pl-10 pr-4 py-2 rounded-xl bg-slate-950 border border-slate-800 text-xs sm:text-sm font-mono text-white focus:outline-none focus:border-emerald-500"
                />
              </div>
              <div className="text-xs font-mono text-slate-400">
                High-Yield GATE 2027 Quick Revision Tables
              </div>
            </div>

            {/* 1. Essential GATE Mathematical Shortcuts */}
            <div className="bg-slate-900/90 border border-slate-800 rounded-2xl p-5 space-y-4">
              <h3 className="text-base font-bold text-white flex items-center gap-2">
                <Sparkles className="w-5 h-5 text-amber-400" />
                <span>1. Essential GATE Mathematical Identities &amp; NAT Shortcuts</span>
              </h3>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-3.5">
                {FORMULA_SHORTCUTS.filter((f) =>
                  `${f.title} ${f.category} ${f.formula} ${f.useCase}`
                    .toLowerCase()
                    .includes(vaultSearch.toLowerCase())
                ).map((item, idx) => (
                  <div
                    key={idx}
                    className="p-4 rounded-xl bg-slate-950 border border-slate-800 space-y-1.5"
                  >
                    <div className="flex items-center justify-between">
                      <span className="text-[11px] font-mono text-cyan-400">{item.category}</span>
                      <span className="text-[11px] font-mono text-amber-300">{item.values}</span>
                    </div>
                    <div className="text-sm font-bold text-white">{item.title}</div>
                    <div className="p-2 rounded-lg bg-slate-900 font-mono text-xs text-emerald-300 border border-slate-800">
                      {item.formula}
                    </div>
                    <p className="text-xs text-slate-400">{item.useCase}</p>
                  </div>
                ))}
              </div>
            </div>

            {/* 2. Data Structure Operations Complexity Table */}
            <div className="bg-slate-900/90 border border-slate-800 rounded-2xl p-5 space-y-4 overflow-x-auto">
              <h3 className="text-base font-bold text-white">
                2. Data Structures Worst / Average Complexity Matrix
              </h3>
              <table className="w-full text-left border-collapse font-mono text-xs">
                <thead>
                  <tr className="border-b border-slate-800 text-slate-400">
                    <th className="py-2.5 px-3">Data Structure</th>
                    <th className="py-2.5 px-3">Access</th>
                    <th className="py-2.5 px-3">Search</th>
                    <th className="py-2.5 px-3">Insert</th>
                    <th className="py-2.5 px-3">Delete</th>
                    <th className="py-2.5 px-3">GATE Critical Note</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-800/70">
                  {DS_COMPLEXITY_TABLE.filter((row) =>
                    `${row.ds} ${row.note}`.toLowerCase().includes(vaultSearch.toLowerCase())
                  ).map((row, idx) => (
                    <tr key={idx} className="hover:bg-slate-950/60">
                      <td className="py-3 px-3 font-bold text-white">{row.ds}</td>
                      <td className="py-3 px-3 text-cyan-300">{row.access}</td>
                      <td className="py-3 px-3 text-emerald-300">{row.search}</td>
                      <td className="py-3 px-3 text-amber-300">{row.insert}</td>
                      <td className="py-3 px-3 text-rose-300">{row.delete}</td>
                      <td className="py-3 px-3 text-slate-300 font-sans">{row.note}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>

            {/* 3. Sorting Algorithms Comparison Table */}
            <div className="bg-slate-900/90 border border-slate-800 rounded-2xl p-5 space-y-4 overflow-x-auto">
              <h3 className="text-base font-bold text-white">
                3. Sorting Algorithms Asymptotic, Stability &amp; Adaptivity Table
              </h3>
              <table className="w-full text-left border-collapse font-mono text-xs">
                <thead>
                  <tr className="border-b border-slate-800 text-slate-400">
                    <th className="py-2.5 px-3">Algorithm</th>
                    <th className="py-2.5 px-3">Best Time</th>
                    <th className="py-2.5 px-3">Avg Time</th>
                    <th className="py-2.5 px-3">Worst Time</th>
                    <th className="py-2.5 px-3">Aux Space</th>
                    <th className="py-2.5 px-3">Stable?</th>
                    <th className="py-2.5 px-3">GATE Special Property</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-800/70">
                  {SORTING_COMPLEXITY_TABLE.filter((row) =>
                    `${row.name} ${row.note}`.toLowerCase().includes(vaultSearch.toLowerCase())
                  ).map((row, idx) => (
                    <tr key={idx} className="hover:bg-slate-950/60">
                      <td className="py-3 px-3 font-bold text-white">{row.name}</td>
                      <td className="py-3 px-3 text-emerald-300">{row.best}</td>
                      <td className="py-3 px-3 text-cyan-300">{row.avg}</td>
                      <td className="py-3 px-3 text-rose-300">{row.worst}</td>
                      <td className="py-3 px-3 text-amber-300">{row.space}</td>
                      <td className="py-3 px-3">{row.stable}</td>
                      <td className="py-3 px-3 text-slate-300 font-sans">{row.note}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}
      </main>
    </div>
  );
}
