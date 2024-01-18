# khollang

## Introduction

**khollang** is an educational programming language made in Python. It has simple pseudocode-like syntax and an ability to limit different parts of its functionality

## Usage

### Locally
You can copy a folder ***interpreter*** where you can run a file ***main.py*** using Python of version 3.10.x+. This file takes two command line arguments: code file and limits file. The code file is mandatory, limits file — not. Limits file is going to be described further.

Example of running:
```bat
python3 main.py code.txt limits.json
```

Additionally, this ***main.py*** you can compress in an executable, if needed

### Online
You can access an online [**Khollang Interpreter**](https://khollang-interpreter.s0urcedev.pp.ua)

## Syntax

### Generals:
* Variable names are case sensitive, syntax — not
* NOT REQUIRED (but recommended): All variable names are in upper case and all syntax is in lower
* NOT REQUIRED (but recommended): Block indentations
* Remeber that functions and procedures have their own memory scope, as opposed to logical blocks that do not
* **//** — comments

### Basic operations
* **input *X*** — inputs a value from the stdin to a variable *X*. The whole line is put to *X*
* **output *X*, *Y*, *Z*, ...** — outputs values of variables *X*, *Y*, *Z*, ... joined by a space. At least one variable is required. Each output is showed as a separte line
* **create *S* *X*** / ***S* *X*** — creates a data structure *S* or puts a default value of a data type in a variable *X*. The list of availabe basic data types and data structures is listed further
* **delete *X*** — deletes a variable *X* from memory
* ***X* = *Y*** / ***X* := *Y*** / ***X* <- *Y*** / ***Y* -> *X*** — assign a value *Y* to a variable *X*

### Basic data types
* **String** — **" "** — string (default — "")
* **Number** — **0** — number (default — 0)
* **Boolean** — **true** / **false** — boolean (default — false)
* **None** — **none** — none

### Operators
* **=** — equal
* **!=** / **<>** — not equal
* **>** — greater
* **>=** — greater or equal
* **<** — less
* **<=** — less or equal
* **NOT** — logical or bitwise NOT
* **AND** — logical or bitwise AND
* **OR** — logical or bitwise OR
* **XOR** — bitwise XOR
* **+** — add
* **-** — subtract
* **\*** — multiply
* **/** — divide
* **mod** — modulo
* **div** — integer division

### If conditions
* **if *X* then** — if *X* is true
* **else if *X* then** — if *X* is true. Used after another if
* **else** — else
* **end if** — an end of a if block

Example:
```
if X < 0 then
    output -1
else if X = 0 then
    output 0
else
    output 1
end if
```


### Match conditions
* **match *X* with** — match *X* with
* **case *Y* then** — if equals *Y*
* **otherwise** — if is not any case
* **end match** — an end of a match block

Example:
```
match X with
    case -1 then
        output -1
    case 0 then
        output 0
    otherwise
        output 1
end match
```

### While loops
* **loop while *X*** — loop while *X* is true
* **end loop** — an end of a loop block

Example:
```
loop while X
    output X
end loop
```

### Until loops
* **loop while *X*** — loop until *X* is true (while *X* is false)
* **end loop** — an end of a loop block

Example:
```
loop until X
    output X
end loop
```

### For loops
* **loop *X* from *Y* to *Z*** / **loop for *X* from *Y* to *Z*** — loop *X* from *Y* to *Z* inclusive with step 1
* **end loop** — an end of a loop block

Examples:
```
loop X from 1 to 10
    output X
end loop
```
```
loop for X from 1 to 10
    output X
end loop
```

### Functions
* **function *X*(*Y*, *Z*, ...)** — a function *X* with arguments *Y*, *Z*, ... All arguments are optional
* **return *X*** — return a value *X* from the function
* **end fuction** — an end of a function block
* ***X*(*Y*, *Z*, ...)** — executes a predeclared function *X* with arguments *Y*, *Z*, ... All arguments are optional

Example:
```
function X(Y, Z)
    return Y + Z
end function

X(1, 2) // returns 3
```

### Procedures
* **procedure *X*(*Y*, *Z*, ...)** — a procedure *X* with arguments *Y*, *Z*, ... All arguments are optional
* **end procedure** — an end of a procedure block
* ***X*(*Y*, *Z*, ...)** — executes a predeclared procedure *X* with arguments *Y*, *Z*, ... All arguments are optional

Example:
```
procedure X(Y, Z)
    output Y + Z
end procedure

X(1, 2) // outputs 3
```

### Data structures
* #### **Array** / **LazyArray** — a lazy array. Its length automatically expands to needs of a program
    * **create Array *X*** / **Array *X*** / **create LazyArray *X*** / **LazyArray *X*** — create a lazy array in a variable *X*
    * **Array(*X*)** / **LazyArray(*X*)** — a direct object of a class lazy array with a body of *X*. *X* is not mandatory. Further this value can be assigned to a variable. Here, the name of the class IS case sensitive as long as it is stored as another variable
    * **[*X*, *Y*, *Z*, ...]** — a short direct form of a lazy array with values *X*, *Y*, *Z*, ... All of them are optional
    * ***X*[*I*]** — get a value with an index *I* from a lazy array *X*
    * ***X*[*I*] = *Y*** — set a value with an index *I* from a azy array *X* with *Y*. Other assignment methods also work
    * ***X*.size()** / ***X*.length()** — get a size/length of a lazy array *X*
* #### **StaticArray** — a static array. Its length does not expand automatically can only be changed with a **resize** method
    * **create StaticArray *X*** / **StaticArray *X*** — create a static array in a variable *X*. By default its length is 0, so you will have to use a **resize** method to use it
    * **StaticArray(*L*, *X*)** — a direct object of a class static array with a length *L* and a body of *X*. *X* is not mandatory. Further this value can be assigned to a variable. Here, the name of the class IS case sensitive as long as it is stored as another variable
    * ***X*[*I*]** — get a value with an index *I* from a static array *X*
    * ***X*[*I*] = *Y*** — set a value with an index *I* from a static array *X* with *Y*. Other assignment methods also work
    * ***X*.size()** / ***X*.length()** — get a size/length of a static array *X*
    * ***X*.resize()** — change a size/length of a static array *X*. It clears its body
* #### **DynamicArray** — a dynamic array. Its length does not expand automatically, but can be changed using methods without clearing it, as **resize** in **StaticArray** does
    * **create DynamicArray *X*** / **DynamicArray *X*** — create a dynamic array in a variable *X*. By default its length is 0
    * **DynamicArray(*X*)** — a direct object of a class dynamic array with a body of *X*. *X* is not mandatory. Further this value can be assigned to a variable. Here, the name of the class IS case sensitive as long as it is stored as another variable
    * **{*A*: *X*, *B*: *Y*, *C*: *Z*, ...}** — a short direct form of a dictionary/map with values *X*, *Y*, *Z*, ... in keys *A*, *B*, *C*, ... All of them are optional
    * ***X*[*I*]** — get a value with an index *I* from a dynamic array *X*
    * ***X*[*I*] = *Y*** — set a value with an index *I* from a dynamic array *X* with *Y*. Other assignment methods also work
    * ***X*.size()** / ***X*.length()** — get a size/length of a dynamic array *X*
    * ***X*.push(*Y*)** — add a value *Y* to the end of a dynamic array *X*
    * ***X*.insert(*I*, *Y*)** — insert a value *Y* to the position *I* in a dynamic array *X*
    * ***X*.pop()** — remove a value from the end of a dynamic array *X*
    * ***X*.remove(*I*)** — remove a value from the position *I* in a dynamic array *X*
* #### **Dictionary** / **Map** — a dictionary/map
    * **create Dictionary *X*** / **Dictionary *X*** / **create Map *X*** / **Map *X*** — create a dictionary/map in a variable *X*
    * **Dictionary()** / **Map()** — a direct object of a class dictionary/map
    * ***X*[*K*]** — get a value with a key *K* from a dictionary/map *X*
    * ***X*[*K*] = *Y*** — set a value with an key *K* from a dictionary/map *X* with *Y*. Other assignment methods also work
    * **{*A*: *X*, *B*: *Y*, *C*: *Z*, ...}** — a short direct form of a dictionary/map with values *X*, *Y*, *Z*, ... in keys *A*, *B*, *C*, ... All of them are optional
* #### **Stack** — a stack
    * **create Stack *X*** / **Stack *X*** — create a stack in a variable *X*
    * **Stack(*X*)** — a direct object of a class stack with a body of *X*. *X* is not mandatory. Further this value can be assigned to a variable. Here, the name of the class IS case sensitive as long as it is stored as another variable
    * ***X*.is_empty()** — check if a stack *X* is empty
    * ***X*.size()** / ***X*.length()** — get a size/length of a stack *X*
    * ***X*.push(*Y*)** — add a value *Y* to a stack *X*
    * ***X*.pop()** — get a value from a stack *X*
* #### **Queue** — a queue
    * **create Queue *X*** / **Queue *X*** — create a queue in a variable *X*
    * **Queue(*X*)** — a direct object of a class queue with a body of *X*. *X* is not mandatory. Further this value can be assigned to a variable. Here, the name of the class IS case sensitive as long as it is stored as another variable
    * ***X*.is_empty()** — check if a queue *X* is empty
    * ***X*.size()** / ***X*.length()** — get a size/length of a queue *X*
    * ***X*.enqueue(*Y*)** — add a value *Y* to a queue *X*
    * ***X*.dequeue()** — get a value from a queue *X*
* #### **BinaryTree** / **BinarySearchTree** — a binary (search) tree
    * **create BinaryTree *X*** / **BinaryTree *X*** / **create BinarySearchTree *X*** / **BinarySearchTree *X*** — create a binary (search) tree in a variable *X*
    * **BinaryTree(*X*)** / **BinarySearchTree(*X*)** — a direct object of a class binary (search) tree with a body of *X*. *X* is not mandatory. Further this value can be assigned to a variable. Here, the name of the class IS case sensitive as long as it is stored as another variable
    * ***X*.is_empty()** — check if a binary (search) tree *X* is empty
    * ***X*.get_min()** — get a minimum value from a binary (search) tree *X*
    * ***X*.get_max()** — get a maximum value from a binary (search) tree *X*
    * ***X*.add(*Y*)** — get a value *Y* to a binary (search) tree *X*
    * ***X*.includes(*Y*)** — check if a binary (search) tree *X* contains a value *Y*
    * ***X*.remove_min()** — remove a minimum value from a binary (search) tree *X*
    * ***X*.remove_max()** — remove a maximum value from a binary (search) tree *X*
    * ***X*.remove(*Y*)** — remove a value *Y* from a binary (search) tree *X*
    * ***X*.get_tree_by_levels()** — get a binary (search) tree *X* by levels
    * ***X*.get_tree_list()** — get a binary (search) tree *X* as a list (array)
    * ***X*.get_tree_sorted()** — get a binary (search) tree *X* as a sort list (array)
* #### **Set** — a set
    * **create Set *X*** / **Set *X*** — create a set in a variable *X*
    * **Set(*X*)** — a direct object of a class set with a body of *X*. *X* is not mandatory. Further this value can be assigned to a variable. Here, the name of the class IS case sensitive as long as it is stored as another variable
    * ***X*[*I*]** — get a value with an index (in a sorted order) *I* from a set *X*
    * ***X*.is_empty()** — check if a set *X* is empty
    * ***X*.size()** / ***X*.length()** — get a size/length of a set *X*
    * ***X*.add(*Y*)** — add a value *Y* to a set *X*. Only unique values are added
    * ***X*.includes(*Y*)** — check if a set *X* contains *Y*
    * ***X*.remove(*Y*)** — remove a value *Y* from a set *X*
    * ***X*.to_array(*Y*)** — present a set as a sorted array (LazyArray). If other type of array is required — it can be converted from LazyArray
* #### **Multiset** — a multiset
    * **create Multiset *X*** / **Multiset *X*** — create a multiset in a variable *X*
    * **Multiset(*X*)** — a direct object of a class multiset with a body of *X*. *X* is not mandatory. Further this value can be assigned to a variable. Here, the name of the class IS case sensitive as long as it is stored as another variable
    * ***X*[*I*]** — get a value with an index (in a sorted order) *I* from a multiset *X*
    * ***X*.is_empty()** — check if a multiset *X* is empty
    * ***X*.size()** / ***X*.length()** — get a size/length of a multiset *X*
    * ***X*.add(*Y*)** — add a value *Y* to a multiset *X*
    * ***X*.includes(*Y*)** — check if a multiset *X* contains *Y*
    * ***X*.remove(*Y*)** — remove a value *Y* from a multiset *X*
    * ***X*.to_array(*Y*)** — present a multiset as a sorted array (LazyArray). If other type of array is required — it can be converted from LazyArray

### Custom structures
* **structure *X*** — a structure *X*
* Attributes inside a structure block:
    * ***Y*** — an empty attribute *Y*
    * ***S* *Y*** — an attribute *Y* with a default data type/structure *S*
    * ***Y* = *Z*** — an attribute *Y* with a default value *Z*. Other assignment methods also work
* **end structure** — an end of a structure block
* **create *X* *V*** / ***X* *V*** — create a structure *X* in a variable *V*. Attributes with default values are assigned with default values, all other — with none values
* ***X*(*A*, *B*, *C*, ...)** — a direct object of a class *X* with attribute values *A*, *B*, *C*, ... Values are assigned in a order how attributes where defined.  Unassigned attributes with default values are assigned with default values, all other — with none values. Further this object can be assigned to a variable. Here, the name of the class IS case sensitive as long as it is stored as another variable
* ***X*.*Y*** — get an attribute *Y* of a structure *X*
* ***X*.*Y* = *Z*** — set a value *Z* to an attribute *Y* of a structure *X*. Other assignment methods also work

Example:
```
structure X
    A
    Number B
    C = "Value"
end structure

D = X()
output D.A // none
output D.B // 0
output D.C // "Value"

E = X(1, 2, "Value2")
output E.A // 1
output E.B // 2
output E.C // "Value2"

F = X(1, 2)
output F.A // 1
output F.B // 2
output F.C // "Value"
```

## Limits and limits files

One of key features **khollang** is an ability to limit different parts of its functionality. It can be done by either providing a limits file locally or inserting limits online in an [interpreter](https://khollang-interpreter.s0urcedev.pp.ua).

### Local limits file
Local limits file can be either a JSON file or a text file. If it is JSON it has to follow this format:

```
{
    "limit1": value1, // integer or null
    "limit2": value2, // integer or null,
    ...
}
```

If it is a text file it has to follow this format:

```
limit1: value1 // integer or null
limit2: value2 // integer or null
...
```

Name of possible limits is listed further in this chapter.

### Online limits
In an [online interpreter](https://khollang-interpreter.s0urcedev.pp.ua) there is an ability to insert limits. It can be done either by providing a limits file (the same as local file) or insert them in a text format directly

### Available limits
* variables
* instructions
* if_statements
* match_statements
* condition_statements
* while_loop_statements
* until_loop_statements
* for_loop_statements
* loop_statements
* functions
* procedures
* functions_and_procedures
* custom_structure_definitions
* numbers
* booleans
* strings
* nones
* lazy_arrays
* static_arrays
* dynamic_arrays
* arrays
* dictionaries_or_maps
* stacks
* queues
* binary_trees
* sets
* multisets
* data_structures
* custom_structures

All limits by default are assigned null
